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

### Phase 3: Process Venues (Each Venue in its Own Task Agent)

**CONTEXT ISOLATION:** Each venue is processed in its own Task agent to prevent context/memory accumulation in the main orchestrator. The orchestrator never touches raw content — it only sees one-line status summaries.

Process the next 5 eligible records. For each record, launch a **Task agent** (subagent_type: `general-purpose`). Process **one venue at a time** (sequentially, not in parallel) to keep memory low.

**The Task agent prompt must include:**
- The record_id, venue_url, listing-site URLs (chateaubee_url, wedinspire_url, fwv_url — pass empty string if absent)
- All three API keys: FIRECRAWL_API_KEY, AIRTABLE_API_KEY, AIRTABLE_BASE_ID
- The working directory path: `workflows/scrape-venue-site/working/`
- The full processing instructions below (copy them into the prompt)
- Instruction to return ONLY a one-line summary: `DONE|{venue_url}|{chars_written}` or `MANUAL_CHECK|{venue_url}|{reason}` or `ERROR|{venue_url}|{reason}`

**Full venue processing instructions (for the agent prompt):**

#### Step A: Scrape

Run the scrape script:
```
python "workflows/scrape-venue-site/scripts/process_venue.py" --scrape-only "{record_id}" "{venue_url}" "{chateaubee_url}" "{wedinspire_url}" "{fwv_url}" "{FIRECRAWL_API_KEY}" "{AIRTABLE_API_KEY}" "{BASE_ID}"
```
- Pass `""` for any empty listing-site URL
- Script outputs one line to stdout: `SCRAPED|venue_chars|pages+listings|sources|listing_chars` or `MANUAL_CHECK|reason|0`
- If MANUAL_CHECK, return immediately with `MANUAL_CHECK|{venue_url}|{reason}`
- Script saves raw content to `working/raw_{record_id}.md` and `working/listing_{record_id}_{CB|WI|FWV}.md`

#### Step B: Structure Content

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

#### Step C: Write to Airtable

Run the write script:
```
python "workflows/scrape-venue-site/scripts/process_venue.py" --write-file "{record_id}" "workflows/scrape-venue-site/working/structured_{record_id}.md" "{AIRTABLE_API_KEY}" "{AIRTABLE_BASE_ID}"
```
- Script reads the file, PATCHes to Airtable, and deletes all temp files (structured + raw + listings)
- Script stdout: `WRITTEN|{chars}` or `AIRTABLE_ERROR|reason|{chars}`

#### Step D: Return Result

Return ONLY a one-line summary: `DONE|{venue_url}|{chars_written}` or `ERROR|{venue_url}|{reason}`. Do NOT return any venue content.

---

**Back in the orchestrator**, after each agent returns:
- Parse the one-line result and log it to `workings_temp.md`
- Track consecutive failures — if >= 2, pause and ask user with AskUserQuestion
- Proceed to the next venue

### Phase 4: Report

1. Summarize the batch: successful, failed, and manual_check counts
2. Save a batch report to `workflows/scrape-venue-site/output/batch-report-{timestamp}.md`
3. Ask the user: "Batch complete (X/5 successful). Proceed with next batch of 5?"
4. If user confirms, return to Phase 3 with the next 5 records
