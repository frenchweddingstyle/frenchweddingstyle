# Venue Schema v1.1.0 — Data Gaps Report

**Date:** 2026-02-17
**Schema version:** v1.1.0 (320+ fields across 21 sections, 9 $defs)
**Records Analyzed:** 23 venues with populated `venue_url_scraped`
**Brochure Text:** 25 of 48 records now have `brochure_text` populated
**Data sources:** Venue websites (scraped), listing sites, brochure PDFs (extracted)

---

## Key Change Since v1.0.0

25 venues now have `brochure_text` populated (up from 0). Brochures are the richest source for pricing granularity, payment schedules, accommodation mandates, and detailed policies. The fill-rate estimates below reflect expected availability across **both** website and brochure data sources.

---

## Section-Level Fill-Rate Heatmap

| Section | Avg Fill Rate | Trend | Primary Source |
|---------|:------------:|:-----:|----------------|
| Identity | ~75% | stable | Website |
| Location | ~65% | stable | Website + listings |
| History | ~50% | stable | Website |
| Spaces | ~55% | +5% | Website + brochure |
| Accommodation | ~55% | +15% | Brochure + website |
| Pricing | ~45% | +20% | Brochure (major uplift) |
| Catering | ~60% | +5% | Website + brochure |
| Drinks | ~35% | +10% | Brochure |
| Vendor Rules | ~50% | +5% | Website + brochure |
| Ceremony | ~50% | stable | Website |
| Amenities | ~45% | stable | Website |
| Activities | ~50% | stable | Website |
| Technical | ~35% | stable | Website |
| Accessibility | ~25% | stable | Website (rarely stated) |
| Sustainability | ~20% | stable | Website |
| Parking | ~55% | stable | Website |
| Policies | ~40% | +15% | Brochure (major uplift) |
| Contact | ~70% | stable | Website |
| Wedding Day | ~45% | stable | Website + brochure |

---

## Data Gap Detail by Section

### Overview (Filtering Fields)
| Field | Availability | Notes |
|-------|:----------:|-------|
| min_price_eur | ~65% | Brochures now providing many missing prices. Some venues still "contact us" only. |
| max_guests | ~85% | Usually stated clearly on venue site or listings. |
| min_guests | ~40% | **New in v1.1.0.** Frequently found in brochures (e.g. "minimum 80 guests"). Rarely on websites. |
| max_sleeping_guests | ~75% | Often requires adding up individual building capacities. |
| total_bedrooms | ~65% | Sometimes only sleeping capacity is given, not bedroom count. |
| estate_size_hectares | ~50% | Often missing or stated in vague terms ("expansive grounds"). |

### Identity
| Field | Availability | Notes |
|-------|:----------:|-------|
| venue_name | 100% | Always present. |
| venue_type | 100% | Always inferrable. |
| exclusivity_model | ~70% | **Updated enum** now includes "optional_exclusivity" — better captures venues offering exclusivity as an upgrade. |
| owner_names | ~40% | Many venues don't name owners on their website. |
| certifications | ~20% | Green Key, Monument Historique — most venues don't list certifications. |
| google_rating | ~15% | Rarely included in scraped content. |

### Location
| Field | Availability | Notes |
|-------|:----------:|-------|
| address (city, postal_code) | ~80% | Usually extractable from footer or contact page. |
| GPS coordinates | ~20% | Rarely explicitly stated. |
| nearest_city | ~70% | Usually mentioned in "Getting There" sections. |
| nearest_airports | ~55% | Travel sections are often sparse. |
| nearby_villages | ~35% | Mostly found on listing sites. |

### History
| Field | Availability | Notes |
|-------|:----------:|-------|
| construction_period | ~65% | Most chateaux mention their era. |
| architectural_style | ~45% | Often described narratively, not as a classification. |
| listed_monument_status | ~15% | Only a few venues are officially classified. |
| historical_families | ~40% | Rich in narrative venues, absent in simpler ones. |
| notable_architectural_features | ~50% | Depends on how much the venue markets its history. |

### Spaces
| Field | Availability | Notes |
|-------|:----------:|-------|
| Named spaces | ~70% | Most venues list their main reception areas. |
| area_sqm per space | ~40% | **Improved +5%.** Brochures sometimes include sqm. Still a major gap. |
| capacity_seated per space | ~45% | Brochures sometimes include per-space capacities. |
| rental_fee_eur per space | ~15% | **New in v1.1.0.** Only found in brochures with itemized pricing (e.g. add-on Chai hire, Taproom fee). |
| soundproofed | ~10% | Rarely mentioned unless it's a key selling point. |
| air_conditioned per space | ~15% | Usually mentioned at venue level, not per space. |

### Accommodation
| Field | Availability | Notes |
|-------|:----------:|-------|
| total_sleeping_capacity | ~80% | Well-covered across websites and listings. |
| mandatory_accommodation_purchase | ~45% | **New in v1.1.0.** Brochures frequently state this (e.g. "accommodation mandatory Saturday night for 48 persons"). |
| mandatory_accommodation_details | ~40% | **New in v1.1.0.** Present wherever the mandate is stated. |
| breakfast_price_per_person_eur | ~30% | **New in v1.1.0.** Found in brochures with itemized pricing. |
| Individual room names | ~40% | Only detailed venues list every room. |
| room_type classification | ~35% | Often rooms are described but not categorized. |
| bed_configuration | ~35% | **Improved +5%.** Brochures sometimes contain this. Still a major gap. |
| bathroom_type | ~25% | **New in v1.1.0.** Brochures sometimes specify bath vs shower. |
| price_per_night_eur (room) | ~20% | Mostly hidden or quoted on request. |
| price_per_night_eur (building) | ~25% | **New in v1.1.0.** Brochures for gite-style venues often quote per-building rates. |
| accessible rooms | ~15% | Rarely stated unless the venue highlights accessibility. |

### Pricing
| Field | Availability | Notes |
|-------|:----------:|-------|
| starting_price_eur | ~70% | **Improved +10%.** Brochures now filling many gaps. Listing sites also help. |
| seasonal_pricing breakdown | ~50% | **Improved +20%.** Brochures are the primary source for this. Major uplift. |
| day_of_week pricing | ~30% | **New in v1.1.0.** Many brochures distinguish Friday vs Saturday weddings. |
| packages with inclusions | ~35% | **Improved +10%.** All-inclusive and package-based venues list these in brochures. |
| package excludes | ~25% | **New in v1.1.0.** Brochures often list what is NOT included per package. |
| vat_rate_percentage | ~35% | **New in v1.1.0.** Frequently stated in brochures (often 20%, sometimes split 10%/20%). |
| tourist_tax_note | ~30% | **New in v1.1.0.** Mentioned in ~30% of brochures. |
| children_catering_price_eur | ~25% | **New in v1.1.0.** Present in venues with detailed catering menus. |
| brunch_cost_per_person_eur | ~30% | **New in v1.1.0.** Commonly found in brochures for multi-day venues. |
| welcome_dinner_cost_eur | ~20% | **New in v1.1.0.** Found where welcome dinners are offered as add-ons. |
| additional_night_rate_eur | ~35% | **New in v1.1.0.** Frequently quoted in brochures. |
| extended_hour_rate_eur | ~20% | **New in v1.1.0.** Only some brochures quote per-hour overtime costs. |
| deposit_percentage | ~55% | **Improved +10%.** Brochures almost always state deposit terms. |
| deposit_amount_eur | ~15% | **New in v1.1.0.** Fewer venues use a fixed amount vs percentage. |
| security_deposit_eur | ~35% | **New in v1.1.0.** Commonly stated in brochures (e.g. 2500-10000 EUR). |
| security_deposit_return_days | ~20% | **New in v1.1.0.** Less commonly specified — e.g. "returned within 21 days". |
| payment_schedule | ~40% | **New in v1.1.0.** Brochures frequently outline 3-4 payment stages. |
| cleaning_fee_eur | ~25% | **New in v1.1.0.** Found in brochures with itemized costs. |
| security_guard_cost_eur | ~20% | **New in v1.1.0.** Quoted where security is mandatory. |
| coordinator_cost_eur | ~15% | **New in v1.1.0.** Rarely quoted separately — usually included or external. |
| price_excludes | ~35% | **New in v1.1.0.** Brochures often explicitly list exclusions. |
| cancellation_policy | ~40% | **Improved +25%.** Brochures almost always contain this. |

### Catering
| Field | Availability | Notes |
|-------|:----------:|-------|
| catering_model | ~75% | Usually clear — in-house vs external vs recommended list. |
| recommended_caterers list | ~30% | Some venues name partners, most just say "recommended list available". |
| late_night_food_available | ~30% | **New in v1.1.0.** Found in brochures describing late-night snack options. |
| professional_kitchen | ~25% | Rarely mentioned unless targeting external caterers. |
| brunch_available | ~50% | **Improved +5%.** Commonly mentioned in multi-day wedding descriptions and brochures. |

### Drinks
| Field | Availability | Notes |
|-------|:----------:|-------|
| corkage_fee | ~35% | **Improved +5%.** Brochures sometimes specify this. |
| corkage_fee_amount_eur | ~15% | **New in v1.1.0.** Only found in venues that charge per-bottle corkage. |
| mandatory_venue_drinks | ~20% | **New in v1.1.0.** Found at vineyard/brewery venues. |
| byo_wine_allowed | ~40% | Usually inferrable from corkage/drinks policy. |
| on_site_wine_production | ~25% | Only wine-estate venues. |
| bar_service_description | ~25% | **Improved +5%.** Usually part of catering packages in brochures. |

### Vendor Rules
| Field | Availability | Notes |
|-------|:----------:|-------|
| vendor_freedom | ~55% | Usually inferrable from catering and services sections. |
| preferred_vendor_list | ~50% | Many mention it exists without listing names. |
| wedding_planner_available | ~40% | Some venues include, some recommend, many don't mention. |
| wedding_planner_mandatory | ~20% | **New in v1.1.0.** Found at luxury venues requiring planner coordination. |
| non_approved_vendor_fee | ~15% | **New in v1.1.0.** Rarely stated — only in detailed brochures with vendor terms. |

### Ceremony
| Field | Availability | Notes |
|-------|:----------:|-------|
| ceremony_types | ~60% | Usually mentioned in services or features sections. |
| chapel_on_site | ~30% | Only applicable to venues with chapels. |
| outdoor_ceremony_locations | ~65% | Well-covered in photo galleries and descriptions. |
| rain_backup_plan | ~30% | **Improved +5%.** Some brochures now specify backup options. Still a major gap. |

### Amenities
| Field | Availability | Notes |
|-------|:----------:|-------|
| swimming_pool | ~70% | Well-documented when present. |
| spa | ~20% | Only a few venues have spa facilities. |
| tennis/petanque | ~30% | Mentioned when available. |
| vineyard_on_site | ~25% | Only wine-estate venues. |
| helipad | ~10% | Very rare but mentioned when available. |

### Technical
| Field | Availability | Notes |
|-------|:----------:|-------|
| wifi_available | ~40% | Often listed in amenities but not always. |
| sound_system_provided | ~25% | Usually mentioned only in corporate/seminar contexts. |
| furniture_provided | ~45% | Important detail — often in listings more than venue sites. |
| ev_charging | ~10% | Emerging amenity, rarely stated. |

### Accessibility
| Field | Availability | Notes |
|-------|:----------:|-------|
| wheelchair_accessible | ~35% | **Significant gap.** Many venues don't address this at all. |
| elevator | ~10% | Very few venues mention this. |
| accessible_rooms | ~10% | Even fewer specify room-level accessibility. |

### Policies
| Field | Availability | Notes |
|-------|:----------:|-------|
| curfew_time | ~45% | **Improved +5%.** Brochures sometimes clarify curfew terms. |
| outdoor_music_curfew | ~35% | **New in v1.1.0.** Brochures frequently split indoor/outdoor curfews. |
| indoor_music_curfew | ~35% | **New in v1.1.0.** Same — brochures are the primary source. |
| setup_access_time | ~30% | **New in v1.1.0.** Found in brochures with event timelines. |
| teardown_deadline | ~25% | **New in v1.1.0.** Less commonly explicit. |
| tent_marquee_policy | ~20% | **New in v1.1.0.** Found in brochures for estates with outdoor capacity. |
| confetti_policy | ~25% | **New in v1.1.0.** Increasingly stated in brochures (eco-awareness). |
| candle_policy | ~20% | **New in v1.1.0.** Heritage/Monument Historique venues often restrict candles. |
| event_insurance_required | ~30% | **New in v1.1.0.** Commonly required — stated in brochures and contracts. |
| event_insurance_cost_eur | ~10% | **New in v1.1.0.** Rarely quoted — most say "required" without giving cost. |
| portable_toilets_policy | ~15% | **New in v1.1.0.** Found at venues with large outdoor capacity. |
| lifeguard_required | ~10% | **New in v1.1.0.** Rare — only venues with mandatory pool access rules. |
| babysitter_mandatory | ~10% | **New in v1.1.0.** Rare — only a few luxury venues mandate this. |
| pet_policy | ~30% | Usually mentioned on listings. |
| lgbtq_friendly | ~25% | Only explicitly stated on progressive or listing-focused venues. |
| check_in/check_out | ~30% | **Improved +10%.** Brochures frequently specify arrival/departure times. |

### Contact
| Field | Availability | Notes |
|-------|:----------:|-------|
| phone_primary | ~80% | Usually in footer or contact page. |
| email_primary | ~75% | Usually extractable. |
| website_url | 100% | Always available (it was the source URL). |
| instagram | ~55% | Social links increasingly present. |
| virtual_tour_url | ~10% | Only a few venues offer Matterport or similar. |

---

## Top 10 Highest-Impact Gaps (Revised for v1.1.0)

These are the fields that matter most to couples but are most commonly missing:

1. **Payment schedule details** (~40%) — Couples need to know instalment timing. Brochures are the only reliable source; most now provide this.
2. **Per-space square metres** (~40%) — Critical for planners calculating layout. Rarely on websites, occasionally in brochures.
3. **Rain backup plan** (~30%) — A top-5 question for couples. Improving with brochures but still a major gap.
4. **Bed configuration per room** (~35%) — Guests need to know bed types. Brochures help but coverage is still patchy.
5. **Wheelchair accessibility details** (~35%) — Legal requirement in France, poorly documented online.
6. **Security deposit amount** (~35%) — New field — essential for budgeting. Found in about a third of brochures.
7. **Seasonal/day-of-week pricing breakdown** (~50%) — **Major improvement.** Was ~30%, now ~50% with brochures. Still needs work.
8. **Indoor vs outdoor curfew split** (~35%) — New fields — couples need to know the specific rules. Brochures are primary source.
9. **Children's catering pricing** (~25%) — New field — important for family weddings. Only some brochures include this.
10. **Cancellation and deposit terms** (~40%) — **Improved** from ~15%. Brochures now providing most of this data.

---

## Comparison: v1.0.0 vs v1.1.0

| Metric | v1.0.0 | v1.1.0 |
|--------|:------:|:------:|
| Total schema fields | ~285 | ~320 |
| $defs | 8 | 9 (+payment_milestone) |
| Brochure records available | 0 | 25 |
| Avg pricing section fill-rate | ~25% | ~45% |
| Avg policies section fill-rate | ~25% | ~40% |
| Avg accommodation fill-rate | ~40% | ~55% |
| Top 10 gaps avg fill-rate | ~28% | ~37% |

---

## Recommendations

1. **Continue brochure extraction** — 23 of 48 venues still lack brochure_text. Prioritize these for the next extraction batch.
2. **Flag Domaine de La Leotardie** — Record `rec9DPDAhdWezQ2G5` has misattributed brochure_text (contains 7 other venues' data). Requires manual re-extraction.
3. **Fix short brochure records** — Chateau de Vauchelles and Chateau des Barrenques have only 48 characters each — likely extraction errors.
4. **Use listing sites as supplements** — Third-party listing sites provide highly structured data (capacity, pricing, features) that venue websites often omit.
5. **Manual enrichment for top gaps** — For the top 10 gaps above, consider a manual enrichment pass for priority venues (rain backup, sqm per space, accessibility).
6. **Schema is production-ready** — v1.1.0 captures ~320 fields including all common brochure patterns. Ready for LLM extraction pipeline testing.

---

## Error Records

- **Chateau Camiac** (recvKUzI2hGz4HkhY): Only 86 characters in `venue_url_scraped` — contains `MANUAL_CHECK: Site returning 500 Internal Server Error`. No data extractable. Requires manual re-scrape.
- **Domaine de La Leotardie** (rec9DPDAhdWezQ2G5): 95,521 characters in `brochure_text` — contains misattributed data from 7 other venues. Requires manual re-extraction.
- **Chateau de Vauchelles** (brochure_text): Only 48 characters — likely extraction error.
- **Chateau des Barrenques** (brochure_text): Only 48 characters — likely extraction error.
