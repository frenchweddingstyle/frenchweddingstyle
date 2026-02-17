# Map Content

Create a comprehensive Hub/Spoke content architecture for the French wedding market with authority flow optimization.

## Usage

```
/map-content
```

## What This Does

Launches the **Content Mapping Workflow** for the Provence pilot region. This systematic workflow will:

1. **Audit Venue Inventory** - Classify your Provence venues by region, type, and features
2. **Conduct Keyword Research** - Identify hub and roundup page opportunities using Ahrefs (manual input)
3. **Analyze Competitors** - Review Wedinspire's SERP presence and identify gaps
4. **Generate Content Architecture** - Create three-tier Hub/Spoke structure:
   - **Tier 1 (Hubs)**: 3-5 high-authority pages targeting main keywords
   - **Tier 2 (Roundups)**: 10-15 curated collection pages targeting mid-tail keywords
   - **Tier 3 (Listings)**: Existing venue pages optimized with internal links
5. **Create Content Briefs** - Individual briefs for each hub and roundup page
6. **Produce Implementation Roadmap** - Prioritized 12-week schedule integrated with your 9 posts/week workflow

## Output

The workflow produces:

- **📄 Content Tree**: `outputs/content-strategy/provence-pilot/content-tree.md`
  - Visual three-tier architecture
  - Authority flow diagram
  - Internal linking strategy
  - Summary statistics

- **📁 Hub Page Briefs**: `outputs/content-strategy/provence-pilot/hub-briefs/`
  - 3-5 individual markdown files
  - Target keywords, content structure, SEO requirements
  - Brand voice guidelines, competitive analysis
  - Ready for immediate content creation

- **📁 Roundup Page Briefs**: `outputs/content-strategy/provence-pilot/roundup-briefs/`
  - 10-15 individual markdown files
  - Category definitions, venue selection criteria
  - Specific venues to feature (8-15 per roundup)
  - Internal linking requirements, Wedinspire comparison

- **📄 Implementation Roadmap**: `outputs/content-strategy/provence-pilot/implementation-roadmap.md`
  - Week-by-week schedule (12 weeks)
  - Priority scores and rationale
  - Integration with existing publishing workflow
  - Success metrics and checkpoints

## Requirements

Before running this command, ensure you have:

✅ **Venue Inventory**: Airtable database or spreadsheet of Provence venues with features (region, type, capacity, amenities)
   - If using Airtable: Prepare to export as CSV or share a read-only view link

✅ **Ahrefs Access**: Login credentials for Ahrefs.com (you'll run queries and paste results)

✅ **Context Loaded**: Run `/prime` first to load brand voice and strategic context

## Workflow Phases

The interactive workflow guides you through 5 phases:

**Phase 1: Discovery & Inventory** (~30 minutes)
- Load venue spreadsheet
- Classify venues by region, type, features
- Identify content gaps

**Phase 2: Keyword Research** (~2 hours)
- Hub page keyword research using Ahrefs (manual input)
- Roundup page opportunity identification
- Competitor SERP analysis

**Phase 3: Architecture Design** (~1 hour)
- Define 3-5 hub pages
- Define 10-15 roundup categories
- Map authority flow

**Phase 4: Content Briefs** (~2-3 hours)
- Generate hub page briefs
- Generate roundup page briefs
- Create listing optimization recommendations

**Phase 5: Prioritization** (~1 hour)
- Calculate priority scores
- Create implementation sequence
- Define success metrics

**Total Time**: 6-8 hours over 1-2 sessions

## Ahrefs Integration (Manual Input - Option 1)

This workflow uses **manual Ahrefs input**:
- Claude provides specific Ahrefs query parameters
- You run queries in Ahrefs and paste results
- Claude analyzes data and builds content architecture

No API integration required - works with your existing Ahrefs subscription.

## Strategic Purpose

This addresses your Q1-Q2 2026 strategic priorities:

- **Priority #4**: Competitive Research & Content Strategy (close Wedinspire gap)
- **Priority #3**: Directory Value Enhancement (showcase venues systematically)
- **Priority #1**: Audience Growth (SEO traffic through roundup pages)

**The Problem**: Your 170+ venue listing pages aren't pushing link juice to high-authority pages. Google wants curated roundup pages, but FWS lacks this middle tier.

**The Solution**: Create a three-tier Hub/Spoke architecture that flows authority from individual listings → curated roundups → main hub pages, systematically targeting keywords from long-tail to head terms.

## What Makes This Different

**Not Just a List** - This is a systematic workflow that:
- ✅ Requires verified Ahrefs data (no guessing)
- ✅ Maps to your actual venue inventory (no assumptions)
- ✅ Enforces brand voice compliance (no AI clichés)
- ✅ Analyzes Wedinspire competition (specific URLs and gaps)
- ✅ Creates actionable briefs (ready to write immediately)
- ✅ Integrates with your 9 posts/week workflow

**Anti-Hallucination Protocol**:
- All keyword data requires Ahrefs source verification
- All venue features verified from inventory
- All competitor URLs must be actual SERP results
- Brand voice checked against tone-of-voice.md

## After This Workflow

Once you complete the Provence pilot and validate success, you can:
- Create similar workflows for Bordeaux, Loire Valley, Côte d'Azur
- Expand to full French market (5-8 hub pages, 30-50 roundup pages)
- Scale the Hub/Spoke architecture across all regions

## Example Use Case

```
You: /map-content

Claude: I'll guide you through mapping the Provence wedding market. This will take 6-8 hours over 1-2 sessions. Let's start with Phase 1: Discovery & Inventory.

First, I need your Provence venue inventory data. Please provide:
- List of venues (names)
- Location (specific area in Provence)
- Venue type (château, villa, farmhouse, etc.)
- Key features (chapel, vineyard, lavender fields, pool, etc.)
- Capacity (guest count)
- Accommodation (sleep count)

You can paste a CSV, share a spreadsheet link, or summarize if extensive.

[You paste venue data]

Claude: Perfect! I've classified your 45 Provence venues:
- By region: Luberon (18), Aix-en-Provence (12), Alpilles (8), Coastal (7)
- By type: Château (15), Villa (12), Domaine (10), Farmhouse (8)
- By features: Vineyard (14), Chapel (9), Lavender fields (7), 200+ capacity (6), Sleeps 50+ (11)

Based on this inventory, I've identified 12 potential roundup categories with sufficient venues (8+ each).

Let's move to Phase 2: Keyword Research. I'll provide specific Ahrefs queries for you to run...

[Workflow continues through all 5 phases]
```

## Notes

- This workflow is **Provence-specific** (pilot region)
- Located in: `workflows/provence-pilot/`
- Uses templates from: `workflows/provence-pilot/content-mapping-templates/`
- Validation checklist: `workflows/provence-pilot/content-mapping-checklists/validation.md`
- Follows proven research-workflow.yaml pattern

## Related Commands

- `/prime` - Initialize session with full context (run this first!)
- `/create-plan` - Plan implementation changes
- `/implement` - Execute implementation plans

---

**Ready to map your content strategy? Run `/map-content` to begin!**