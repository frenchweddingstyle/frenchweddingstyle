# Brochure Link Extraction — Supplementary Instructions

This document supplements `workflow.yml` with detailed guidance on the extraction pipeline, per-type handling, content cleaning, and error handling.

**Objective:** Extract text from brochure links in Airtable and write consolidated Markdown to `brochure_text`.

> **Claude-orchestrated pipeline:** No Python script needed. Claude uses MCP tools directly (Google Drive MCP for folder listing + doc reading, Firecrawl MCP for web/PDF scraping, Airtable MCP for read/write).

---

## URL Classification

Each `brochure_link` value is classified in order. First match wins:

| Priority | Pattern | Type | Action |
|----------|---------|------|--------|
| 1 | Contains `@` and no `/` | SKIP_EMAIL | Skip silently |
| 2 | Does not start with `http` | SKIP_NOTE | Skip silently |
| 3 | Contains `drive.google.com/file/d/` | GDRIVE_FILE | Firecrawl PDF scrape |
| 4 | Contains `drive.google.com/drive/folders/` | GDRIVE_FOLDER | GDrive MCP list + per-file extract |
| 5 | Contains `docs.google.com/document/d/` | GDOCS | GDrive MCP getGoogleDocContent |
| 6 | Starts with `http` (catch-all) | WEB_SCRAPE | Firecrawl markdown scrape |

---

## Extraction by Type

### Type: GDRIVE_FILE (Google Drive single file)

These are typically PDFs shared via Google Drive.

**Step 1 — Primary attempt:**
```
mcp__firecrawl__firecrawl_scrape({
  url: "{brochure_link}",
  formats: ["markdown"],
  parsers: ["pdf"],
  waitFor: 8000
})
```

**Step 2 — Fallback (if Step 1 returns empty/fails):**
Extract the file ID from the URL (between `/file/d/` and the next `/`), then try:
```
mcp__firecrawl__firecrawl_scrape({
  url: "https://drive.google.com/uc?export=download&id={FILE_ID}",
  formats: ["markdown"],
  parsers: ["pdf"],
  waitFor: 8000
})
```

**Step 3 — If both fail:**
Write `[ERROR]: Link unreachable.` to `brochure_text`.

### Type: GDRIVE_FOLDER (Google Drive folder)

These folders contain multiple brochure files (PDFs, docs, images).

**Step 1 — List folder contents:**
Extract folder ID from URL (between `/folders/` and `?` or end of string).
```
mcp__google-drive__listFolder({ folderId: "{FOLDER_ID}" })
```

**Step 2 — Relevance pre-filter (filename check):**
Before extracting, check each file's name against the venue name. Extract the venue's core identifying word(s) (e.g., "Leotardie" from "Domaine de La Leotardie", "Barbirey" from "Château de Barbirey"). Skip common words like Château, Domaine, Manoir, Bastide, Le, La, De, Du, Des, Les.

For each file:
- If the filename **clearly names a different venue** (e.g., "Château Comtesse Lafond" in a folder for "Domaine de La Leotardie"), **skip that file** — it belongs to another venue.
- If the filename is generic (e.g., "Prices.pdf", "Wedding brochure.pdf") or references the correct venue, **proceed with extraction**.
- Filenames referencing caterers, florists, or service providers are fine to include (these are supplementary vendor docs).

**Step 3 — Extract each file:**
For each file that passed the relevance pre-filter:

- **Google Docs** (mimeType contains `document`): Use `mcp__google-drive__getGoogleDocContent({ documentId: "{file.id}" })`
- **Google Sheets** (mimeType contains `spreadsheet`): Use `mcp__google-drive__getGoogleSheetContent({ spreadsheetId: "{file.id}", range: "A1:Z1000" })`
- **Google Slides** (mimeType contains `presentation`): Use `mcp__google-drive__getGoogleSlidesContent({ presentationId: "{file.id}" })`
- **PDFs** (mimeType contains `pdf` or filename ends in `.pdf`): Use Firecrawl scrape with `parsers: ["pdf"]` on the file's Drive URL (`https://drive.google.com/file/d/{file.id}/view`)
- **Images** (.jpg, .png, .gif, .webp): Note as unreadable — no OCR available
- **Other formats** (.zip, .exe, etc.): Note as unsupported

**Step 4 — Relevance post-check (content validation):**
After extracting content from each file, verify relevance:
- Check if the venue's core identifying word appears at least once in the extracted text.
- If it does NOT appear, and the content prominently references a **different venue name** (5+ mentions), discard that file's content.
- Generic content (caterer menus, T&Cs without venue names) is acceptable — keep it.
- If ALL files fail relevance checks, write: `[ERROR]: Folder contains brochures from other venues. Needs manual review.`

**Step 5 — Consolidate:**
Combine all extracted content with headers and dividers:
```markdown
### Source: {filename_1}

{content_1}

---

### Source: {filename_2}

{content_2}
```

**Step 6 — Handle partial failures:**
If some files extracted successfully but others failed:
- Prepend `[WARNING]: Some files in folder were unreadable.` followed by two newlines
- Include all successfully extracted content below the warning

If ALL files failed or folder is empty:
- Write `[ERROR]: Files are images without readable text.` (if all were images)
- Write `[ERROR]: Link unreachable.` (if folder couldn't be accessed)

### Type: GDOCS (Google Docs document)

Direct text extraction — simplest case.

**Step 1:**
Extract document ID from URL (between `/document/d/` and the next `/`).
```
mcp__google-drive__getGoogleDocContent({ documentId: "{DOC_ID}" })
```

**Step 2:**
The response contains the full document text. Use as-is (Google Docs content is already clean).

### Type: WEB_SCRAPE (Calameo, Canva, Heyzine, etc.)

Web-based brochure platforms and design tools.

**Step 1:**
```
mcp__firecrawl__firecrawl_scrape({
  url: "{brochure_link}",
  formats: ["markdown"],
  onlyMainContent: true,
  waitFor: 8000
})
```

**Step 2 — Special handling for Safe Links:**
Some URLs are wrapped in Outlook/SafeLinks redirects (e.g., `kor01.safelinks.protection.outlook.com`). Extract the actual URL from the `url=` parameter, URL-decode it, and scrape the decoded URL instead.

**Step 3 — If scrape returns empty:**
Write `[ERROR]: Files are images without readable text.`

---

## Content Cleaning

Brochure content is generally cleaner than website scrapes, but still strip:

- Cookie consent banners and GDPR notices
- Navigation menus and footer links
- "Share", "Print", "Download" button text
- Platform branding (e.g., "Published with Calameo", "Made with Canva")
- Page numbers from PDF extraction (e.g., isolated "1", "2", "3" lines)

**Preserve:**
- All tables (pricing, package details, menu options)
- Bullet point lists
- Pricing hierarchies and package breakdowns
- Section headings and structure
- Contact information

**Deduplication:**
When multiple files from the same folder contain identical "Terms & Conditions" or "General Conditions" blocks, keep only the most complete version. Other content is kept in full.

---

## Safety Rules

1. **Never overwrite**: Before writing to `brochure_text`, confirm the field is empty via the Airtable filter. If a record already has content, skip it.
2. **Never modify source fields**: `brochure_link` is read-only for this workflow.
3. **Rate limiting**: Wait at least 2 seconds between Firecrawl API calls.
4. **Batch confirmation**: Always ask the user before proceeding to the next batch.
5. **Character limit**: Truncate at 95,000 characters if needed. Cut at last complete paragraph and append `\n\n[Content truncated at 95,000 character limit]`.

---

## Logging Format (workings_temp.md)

Each session appends a block:

```markdown
---

## Session: {timestamp}
**Total eligible records:** {count}
**Breakdown:** {X} GDrive files, {Y} folders, {Z} docs, {W} web, {S} skipped

### Batch 1 (Records 1-5)

| # | Record ID   | Venue Name              | URL Type      | Status    | Files | Chars  | Notes                 |
|---|-------------|-------------------------|---------------|-----------|-------|--------|-----------------------|
| 1 | recABC123   | Chateau de la Napoule   | GDRIVE_FILE   | SUCCESS   | 1     | 12,450 |                       |
| 2 | recDEF456   | Chateau de Lassalle     | GDRIVE_FOLDER | SUCCESS   | 4     | 28,320 | 1 image skipped       |
| 3 | recGHI789   | Domaine du Rodier       | GDOCS         | SUCCESS   | 1     | 5,100  |                       |
| 4 | recJKL012   | Example Venue           | WEB_SCRAPE    | ERROR     | 0     | 0      | Link unreachable      |
| 5 | recMNO345   | Another Venue           | GDRIVE_FILE   | SUCCESS   | 1     | 8,900  |                       |

**Batch 1 Summary:** 4 success, 1 error
**Total chars written:** 54,770
```
