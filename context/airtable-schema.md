# Airtable Schema — North Star Reference

> **Base**: French Wedding Style | **ID**: `appFQYNRTuooIRZZz` | **Plan**: Team (Plus) — 50k records/table, 5 req/sec API
> **Last Audited**: 2026-02-20 | **Tables**: 14 live

This document is the single source of truth for the Airtable database structure. It tracks the **live state** (what exists now), the **target state** (what the gameplan prescribes), and a **delta tracker** showing what's done vs. pending.

**Update rule**: Every time Claude reads from or writes to Airtable, check whether this document needs updating.

---

## Table of Contents

1. [Delta Summary Dashboard](#delta-summary-dashboard)
2. [Table Inventory](#table-inventory)
3. [Venues](#1-venues)
4. [Suppliers](#2-suppliers)
5. [Real Weddings](#3-real-weddings)
6. [Regions](#4-regions)
7. [Locations](#5-locations)
8. [Sales Log](#6-sales-log)
9. [Magazines](#7-magazines)
10. [Article Table](#8-article-table)
11. [[Admin] AI Prompts](#9-admin-ai-prompts)
12. [vf_table](#10-vf_table)
13. [Instagram Educational Posts](#11-instagram-educational-posts)
14. [Vendor Categories](#12-vendor-categories)
15. [Venue Review Data](#13-venue-review-data)
16. [Lookup](#14-lookup)
17. [Tables to Create (Target)](#tables-to-create-target)
18. [Tables to Remove (Target)](#tables-to-remove-target)
19. [Cross-Table Standards](#cross-table-standards)
20. [Key Relationships](#key-relationships)
21. [Naming Conventions](#naming-conventions)
22. [API Rate Limit Strategy](#api-rate-limit-strategy)

---

## Delta Summary Dashboard

| Change Category | Total | Done | Pending | Blocked |
|----------------|-------|------|---------|---------|
| Tables to rename | 3 | 0 | 3 | 0 |
| Tables to remove | 2 | 2* | 0 | 0 |
| Tables to create | 5 | 1 | 4 | 0 |
| Fields to add | ~28 | 0 | ~28 | 0 |
| Fields to remove | ~8 | 0 | ~8 | 0 |
| Fields to rename | ~12 | 0 | ~12 | 0 |
| Views to create | ~20 | 0 | ~20 | 0 |

*\* "Memberships" and "Venue (VoiceFlow)" were listed in the gameplan as tables to remove. Neither exists in the live DB — either already deleted or were misidentified. However, **2 unlisted tables** (Venue Review Data, Lookup) were found in the live DB that the gameplan did not account for.*

---

## Table Inventory

| # | Table Name (Live) | Table ID | Target Name | Records (est.) | Status | Role |
|---|-------------------|----------|-------------|----------------|--------|------|
| 1 | Venues | `tblIEJQNynXIsD8GL` | Venues (keep) | ~200+ | Active — needs optimization | Core content |
| 2 | Suppliers | `tblbj0jslo73AmQ5A` | **Vendors** (rename) | ~50-100 | Active — rename + optimize | Core content |
| 3 | Real Weddings | `tbljA9gnZH0Of1Xbz` | Real Weddings (keep) | ~200+ | Active — needs optimization | Core content |
| 4 | Regions | `tblQGaFvwoQzda8DH` | Regions (keep) | ~15-20 | Active — add fields | Taxonomy |
| 5 | Locations | `tbl3QMtqbOqLdKKY5` | Locations (keep) | ~50-100 | Active — add fields | Taxonomy |
| 6 | Sales Log | `tblbkgGY0vKvOYB7q` | Sales Log (keep) | ~50-100 | Active — no changes | Operations |
| 7 | Magazines | `tbl8isaplWP4Dhgiq` | Magazines (keep) | ~5-10 | Active — low priority | Reference |
| 8 | Article Table | `tblw67BNZGYURhwIH` | **Articles** (rename) | ~200+ | Active — rename + optimize | Core content |
| 9 | [Admin] AI Prompts | `tbl8lfXfGEkSgFLpC` | [Admin] AI Prompts (keep) | ~10-20 | Active — no changes | System |
| 10 | vf_table | `tblPXaJGDQyTtNK1w` | **VoiceFlow Agents** (rename) | ~25+ | Active — rename | Integration |
| 11 | Instagram Educational Posts | `tblAMMpVXx36L46XV` | Keep as-is | Unknown | Active — no changes | Social |
| 12 | Vendor Categories | `tblUk4uFlHBPXF2Nc` | Vendor Categories (expand) | ~8-10 | Active — needs expansion | Taxonomy |
| 13 | Venue Review Data | `tbli80M6XESvyktAg` | **TBD** — not in gameplan | Unknown | **NEEDS REVIEW** | Content? |
| 14 | Lookup | `tbl9XwmhN5thwIgAb` | **TBD** — not in gameplan | Unknown | **NEEDS REVIEW** | Legacy? |
| 15 | Location Pages | `tblOgYxCad7qGUTB2` | Location Pages (new) | 36 | **Active — just created** | Core content |
| 16 | Hub Pages | — | Hub Pages (new) | 0 | **TO CREATE** | Core content — curated venue collections |

---

## 1. Venues

**Table ID**: `tblIEJQNynXIsD8GL` | **Views**: Grid view | **Role**: Core content table

### Live Fields (48 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | venue_name | singleLineText | `fldaylT3LCKJYZnDS` | Primary identifier |
| 2 | venue_url_scraped | multilineText | `fldeRmaPxxw3mLqHi` | Scraped website content (Markdown) |
| 3 | venue_url | url | `fldXLFFZUbyhxxpEP` | Venue's own website URL |
| 4 | brochure_text | multilineText | `fldwitXHAFuCt2r8U` | Extracted brochure content |
| 5 | full_venue_json | richText | `fldNNdlQP6SljNwaX` | Complete JSON record (~320 fields) |
| 6 | summary_venue_json | richText | `fldta1FdbnJz49mVQ` | 20-field summary JSON |
| 7 | Email | email | `fldIwrrmXL6iUR8m4` | Contact email |
| 8 | Brochure Text (Email) | richText | `flds1Fu7pwyMbOHfT` | **REDUNDANT** — duplicate of brochure_text? |
| 9 | brochure_link | url | `fldVwTdlM6xykr7VG` | Source brochure URL |
| 10 | Profile Image | multipleAttachments | `fldufwJShaE2h1o9l` | Venue images |
| 11 | venue_address | multilineText | `fldiInn3YgFESFOVd` | Physical address |
| 12 | image_url | url | `fldEyYOzuj3ToirIP` | Card thumbnail URL |
| 13 | fws_url | url | `fldvNHP5ccON2dPUF` | FWS listing page URL |
| 14 | fwv_url | url | `fldpik3w3RcXHXRO9` | French Wedding Venues URL |
| 15 | chateaubee_url | url | `fldRNcTbbXlMSql8t` | Chateaubee listing URL |
| 16 | wedinspire_url | url | `fld4mY8vWHU8GgfBy` | WedInspire listing URL |
| 17 | gps_coordinates | singleLineText | `fld6Ud74eCiVXgyX8` | Lat/lon from geocoding |
| 18 | Venue Description | formula | `fld8zcMrhQWr9uJTO` | Concatenates name + region + about + address |
| 19 | venue_listing | multilineText | `fldcl1wpk7nTkqbcH` | Generated listing content |
| 20 | FWS Member | singleSelect | `fldXy34qCBX7dG5WZ` | Options: Listing, No Listing |
| 21 | Venue Summary | singleLineText | `fldUtGsFueMfXnNwj` | Short summary text |
| 22 | main_region | multipleRecordLinks | `fldvtYoMEB8vKiar1` | → Regions (prefersSingle) |
| 23 | region | formula | `fldgFXJjfE2b27eod` | ARRAYJOIN of main_region |
| 24 | venue_type_style | multipleSelects | `fldtpEKtY6vx6DbPR` | 17 options (Chateau, Villa, Hotel, etc.) |
| 25 | max_guest_capacity | number (int) | `fldAuTP76RFJImNry` | Maximum guests |
| 26 | guest_sleep_onsite | number (int) | `fldl26JNXEWMYC3i8` | On-site accommodation capacity |
| 27 | features_venue | multipleSelects | `fldr0ZSweXLTXRndu` | 17 options (Pool, Fireworks, Pet Friendly, etc.) |
| 28 | venue_only_dry_hire_price_eur | currency (EUR) | `fldWJL7KZlTgje8TS` | Dry hire price |
| 29 | min_from_price_eur | currency (EUR) | `fldmoY37H4dAX4ZiX` | Minimum price |
| 30 | max_from_price_eur | currency (EUR) | `fldQh8Y3BHXr7ELCD` | Maximum price |
| 31 | FWS Review | url | `fldkYp6sxexOY45ng` | Link to FWS review blog post |
| 32 | Member | formula | `fldqnIYYCF9s5I1z1` | **BROKEN** — references deleted field. Shows error. |
| 33 | Instagram | url | `fldSGdbEBSBFT74ys` | Venue Instagram URL |
| 34 | Phone | phoneNumber | `fld0iCgjvcC7bbCG4` | Contact phone |
| 35 | Google Drive | url | `fldc2J2CgJGDQMkxP` | Google Drive folder link |
| 36 | Minimum Nights | singleLineText | `fldpmjoMj1azkyLGH` | Min rental nights |
| 37 | Social Media Posts | singleLineText | `fldT1OVIYJ4tOoWtu` | Social media tracking |
| 38 | Closest Town/ City | singleSelect | `fldVz6FLlXQgAbhVy` | 21 options (Aix, Marseille, Nice, Paris, etc.) |
| 39 | what_we_love | multilineText | `fldVOr7mvM0B9ZrNv` | Editorial "what we love" section |
| 40 | VoiceFLow | formula | `fldn1kWsd5pn9mdLh` | **REDUNDANT** — JSON formula for VoiceFlow (vf_table already handles this) |
| 41 | About | multilineText | `fldlfpyqA9JntoGjD` | Old listing page section |
| 42 | Accom/ Amen | multilineText | `fldIVhyl55huhAVEB` | Old listing page section |
| 43 | Getting There | multilineText | `fldq5MdV0AS0AXLu0` | Old listing page section |
| 44 | Beyond Weddings | multilineText | `fldUnnfIjv6WAcWHG` | Old listing page section |
| 45 | Pricing | richText | `fldbDkdTG0p1kPJxO` | Old listing page section |
| 46 | Locations | multipleRecordLinks | `fldsrC8FSRaVvI8ig` | → Locations |
| 47 | Contact Info | singleLineText | `fldgQx5r2IxBDnito` | Contact details |
| 48 | Real Weddings | multipleRecordLinks | `fld7JD8i8PE8zj6xi` | → Real Weddings |
| 49 | Real Weddings 2 | singleLineText | `fldd9q91hHuX5UPQu` | **REDUNDANT** — text duplicate of linked field? |
| 50 | Sales Log | multipleRecordLinks | `fldm8o0uEzSpgN78T` | → Sales Log |
| 51 | vf_table | multipleRecordLinks | `fldEXFWdd1oqKHlBK` | → vf_table |
| 52 | vf_table 2 | singleLineText | `fldnzIQ9Ji0KJO17z` | **REDUNDANT** — unclear purpose |
| 53 | location_pages | multipleRecordLinks | `fldeMfwIsJ5iZ2B3D` | → Location Pages (full branch: parent region + sub-region + cities + areas) |

### Proposed Changes (from Gameplan)

| Action | Field | Details | Status |
|--------|-------|---------|--------|
| REMOVE | Brochure Text (Email) | Redundant with brochure_text | Pending |
| REMOVE | Real Weddings 2 | Text duplicate of linked field | Pending |
| REMOVE | vf_table 2 | Redundant/unclear purpose | Pending |
| REMOVE | VoiceFLow (formula) | Redundant — vf_table looks up full_venue_json directly | Pending |
| REMOVE | Member (formula) | Broken formula — references deleted field | Pending |
| ADD | publish_status | singleSelect: Draft, Review, Published, Archived | Pending |
| ADD | meta_title | singleLineText (60 chars, for SEO) | Pending |
| ADD | meta_description | multilineText (155 chars, for SEO) | Pending |
| ADD | url_slug | formula from venue_name (e.g., "villa-les-sablettes") | Pending |
| RENAME | About → about_text | Provisional — may consolidate with full_venue_json | Pending |
| RENAME | Accom/ Amen → accommodation_amenities | Provisional | Pending |
| RENAME | Getting There → getting_there | Provisional | Pending |
| RENAME | Beyond Weddings → beyond_weddings | Provisional | Pending |
| RENAME | Pricing → pricing_details | Provisional | Pending |
| RENAME | Contact Info → contact_info | Provisional | Pending |
| ADD | primary_style | singleSelect | Split from `venue_type_style` — single primary style for hub page filtering. Options: Chateau, Villa, Vineyard, Farmhouse, Garden, Barn, Domaine, Beach, Orangerie, Hotel, Manor, Estate | Pending |
| ADD | style_attributes | multipleSelects | Split from `venue_type_style` — secondary/additional style tags | Pending |

### Data Gaps (Blocking Hub Pages)

- **Style classification**: 130/189 venues (69%) have no `venue_type_style` value — blocks all Style hub pages
- **Pricing**: ~60% of venues missing `min_from_price_eur`/`max_from_price_eur` — data exists in `full_venue_json`, needs extraction to columns for Budget hub page filtering

### Hybrid Data Model (Key Principle)

**Individual columns** (for filtering, sorting, VoiceFlow, website filter UI):
`venue_name`, `venue_type_style`, `features_venue`, `max_guest_capacity`, `guest_sleep_onsite`, `min_from_price_eur`, `max_from_price_eur`, `main_region`, `Locations`, `Closest Town/ City`, `gps_coordinates`, `image_url`, `fws_url`, `FWS Member`, `publish_status` (to add)

**JSON blobs** (for detailed page rendering):
`full_venue_json` (~320 fields), `summary_venue_json` (20 fields)

---

## 2. Suppliers

**Table ID**: `tblbj0jslo73AmQ5A` | **Views**: Grid view | **Target Name**: **Vendors**

### Live Fields (21 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | Supplier | multilineText | `fldDdCmIyDU46I52H` | Primary name field |
| 2 | Listing ID | number (int) | `fldOZbN88uVTryUhL` | WordPress listing ID |
| 3 | Vendor Category | singleSelect | `fldJV9tB3PaWKoaxC` | 8 options: Venue, Photographer, Celebrant, Florist, Entertainment, Entertainer, Planner, Videographer |
| 4 | Lookup Key | formula | `fldIcbGGOqmKBVloI` | Lowercase name + domain for matching |
| 5 | Email | email | `fldwD7zNlkBmzyo6C` | Contact email |
| 6 | Website | url | `fldjlH9n4x2dq0l6b` | Vendor website |
| 7 | Contact Info | singleLineText | `fldzS4mJ2k6VNGOj4` | Contact details |
| 8 | Real Weddings (Photographer) | multipleRecordLinks | `fldUEirJrXBf5tq3A` | → Real Weddings (as Photographer) |
| 9 | Regions | multipleRecordLinks | `fldKaHDMIZi79Uk0r` | → Regions |
| 10 | Last Payment | date (ISO) | `fldSVKO5Tmlbusa20` | Last payment date |
| 11 | Membership Plan | singleSelect | `fldI8q6QwP4gJLyZE` | ~20 options (messy — many duplicates with trailing spaces) |
| 12 | Field 11 | singleSelect | `fld5MgemqfD8fV2PL` | **UNCLEAR** — ad-hoc notes/statuses as select options |
| 13 | Membership renewal | date (ISO) | `fldr3dpe8i4dXq4Cv` | Renewal date |
| 14 | Instagram Post | date (ISO) | `fldmTdtG1XzyiG0Qk` | Last Instagram post date |
| 15 | FWS URL | multilineText | `fld5ryUcmW1vNbTxO` | FWS listing URL |
| 16 | Contact Number | multilineText | `fldPd8jNQa7dq8w69` | Phone number |
| 17 | Package | singleSelect | `flde5jNDqbGTZNq4V` | **REDUNDANT** — overlaps with Membership Plan. 5 options (mix of language and package types) |
| 18 | Venues | singleLineText | `fldAbxRwSChRdgxsP` | **SHOULD BE** linked record if needed |
| 19 | Social Media Posts | singleLineText | `fldaqFJHc7s6z8XW7` | Social media tracking |
| 20 | Invoicing | multipleRecordLinks | `fldmLACvO1y3cx5G1` | → Sales Log |
| 21 | Real Weddings (Planner) | multipleRecordLinks | `flddE2jvFxY2C1Gzc` | → Real Weddings (as Planner) |
| 22 | Instagram Educational Posts | multipleRecordLinks | `fldmkxt5lwbZUZJ59` | → Instagram Educational Posts |

### Known Issues

- **Membership Plan** has ~20 options with many near-duplicates: "6 month free", "6 month free " (trailing space), "6month Free", "Premium", "Premium " (trailing space), "Signature", "Signature " (trailing space). Needs consolidation.
- **Field 11** is a singleSelect being used as a free-text notes field (options like "need more value from us", "paid 3000 euros for banner ad + premium listing"). Should be a multilineText or removed.
- **Package** overlaps with Membership Plan and contains language-related options ("French", "English") mixed with package descriptions.

### Proposed Changes (from Gameplan)

| Action | Field | Details | Status |
|--------|-------|---------|--------|
| RENAME TABLE | Suppliers → Vendors | Aligns with public-facing terminology | Pending |
| RENAME | Supplier → vendor_name | snake_case convention | Pending |
| RENAME | Listing ID → listing_id | snake_case convention | Pending |
| RENAME | Vendor Category → vendor_category | Convert to linked record to Vendor Categories table | Pending |
| REMOVE | Field 11 | Unclear purpose, inconsistent naming | Pending |
| REMOVE | Package | Overlaps with Membership Plan | Pending |
| REMOVE | Venues (text) | Should be linked record if needed | Pending |
| ADD | publish_status | singleSelect: Draft, Review, Published, Archived | Pending |
| ADD | meta_title | singleLineText (SEO) | Pending |
| ADD | meta_description | multilineText (SEO) | Pending |
| ADD | url_slug | singleLineText (e.g., "nicolas-elsen") | Pending |
| ADD | profile_image | attachment | Pending |
| ADD | about_text | multilineText (vendor description) | Pending |

---

## 3. Real Weddings

**Table ID**: `tbljA9gnZH0Of1Xbz` | **Views**: Grid view, Calendar, Gallery | **Role**: Core content

### Live Fields (17 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | Blog Title | singleLineText | `fldnDVrlWA0uNEsvB` | Post title |
| 2 | Timestamp | singleLineText | `flduziokb3GLwz5H7` | Submission timestamp (text, not date) |
| 3 | RW Status | singleSelect | `fldjUDJk4cYWP3coS` | 8 options: Not Started → Published |
| 4 | Created Time | createdTime | `fldshaswiILCLSwMN` | Auto-generated |
| 5 | Form | singleLineText | `fldpAHCxiG2omwQUR` | Submission form link |
| 6 | Contact Name | singleLineText | `fldqSli2ZESx3nve4` | Submitter name |
| 7 | Scheduled/ Posted | date (friendly) | `fldfzSCpVJLz0PROz` | Publish/schedule date |
| 8 | Venue | multipleRecordLinks | `fldK09rW7tpUkSJv3` | → Venues |
| 9 | Venue Description (lookup) | multipleLookupValues | `fldp3eWfxemBFvp32` | Looks up Venue Description from Venues |
| 10 | Photographer | multipleRecordLinks | `fld16Jme4pWjnhbVF` | → Suppliers (prefersSingle) |
| 11 | Planner | multipleRecordLinks | `fld9pwjyMmQ5lv2t1` | → Suppliers (prefersSingle) |
| 12 | Regions | multipleRecordLinks | `fldmKs6Zk3HSbDZZ4` | → Regions |
| 13 | Wedding Team | richText | `fldaiZ5JBIJP1Jhsp` | Credits for all vendors |
| 14 | Magazine | multipleRecordLinks | `fldlVyUXI7v4tysBJ` | → Magazines |
| 15 | FWS URL | url | `fldTXGQDkOpPe7eXx` | Published post URL |
| 16 | Pin | checkbox | `fldkHB5CHHkYh0JdO` | Pinned/featured flag |
| 17 | Google Drive Link | url | `fldRBBlgVPHk3SyvY` | Image folder |
| 18 | Image | multipleAttachments | `fldlCvkkKh59TOTsg` | Attached images |

### Proposed Changes (from Gameplan)

| Action | Field | Details | Status |
|--------|-------|---------|--------|
| ADD | publish_status | singleSelect — align with Draft → Review → Published → Archived (supplement RW Status) | Pending |
| ADD | meta_title | singleLineText (SEO) | Pending |
| ADD | meta_description | multilineText (SEO) | Pending |
| ADD | url_slug | singleLineText | Pending |
| ADD | featured_image | attachment (primary image for cards/social) | Pending |
| ADD | image_gallery_urls | multilineText (JSON array of processed image URLs) | Pending |
| RENAME | Blog Title → title | snake_case convention | Pending |
| RENAME | Contact Name → submitted_by | Clearer purpose | Pending |

---

## 4. Regions

**Table ID**: `tblQGaFvwoQzda8DH` | **Views**: Grid view | **Role**: Top-level geography taxonomy

### Live Fields (6 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | Regions of France | singleLineText | `fldz8JyKEJShFtY4D` | Region name (e.g., "Provence") |
| 2 | Venues | multipleRecordLinks | `fldVCsSfnNVKXXWbi` | → Venues (inverse of main_region) |
| 3 | Locations | multipleRecordLinks | `fldy7Y1QTIKnTfkao` | → Locations |
| 4 | Real Weddings | multipleRecordLinks | `fldCgYJZcP849keWp` | → Real Weddings |
| 5 | Suppliers | multipleRecordLinks | `fld0VDga75Au8Rtg1` | → Suppliers |
| 6 | Description | aiText | `fldGuoIZig7XMn6xN` | AI-generated regional description |

### Proposed Changes (from Gameplan)

| Action | Field | Details | Status |
|--------|-------|---------|--------|
| ADD | url_slug | singleLineText (e.g., "provence", "south-of-france") | Pending |
| ADD | page_title | singleLineText (for location page SEO) | Pending |

---

## 5. Locations

**Table ID**: `tbl3QMtqbOqLdKKY5` | **Views**: Grid view | **Role**: Sub-region taxonomy

### Live Fields (3 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | Location | singleLineText | `fldRS1fd4qV53JJZZ` | Location name |
| 2 | Region | multipleRecordLinks | `fldzkORjJorXfSlbb` | → Regions |
| 3 | Venues | multipleRecordLinks | `fld64Pd88zuNVOdjw` | → Venues (inverse of Locations) |

### Proposed Changes (from Gameplan)

| Action | Field | Details | Status |
|--------|-------|---------|--------|
| ADD | url_slug | singleLineText (e.g., "provence", "french-riviera") | Pending |
| ADD | parent_url_path | singleLineText (e.g., "/locations/south-of-france/") | Pending |

---

## 6. Sales Log

**Table ID**: `tblbkgGY0vKvOYB7q` | **Views**: Grid view | **Role**: Operations (invoicing)

### Live Fields (13 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | Invoice Invoice Number | multilineText | `flddUM8EYISfiPB2t` | Invoice number |
| 2 | Client Name | multilineText | `fld74NsWWrp6cGwCN` | Client name |
| 3 | Invoice Date | date (D/M/YYYY) | `fldfFNYuwHWa1EZM1` | Invoice date |
| 4 | Renewal Date | formula | `fldO2VyfDx8giW0iI` | +1 year from invoice date |
| 5 | Alert | formula | `fldvUp4S9VzEI2S78` | Overdue / Due Soon / OK |
| 6 | Venues | multipleRecordLinks | `fldT556CtvoFTs9KC` | → Venues |
| 7 | Supplier | multipleRecordLinks | `fldGzJp9YfVk2Blw9` | → Suppliers |
| 8 | Package | multipleSelects | `fldAPmyTpt8JBeRui` | 9 options: Venue/Supplier tiers + extras |
| 9 | Invoice Paid to Date | number (2dp) | `fld5Krpa9wWhQ4ckf` | Amount paid |
| 10 | Invoice Due Date | date (D/M/YYYY) | `fldHFF89sjn4JLU8P` | Payment due date |
| 11 | Invoice Status | singleSelect | `fldi61zcpvzmoyp0Q` | Paid, Sent, Cancelled, Draft |
| 12 | Client Currency | singleSelect | `fldVHoDURj2X1Eow1` | EUR, AUD, GBP |
| 13 | Invoice Exchange Rate | number (2dp) | `fldU9QqrcMsDqRjTh` | Exchange rate |

**No changes planned** — internal operations table.

---

## 7. Magazines

**Table ID**: `tbl8isaplWP4Dhgiq` | **Views**: Grid view | **Role**: Magazine feature tracking

### Live Fields (3 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | Name | singleLineText | `fldmrJECqhwEVJlAp` | Magazine name |
| 2 | Cover | multipleAttachments | `fldXvNEHj0fy7ledl` | Cover image |
| 3 | Real Weddings | multipleRecordLinks | `fldpttPCJ22LlIpSL` | → Real Weddings |

**No changes planned** — low priority reference table.

---

## 8. Article Table

**Table ID**: `tblw67BNZGYURhwIH` | **Views**: Grid view | **Target Name**: **Articles**

### Live Fields (6 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | Keyword | multilineText | `flde42Y06Qvz5L1Ki` | Target keyword |
| 2 | Category | singleSelect | `fldQEFvqPwber6FLO` | 37 options (very granular) |
| 3 | Status | singleSelect | `fldJNM1Ppmpptbcea` | Published, Needs Updating, Updated, Draft in WordPress, Brief Done, Not started |
| 4 | URL | multilineText | `fldO84Zii4UXSnims` | Current WordPress URL |
| 5 | Title | multilineText | `fldw3XMBHEjiN1WH1` | Article title |
| 6 | Subtitle | singleLineText | `fldJXQ3tfwbByGLK0` | Subtitle |
| 7 | Google Doc Link | richText | `fld0WnfiEGlPQARmg` | Link to content in Google Docs |

### Proposed Changes (from Gameplan)

| Action | Field | Details | Status |
|--------|-------|---------|--------|
| RENAME TABLE | Article Table → Articles | Clearer naming | Pending |
| ADD | publish_status | singleSelect — supplement existing Status | Pending |
| ADD | meta_title | singleLineText (SEO) | Pending |
| ADD | meta_description | multilineText (SEO) | Pending |
| ADD | url_slug | singleLineText | Pending |
| ADD | content_body | richText (article content — currently in Google Docs) | Pending |
| RENAME | Keyword → primary_keyword | snake_case convention | Pending |
| RENAME | URL → current_wp_url | Clarifies purpose (migration mapping) | Pending |

---

## 9. [Admin] AI Prompts

**Table ID**: `tbl8lfXfGEkSgFLpC` | **Views**: Grid view | **Role**: System/workflow support

### Live Fields (3 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | Name | singleLineText | `fldvSdG8UuXMg9sXN` | Prompt identifier |
| 2 | Prompt_Text | multilineText | `fldf8oNYNBjH78syG` | Prompt content |
| 3 | Record ID | formula | `fld4680tmefzAgLqH` | RECORD_ID() |

**No changes planned** — workflow support table.

---

## 10. vf_table

**Table ID**: `tblPXaJGDQyTtNK1w` | **Views**: Grid view | **Target Name**: **VoiceFlow Agents**

### Live Fields (8 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | venue_id | singleLineText | `fldiZBqKA88GZRqZ3` | Venue identifier |
| 2 | Live | checkbox | `fld3MnIdYSauOWIK1` | Is agent live? |
| 3 | venue_name | singleLineText | `fldEhLJ2d7doO8OE4` | Venue name |
| 4 | Venues | multipleRecordLinks | `fldd6sHTwDkLev07k` | → Venues (prefersSingle) |
| 5 | image_url (from Venues) | multipleLookupValues | `fldEp52jJS2RaUgvL` | Lookup: image_url from Venues |
| 6 | full_venue_json (from Venues) | multipleLookupValues | `fldCl1ZaqDVzfVdxk` | Lookup: full_venue_json from Venues |
| 7 | profile_url | url | `fldidtKXWhmymDzhP` | VoiceFlow profile URL |
| 8 | json_file | multilineText | `flduqXA6ShD06YLxw` | JSON file reference |

### Proposed Changes (from Gameplan)

| Action | Field | Details | Status |
|--------|-------|---------|--------|
| RENAME TABLE | vf_table → VoiceFlow Agents | Clearer purpose | Pending |

---

## 11. Instagram Educational Posts

**Table ID**: `tblAMMpVXx36L46XV` | **Views**: Grid view | **Role**: Social content tracking

### Live Fields (10 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | Post | singleLineText | `fld00y1GHFDNb20ur` | Post identifier |
| 2 | Vendor | multipleRecordLinks | `fldoPSVpbCcQfoUTE` | → Suppliers (prefersSingle) |
| 3 | Vendor Type | multipleRecordLinks | `fldRa0jrJZve4iFCc` | → Vendor Categories (prefersSingle) |
| 4 | Date Schedule/ Posted | date (local) | `fldbzFoTZasqBEV5y` | Post date |
| 5 | Message 1 | singleLineText | `fldCOpuwFbXEqpVei` | Content slide 1 |
| 6 | Message 2 | singleLineText | `fldbJPvvzOldZi9hd` | Content slide 2 |
| 7 | Message 3 | singleLineText | `fld540WqXMoFxbIXe` | Content slide 3 |
| 8 | Message 4 | singleLineText | `fldKzJwxSgrlz1IS2` | Content slide 4 |
| 9 | Message 5 | singleLineText | `fldyzhPQ9D7S57PTe` | Content slide 5 |
| 10 | Message 6 | singleLineText | `fldY2qNZmttShsriF` | Content slide 6 |

**No changes planned** — social content tracking.

---

## 12. Vendor Categories

**Table ID**: `tblUk4uFlHBPXF2Nc` | **Views**: Grid view | **Role**: Taxonomy for vendor types

### Live Fields (7 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | Name | singleLineText | `fldHqHAIQprtybVsI` | Category name |
| 2 | Notes | multilineText | `fldZcuWXt83OXibJg` | Category notes |
| 3 | Assignee | singleCollaborator | `fldgmNDtG4GKHDRap` | Team member |
| 4 | Status | singleSelect | `fldmhdgKadQyUbMBD` | Todo, In progress, Done |
| 5 | Attachments | multipleAttachments | `fldmDCyJ8aXTLkgar` | Related files |
| 6 | Attachment Summary | aiText | `fldMzHcLwbw3UxJUy` | AI summary of attachments |
| 7 | Instagram Educational Posts | multipleRecordLinks | `fldSiS3oCfJNGmwgX` | → Instagram Educational Posts |

**Note**: This table appears to be using the default Airtable task template structure (Name, Notes, Assignee, Status). It needs significant rework to serve as a proper vendor taxonomy.

### Proposed Changes (from Gameplan)

| Action | Field | Details | Status |
|--------|-------|---------|--------|
| ADD | url_slug | singleLineText (e.g., "wedding-photography") | Pending |
| ADD | description | multilineText (for category hub page) | Pending |
| ADD | page_template | singleLineText (which template for hub page) | Pending |
| ADD | display_order | number (navigation ordering) | Pending |
| REWORK | Connect to Vendors | Replace singleSelect in Vendors with linked records | Pending |

---

## 13. Venue Review Data

**Table ID**: `tbli80M6XESvyktAg` | **Views**: Grid view | **Role**: **NOT IN GAMEPLAN — needs review**

### Live Fields (13 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | Venue | multilineText | `fld11LzLjsdExIM6g` | Venue name (text, not linked) |
| 2 | Posted | date (local) | `fldDpJccLHfsMArqq` | Post date |
| 3 | Review URL | url | `fld6M3d6ub50h7P2Q` | Review blog post URL |
| 4 | Google Doc | url | `fldfnOL5sHzZYfCk7` | Google Doc link |
| 5 | Field 5 | url | `fld3msbb1p6f2Dc3L` | Unnamed — unclear purpose |
| 6 | # Reviews | number (int) | `fldnGCSxfkTLgdWCr` | Number of reviews |
| 7 | Review 1 | url | `fldXOageLXpQjX2Ls` | Individual review link |
| 8 | Review 2 | url | `fldLFv6Ax0td9CI56` | Individual review link |
| 9 | Review 3 | url | `flddU3JNkjYhUNJdq` | Individual review link |
| 10 | Review 4 | url | `fldoalYvVUIfwqcHz` | Individual review link |
| 11 | Review 5 | url | `fldX329x0nIfRYc30` | Individual review link |
| 12 | Region | singleSelect | `fldbcAS9URiA9nN0T` | 13 region options (separate from Regions table) |
| 13 | Field 13 | currency ($) | `fldtzqoS6GVMdR7J6` | Unnamed — unclear purpose |

**Assessment**: Tracks venue review blog posts and their source Google Reviews. Has unnamed fields and uses text for venue name instead of linked records. Appears to support the "3x Venue Review Posts/week" publishing cadence mentioned in current-data.md. **Decision needed**: Keep, merge into Articles, or deprecate?

---

## 14. Lookup

**Table ID**: `tbl9XwmhN5thwIgAb` | **Views**: Grid view | **Role**: **NOT IN GAMEPLAN — needs review**

### Live Fields (25 fields)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | Venue | multilineText | `fldsX1NbvdDYnkniv` | Venue name |
| 2 | Listing ID | number (int) | `fldd7WjiAzpiezz6L` | WordPress listing ID |
| 3 | Website | multilineText | `fldnje1L5bjxSHnyO` | Venue website |
| 4 | Address | multilineText | `fld9ZoQQtmRL4QMdd` | Venue address |
| 5 | Region | singleSelect | `fldrizmehuWQJTwbn` | 12 region options |
| 6 | Region temp | singleSelect | `fldYZsdXB1eQyceC4` | Temporary region mapping |
| 7 | Email | multilineText | `flduaQeKSPBkKkRY4` | Email |
| 8 | Phone | multilineText | `fldqN48n5EJxdg1nN` | Phone |
| 9 | FWV URL | multilineText | `fldM3npu41xYadYf3` | French Wedding Venues URL |
| 10 | CB URL | multilineText | `fldR2RALC64S6TtSO` | Chateaubee URL |
| 11 | FWS URL | multilineText | `fldye9bAZdDFVeP1Z` | FWS URL |
| 12 | Invoicing | multilineText | `fldybanLmYBqoGkQh` | Invoice info |
| 13 | Hosts | number (int) | `fldwXvP26FcbdtE79` | Guest capacity |
| 14 | Sleeps | number (int) | `flditnE90SwDYhASz` | Sleep capacity |
| 15 | € From | singleLineText | `fldddbxRrUTrIs4yx` | Min price (text) |
| 16 | € To | singleLineText | `fldOLop1urQkKsMUJ` | Max price (text) |
| 17 | Minimum Nights | number (int) | `fldAfvFZP2UkRNnvn` | Min nights |
| 18 | Chateaubee Info | multilineText | `fldTB1bm3zPCuxTSR` | Chateaubee description |
| 19 | What we Love | multilineText | `fldLLICmo5y6tdlVk` | Editorial text |
| 20 | About | multilineText | `fldMqNTDEoRnfvHRM` | About section |
| 21 | Accom/ Amen | multilineText | `fldN0SuCAQCxRiXPw` | Accommodation |
| 22 | Getting There | multilineText | `fldkb4X9RKJhyNDlk` | Directions |
| 23 | Beyond Weddings | multilineText | `fldPMRYZdzsRdjeQW` | Beyond weddings |
| 24 | Pricing | multilineText | `fldPbJzb4tPgVlKOv` | Pricing details |
| 25 | Brochure Text (Email) | multilineText | `fldHDFLF0BPaimA9E` | Brochure text |
| 26 | 2026 Brochure | multilineText | `flduWIEpdkm1wpSJv` | 2026 brochure content |
| 27 | 2027 Brochure | multilineText | `fldGUeGfXbQBIiSL5` | 2027 brochure content |
| 28 | Real Weddings | multilineText | `flduQuA0vhFf9EJO9` | Real weddings text |

**Assessment**: This appears to be a **legacy data import/staging table** — mirrors Venues table structure but with all text fields (no linked records, no formulas). Fields like "Region temp", "€ From" (text), "Chateaubee Info" suggest it was used to import venue data from an external source (possibly a spreadsheet from Chateaubee). **Likely safe to archive/remove** once confirmed no active workflows reference it.

---

## 15. Location Pages

**Table ID**: `tblOgYxCad7qGUTB2` | **Views**: Grid view | **Role**: Core content — location landing pages

**Records**: 36 (initial load from WordPress location hierarchy)

| # | Field Name | Type | Field ID | Notes |
|---|-----------|------|----------|-------|
| 1 | location_name | singleLineText | `fldPqrD80YIz0ZsQj` | Primary field — display name (e.g., "Provence") |
| 2 | level | singleSelect | `fldQz5QWY9P7r2y9v` | Hierarchy depth: Region, Sub-region, City, Area |
| 3 | publish_status | singleSelect | `fldccWkVy0Sc51iXm` | Draft, Review, Published, Archived |
| 4 | url_slug | singleLineText | `fld3mRfr2MCZezOqs` | URL path component (e.g., "provence") |
| 5 | current_wp_url | url | `fldA8xsGdx0o1K04Z` | Current WordPress URL |
| 6 | meta_title | singleLineText | `fldDHCDvRoqKdMFTN` | SEO page title (60 chars max) |
| 7 | meta_description | multilineText | `flduaOfWDmfywZuIO` | SEO description (155 chars max) |
| 8 | intelligence_data | multilineText | `fldAdI6YzJbSuwbut` | Research from /location-page generation |
| 9 | venue_groupings | multilineText | `fld6XEfEkvcFvgmsb` | JSON of venues grouped by sub-region |
| 10 | generated_html | multilineText | `fldOQM5zRv6jWyPEj` | Final rendered HTML from /location-page workflow |
| 11 | featured_venues | multipleRecordLinks | `fld6cNCwEiQRcXy7T` | → Venues (featured on page) |
| 12 | last_generated | date (ISO) | `fldQM4cgRwcKlBXvL` | When content was last generated |
| 13 | region | multipleRecordLinks | `fldJoMRJsYldHpgqN` | → Regions (parent region) |
| 14 | location | multipleRecordLinks | `fldyrTs2irGnOd5VS` | → Locations (linked location) |
| 15 | parent_page | multipleRecordLinks | `fldhHWHuXZMocG3ym` | → Location Pages (self-referencing hierarchy) |
| 16 | child_pages | multipleRecordLinks | `fldEKy49IL3K4fyNa` | → Location Pages (auto-created inverse of parent_page) |

### Hierarchy Structure

```
South of France (Region)
├── Provence (Sub-region)
│   ├── Aix-en-Provence (City)
│   ├── Marseille (City)
│   ├── Avignon (City)
│   └── French Riviera (City)
│       ├── Nice (Area)
│       ├── Cannes (Area)
│       ├── Saint Tropez (Area)
│       └── Antibes (Area)
├── Occitanie (Sub-region)
│   ├── Carcassonne, Montpellier, Toulouse
├── Corsica (Sub-region)
├── Nouvelle-Aquitaine (Sub-region)
│   ├── Bordeaux, Dordogne, Biarritz, Lourdes
└── Auvergne-Rhone-Alpes (Sub-region)
    ├── Lyon, Annecy, Chamonix

North of France (Region)
├── Brittany, Normandy, Hauts-de-France, Burgundy
├── Ile-de-France (Sub-region)
│   └── Versailles (City)
├── Loire Region (Sub-region)
└── Grand Est (Sub-region)
    ├── Champagne, Strasbourg, Nancy
```

---

## 16. Hub Pages

**Table ID**: — (TO CREATE) | **Views**: Grid view, Kanban (by publish_status) | **Role**: Core content — curated venue collection/roundup pages

Hub pages are **curated collection pages** that group and present FWS member venues by specific criteria (geography, style, features, capacity, budget, season, or niche). They are distinct from Location Pages (destination guides) and individual Venue Listings.

**Total planned**: 86 unique hub pages + 1 pillar page, organized into 7 branches:
1. **Geography** — 50 pages (macro-regional → regional → sub-regional + style intersections)
2. **Style** — 10 pages (château, vineyard, villa, farmhouse, garden, barn, domaine, beach, orangerie, marquee)
3. **Features** — 12 pages (pool, all-inclusive, exclusive-use, accommodation + sleeping capacity tiers)
4. **Capacity** — 4 pages (intimate, small, medium, large)
5. **Budget** — 4 pages (affordable, mid-range, premium, luxury)
6. **Seasonal** — 4 pages (spring, summer, autumn, winter)
7. **Niche** — 2 pages (elopements, vow renewals)

### Proposed Fields

| # | Field Name | Type | Notes |
|---|-----------|------|-------|
| 1 | page_title | singleLineText | Hub page title (e.g., "Château Wedding Venues in Provence") |
| 2 | url_slug | singleLineText | URL path (e.g., "chateau-wedding-venues-in-provence") |
| 3 | page_type | singleSelect | National Style, Style×Region, National Feature, Feature×Region, National Capacity, Seasonal, Budget, Elopement, Vow Renewal, Macro-Regional, Regional, Sub-Regional |
| 4 | target_keyword | singleLineText | Primary SEO keyword |
| 5 | meta_title | singleLineText | SEO title (60 chars max) |
| 6 | meta_description | multilineText | SEO description (155 chars max) |
| 7 | featured_venues | multipleRecordLinks | → Venues — curated venue selection for this page |
| 8 | region_scope | multipleRecordLinks | → Regions — which region(s) this page covers |
| 9 | style_filter | multipleSelects | Which style(s) to filter venues by |
| 10 | feature_filter | multipleSelects | Which feature(s) to filter venues by |
| 11 | capacity_filter | singleSelect | Capacity tier: intimate, small, medium, large |
| 12 | budget_filter | singleSelect | Budget tier: affordable, mid-range, premium, luxury |
| 13 | season_filter | singleSelect | Season: spring, summer, autumn, winter |
| 14 | publish_status | singleSelect | Draft, Review, Published, Archived |
| 15 | priority_tier | singleSelect | P0, P1, P2, P3 |
| 16 | score_total | number | Composite priority score (max 25) |
| 17 | score_breakdown | singleLineText | "SD:5 CL:4 DR:3 RI:5 CG:5" |
| 18 | generated_html | multilineText | Rendered page HTML |
| 19 | last_refreshed | date | When content was last generated/updated |
| 20 | competitor_url | url | Competitor page this is matching (if any) |
| 21 | linked_planning_guides | multipleRecordLinks | → Articles — which planning guides link to this hub |
| 22 | notes | multilineText | Editorial notes |

### Hub Page Content Template (8 blocks)

```
1. Hero + H1 (keyword-optimized title)
2. Introduction (200-300 words, SEO context)
3. Featured Venues Grid (5-12 curated members with cards)
4. Why Choose This Type/Region (editorial benefit section)
5. Comparison Table (venue name, capacity, price tier, sleeps)
6. Expert Tips (3-5 practical tips)
7. FAQ Accordion (schema markup for AI search)
8. Planning Section (links to 2-4 related planning guides)
9. Related Hub Pages + Location Pages (auto-generated cross-links)
```

### Cross-Linking Architecture

When a hub page is published:
- All venues in `featured_venues` → automatically get "Featured in" link on their listing page
- Location pages covering same region → automatically add link to hub page
- Parent hub pages → automatically add new page to "Related" section
- "Related Hub Pages" cross-links → algorithmically generated from shared tags

### P0 Hub Pages (Build First)

| Rank | Hub Page | URL Slug | Search Volume |
|------|----------|----------|---------------|
| 1 | Château Wedding Venues in France | chateau-wedding-venues-in-france | 82.7K cluster |
| 2 | Wedding Venues in Loire Valley | wedding-venues-loire-valley | 27K |
| 3 | Wedding Venues in Provence | wedding-venues-in-provence | TBD |
| 4 | All-Inclusive Wedding Venues France | all-inclusive-wedding-venues-france | 2.9K |
| 5 | Intimate Wedding Venues in France | intimate-wedding-venues-in-france | 2.5K |

### Critical Dependencies

1. **Venue style classification** — 130/189 venues (69%) need style tags before style hub pages can launch
2. **Price data extraction** — ~60% of venues missing `min_from_price_eur`/`max_from_price_eur` (data exists in `full_venue_json`, needs extraction to columns)
3. **Hub page template** development in Astro
4. **Cross-linking automation** logic

**Status**: TO CREATE

---

## Tables to Create (Target)

These tables are proposed in the gameplan but do not yet exist.

### ~~Location Pages~~ — CREATED

**Status**: Done — created 2026-02-20. See Table 15 in live schema below.

### [Admin] SEO Redirects (new)

| Field | Type | Purpose |
|-------|------|---------|
| old_url | url | WordPress URL |
| new_url | url | New site URL |
| status_code | singleSelect | 301 (permanent), 302 (temporary), 410 (gone) |
| content_type | singleSelect | Location, Venue, Vendor, Article, Real Wedding, Other |
| verified | checkbox | Has redirect been tested? |
| notes | multilineText | Migration notes |

**Status**: Pending

### [Admin] Site Config (new)

| Field | Type | Purpose |
|-------|------|---------|
| config_key | singleLineText | e.g., "homepage_featured_venues" |
| config_value | multilineText | JSON or text value |
| description | multilineText | What this config controls |
| last_updated | lastModifiedTime | Auto-tracked |

**Status**: Pending

### Media Assets (new)

| Field | Type | Purpose |
|-------|------|---------|
| filename | singleLineText | Original filename |
| source_url | url | WordPress media library URL |
| cdn_url | url | New CDN URL after migration |
| alt_text | singleLineText | SEO alt text |
| dimensions | singleLineText | e.g., "1920x1080" |
| file_size_kb | number | File size |
| format | singleSelect | jpg, png, webp, avif |
| associated_content | multipleRecordLinks | Venue/RW/Article link |
| migration_status | singleSelect | Pending, Migrated, Optimized, Error |

**Status**: Pending

---

## Tables to Remove (Target)

| Table | Gameplan Status | Live Status | Action |
|-------|----------------|-------------|--------|
| Memberships | Listed for removal | **Not found in live DB** | Already removed or was misidentified |
| Venue (VoiceFlow) | Listed for removal (legacy) | **Not found in live DB** | Already removed |
| Venue Review Data | Not in gameplan | **Exists in live DB** | Needs decision: keep, merge into Articles, or archive |
| Lookup | Not in gameplan | **Exists in live DB** | Likely legacy staging table — confirm and archive |

---

## Cross-Table Standards

### Publishing Workflow Fields

Every content table (Venues, Vendors, Real Weddings, Articles, Location Pages) should have:

| Field | Type | Constraint | Purpose |
|-------|------|-----------|---------|
| publish_status | singleSelect | Draft → Review → Scheduled → Published → Archived | Controls website build inclusion |
| meta_title | singleLineText | 60 chars max | SEO page title |
| meta_description | multilineText | 155 chars max | SEO description |
| url_slug | singleLineText | Auto from name/title | URL path component |

**Current status**: None of these fields exist on any table yet.

### Airtable Automations (Target)

| Trigger | Action | Status |
|---------|--------|--------|
| publish_status → "Published" | Webhook → Cloudflare deploy hook → site rebuild | Not set up |
| publish_status → "Review" | Notification to reviewer | Not set up |
| New Real Wedding record | Auto-populate meta_title, url_slug from Blog Title | Not set up |
| Venue update | Trigger VoiceFlow knowledge base refresh | Not set up |

---

## Key Relationships

```
Regions ──┬── Venues (main_region)
          ├── Locations
          ├── Real Weddings
          └── Suppliers

Locations ── Venues

Venues ──┬── Real Weddings
         ├── Sales Log
         ├── vf_table
         └── Location Pages (location_pages)

Suppliers ──┬── Real Weddings (Photographer)
            ├── Real Weddings (Planner)
            ├── Sales Log (as Supplier)
            └── Instagram Educational Posts

Vendor Categories ── Instagram Educational Posts

Magazines ── Real Weddings

Location Pages ──┬── Venues (featured_venues)
                 ├── Regions (region)
                 ├── Locations (location)
                 └── Location Pages (parent_page ↔ child_pages)
```

**Note**: Venue Review Data and Lookup tables have **zero linked records** — they use text fields for all references, making them isolated from the relational graph.

---

## Naming Conventions

| Element | Convention | Current Compliance | Example |
|---------|-----------|-------------------|---------|
| Table names | PascalCase plural | Partial — "vf_table", "Article Table" break convention | Venues, Vendors, Articles |
| Field names | snake_case | Mixed — many use Title Case or have spaces | venue_name, publish_status |
| Link fields | Descriptive | Partial — some just say "Venues" | linked_region, linked_photographer |
| Formula fields | snake_case | Mostly compliant | url_slug, full_url_path |
| System tables | [Admin] prefix | Compliant for AI Prompts | [Admin] SEO Redirects |

---

## API Rate Limit Strategy

**Plan**: Team (Plus) — 5 requests/second

**Build-time**:
1. Fetch ALL records per table in single paginated request
2. Use `maxRecords` + `offset` pagination
3. 200ms delay between table fetches
4. Cache locally during build (JSON files)
5. Total fetch: ~30-60 seconds for all tables

**Runtime**:
1. Edge-cache in Cloudflare KV (5-min TTL)
2. Batch related queries
3. Use `filterByFormula` to minimize transfer
4. Never call Airtable from client-side JS
5. All calls through Cloudflare Workers (server-side only)

---

## Changelog

| Date | Change | By |
|------|--------|-----|
| 2026-02-20 | Initial document created — full audit of 14 live tables against gameplan | Claude |
| 2026-02-20 | Location Pages table created (tblOgYxCad7qGUTB2) — 16 fields, 36 records from WordPress location hierarchy | Claude |
| 2026-02-20 | Added `location_pages` linked field to Venues (fldeMfwIsJ5iZ2B3D) — mapped all venues to Location Pages via Region → full branch | Claude |

---

*This document is auto-referenced by Claude during Airtable operations. Keep it current.*
