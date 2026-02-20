"""
Step 2: Venue Lookup — Query Airtable for member venues, parse full_venue_json.

This module is called by the Claude slash command (not run standalone).
It provides the data structures and helper functions that the Claude agent
uses to query Airtable via MCP, parse venue JSON, derive tags, group venues
by sub-region, and calculate cost tiers.

The Claude agent will:
1. Query Airtable Venues table for FWS Members in the target region
2. Parse each venue's full_venue_json
3. Derive 2 "Best For" tags per venue
4. Group venues by sub-region (matching Step 1's sub_regions)
5. Calculate data-driven cost tiers
6. Save to working/{slug}/venues.json
"""

import json
import os
import random
import re


def slugify(name: str) -> str:
    """Convert venue name to URL-friendly slug."""
    slug = name.lower().strip()
    slug = re.sub(r'[àáâãäå]', 'a', slug)
    slug = re.sub(r'[èéêë]', 'e', slug)
    slug = re.sub(r'[ìíîï]', 'i', slug)
    slug = re.sub(r'[òóôõö]', 'o', slug)
    slug = re.sub(r'[ùúûü]', 'u', slug)
    slug = re.sub(r'[ç]', 'c', slug)
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug


def parse_venue_json(raw_json: str) -> dict | None:
    """Parse the full_venue_json field from Airtable. Returns None on failure."""
    if not raw_json:
        return None
    try:
        return json.loads(raw_json)
    except (json.JSONDecodeError, TypeError):
        return None


def extract_venue_card_data(venue_json: dict, airtable_record: dict) -> dict:
    """
    Extract display data for a venue card from full_venue_json + Airtable fields.

    Returns a flat dict with all fields needed for the venue card template.
    """
    identity = venue_json.get("identity", {})
    overview = venue_json.get("overview", {})
    location = venue_json.get("location", {})
    history = venue_json.get("history", {})

    # Get the name — prefer JSON, fall back to Airtable field
    name = identity.get("venue_name") or airtable_record.get("venue_name", "Unknown Venue")

    # Price display
    min_price = overview.get("min_price_eur")
    price_display = f"From €{min_price:,}" if min_price else "On request"

    # Capacity
    max_guests = overview.get("max_guests")
    capacity_display = str(max_guests) if max_guests else "TBC"

    # Airport
    airports = location.get("nearest_airports", [])
    if airports and isinstance(airports, list) and len(airports) > 0:
        airport = airports[0]
        airport_name = airport.get("name", "")
        airport_dist = airport.get("distance_text", "")
        airport_display = f"{airport_name} ({airport_dist})" if airport_dist else airport_name
    else:
        airport_display = "See listing"

    # Sub-region
    sub_region = location.get("sub_region", "")

    # Short CTA name (strip "Château de ", "Domaine de ", etc.)
    cta_name = name
    for prefix in ["Château de ", "Château du ", "Château d'", "Domaine de ",
                    "Domaine du ", "Domaine d'", "Bastide de ", "Bastide du ",
                    "Mas de ", "Mas du ", "Le Mas ", "La Bastide "]:
        if name.startswith(prefix):
            cta_name = name[len(prefix):]
            break

    return {
        "name": name,
        "slug": slugify(name),
        "venue_type": identity.get("venue_type", ""),
        "description": identity.get("short_description", ""),
        "price": price_display,
        "min_price_eur": min_price,
        "capacity": capacity_display,
        "max_guests": max_guests,
        "max_sleeping_guests": overview.get("max_sleeping_guests"),
        "airport": airport_display,
        "sub_region": sub_region,
        "location": sub_region or location.get("region", ""),
        "image_url": airtable_record.get("image_url", ""),
        "cta_name": cta_name,
        "explore_url": airtable_record.get("fws_url", ""),
        "review_url": airtable_record.get("FWS Review", ""),
        "real_weddings_linked": airtable_record.get("Real Weddings", []),
        # For tag derivation
        "_construction_period": history.get("construction_period", ""),
        "_construction_year": history.get("construction_year"),
        "_chapel": venue_json.get("ceremony", {}).get("chapel_on_site"),
        "_gardens": venue_json.get("amenities", {}).get("gardens_description"),
        "_child_friendly": venue_json.get("policies", {}).get("child_friendly"),
        "_pricing_model": venue_json.get("pricing", {}).get("pricing_model"),
        "_distance_to_coast": location.get("distance_to_coast"),
        "_landscape": location.get("landscape_description", ""),
        "_vineyard": venue_json.get("amenities", {}).get("vineyard_on_site"),
    }


def derive_tags(venue: dict) -> list[str]:
    """
    Derive 2 "Best For" tags for a venue based on its data.
    Returns a list of 2 strings.
    """
    candidates = []

    # Character tags
    year = venue.get("_construction_year")
    period = venue.get("_construction_period", "")
    if year and year < 1800:
        candidates.append(("character", "Historic"))
    elif period and any(c in period.lower() for c in ["16th", "17th", "15th", "14th", "13th", "medieval"]):
        candidates.append(("character", "Historic"))

    if venue.get("_chapel") and venue.get("_gardens"):
        candidates.append(("character", "Romantic"))

    # Practical tags
    max_g = venue.get("max_guests")
    if max_g and max_g < 80:
        candidates.append(("practical", "Intimate"))
    elif max_g and max_g > 200:
        candidates.append(("practical", "Grand"))

    if venue.get("_child_friendly"):
        candidates.append(("practical", "Family-Friendly"))

    if venue.get("_pricing_model") == "all_inclusive":
        candidates.append(("practical", "All-Inclusive"))

    # Location tags
    coast = venue.get("_distance_to_coast", "")
    if coast and ("seafront" in str(coast).lower() or "beach" in str(coast).lower()):
        candidates.append(("location", "Seaside"))

    landscape = venue.get("_landscape", "").lower()
    if venue.get("_vineyard"):
        candidates.append(("location", "Vineyard"))

    if any(w in landscape for w in ["hilltop", "perched", "hill", "cliff", "elevated"]):
        candidates.append(("location", "Hilltop"))

    if any(w in landscape for w in ["countryside", "rural", "pastoral", "farmland"]):
        candidates.append(("location", "Countryside"))

    # Pick 2 tags, preferring diversity across categories
    if len(candidates) < 2:
        # Fill with venue type fallback
        vtype = venue.get("venue_type", "")
        type_map = {
            "chateau": "Historic",
            "bastide": "Countryside",
            "mas": "Countryside",
            "domaine": "Vineyard",
            "hotel": "All-Inclusive",
            "abbaye": "Historic",
            "manoir": "Historic",
        }
        fallback = type_map.get(vtype, "Countryside")
        if not any(c[1] == fallback for c in candidates):
            candidates.append(("fallback", fallback))

    # Deduplicate by label
    seen = set()
    unique = []
    for cat, label in candidates:
        if label not in seen:
            seen.add(label)
            unique.append((cat, label))

    # Prefer diversity: pick from different categories if possible
    if len(unique) >= 2:
        categories_seen = set()
        result = []
        for cat, label in unique:
            if cat not in categories_seen and len(result) < 2:
                categories_seen.add(cat)
                result.append(label)
        # Fill remaining from what's left
        for cat, label in unique:
            if label not in result and len(result) < 2:
                result.append(label)
        return result[:2]

    return [c[1] for c in unique[:2]] if unique else ["Countryside", "Romantic"]


def group_by_sub_region(venues: list[dict], sub_region_names: list[str]) -> dict[str, list[dict]]:
    """
    Group venues by sub-region, matching against the sub_region_names from research.

    Venues that don't match any sub-region get placed in an "Other" group.
    Randomize order within each group.
    """
    groups = {name: [] for name in sub_region_names}
    groups["Other"] = []

    for venue in venues:
        v_region = (venue.get("sub_region") or "").lower()
        matched = False
        for name in sub_region_names:
            if name.lower() in v_region or v_region in name.lower():
                groups[name].append(venue)
                matched = True
                break
        if not matched:
            groups["Other"].append(venue)

    # Randomize within each group
    for name in groups:
        random.shuffle(groups[name])

    # Remove empty groups
    return {k: v for k, v in groups.items() if v}


def calculate_cost_tiers(venues: list[dict]) -> list[dict]:
    """
    Calculate 3 cost tiers from actual venue pricing data.

    Returns list of 3 dicts with tier info including real min/max from data.
    """
    prices = [v["min_price_eur"] for v in venues if v.get("min_price_eur")]
    if not prices:
        return _default_cost_tiers()

    prices.sort()
    n = len(prices)

    if n < 3:
        return _default_cost_tiers()

    # Split into thirds
    t1 = prices[:n // 3]
    t2 = prices[n // 3: 2 * n // 3]
    t3 = prices[2 * n // 3:]

    return [
        {
            "name": 'The "Chic Boutique"',
            "total_range": f"€{min(t1):,} - €{max(t1):,}",
            "ideal_for": "Bastides & Intimate Properties",
            "min_price": min(t1),
            "max_price": max(t1),
            "includes": [
                f"Venue Hire: €{min(t1):,} - €{max(t1):,}",
                "Catering: €150 - €180 per head",
                "Simple local florals & DIY decor",
                "Local DJ & Acoustic Duo",
            ],
        },
        {
            "name": 'The "Heritage Grandeur"',
            "total_range": f"€{min(t2):,} - €{max(t2):,}",
            "ideal_for": "Classic Châteaux",
            "min_price": min(t2),
            "max_price": max(t2),
            "includes": [
                f"Venue Hire: €{min(t2):,} - €{max(t2):,}",
                "Catering: €200 - €250 per head",
                "Full planning service included",
                "Multi-day events (Brunch etc)",
            ],
        },
        {
            "name": 'The "Ultra Luxe"',
            "total_range": f"€{min(t3):,}+",
            "ideal_for": "Premium Estates & Palaces",
            "min_price": min(t3),
            "max_price": max(t3),
            "includes": [
                f"Venue Hire: €{min(t3):,}+",
                "Michelin-standard catering",
                "High-end production & lighting",
                "Guest concierge services",
            ],
        },
    ]


def _default_cost_tiers() -> list[dict]:
    """Fallback cost tiers when insufficient pricing data."""
    return [
        {
            "name": 'The "Chic Boutique"',
            "total_range": "€5,000 - €10,000",
            "ideal_for": "Bastides & Intimate Properties",
            "includes": [
                "Venue Hire: €5,000 - €10,000",
                "Catering: €150 - €180 per head",
                "Simple local florals & DIY decor",
                "Local DJ & Acoustic Duo",
            ],
        },
        {
            "name": 'The "Heritage Grandeur"',
            "total_range": "€12,000 - €25,000",
            "ideal_for": "Classic Châteaux",
            "includes": [
                "Venue Hire: €12,000 - €25,000",
                "Catering: €200 - €250 per head",
                "Full planning service included",
                "Multi-day events (Brunch etc)",
            ],
        },
        {
            "name": 'The "Ultra Luxe"',
            "total_range": "€30,000+",
            "ideal_for": "Premium Estates & Palaces",
            "includes": [
                "Venue Hire: €30,000+",
                "Michelin-standard catering",
                "High-end production & lighting",
                "Guest concierge services",
            ],
        },
    ]


def save_venues(slug: str, data: dict, working_dir: str) -> str:
    """Save venues JSON to working directory. Returns file path."""
    output_dir = os.path.join(working_dir, slug)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "venues.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return output_path


def load_venues(slug: str, working_dir: str) -> dict:
    """Load venues JSON from working directory."""
    path = os.path.join(working_dir, slug, "venues.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)