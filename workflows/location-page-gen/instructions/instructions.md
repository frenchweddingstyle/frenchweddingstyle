# Location Page Content Instructions

## Purpose

Generate informative, bride-facing blog posts about wedding venues in specific French locations. Each page serves as a comprehensive guide for couples researching a particular region.

## Tone of Voice

All content MUST comply with the brand tone defined in `context/tone-of-voice.md`. Key rules:

### Write Like a Human
- Conversational, specific, helpful, real
- Write like you're telling a friend about these venues
- Use active voice and direct language
- Include specific sensory details and concrete descriptions

### Forbidden Words (NEVER use)
timeless, sophistication, sophisticated, nestled, nestling, opulent, opulence, meticulous, meticulously, effortless, effortlessly, curated, boasts, boasting, stunning, breathtaking, exquisite, impeccable, flawless, ethereal, whimsical, enchanting, magical, captivating, mesmerizing, luxe, luxury, elegant, elegance, glamorous, glam, lavish, sumptuous, decadent, extravagant, high-end, upscale, exclusive, premier, trendy, on-trend, viral, buzzy, hyped, hot, must-have, must-see, of-the-moment, cutting-edge, next-level, beautiful, gorgeous, lovely, amazing, incredible, awesome, perfect, unique, special, memorable, dream, dreamy, unforgettable, ultimate, definitive

### Instead of Forbidden Words
- Instead of "beautiful flowers" → "garden roses in cream and blush"
- Instead of "stunning venue" → describe what makes it special
- Instead of "elegant elegance" → show it through specific details
- Instead of "nestled in" → use "set among", "between", "surrounded by", "in the middle of"

## Content Guidelines

### Venue Descriptions (2-3 sentences each)
- Use the venue's `identity.short_description` from the JSON as a starting point
- Enhance with specific architectural or landscape details from the full JSON
- Focus on what makes this venue different from others in the same region
- Paint a picture of arrival — what would you see and feel?

### Sub-Region Descriptions
- 2-3 sentences introducing the area's wedding appeal
- Mention specific towns, landscape features, or cultural details
- Ground it in geography couples can look up
- Avoid generic "rolling hills" language — be specific

### Expert Tips
- Practical, actionable advice
- Based on real planning considerations for the region
- Each tip should save couples time, money, or stress
- 1-2 sentences max per tip

### FAQ Answers
- Direct, honest, and useful
- Reference actual logistics (airports, distances, legal requirements)
- Include specific numbers where possible (costs, timelines, distances)

### Cost Breakdown
- Data-driven from actual venue pricing in Airtable
- Three tiers calculated from the real price spread
- Include real per-head catering estimates
- Hidden costs must be genuine and region-specific

## Venue Tag Rules

Each venue gets exactly 2 tags. Tags should:
1. Differentiate this venue from others in the same sub-region
2. Mix character and practical attributes
3. Be chosen from the approved tag vocabulary (see workflow.yml)
4. Prioritize what a bride would actually search for

## Internal Links

- `explore_url` → Always show (links to FWS listing page)
- `review_url` → Only show if venue has a FWS Review URL
- `real_wedding_url` → Only show if venue has linked Real Weddings
- Never show a CTA button with no URL behind it

## Venue Ordering

- Venues within each sub-region are displayed in random order
- No venue is prioritized over another
- Randomize on each generation

## WordPress Deployment (WPCode)

The output HTML is a **self-contained WPCode snippet** — not a full HTML document. It includes inline Tailwind CDN, Google Fonts, and scoped styles.

### How to deploy

1. Open **WPCode** in WordPress admin → **Add Snippet** → **Custom Code (New Snippet)**
2. Set snippet type to **HTML Snippet**
3. Paste the entire contents of `output/{slug}.html` into the code editor
4. Set insertion method:
   - **Shortcode** (recommended) → Place the shortcode on the target page/post
   - Or **Auto Insert** → specific page/URL
5. Activate the snippet

### SEO

- **Title, meta description, and Open Graph tags** are managed via **Yoast SEO** on the WordPress page where the snippet is inserted — not included in the HTML output
- **JSON-LD schema** (ItemList markup) can be added via Yoast's Schema tab or a separate WPCode snippet inserted in the `<head>` if needed

### Style isolation

All Tailwind utilities are scoped to `#fws-location-page` via the `important` selector strategy. This prevents the FWS styles from leaking into the WordPress theme and vice versa. Custom CSS for headings and body text is also scoped to the container.