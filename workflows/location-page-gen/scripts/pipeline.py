"""
Pipeline Orchestrator — Main entry point for the location page generation pipeline.

This module is used by the Claude slash command as a reference and utility layer.
The actual orchestration happens in the slash command itself, which:
1. Asks the user for a target location
2. Looks up the location hierarchy
3. Runs Steps 1-4 with pauses between each

This file provides shared utilities: path resolution, location lookup,
slug generation, and progress tracking.
"""

import json
import os
import re

# Path constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKFLOW_DIR = os.path.join(SCRIPT_DIR, "..")
WORKING_DIR = os.path.join(WORKFLOW_DIR, "working")
OUTPUT_DIR = os.path.join(WORKFLOW_DIR, "output")
ROOT_DIR = os.path.join(WORKFLOW_DIR, "..", "..")
LOCATION_HIERARCHY_PATH = os.path.join(ROOT_DIR, "reference", "location-pages.json")


def load_location_hierarchy() -> dict:
    """Load the location hierarchy from reference/location-pages.json."""
    with open(LOCATION_HIERARCHY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def lookup_location(location_name: str) -> dict | None:
    """
    Look up a location in the hierarchy by name.

    Returns dict with:
        - name: Display name
        - url: FWS URL
        - sub_regions: Dict of sub-region data
        - tier: 'top' | 'sub_region' | 'city'

    Returns None if not found.
    """
    hierarchy = load_location_hierarchy()

    # Check top-level locations (South of France, North of France)
    for top_name, top_data in hierarchy.items():
        if _name_match(location_name, top_name):
            return {
                "name": top_name,
                "url": top_data.get("url", ""),
                "sub_regions": top_data.get("sub_regions", {}),
                "tier": "top",
            }

        # Check sub-regions
        for sr_name, sr_data in top_data.get("sub_regions", {}).items():
            if _name_match(location_name, sr_name):
                if isinstance(sr_data, str):
                    return {
                        "name": sr_name,
                        "url": sr_data,
                        "sub_regions": {},
                        "tier": "sub_region",
                    }
                return {
                    "name": sr_name,
                    "url": sr_data.get("url", ""),
                    "sub_regions": sr_data.get("cities", {}),
                    "tier": "sub_region",
                }

    return None


def _name_match(query: str, target: str) -> bool:
    """Case-insensitive partial name match."""
    return query.lower().strip() in target.lower() or target.lower() in query.lower().strip()


def make_slug(location_name: str) -> str:
    """Convert location name to URL-friendly slug."""
    slug = location_name.lower().strip()
    slug = re.sub(r'[àáâãäå]', 'a', slug)
    slug = re.sub(r'[èéêë]', 'e', slug)
    slug = re.sub(r'[ìíîï]', 'i', slug)
    slug = re.sub(r'[òóôõö]', 'o', slug)
    slug = re.sub(r'[ùúûü]', 'u', slug)
    slug = re.sub(r'[ç]', 'c', slug)
    slug = re.sub(r"'", '', slug)
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug


def get_working_dir(slug: str) -> str:
    """Get the working directory path for a location slug, creating if needed."""
    path = os.path.join(WORKING_DIR, slug)
    os.makedirs(path, exist_ok=True)
    return path


def check_step_completion(slug: str) -> dict[str, bool]:
    """Check which pipeline steps have been completed for a slug."""
    working = os.path.join(WORKING_DIR, slug)
    return {
        "research": os.path.exists(os.path.join(working, "research.json")),
        "venues": os.path.exists(os.path.join(working, "venues.json")),
        "links": os.path.exists(os.path.join(working, "links.json")),
        "draft": os.path.exists(os.path.join(working, "draft.html")),
        "output": os.path.exists(os.path.join(OUTPUT_DIR, f"{slug}.html")),
    }


def get_region_filter_values(location_name: str) -> list[str]:
    """
    Generate Airtable region filter values for a location.

    For top-level locations like "South of France", returns all sub-region
    names that should be searched in the Airtable `region` field.
    """
    location = lookup_location(location_name)
    if not location:
        return [location_name]

    if location["tier"] == "top":
        # Return all sub-region names
        return list(location["sub_regions"].keys())
    elif location["tier"] == "sub_region":
        return [location["name"]]
    else:
        return [location_name]


def list_available_locations() -> list[str]:
    """List all locations available in the hierarchy."""
    hierarchy = load_location_hierarchy()
    locations = []
    for top_name, top_data in hierarchy.items():
        locations.append(top_name)
        for sr_name in top_data.get("sub_regions", {}).keys():
            locations.append(f"  - {sr_name}")
    return locations