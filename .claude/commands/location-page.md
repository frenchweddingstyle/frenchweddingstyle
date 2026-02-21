# Location Page Generator

> **Model: opus** — This command requires multi-source research synthesis, editorial writing, and complex pipeline logic. Keep on Opus.

Generate a bride-facing informative blog post as a single static HTML file with Tailwind CSS for a target wedding location in France.

## Setup

Before starting, read these files to understand the pipeline:
- `workflows/location-page-gen/instructions/workflow.yml` — Pipeline logic and field mappings
- `workflows/location-page-gen/instructions/instructions.md` — Tone of voice rules and content guidelines
- `context/tone-of-voice.md` — Brand voice standards and forbidden words

Import the Python helper modules (these provide data structures, validation, and file I/O):
- `workflows/location-page-gen/scripts/pipeline.py` — Location lookup, slug generation, paths
- `workflows/location-page-gen/scripts/step1_intelligence.py` — Research schema and validation
- `workflows/location-page-gen/scripts/step2_venues.py` — Venue parsing, tag derivation, cost tiers
- `workflows/location-page-gen/scripts/step3_links.py` — Link assembly and status reporting
- `workflows/location-page-gen/scripts/step4_compile.py` — Jinja2 rendering and output
- `workflows/location-page-gen/scripts/tone_checker.py` — Forbidden word scanning

## Interactive Flow

### 1. Ask for Target Location

Ask the user which location they want to generate a page for. Offer these options:
- South of France
- North of France
- Or a specific sub-region (Provence, Occitanie, etc.)

Look up the location in `reference/location-pages.json` to confirm the tier and available sub-regions.

### 2. Confirm Sub-Regions

Show the user which sub-regions will be covered in the article. For "South of France", this includes Provence, Occitanie, Corsica, Nouvelle-Aquitaine, etc. Ask if they want to adjust.

---

## Step 1: Intelligence (Firecrawl Research)

Use Firecrawl MCP tools to research the target location:

1. **Search** using `firecrawl_search` with queries like:
   - "best wedding destinations in {location} France"
   - "wedding planning tips {location} France"
   - "destination wedding {location} France cost guide"

2. **Scrape** the top 3-5 results using `firecrawl_scrape` to get full article content.

3. **Synthesize** the research into the structured JSON format defined in `step1_intelligence.py`:
   - `sub_regions`: 3-6 wedding sub-regions with descriptions
   - `expert_tips`: 6-8 practical tips
   - `key_insights`: accessibility, timing, budgeting, legal facts
   - `brides_tip`: One standout callout tip
   - `hidden_costs`: 3+ region-specific hidden costs
   - `faqs`: 6 frequently asked questions
   - `seasonal_savings`: High/mid/low season pricing

4. **Validate** using `step1_intelligence.validate_research()`

5. **Run tone check** on all text using `tone_checker.check_dict_values()`

6. **Save** to `workflows/location-page-gen/working/{slug}/research.json`

**PAUSE** — Present a summary of the research to the user and wait for approval.

---

## Step 2: Venue Lookup (Airtable)

Query Airtable for member venues in the target location:

1. **Search Airtable** using MCP `search_records` or `list_records`:
   - Table: Venues (`tblIEJQNynXIsD8GL`)
   - Filter for `FWS Member` = 'Listing'
   - Filter for matching `region` field
   - Request fields: `venue_name`, `full_venue_json`, `image_url`, `fws_url`, `FWS Review`, `Real Weddings`, `region`, `Closest Town/ City`

2. **Parse** each venue's `full_venue_json` field using `step2_venues.parse_venue_json()`

3. **Extract** card data using `step2_venues.extract_venue_card_data()`

4. **Derive tags** using `step2_venues.derive_tags()` — 2 tags per venue

5. **Group by sub-region** using `step2_venues.group_by_sub_region()` matching Step 1's sub-regions

6. **Calculate cost tiers** using `step2_venues.calculate_cost_tiers()`

7. **Save** to `workflows/location-page-gen/working/{slug}/venues.json`

**PAUSE** — Present the venue list with groupings and tags to the user. Show which venues are in each sub-region and the calculated cost tiers.

---

## Step 3: Link Assembly

Assemble CTA links for each venue:

1. For each venue from Step 2:
   - `explore_url` = `fws_url` (always present for members)
   - `review_url` = `FWS Review` field (may be null)
   - For Real Weddings: query the linked `Real Weddings` records in Airtable to get their `FWS URL` field

2. Use `step3_links.assemble_links()` to merge links

3. Generate link status report using `step3_links.get_link_status()`

4. **Save** to `workflows/location-page-gen/working/{slug}/links.json`

**PAUSE** — Show which venues have complete vs partial links. User confirms.

---

## Step 4: Compilation

Generate the final HTML:

1. **Load all data** from the working directory

2. **Generate editorial content** (you write these, enforcing tone-of-voice rules):
   - `subtitle`: 1-2 sentence italic subtitle for the header
   - `intro_paragraph`: Opening paragraph about the location
   - `why_choose_text`: "Why Choose {Location}" section
   - `meta_description`: 155-char SEO description
   - `cost_intro`: Intro text for the cost section
   - `sub_region_descriptions`: Enhanced descriptions for each sub-region
   - `venue_type_sections`: Group any ungrouped venues by type (chateau, bastide, etc.)

3. **Run tone check** on ALL editorial content using `tone_checker.check_dict_values()`. If violations found, rewrite until clean.

4. **Build template context** using `step4_compile.build_template_context()`

5. **Render HTML** using `step4_compile.render_page()`

6. **Save draft** to `workflows/location-page-gen/working/{slug}/draft.html`

**PAUSE** — Tell the user the draft is ready for review at the draft path. Ask if they approve.

7. On approval, **promote** using `step4_compile.promote_to_output()` to copy to `workflows/location-page-gen/output/{slug}.html`

---

## Important Rules

- **Tone enforcement**: Run `tone_checker` on ALL generated text. Never publish content with forbidden words.
- **Venue ordering**: Randomize venue order within each sub-region.
- **Missing CTAs**: Hide CTA buttons when URLs are null (never show empty links).
- **Data-driven costs**: Cost tiers must be calculated from actual venue pricing, not hardcoded.
- **Pause between steps**: Always pause and show the user what was produced before continuing.
- **No hero image**: The template uses a text-only header (no hero image section).
