"""
Step 4: Compilation — Generate final HTML using Jinja2 template.

This module is called by the Claude slash command (not run standalone).
It provides the rendering function that takes all data from Steps 1-3
and produces the final HTML blog post.

The Claude agent will:
1. Load research.json, venues.json, links.json from working/{slug}/
2. Generate editorial content (intro, sub-region descriptions, why-choose, etc.)
3. Run all text through tone_checker.py
4. Call render_page() with the full context
5. Save draft to working/{slug}/draft.html
6. On approval, copy to output/{slug}.html
"""

import json
import os
import shutil

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    Environment = None
    FileSystemLoader = None


# Path constants (relative to this script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "..", "templates")
WORKING_DIR = os.path.join(SCRIPT_DIR, "..", "working")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "output")


def build_template_context(
    location_name: str,
    slug: str,
    research: dict,
    venues: list[dict],
    editorial: dict,
) -> dict:
    """
    Build the full Jinja2 template context dict.

    Args:
        location_name: Display name (e.g., "the South of France")
        slug: URL slug (e.g., "south-of-france")
        research: Step 1 research.json data
        venues: Step 3 links.json data (venues with resolved links)
        editorial: AI-generated editorial content dict with keys:
            - subtitle: italic subtitle for header
            - intro_paragraph: opening paragraph
            - why_choose_text: "Why Choose" section content
            - meta_description: 155-char SEO description
            - cost_intro: intro text for cost section
            - sub_region_descriptions: dict mapping sub-region name -> description
            - venue_type_sections: list of dicts with name, description, venue_slugs

    Returns:
        Complete template context dict ready for Jinja2 rendering.
    """
    # Build sub-region sections with matched venues
    sub_regions = []
    for sr in research.get("sub_regions", []):
        sr_name = sr["name"]
        sr_venues = [v for v in venues if _matches_sub_region(v, sr_name)]
        sub_regions.append({
            "name": sr_name,
            "description": editorial.get("sub_region_descriptions", {}).get(sr_name, sr.get("description", "")),
            "venues": sr_venues,
        })

    # Build venue type sections
    venue_types = []
    for vt in editorial.get("venue_type_sections", []):
        vt_venues = [v for v in venues if v.get("slug") in vt.get("venue_slugs", [])]
        if vt_venues:
            venue_types.append({
                "name": vt["name"],
                "description": vt["description"],
                "venues": vt_venues,
            })

    return {
        "location_name": location_name,
        "slug": slug,
        "subtitle": editorial.get("subtitle", ""),
        "intro_paragraph": editorial.get("intro_paragraph", ""),
        "meta_description": editorial.get("meta_description", ""),
        "venues": venues,
        "key_insights": research.get("key_insights", {}),
        "why_choose_text": editorial.get("why_choose_text", ""),
        "sub_regions": sub_regions,
        "venue_types": venue_types,
        "cost_intro": editorial.get("cost_intro", ""),
        "cost_tiers": research.get("cost_tiers", []),
        "hidden_costs": research.get("hidden_costs", []),
        "seasonal_savings": research.get("seasonal_savings", {}),
        "expert_tips": research.get("expert_tips", []),
        "brides_tip": research.get("brides_tip", {}),
        "faqs": research.get("faqs", []),
    }


def _matches_sub_region(venue: dict, sub_region_name: str) -> bool:
    """Check if a venue belongs to a sub-region by name matching."""
    v_region = (venue.get("sub_region") or venue.get("location") or "").lower()
    sr_lower = sub_region_name.lower()
    return sr_lower in v_region or v_region in sr_lower


def render_page(context: dict) -> str:
    """
    Render the location page HTML from the Jinja2 template.

    Returns the complete HTML string.
    """
    if Environment is None:
        raise ImportError(
            "Jinja2 is not installed. Run: python -m pip install jinja2"
        )

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=True,
    )
    template = env.get_template("location-page.html")
    return template.render(**context)


def save_draft(slug: str, html: str) -> str:
    """Save draft HTML to working directory. Returns file path."""
    output_dir = os.path.join(WORKING_DIR, slug)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "draft.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def promote_to_output(slug: str) -> str:
    """Copy draft.html to output/{slug}.html. Returns output file path."""
    draft_path = os.path.join(WORKING_DIR, slug, "draft.html")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
    shutil.copy2(draft_path, output_path)
    return output_path


def load_all_data(slug: str) -> tuple[dict, list[dict], dict]:
    """
    Load all intermediate data for a slug.

    Returns: (research, venues_with_links, original_venues_data)
    """
    research_path = os.path.join(WORKING_DIR, slug, "research.json")
    venues_path = os.path.join(WORKING_DIR, slug, "venues.json")
    links_path = os.path.join(WORKING_DIR, slug, "links.json")

    with open(research_path, "r", encoding="utf-8") as f:
        research = json.load(f)
    with open(venues_path, "r", encoding="utf-8") as f:
        venues_data = json.load(f)
    with open(links_path, "r", encoding="utf-8") as f:
        venues_with_links = json.load(f)

    return research, venues_with_links, venues_data