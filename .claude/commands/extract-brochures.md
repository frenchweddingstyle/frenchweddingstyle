# Extract Brochures

> **Model: sonnet** — This command follows rule-based extraction patterns. Switch to Sonnet before running (`/model sonnet`).

Extract text from brochure links in Airtable (Google Drive files/folders, Google Docs, Calameo, Canva, etc.), convert to Markdown, and write back to the `brochure_text` column.

Claude orchestrates directly via MCP tools — no Python script needed. **Do NOT read workflow.yml or instructions.md during execution.**

## Instructions

### Phase 1: Load Credentials

Read `.env` and extract: `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, `FIRECRAWL_API_KEY`. Confirm all 3 are present.

### Phase 2: Discovery

1. Query Airtable via MCP for eligible records:
   ```
   mcp__airtable__list_records({
     baseId: "appFQYNRTuooIRZZz",
     tableId: "tblIEJQNynXIsD8GL",
     filterByFormula: "AND(NOT({brochure_link}=''),{brochure_text}='')",
     maxRecords: 200
   })
   ```
2. For each record, extract the `brochure_link` value and classify:
   - Contains `@` and no `/` → **SKIP** (email)
   - Does not start with `http` → **SKIP** (text note)
   - Contains `drive.google.com/file/d/` → **GDRIVE_FILE**
   - Contains `drive.google.com/drive/folders/` → **GDRIVE_FOLDER**
   - Contains `docs.google.com/document/d/` → **GDOCS**
   - Starts with `http` (catch-all) → **WEB_SCRAPE**
3. Build the actionable list (exclude SKIPs), report breakdown to user
4. Create/append session header to `workflows/extract-brochures/working/workings_temp.md`

### Phase 3: Extract Batch (5 records at a time)

Process the next 5 actionable records. For each record:

#### GDRIVE_FILE (Google Drive single file — usually PDF)
1. Scrape with Firecrawl using PDF parser:
   ```
   mcp__firecrawl__firecrawl_scrape({
     url: "{brochure_link}",
     formats: ["markdown"],
     parsers: ["pdf"],
     waitFor: 8000
   })
   ```
2. If empty/fails, extract file ID and try download URL:
   - ID = text between `/file/d/` and next `/`
   - Retry: `https://drive.google.com/uc?export=download&id={ID}`
3. If both fail → write `[ERROR]: Link unreachable.`

#### GDRIVE_FOLDER (Google Drive folder)
1. Extract folder ID (between `/folders/` and `?` or end)
2. List contents: `mcp__google-drive__listFolder({ folderId: "{ID}" })`
3. For each file:
   - Google Docs → `mcp__google-drive__getGoogleDocContent({ documentId: "{file.id}" })`
   - Google Sheets → `mcp__google-drive__getGoogleSheetContent({ spreadsheetId: "{file.id}", range: "A1:Z1000" })`
   - Google Slides → `mcp__google-drive__getGoogleSlidesContent({ presentationId: "{file.id}" })`
   - PDFs → Firecrawl scrape `https://drive.google.com/file/d/{file.id}/view` with `parsers: ["pdf"]`
   - Images (.jpg, .png) → skip (note as unreadable)
4. Consolidate with headers + dividers:
   ```
   ### Source: {filename}

   {content}

   ---
   ```
5. If some files failed: prepend `[WARNING]: Some files in folder were unreadable.`
6. If ALL failed: write `[ERROR]: Files are images without readable text.`

#### GDOCS (Google Docs)
1. Extract doc ID (between `/document/d/` and next `/`)
2. Read: `mcp__google-drive__getGoogleDocContent({ documentId: "{ID}" })`

#### WEB_SCRAPE (Calameo, Canva, Heyzine, etc.)
1. If URL contains `safelinks.protection.outlook.com`: extract actual URL from `url=` parameter, URL-decode it
2. Scrape: `mcp__firecrawl__firecrawl_scrape({ url: "{url}", formats: ["markdown"], onlyMainContent: true, waitFor: 8000 })`
3. If empty → write `[ERROR]: Files are images without readable text.`

#### After extraction (all types):
- Clean content: strip cookie banners, nav menus, platform branding, isolated page numbers
- Preserve: tables, bullet lists, pricing, headings, contact info
- Truncate at 95,000 chars if needed (cut at last complete paragraph, append truncation notice)
- Write to Airtable: `mcp__airtable__update_records({ baseId, tableId, records: [{ id: record_id, fields: { brochure_text: content } }] })`
- On any error: write the appropriate `[ERROR]: ...` marker
- Log result to `workings_temp.md`
- Track consecutive failures — if 2+ in a row, pause and AskUserQuestion

### Phase 4: Report

1. Summarize the batch: successful, failed, error counts
2. Save batch report to `workflows/extract-brochures/output/batch-report-{date}.md`
3. Ask the user: "Batch complete (X/5 successful). Proceed with next batch of 5?"
4. If user confirms, return to Phase 3 with the next 5 records