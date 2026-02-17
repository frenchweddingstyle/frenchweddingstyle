# Extract Brochures — Final Report
**Date:** 2026-02-17 (Session 2)

## Summary

| Metric | Count |
|--------|-------|
| Total Airtable records queried | 200 |
| Skipped (emails) | 64 |
| Skipped (text notes) | 9 |
| **Actionable records** | **127** |
| Successfully extracted | 108 |
| Errors | 19 |
| **Success rate** | **85%** |

## Breakdown by Type

| Type | Total | OK | Error | Success Rate |
|------|-------|-----|-------|-------------|
| GDRIVE_FILE | 86 | 79 | 7 | 92% |
| GDRIVE_FOLDER | 28 | 27 | 1 | 96% |
| GDOCS | 4 | 2 | 2 | 50% |
| WEB_SCRAPE | 9 | 1 | 8 | 11% |

## Error Summary (19 total)

### Image-based PDFs (no extractable text) — 4
- Hotel Plaza Athenee
- Chateau Belle Epoque
- Domaine De L'abbaye De Maizieres
- Chateau de la Valouze

### Canva designs (not scrapable) — 3
- Chateau de Vauchelles
- Chateau de la Gruerie
- Domaine de Vauluisant

### Calameo flipbooks (image-based) — 3
- Chateau des Barrenques
- Abbaye Saint Sever de Rustan
- Domaine de La Thibaudiere

### Heyzine flipbook (image-based) — 1
- Grand Hotel du Cap Ferrat

### Image-based uploaded docs — 2
- Coeur De Combray
- Chateau De La Poterie

### Link unreachable / download failed — 3
- Hotel Crillon le Brave
- Chateau de Maulmont
- Chateau Soulac

### Chateau d'Aveny (Calameo) — 1
### Script timeout — 1
- Chateau de Villele (GDRIVE_FOLDER)

## Processing Details

- **Batches processed:** 26
- **Processing method:** Python script (`extract_brochure.py`) for Google Drive URLs; Firecrawl MCP for web scrapes
- **Parallel execution:** 5 concurrent extractions per batch
- **Airtable field updated:** `brochure_text`
- **Error markers:** `[ERROR]: ...` written for all failed records

## Notes

- All WEB_SCRAPE errors are inherent platform limitations (Canva, Calameo, Heyzine render as images — no text extractable)
- "Link unreachable" errors may be permission issues or deleted files
- Image-based PDFs contain scanned pages without OCR text layer
- Full session log: `workflows/extract-brochures/working/workings_temp.md`
