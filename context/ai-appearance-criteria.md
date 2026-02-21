# AI Appearance Criteria — Master Reference

> **Purpose**: This is the governing reference for how every page on the FWS website must be structured to appear in AI search results (Google AI Overviews, ChatGPT, Perplexity). Every content template, hub page spec, blog article, and venue listing must comply with these criteria.
>
> **Status**: Active | **Created**: 2026-02-21
> **Sources**: [Yotpo](https://www.yotpo.com/blog/ranking-ai-search-geo-tips/) | [Wellows](https://wellows.com/blog/google-ai-overviews-ranking-factors/) | [RankMax](https://www.rankmax.com.au/articles/gen-ai-seo) | [Search Engine Land](https://searchengineland.com/authority-ai-search-469466)

---

## 1. The Shift: Answer Engines, Not Search Engines

Traditional SEO optimised for link clicks. AI search optimises for **synthesis** — your content gets extracted, summarised, and cited inside an AI-generated answer. The user may never visit your page.

**What this means for FWS**:
- CTR has dropped ~61% for AI Overview queries
- 47% of AI Overview citations come from pages ranked **below position 5** — domain authority alone doesn't win
- 90% of ChatGPT citations go to pages ranked 21 or lower — content quality trumps traditional rank
- 76% of Google AI Overview citations also rank in the top 10 — traditional SEO still matters as a foundation

**New metrics to track**:
| Metric | What It Measures |
|--------|-----------------|
| AI Presence Rate | % of target queries where FWS appears in AI responses |
| Share of Citation | How often FWS is cited vs. competitors in AI answers |
| AI Referral Traffic | Direct visits from ChatGPT, Perplexity, Google AIO |
| Brand mention frequency | Unlinked mentions across forums, reviews, social, press |

---

## 2. The Seven Core Ranking Factors

Ranked by measured impact on AI Overview citation probability.

### 2.1 Semantic Completeness (r=0.87)

Content must provide **self-contained answers** requiring no external context. AI systems extract passages — if a passage depends on surrounding content to make sense, it won't be cited.

**Rules**:
- Each section must pass the "island test" — it stands alone if extracted
- Optimal answer passage length: **134-167 words** per key answer block
- Start sections with a direct answer, then context and data, then nuance (inverted pyramid)
- Avoid pronouns referencing earlier content ("As mentioned above...")
- Avoid forward-references ("We'll cover this later...")
- Pages scoring 8.5/10+ on completeness are **4.2x more likely** to appear in AI Overviews

**FWS application**: Every hub page section (SEO intro, tips, FAQ answers) must be self-contained. A FAQ answer about "How much does a Provence wedding cost?" must include the answer within that block, not reference a table elsewhere on the page.

### 2.2 Multi-Modal Content Integration (r=0.92)

The **highest correlation factor**. Pages with text + images + video + schema see **317% higher selection rates** vs. text-only.

**Rules**:
- Every hub page must include **2-3 contextual images** with descriptive alt text
- Include **60-90 second explainer videos** where possible (venue tours, region overviews)
- Implement `ImageObject`, `VideoObject`, `HowTo`, `FAQ` schema markup
- Captions must link visuals to surrounding text content
- Real wedding photography and venue imagery = natural multi-modal content advantage for FWS

**Platform differences**:
| Platform | Prioritises |
|----------|------------|
| Google AI Overviews | Images + structured data |
| ChatGPT | Citations + text quality |
| Perplexity | Recency + verifiable claims |

### 2.3 Real-Time Factual Verification (r=0.89)

Content with verifiable claims gets **89% higher selection probability**. AI systems evaluate whether claims can be cross-referenced against trusted sources.

**Citation tier system**:
| Tier | Source Type | Citation Boost | FWS Examples |
|------|-----------|---------------|-------------|
| **Tier 1** | Government data, institutional research (.gov/.edu) | +132% | French legal requirements, official tourism statistics |
| **Tier 2** | Established publications with editorial standards | +78% | Vogue, Brides, travel publications |
| **Tier 3** | Expert quotes with credentials | +52% | Named wedding planners, venue owners |

**Rules**:
- Every major claim must have a specific, verifiable source
- Statistics must include recent publication dates
- Never use vague citations ("studies show", "experts say")
- Never self-reference as sole authority ("according to our data")
- Real wedding data (actual costs, guest counts, timelines) = Tier 3 verifiable evidence

### 2.4 Vector Embedding Alignment (r=0.84)

AI doesn't match keywords — it matches **meaning**. Content must cover the full semantic neighbourhood of a topic.

**Rules**:
- Use natural language variations, not exact keyword repetition
- Include **15-20 LSI (related) terms** naturally per 1,000 words
- Explicitly connect related concepts ("Provence, located in the south of France, is known for...")
- Cover the entire semantic field: a page about "château wedding venues" should also mention castle, manor, estate, historic, turrets, grounds, estate wedding, French countryside
- Cosine similarity above 0.88 = **7.3x higher selection rates**

**FWS application**: Hub pages already have rich semantic fields through venue descriptions, regional context, and comparison tables. Ensure planning guides cover adjacent concepts, not just the headline topic.

### 2.5 E-E-A-T Authority Signals (r=0.81)

96% of AI Overview content comes from verified authoritative sources. Authority is now **externally validated** — it comes from what others say about you, not what you say about yourself.

**Experience**:
- First-hand implementation details and specific metrics
- Real wedding stories with actual costs, timelines, and logistics
- Before/after evidence and behind-the-scenes content

**Expertise**:
- Author credentials prominently displayed on every article
- Author Schema implementation (Person nested in Article)
- Expert interviews with named planners, photographers, venue owners
- Technical accuracy in legal/logistics content

**Authoritativeness**:
- Citations by other authoritative publications
- Cross-platform visibility (Instagram, Pinterest, YouTube, press)
- Industry recognition (awards, features, partnerships)
- Knowledge Graph entity status for "French Wedding Style"

**Trustworthiness**:
- HTTPS, clear contact info, About page, privacy policy
- Content freshness indicators ("Last updated" dates on every page)
- Transparent correction policies
- No misleading headlines, no intrusive ads

**Trust killers**: Expired SSL, hidden contact info, intrusive pop-ups, misleading clickbait, slow page load.

### 2.6 Entity Knowledge Graph Density (r=0.76)

Content with **15+ connected entities** per 1,000 words shows **4.8x higher selection probability**.

**Rules**:
- Use full entity names on first mention (e.g., "Château de Tourreau in Provence" not "the venue")
- Include relevant entities from the topic's ecosystem: venue names, regions, planners, photographers, traditions
- Link entities to authoritative sources (official websites, Wikipedia)
- Show entity **relationships**, don't just list them ("Château de Sannes, a 17th-century estate in the Luberon area of Provence, is one of the most sought-after wedding venues in southern France")
- Entity types that matter: people, places, organisations, venues, regions, traditions, costs

**FWS advantage**: Every hub page naturally contains 20+ entities (venue names, region names, towns, planners). Make these connections explicit rather than assuming the reader knows the geography.

### 2.7 Structured Data / Schema Markup

Properly structured content shows **73% higher selection rates** vs. unmarked.

**Required schema per page type**:

| Page Type | Required Schema | Notes |
|-----------|----------------|-------|
| Hub page | `ItemList`, `FAQPage`, `BreadcrumbList`, `Article` | Already in strategy — add `ImageObject` for venue photos |
| Venue listing | `LocalBusiness`, `Place`, `Product`, `BreadcrumbList`, `ImageObject` | Include `AggregateRating` when reviews exist |
| Planning guide | `Article`, `FAQPage`, `HowTo`, `BreadcrumbList`, `Person` (author) | `Person` schema with credentials is critical |
| Real wedding | `BlogPosting`, `ImageGallery`, `BreadcrumbList`, `Person` | Author + photographer entities |
| Location page | `Place`, `ItemList`, `FAQPage`, `BreadcrumbList` | Already in strategy |

**Additional requirements**:
- Nest schema properly: `Article` → contains `Author` (`Person`) → affiliated with `Organization`
- Validate all schema with Google's Rich Results Test
- `llms.txt` file to guide AI crawlers to high-value content pages

---

## 3. Content Format Priorities

These content types have the highest AI citation rates:

| Format | Why AI Cites It | FWS Application |
|--------|----------------|-----------------|
| **Comparison tables** | Scannable, structured, fact-dense | Hub page comparison tables (already planned) |
| **Ultimate guides** | Comprehensive, self-contained authority | Planning guides ("Complete Guide to Getting Married in France") |
| **FAQ sections** | Direct question-answer pairs | Hub page FAQs + planning guide FAQs |
| **Statistics pages** | Verifiable data points AI can extract | Cost breakdowns, regional venue counts, capacity data |
| **Glossaries / definitions** | Clean entity definitions for Knowledge Graph | French wedding terminology guide |
| **How-to content** | Step-by-step structure AI can follow | Planning timelines, legal process guides |
| **Listicles with data** | Structured, extractable | "10 Best Château Wedding Venues in Provence" (hub pages) |

---

## 4. The Three Authority Pillars

Authority in AI search is built across three pillars — on-site content alone is not enough.

### 4.1 Category Authority

Establish FWS as **the** definitive voice on destination weddings in France. Not just a directory — the reference point others defer to.

**Actions**:
- Publish original data (average costs by region, booking trends, seasonal pricing) that others cite
- Take clear editorial positions ("Why the Dordogne is underrated for weddings")
- Create the content that planners and couples share as reference material

### 4.2 Canonical Authority

Create **explanation-first content** designed to be cited and reused.

**Actions**:
- Hub pages, guides, FAQs, and glossaries must be structurally sound, consistently updated, and clearly authored
- Every piece must be self-contained enough that AI can extract and cite a passage
- "Last updated" dates on all content — 23% of AI-featured content is less than 30 days old

### 4.3 Distributed Authority

Build credible presence across platforms FWS doesn't control.

**Actions**:
- Digital PR: Features in Vogue, Brides, travel publications, wedding blogs
- YouTube: Venue tours, region guides, real wedding highlights — YouTube comments are a leading factor correlated with AI mentions
- Reddit / forums: Authentic participation in r/weddingplanning, expat communities
- Reviews: Google Business reviews, Trustpilot, wedding platform reviews
- Instagram / Pinterest: Already strong — maintain and grow
- Podcast appearances: Wedding planning podcasts, destination wedding episodes

---

## 5. Technical Requirements

### Crawler Access
- Ensure `GPTBot`, `ClaudeBot`, `PerplexityBot` are **not blocked** in robots.txt
- Create `llms.txt` pointing AI crawlers to high-value content (pillar pages, hub pages, planning guides)
- All critical content must be accessible without JavaScript rendering (SSR or static HTML)

### Page Speed
- Core Web Vitals: INP under 200ms
- Server-Side Rendering for critical content
- AI agents have limited rendering budgets — content must be in initial HTML

### Freshness Signals
- "Last updated" date on every page (visible + in schema)
- Regular content refreshes — at least quarterly for hub pages
- 23% of AI-featured content is less than 30 days old

### Security & Trust
- HTTPS everywhere (non-negotiable)
- Clear About page, Contact page, Privacy Policy
- Author bios on all editorial content
- No intrusive interstitials or deceptive ads

---

## 6. FWS-Specific Implementation Checklist

This checklist applies to every content template and page type.

### Per-Page Requirements

- [ ] **Self-contained answer blocks**: Every section passes the "island test" (134-167 words per answer block)
- [ ] **Inverted pyramid**: Direct answer first, context second, nuance third
- [ ] **Multi-modal**: 2-3 contextual images with alt text per page minimum
- [ ] **Verifiable claims**: Every statistic/claim has a named source and date
- [ ] **Entity density**: 15+ connected entities per 1,000 words, with explicit relationships
- [ ] **Schema markup**: Full nested schema per page type (see Section 2.7)
- [ ] **Author attribution**: Named author with credentials and Person schema
- [ ] **Freshness date**: "Last updated" visible on page and in schema
- [ ] **No fluff**: Remove subjective adjectives without evidence ("stunning", "perfect", "amazing")
- [ ] **LSI coverage**: 15-20 semantically related terms per 1,000 words

### Site-Wide Requirements

- [ ] `llms.txt` created and maintained
- [ ] AI crawler bots not blocked in robots.txt
- [ ] All critical content SSR or static HTML
- [ ] Core Web Vitals passing (INP < 200ms)
- [ ] HTTPS, About page, Contact page, Privacy Policy all present
- [ ] Author bio pages with credentials for all editorial contributors
- [ ] Nested schema: Article → Person (author) → Organization (FWS)
- [ ] Comparison tables on all hub pages
- [ ] FAQ sections with FAQPage schema on all hub and guide pages
- [ ] "Last updated" dates on all content pages

### Distributed Authority Actions

- [ ] Digital PR calendar: Target 2+ features per quarter in wedding/travel publications
- [ ] YouTube channel: Venue tours and region guides
- [ ] Reddit/community presence: Authentic participation in wedding planning communities
- [ ] Review generation: Google Business + wedding platform reviews
- [ ] Podcast guest appearances: Destination wedding shows

---

## 7. Content Strategy Integration Points

This file must be cross-referenced when working on:

| Activity | How This File Applies |
|----------|----------------------|
| Hub page template design | Section 2 (all 7 factors) + Section 6 per-page checklist |
| Planning guide writing | Section 2.1 (self-contained blocks) + 2.3 (verifiable claims) + 2.5 (author attribution) |
| Venue listing template | Section 2.7 (schema) + 2.2 (multi-modal) + 2.6 (entity density) |
| URL structure decisions | No direct impact — AI cares about content quality, not URL format |
| Blog article creation | Section 3 (content formats) + Section 2.1 (inverted pyramid) + Section 6 checklist |
| Real wedding posts | Section 2.3 (verifiable data — real costs, real timelines) + 2.2 (photography) |
| Technical site build | Section 5 (crawler access, page speed, SSR, llms.txt) |
| Marketing / PR | Section 4.3 (distributed authority) + Section 6 distributed authority actions |
| Airtable schema | Track "last_updated" date, author attribution, schema validation status per page |
| Content refresh cycle | Section 5 freshness signals — quarterly hub page reviews minimum |

---

## 8. Tone Implications

Cross-reference with `context/tone-of-voice.md`. Key intersections:

- **Remove fluff adjectives** aligns with existing forbidden word list — extend the list to include: "stunning", "perfect", "amazing", "world-class", "breathtaking", "one-of-a-kind" unless backed by specific evidence
- **Fact density over prose** — every paragraph should contain at least one extractable, verifiable fact
- **Expert positioning** — FWS editorial voice should read as knowledgeable insider, not marketing copy
- **Specificity wins** — "From €15,000 for 80 guests" beats "affordable pricing available"
