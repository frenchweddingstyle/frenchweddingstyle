"""
Step 3: Link Assembly — Assemble CTA links for each venue.

This module is called by the Claude slash command (not run standalone).
It provides helpers for the Claude agent to look up linked Real Wedding
records in Airtable and merge CTA links into the venue data.

The Claude agent will:
1. For each venue from Step 2:
   - explore_url = fws_url (always present for members)
   - review_url = FWS Review field (may be null — hide CTA if missing)
   - real_wedding_url = look up linked Real Weddings → get FWS URL
2. Merge links into venue data
3. Save to working/{slug}/links.json
"""

import json
import os


def assemble_links(venue: dict, real_wedding_urls: dict[str, str] | None = None) -> dict:
    """
    Assemble CTA links for a single venue.

    Args:
        venue: Venue dict from Step 2
        real_wedding_urls: Mapping of Real Wedding record IDs → blog URLs.
                          Claude agent populates this from Airtable lookups.

    Returns:
        Updated venue dict with resolved link fields.
    """
    links = {
        "explore_url": venue.get("explore_url", ""),
        "review_url": venue.get("review_url", ""),
        "real_wedding_url": "",
    }

    # Resolve Real Wedding linked records
    linked_rw = venue.get("real_weddings_linked", [])
    if linked_rw and real_wedding_urls:
        # Use first linked Real Wedding that has a URL
        for rw_id in linked_rw:
            url = real_wedding_urls.get(rw_id, "")
            if url:
                links["real_wedding_url"] = url
                break

    # Merge into venue
    venue.update(links)

    # Clean up internal fields
    venue.pop("real_weddings_linked", None)

    return venue


def get_link_status(venues: list[dict]) -> dict:
    """
    Generate a summary of link completeness for user review.

    Returns dict with counts and details.
    """
    complete = []
    partial = []

    for v in venues:
        name = v.get("name", "Unknown")
        has_explore = bool(v.get("explore_url"))
        has_review = bool(v.get("review_url"))
        has_rw = bool(v.get("real_wedding_url"))

        status = {
            "name": name,
            "explore": has_explore,
            "review": has_review,
            "real_wedding": has_rw,
        }

        if has_explore and has_review and has_rw:
            complete.append(status)
        else:
            partial.append(status)

    return {
        "total": len(venues),
        "complete": len(complete),
        "partial": len(partial),
        "complete_venues": complete,
        "partial_venues": partial,
    }


def format_link_report(status: dict) -> str:
    """Format link status into a readable report string."""
    lines = [
        f"Link Assembly: {status['total']} venues",
        f"  Complete (all 3 CTAs): {status['complete']}",
        f"  Partial (missing some CTAs): {status['partial']}",
        "",
    ]

    if status["partial_venues"]:
        lines.append("Venues with missing links:")
        for v in status["partial_venues"]:
            missing = []
            if not v["explore"]:
                missing.append("Explore")
            if not v["review"]:
                missing.append("Review")
            if not v["real_wedding"]:
                missing.append("Real Wedding")
            lines.append(f"  - {v['name']}: missing {', '.join(missing)}")

    return "\n".join(lines)


def save_links(slug: str, venues: list[dict], working_dir: str) -> str:
    """Save links JSON to working directory. Returns file path."""
    output_dir = os.path.join(working_dir, slug)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "links.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(venues, f, indent=2, ensure_ascii=False)
    return output_path


def load_links(slug: str, working_dir: str) -> list[dict]:
    """Load links JSON from working directory."""
    path = os.path.join(working_dir, slug, "links.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)