# Generate Venue JSON

Extract structured JSON records from scraped venue content and brochure text in Airtable, save locally, and write back to Airtable.

The pipeline reads `venue_url_scraped` and `brochure_text`, validates they refer to the same venue, extracts structured data into a full JSON record (~320 fields) and a summary JSON record (20 fields), saves both locally to `outputs/venue-json/{venue-slug}/`, and writes them to `full_venue_json` and `summary_venue_json` fields in Airtable. **Do NOT read workflow.yml or instructions.md during execution.**

## Instructions

### Phase 1: Load Credentials

Read `.env` and extract: `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`. Confirm both are present. (Firecrawl not needed for this pipeline.)

### Phase 2: Discovery

1. Query Airtable for eligible records (venue_url_scraped populated AND full_venue_json empty):
   ```
   curl -s -X GET "https://api.airtable.com/v0/{BASE_ID}/Venues?filterByFormula=AND(NOT(%7Bvenue_url_scraped%7D%3D'')%2C%7Bfull_venue_json%7D%3D'')&fields%5B%5D=venue_name&pageSize=100" -H "Authorization: Bearer {KEY}" -H "Content-Type: application/json"
   ```
2. Handle pagination: if response contains `offset`, fetch next page
3. Build array of tuples: `{record_id, venue_name}`
4. Filter out records where `venue_name` is empty
5. Report total eligible records to user
6. Create/append session header to `workflows/scrape-venue-site/working/workings_temp.md`

### Phase 3: Process Batch (5 records at a time)

For each record in the batch:

#### Step 1: Fetch source content

Run the Python script to download content from Airtable to temp files:

```
python "workflows/scrape-venue-site/scripts/process_venue.py" --fetch-json-sources "{record_id}" "{venue_name}" "{AIRTABLE_API_KEY}" "{AIRTABLE_BASE_ID}"
```

- Script stdout: `FETCHED|{scraped_chars}|{brochure_chars}` or `NO_CONTENT|reason` or `FETCH_ERROR|reason`
- On `NO_CONTENT` or `FETCH_ERROR`, skip this record and log to workings_temp.md
- Content is saved to `workflows/scrape-venue-site/working/scraped_{record_id}.md` and optionally `brochure_{record_id}.md`

#### Step 2: Extract JSON (Delegated to Task Agent)

**CONTEXT MANAGEMENT:** Each venue's content can be 190k+ chars combined. Delegate the full extraction to a **Task agent** (subagent_type: `general-purpose`). You may run up to 2 agents in parallel if multiple venues are ready.

**Compute the venue slug** from the venue_name before launching the agent:
- Lowercase, replace spaces with hyphens, remove accents, strip non-alphanumeric characters except hyphens
- E.g. "Chateau de Pondres" → "chateau-de-pondres", "Domaine du Réveillon" → "domaine-du-reveillon"

**The Task agent prompt must include:**

1. The record_id, venue_name, venue_slug, and the working directory path (`workflows/scrape-venue-site/working/`)
2. Whether a brochure file exists (so the agent knows what to read)
3. The full extraction instructions below (copy them into the prompt)
4. Instruction to save output to:
   - `outputs/venue-json/{venue_slug}/{venue_slug}_full.json`
   - `outputs/venue-json/{venue_slug}/{venue_slug}_summary.json`
5. Instruction to return ONLY a one-line summary: `SUCCESS|{full_chars}|{summary_chars}` or `ERROR|{reason}`

**Extraction instructions (copy into Task agent prompt):**

You are a structured data extraction specialist. Your task is to extract a comprehensive JSON record from French wedding venue content.

**Step A: Read source files**
1. Read `workflows/scrape-venue-site/working/scraped_{record_id}.md` (venue website + listing site content)
2. Read `workflows/scrape-venue-site/working/brochure_{record_id}.md` (brochure text, if it exists)
3. Read `outputs/venue-json-templates/venue_golden_record.json` (structural template — your output MUST match this exact structure)
4. Read `outputs/venue-json-templates/venue_reduced_record.json` (summary template — your summary output MUST match this exact structure)

**Step B: Validate venue identity**
- Confirm that the scraped content and brochure text (if present) refer to the same venue: "{venue_name}"
- Check for matching venue name, address, or other identifying details across both sources
- If the brochure clearly refers to a DIFFERENT venue, ignore the brochure entirely and extract from scraped content only. Note this in your return message.

**Step C: Extract full JSON record**

Using the golden record as your structural template, extract data from the source content into every applicable field. Follow these rules strictly:

1. **Structure**: Your output JSON must have the EXACT same section structure and field names as the golden record. All 22 top-level sections: overview, identity, location, history, spaces, accommodation, pricing, catering, drinks, vendor_rules, ceremony, amenities, activities, technical, accessibility, sustainability, parking, policies, contact, event_types, wedding_day_details.

2. **Extraction rules**:
   - Only extract information EXPLICITLY stated in the source text
   - NEVER guess, infer, or fabricate data. If information is not present, use `null`
   - For arrays: use `null` (not empty array `[]`) when no data is available
   - For objects: include all fields from the template, set unknown ones to `null`
   - For numbers: extract exact figures as stated, convert to EUR if needed
   - For booleans: only set `true`/`false` when explicitly confirmed or denied. Use `null` when uncertain
   - Prefer English content over French when both exist
   - If scraped content and brochure disagree, prefer the brochure (usually more current)

3. **Source merging priority**: Brochure > Venue Website > Listing Sites
   - Brochure data is typically the most current and accurate (venue's own marketing material)
   - Venue website is the primary source for identity, history, and contact
   - Listing sites supplement with reviews, ratings, and third-party descriptions

4. **FORBIDDEN BRAND MENTIONS**: The output JSON must NEVER contain the names "ChateauBee", "WedInspire", or "French Wedding Venues" (or any variation of these). These are third-party listing sites used as data sources but must NOT appear in any field of the output JSON — not in descriptions, notes, media_features, or any other field. If a data point was sourced from one of these sites, state the fact without naming the source (e.g. "Starting price for 2026-2027" instead of "Starting price from WedInspire listing for 2026-2027").

5. **No `source_quality_notes`**: Do NOT include a `source_quality_notes` field in the output JSON. This field is excluded from the schema.

6. **Spaces array**: Create one entry per distinct named space (ceremony spots, reception halls, dining rooms, terraces, gardens). Follow the event_space structure from the golden record exactly.

7. **Accommodation buildings array**: Create one entry per distinct building/gite/cottage. Include individual room details in the rooms sub-array where available.

8. **Pricing**: Extract ALL pricing information. Seasonal pricing, packages, per-person costs, extras. Use the exact structure from the golden record.

9. **Do NOT include a `_meta` key** in the full record — only the summary record has that.

**Step D: Generate summary JSON record**

Using the reduced record template, extract the 20 core fields. These MUST be consistent with the full record:
- `venue_name` from identity.venue_name
- `venue_type` from identity.venue_type
- `short_description` from identity.short_description
- `region` from location.region
- `department` from location.address.department
- `nearest_city` formatted as "CityName (distance)" from location.nearest_city
- `max_guests` from overview.max_guests
- `min_guests` from overview.min_guests
- `max_sleeping_guests` from overview.max_sleeping_guests
- `total_bedrooms` from overview.total_bedrooms
- `starting_price_eur` from overview.min_price_eur
- `exclusivity_model` from identity.exclusivity_model
- `catering_model` from catering.catering_model
- `on_site_accommodation` from accommodation.on_site_accommodation
- `swimming_pool` from amenities.swimming_pool
- `chapel_on_site` from ceremony.chapel_on_site
- `curfew` from policies.curfew_time
- `child_friendly` from policies.child_friendly
- `google_rating` from identity.google_rating
- `website_url` from contact.website_url

Include the `_meta` block:
```json
{
  "_meta": {
    "description": "Venue Reduced Record — 20 core fields for high-level filtering and bride-facing comparison.",
    "schema_version": "v1.1.0",
    "field_count": 20,
    "golden_record_ref": "{venue_slug}_full.json"
  }
}
```

**Step E: Save output files**
1. Create directory `outputs/venue-json/{venue_slug}/` if it does not exist
2. Save the full JSON to `outputs/venue-json/{venue_slug}/{venue_slug}_full.json`
   - Use 2-space indentation, ensure_ascii=false for French characters
3. Save the summary JSON to `outputs/venue-json/{venue_slug}/{venue_slug}_summary.json`
   - Use 2-space indentation

**Step F: Clean up temp files**
Delete the temp source files:
- `workflows/scrape-venue-site/working/scraped_{record_id}.md`
- `workflows/scrape-venue-site/working/brochure_{record_id}.md` (if it exists)

**Step G: Return result**
Return ONLY a one-line summary:
- `SUCCESS|{full_json_char_count}|{summary_json_char_count}`
- `ERROR|{reason}`

Do NOT return the JSON content itself.

---

#### Step 3: Write JSON to Airtable

After each agent returns with `SUCCESS`, the orchestrator runs:

```
python "workflows/scrape-venue-site/scripts/process_venue.py" --write-json "{record_id}" "outputs/venue-json/{venue_slug}/{venue_slug}_full.json" "outputs/venue-json/{venue_slug}/{venue_slug}_summary.json" "{AIRTABLE_API_KEY}" "{AIRTABLE_BASE_ID}"
```

- Script reads both JSON files and PATCHes `full_venue_json` and `summary_venue_json` to Airtable in one request
- Script stdout: `JSON_WRITTEN|{full_chars}|{summary_chars}` or `AIRTABLE_ERROR|reason|chars`
- Log the result to `workings_temp.md`
- 2+ consecutive failures → pause and ask user with AskUserQuestion

### Phase 4: Report

1. Summarize the batch: successful, failed, no_content, error counts
2. Save batch report to `workflows/scrape-venue-site/output/json-batch-report-{timestamp}.md`
3. Ask the user: "Batch complete (X/5 successful). Proceed with next batch of 5?"
4. If user confirms, return to Phase 3 with the next 5 records
