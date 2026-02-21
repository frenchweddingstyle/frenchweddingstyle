# Venue Listing Generator

> **Model: opus** — This command requires creative writing with strict tone compliance. Keep on Opus.

Generate a structured venue listing from a raw brochure text dump.

## Instructions

### Phase 1: Load Context

Read the following files in order before doing anything else:

1. `workflows/venue-listing-gen/instructions/workflow.yml` — workflow config and processing steps
2. `workflows/venue-listing-gen/instructions/template.md` — output structure
3. `context/tone-of-voice.md` — brand voice (focus on **Vendor/Venue Listing Pages** section)
4. `reference/location-pages.json` — internal linking URL data

### Phase 2: Get Input

Ask the user to paste the raw venue brochure text. Wait for them to provide it before proceeding.

### Phase 3: Execute

Follow Steps 1–8 from `workflow.yml` exactly:

1. **Parse** the pasted text — map data to template sections
2. **Categorize** — select French region tag and location hierarchy
3. **Write content** — populate all template sections using the Vendor/Venue Listing tone
4. **Extract business details** — contact info, specs, facilities checklist
5. **Generate SEO & FAQs** — pricing, 6 FAQs, reviews, Yoast SEO
6. **Insert 2 internal links** — 1 in About the Venue, 1 in Additional Offerings, using `location-pages.json`
7. **Compliance check** — scan for forbidden AI clichés, verify tone, confirm links
8. **Save** to `workflows/venue-listing-gen/output/{venue-name-slug}.md`

### Flagging Rules

- Content generated via web search or inference: `[AI-generated — verify]`
- Missing data not in brochure: `[Not provided — check with venue]`

### Output

Display the completed listing to the user after saving.
