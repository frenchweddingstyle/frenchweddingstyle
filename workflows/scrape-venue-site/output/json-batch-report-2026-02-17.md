# Venue JSON Generation — Batch Report
## Date: 2026-02-17
## Total eligible: 14 | Processed: 13 | Skipped: 1

---

### Batch 1 (5/5 successful)

| # | Venue | Slug | Full Chars | Summary Chars | Sources |
|---|-------|------|------------|---------------|---------|
| 1 | Bastide du Puget | bastide-du-puget | 23,474 | 1,081 | scraped+brochure |
| 2 | Chateau de Saint-Martin-du-Tertre | chateau-de-saint-martin-du-tertre | 31,388 | 1,140 | scraped+brochure |
| 3 | Château d'Aveny | chateau-daveny | 29,891 | 1,049 | scraped only |
| 4 | Domaine de Lamanon | domaine-de-lamanon | 19,104 | 1,099 | scraped only |
| 5 | Chateau de Sannes | chateau-de-sannes | 15,797 | 1,114 | scraped only |

### Batch 2 (5/5 successful)

| # | Venue | Slug | Full Chars | Summary Chars | Sources |
|---|-------|------|------------|---------------|---------|
| 6 | Chateau de Pondres | chateau-de-pondres | 21,449 | 1,068 | scraped only |
| 7 | Chateau de Saint Cecile | chateau-de-saint-cecile | 20,976 | 1,065 | scraped+brochure |
| 8 | Collines de Manon | collines-de-manon | 19,356 | 1,161 | scraped+brochure |
| 9 | Chateau de Sanse | chateau-de-sanse | 17,384 | 1,046 | scraped only |
| 10 | Chateau de Villette | chateau-de-villette | 19,275 | 1,034 | scraped only |

### Batch 3 (3/4 successful, 1 skipped)

| # | Venue | Slug | Full Chars | Summary Chars | Sources |
|---|-------|------|------------|---------------|---------|
| 11 | Chateau Camiac | — | SKIPPED | — | MANUAL_CHECK marker |
| 12 | Chateau de Ferrieres | chateau-de-ferrieres | 32,354 | 1,134 | scraped+brochure |
| 13 | Chateau de Robernier | chateau-de-robernier | 15,981 | 1,078 | scraped only |
| 14 | Chateau la Tour Vaucros | chateau-la-tour-vaucros | 32,163 | 1,065 | scraped only |

---

### Summary

- **Total venues processed:** 13/14
- **Skipped:** 1 (Chateau Camiac — site returning 500 errors during scraping)
- **Total full JSON chars written:** 298,592
- **Total summary JSON chars written:** 14,134
- **Venues with brochure data:** 5 (Bastide du Puget, Chateau de Saint-Martin-du-Tertre, Chateau de Saint Cecile, Collines de Manon, Chateau de Ferrieres)
- **Venues with scraped content only:** 8

### Bug Fix Applied
- Fixed `process_venue.py` `--fetch-json-sources` mode: Airtable single-record GET endpoint doesn't support `fields[]` query parameter (returns 422). Removed the field filtering — now fetches all fields from the record.
