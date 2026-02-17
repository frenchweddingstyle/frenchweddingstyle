# Scrape Venue Sites

Scrape venue websites from Airtable, convert to Markdown, intelligently structure with Claude, and write back to Airtable.

The pipeline has two stages: (1) `process_venue.py --scrape-only` handles map/scrape/basic-clean and saves raw files to `working/`, (2) Claude reads the raw files, strips remaining noise semantically, organizes into structured sections, and writes to Airtable via MCP. **Do NOT read workflow.yml or instructions.md during execution.**

## Instructions

### Phase 1: Load Credentials

Read `.env` and extract: `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, `FIRECRAWL_API_KEY`. Confirm all 3 are present.

### Phase 2: Discovery

1. Query Airtable for eligible records (venue_url populated, venue_url_scraped empty):
   ```
   curl -s -X GET "https://api.airtable.com/v0/{BASE_ID}/Venues?filterByFormula=AND(NOT(%7Bvenue_url%7D%3D'')%2C%7Bvenue_url_scraped%7D%3D'')&fields%5B%5D=venue_url&fields%5B%5D=chateaubee_url&fields%5B%5D=wedinspire_url&fields%5B%5D=fwv_url&pageSize=100" -H "Authorization: Bearer {KEY}" -H "Content-Type: application/json"
   ```
2. Handle pagination: if response contains `offset`, fetch next page
3. Build array of tuples: `{record_id, venue_url, chateaubee_url, wedinspire_url, fwv_url}`
4. Report total eligible records to user (and how many have listing-site URLs)
5. Create/append session header to `workflows/scrape-venue-site/working/workings_temp.md`

### Phase 3: Scrape Batch

Process the next 5 eligible records. For each record, run the script with `--scrape-only`:

```
python "workflows/scrape-venue-site/scripts/process_venue.py" --scrape-only "{record_id}" "{venue_url}" "{chateaubee_url}" "{wedinspire_url}" "{fwv_url}" "{FIRECRAWL_API_KEY}" "{AIRTABLE_API_KEY}" "{BASE_ID}"
```

- Pass `""` for any empty listing-site URL
- Script outputs one line to stdout: `SCRAPED|venue_chars|pages+listings|sources|listing_chars` or `MANUAL_CHECK|reason|0`
- Parse that line and log the result to `workings_temp.md`
- Progress messages appear on stderr (visible in terminal)
- 2+ consecutive failures → pause and ask user with AskUserQuestion
- Script saves raw content to `working/raw_{record_id}.md` and `working/listing_{record_id}_{CB|WI|FWV}.md`

### Phase 3.5: Structure Content (Delegated to Task Agents)

**CONTEXT MANAGEMENT:** Each venue's raw content is 50-150k chars. To avoid blowing the context window, delegate the entire structure+write cycle for each venue to a **Task agent**. The full content never enters the orchestrator's context.

For each record that returned `SCRAPED` in Phase 3, launch a **Task agent** (subagent_type: `general-purpose`). You may run up to 2 agents in parallel if multiple venues are ready.

**The Task agent prompt must include:**
- The record_id, the working directory path, and which listing files exist (CB/WI/FWV)
- The full structuring instructions below (copy them into the prompt)
- Instruction to save output to `working/structured_{record_id}.md`
- Instruction to return ONLY a one-line summary: `SUCCESS|{char_count}` or `ERROR|{reason}`

**Structuring instructions (for the agent prompt):**

1. **Read raw files** from `working/`:
   - `working/raw_{record_id}.md` (venue website content)
   - `working/listing_{record_id}_CB.md`, `working/listing_{record_id}_WI.md`, `working/listing_{record_id}_FWV.md` (if they exist)

2. **Strip remaining noise** (semantic — catches what regex missed):
   - Related venue listings (other venues with names, regions, guest counts)
   - Cookie detail tables, tracker descriptions
   - Keyboard shortcut tables, map attribution
   - Duplicate reviews (same text appearing twice from carousel/pagination)
   - Language-duplicated content (keep English, drop French/Spanish duplicates of same info)
   - Directory boilerplate, social widgets, booking form remnants

3. **Organize venue content into 5 sections** (semantic understanding, not keyword matching):
   - **Overview & History** — founding, heritage, architecture, who runs it, what makes it distinctive
   - **Event Logistics** — ceremony locations, capacities, catering, vendor policies, pricing, what's included
   - **Accommodation Breakdown** — every room/suite/gite by name with capacity, beds, description
   - **Amenities & Facilities** — pool, grounds (acreage), spa, parking, WiFi, restaurant, chapel
   - **Travel & Contact** — address, phone, email, airports, train stations, driving distances

4. **No-deletion policy**: ALL factual venue info must be retained. Move to the correct section, never drop.

5. **Listing site content**: Clean noise but keep the listing site's own structure (don't reorganize into 5 sections).

6. **Assemble final document** under bold source headings:
   ```
   **Venue Website**

   ## Overview & History
   {content}

   ## Event Logistics
   {content}

   ## Accommodation Breakdown
   {content}

   ## Amenities & Facilities
   {content}

   ## Travel & Contact
   {content}

   ---

   **ChateauBee**
   {cleaned listing content}

   ---

   **WedInspire**
   {cleaned listing content}
   ```

7. **Truncate** if over 95,000 chars (cut at last complete paragraph, append `\n\n[Content truncated at 95,000 character limit]`).

8. **Save** the final document to `working/structured_{record_id}.md` using the Write tool.

9. **Return** ONLY: `SUCCESS|{char_count}` or `ERROR|{reason}`. Do NOT return the content itself.

**After each agent returns**, the orchestrator runs:

```
python "workflows/scrape-venue-site/scripts/process_venue.py" --write-file "{record_id}" "workflows/scrape-venue-site/working/structured_{record_id}.md" "{AIRTABLE_API_KEY}" "{AIRTABLE_BASE_ID}"
```

- Script reads the file, PATCHes to Airtable, and deletes all temp files (structured + raw + listings)
- Script stdout: `WRITTEN|{chars}` or `AIRTABLE_ERROR|reason|{chars}`
- Log the result to `workings_temp.md`

### Phase 4: Report

1. Summarize the batch: successful, failed, and manual_check counts
2. Save a batch report to `workflows/scrape-venue-site/output/batch-report-{timestamp}.md`
3. Ask the user: "Batch complete (X/5 successful). Proceed with next batch of 5?"
4. If user confirms, return to Phase 3 with the next 5 records
