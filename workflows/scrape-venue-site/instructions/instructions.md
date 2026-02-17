# Venue Website Scraper — Supplementary Instructions

This document supplements `workflow.yml` with detailed guidance on the content processing pipeline, error handling, logging format, and safety rules.

**Objective:** Execute the Venue Scrape & Synthesis loop.

> **Two-stage pipeline:** Stage 1 (script) handles scraping and basic cleaning via `process_venue.py --scrape-only`. Stage 2 (Claude) reads the raw files, strips remaining noise semantically, organizes into structured sections, and writes to Airtable via MCP. This document serves as the authoritative reference for both stages.

---

## Source Columns

Each Airtable record has up to **4 URL columns** to scrape:

| Column | Type | Description |
|--------|------|-------------|
| `venue_url` | **Primary (mandatory)** | The venue's own website. If empty, skip the entire record. |
| `chateaubee_url` | Optional listing site | ChateauBee listing page for this venue |
| `wedinspire_url` | Optional listing site | WedInspire listing page for this venue |
| `fwv_url` | Optional listing site | French Wedding Venues listing page for this venue |

All scraped content is written to **one field**: `venue_url_scraped`, combined under bold headings.

---

## Content Processing Pipeline

The pipeline processes each venue record in three parts:

### Part 1: Venue Website (MANDATORY)

The venue's own website (`venue_url`) gets the full multi-page treatment.

**Stage 1: Map & Scrape (Multi-Page)**

Each venue website contains critical information spread across multiple pages (homepage, wedding, accommodation, activities, contact, etc.). A single-page scrape misses most of this content.

**Step 1 — Map:** Call Firecrawl `/v2/map` with the `venue_url` to discover all pages on the site. This returns an array of `{url, title, description}` objects.

**Step 2 — Filter:** Apply these rules to the discovered URLs:
- Remove excluded patterns (sitemaps, blog posts, press, legal pages — see `workflow.yml` page_filter)
- When both French and English versions exist (e.g., `/mariage` and `/wedding`), prefer English
- Always include the original `venue_url` as the first page
- Cap total pages at `max_pages` (default 20) to control Firecrawl credit usage
- Prioritize pages with titles/descriptions mentioning: wedding, accommodation, rooms, rental, seminar, activities, contact, pricing

**Step 3 — Scrape each page:** Call Firecrawl `/v2/scrape` for each filtered URL individually with `onlyMainContent: false` and `waitFor: 8000`. The `onlyMainContent: false` setting is critical — JS-heavy sites lose actual content with `true`. The extra nav/footer noise is handled by cleaning. Wait `rate_limit_delay` seconds between calls.

**Step 4 — Combine:** Concatenate all page markdowns into a single document, prefixed with `## Page: {url}` headers.

**If the map returns 0 results or fails:** Fall back to scraping only the `venue_url` directly.

**Stage 2: Basic Clean (Regex-Based Noise Removal)**

The script applies deterministic regex-based cleaning to strip common noise patterns:

- **Cookie consent banners** and privacy policy text (GDPR prompts, "Accept all cookies", etc.)
- **Booking engine widgets** (Arrival/Departure/Adults search bars, date pickers, availability checkers)
- **Repeated navigation menus** (blocks of 5+ consecutive short link lines)
- **Footer boilerplate** (copyright notices, social media link lists, "All rights reserved", agency credits)
- **Cookie detail tables** (rows containing `_gcl_au`, `_ga`, `_fbp`, etc.)
- **Map widget noise** (keyboard shortcut tables, map data attribution strings)
- **Directory-site boilerplate** (CTAs like "Enquire today", "Handpicked for you", related venue listings)
- **Image-only lines** with no surrounding text
- **Excessive blank lines** (collapse 3+ consecutive blank lines to a single blank line)

In `--scrape-only` mode, the script saves the basic-cleaned content to `working/raw_{record_id}.md` and any listing-site content to `working/listing_{record_id}_{CB|WI|FWV}.md`.

**Stage 3: Intelligent Structuring (Claude-Powered)**

Claude reads the raw files and applies semantic understanding to finish the job:

**3a. Strip remaining noise** (catches what regex missed):
- Related venue listings (other venues with names, regions, guest counts)
- Cookie detail tables and tracker descriptions that survived regex
- Duplicate reviews (same text appearing twice from carousel/pagination)
- Language-duplicated content (keep English, drop French/Spanish duplicates of same info)
- Directory boilerplate, social widgets, booking form remnants

**3b. Organize venue content into 5 sections** (semantic, not keyword-based):

1. **Overview & History** — founding, heritage, architecture, who runs it, what makes it distinctive
2. **Event Logistics** — ceremony locations, capacities, catering, vendor policies, pricing, what's included
3. **Accommodation Breakdown** — every room/suite/gite by name with capacity, beds, description
4. **Amenities & Facilities** — pool, grounds (acreage), spa, parking, WiFi, restaurant, chapel
5. **Travel & Contact** — address, phone, email, airports, train stations, driving distances

**No-deletion policy:** ALL factual venue info must be retained. Move to the correct section, never drop. If a section has no relevant data, omit the header entirely rather than leaving it empty.

**3c. Listing site content:** Clean noise but keep the listing site's own structure (don't reorganize into the 5 sections).

### Part 2: Listing Sites (OPTIONAL)

For each populated listing-site column (`chateaubee_url`, `wedinspire_url`, `fwv_url`):

- **Single-page scrape only** — no map step. These are individual listing pages, not full websites.
- Call Firecrawl `/v2/scrape` with `onlyMainContent: false`, `waitFor: 8000`.
- Clean: apply the same basic regex noise removal as Stage 2 above.
- In `--scrape-only` mode, save to `working/listing_{record_id}_{CB|WI|FWV}.md`.
- **Retain all non-noise content as-is** — do not categorize or restructure. Listing sites have their own structure.
- If the scrape fails, apply normal error handling but do NOT fail the entire record — mark just that source as failed in the log.

### Part 3: Combine & Output

Assemble the final document with bold headings per source:

```
**Venue Website**
{cleaned & categorized venue_url content}

**ChateauBee**
{cleaned chateaubee content — only if chateaubee_url was populated and scraped}

**WedInspire**
{cleaned wedinspire content — only if wedinspire_url was populated and scraped}

**French Wedding Venues**
{cleaned fwv content — only if fwv_url was populated and scraped}
```

- Omit any listing-site heading entirely if that column was empty or scrape failed.
- Save the combined document into the `venue_url_scraped` cell in Airtable.

---

## Safety Check: Truncation

If the resulting text is over **95,000 characters**, truncate the least important bottom sections (usually redundant contact footers) to ensure it fits the Airtable cell.

- Cut at the last complete paragraph before the 95,000 character mark.
- Append: `\n\n[Content truncated at 95,000 characters]`

---

## Error Classification

| HTTP Status / Condition     | Action                                  |
|-----------------------------|-----------------------------------------|
| 200 + non-empty markdown    | Success — write to Airtable             |
| 200 + empty/null markdown   | Write MANUAL_CHECK marker               |
| 403 Forbidden               | Write MANUAL_CHECK marker               |
| 404 Not Found               | Write MANUAL_CHECK marker               |
| 408/504 Timeout             | Retry once after 5s, then MANUAL_CHECK  |
| 429 Rate Limited            | Wait 30 seconds, retry once             |
| 500+ Server Error           | Retry once after 5s, then MANUAL_CHECK  |
| Network/DNS failure         | Write MANUAL_CHECK marker               |

---

## MANUAL_CHECK Marker Format

When a venue cannot be scraped, write exactly this format to `venue_url_scraped`:

```
MANUAL_CHECK -- [REASON] -- [TIMESTAMP]
```

Examples:
- `MANUAL_CHECK -- 403 Forbidden -- 2026-02-15T14:30:00Z`
- `MANUAL_CHECK -- Empty content returned -- 2026-02-15T14:31:00Z`
- `MANUAL_CHECK -- DNS resolution failed -- 2026-02-15T14:32:00Z`

---

## workings_temp.md Format

Each session appends a session block to `working/workings_temp.md`:

```markdown
---

## Session: 2026-02-15T14:00:00Z
**Total eligible records:** 23
**Credentials loaded:** Airtable (OK), Firecrawl (OK)

### Batch 1 (Records 1-5)

| # | Record ID   | Venue URL                           | Sources Scraped          | Status       | Pages | Chars  | Notes                 |
|---|-------------|-------------------------------------|--------------------------|--------------|-------|--------|-----------------------|
| 1 | recABC123   | https://chateau-example.com         | Venue, CB, WI            | SUCCESS      | 8+1+1 | 18,450 |                       |
| 2 | recDEF456   | https://domaine-blocked.fr          | Venue                    | MANUAL_CHECK | 0     | 0      | 403 Forbidden         |
| 3 | recGHI789   | https://villa-example.com           | Venue, FWV               | SUCCESS      | 5+1   | 10,320 |                       |
| 4 | recJKL012   | https://mas-example.com             | Venue, CB, WI, FWV       | SUCCESS      | 12+3  | 22,100 | Truncated from 102k   |
| 5 | recMNO345   | https://chateau-offline.com         | Venue                    | MANUAL_CHECK | 0     | 0      | Empty content returned|

**Batch 1 Summary:** 3 success, 2 manual_check
**Total chars written:** 35,870

---
```

---

## Safety Rules

1. **Never overwrite**: Before writing to `venue_url_scraped`, confirm the field is empty. If the Airtable record already has content in `venue_url_scraped`, skip it entirely.
2. **Never modify source fields**: `venue_url`, `chateaubee_url`, `wedinspire_url`, and `fwv_url` are all read-only for this workflow.
3. **Rate limiting**: Wait at least 2 seconds between Firecrawl API calls.
4. **Batch confirmation**: Always ask the user before proceeding to the next batch.
5. **Payload via file**: Write JSON payloads to `working/payload.json` and use `curl -d @working/payload.json` to avoid shell argument length limits with large markdown content.

---

## Curl Command Reference

### List eligible records
```bash
curl -s -X GET \
  "https://api.airtable.com/v0/{BASE_ID}/Venues?filterByFormula=AND(NOT(%7Bvenue_url%7D%3D'')%2C%7Bvenue_url_scraped%7D%3D'')&fields%5B%5D=venue_url&fields%5B%5D=chateaubee_url&fields%5B%5D=wedinspire_url&fields%5B%5D=fwv_url&pageSize=100" \
  -H "Authorization: Bearer {AIRTABLE_API_KEY}" \
  -H "Content-Type: application/json"
```

### Map all pages on a venue website (Step 1)
```bash
curl -s -X POST \
  'https://api.firecrawl.dev/v2/map' \
  -H 'Authorization: Bearer {FIRECRAWL_API_KEY}' \
  -H 'Content-Type: application/json' \
  -d '{"url": "{VENUE_URL}"}'
```
Returns: `{"success": true, "links": [{"url": "...", "title": "...", "description": "..."}]}`

### Scrape a single page with Firecrawl (Step 2, repeat per page)
```bash
curl -s -X POST \
  'https://api.firecrawl.dev/v2/scrape' \
  -H 'Authorization: Bearer {FIRECRAWL_API_KEY}' \
  -H 'Content-Type: application/json' \
  -d '{"url": "{PAGE_URL}", "formats": ["markdown"], "onlyMainContent": false, "timeout": 120000, "waitFor": 8000}'
```

### Update Airtable record (via payload file)
```bash
curl -s -X PATCH \
  'https://api.airtable.com/v0/{BASE_ID}/Venues/{RECORD_ID}' \
  -H 'Authorization: Bearer {AIRTABLE_API_KEY}' \
  -H 'Content-Type: application/json' \
  -d @working/payload.json
```

### Write MANUAL_CHECK marker
```bash
curl -s -X PATCH \
  'https://api.airtable.com/v0/{BASE_ID}/Venues/{RECORD_ID}' \
  -H 'Authorization: Bearer {AIRTABLE_API_KEY}' \
  -H 'Content-Type: application/json' \
  -d '{"fields": {"venue_url_scraped": "MANUAL_CHECK -- {REASON} -- {TIMESTAMP}"}}'
```
