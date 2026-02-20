"""
Step 1: Intelligence — Firecrawl research + AI synthesis.

This module is called by the Claude slash command (not run standalone).
It provides the data structures and helper functions that the Claude agent
uses to perform Firecrawl searches, scrape results, and synthesize research
into the structured JSON format expected by subsequent steps.

The Claude agent will:
1. Use firecrawl_search MCP to find wedding blog/travel articles
2. Use firecrawl_scrape MCP on top results to extract content
3. Synthesize into the RESEARCH_SCHEMA structure
4. Save to working/{slug}/research.json
"""

import json
import os

# Schema for the research output JSON
RESEARCH_SCHEMA = {
    "sub_regions": [
        {
            "name": "str — Sub-region name (e.g., 'French Riviera / Cote d\\'Azur')",
            "description": "str — 2-3 sentence bride-friendly intro",
            "key_towns": ["str — Notable towns in this sub-region"],
            "wedding_appeal": "str — Why brides choose this area",
        }
    ],
    "expert_tips": [
        {
            "title": "str — Short punchy title",
            "body": "str — 1-2 sentence practical tip",
        }
    ],
    "key_insights": {
        "accessibility": "str — How to get there, airport info",
        "optimal_timing": "str — Best months for weddings",
        "budgeting": "str — What venue hire typically includes",
        "legal_facts": "str — Legal requirements for foreign couples",
    },
    "brides_tip": {
        "title": "str — Standout tip title",
        "body": "str — The tip content (1-2 sentences)",
    },
    "hidden_costs": [
        {
            "name": "str — Cost name (e.g., 'SACEM Tax')",
            "description": "str — What it is and why it applies",
            "range": "str — Typical cost range (e.g., '€150-€300')",
        }
    ],
    "faqs": [
        {
            "question": "str — Common question brides ask",
            "answer": "str — Practical, honest answer",
        }
    ],
    "seasonal_savings": {
        "high": {"months": "str — e.g., 'July - Aug'", "price_pct": "100%"},
        "mid": {"months": "str — e.g., 'June / Sept'", "price_pct": "str — e.g., '85% - 90%'"},
        "low": {"months": "str — e.g., 'Oct - May'", "price_pct": "str — e.g., '60% - 75%'"},
    },
}

# Search queries template — Claude agent fills in {location}
SEARCH_QUERIES = [
    "best wedding destinations in {location} France",
    "wedding planning tips {location} France",
    "wedding venues {location} France guide",
    "destination wedding {location} France cost",
]


def get_search_queries(location: str) -> list[str]:
    """Generate Firecrawl search queries for a target location."""
    return [q.format(location=location) for q in SEARCH_QUERIES]


def save_research(slug: str, data: dict, working_dir: str) -> str:
    """Save research JSON to working directory. Returns file path."""
    output_dir = os.path.join(working_dir, slug)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "research.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return output_path


def load_research(slug: str, working_dir: str) -> dict:
    """Load research JSON from working directory."""
    path = os.path.join(working_dir, slug, "research.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_research(data: dict) -> list[str]:
    """Validate research data has all required fields. Returns list of issues."""
    issues = []
    required_keys = ["sub_regions", "expert_tips", "key_insights", "brides_tip",
                     "hidden_costs", "faqs", "seasonal_savings"]
    for key in required_keys:
        if key not in data:
            issues.append(f"Missing required key: {key}")

    if "sub_regions" in data:
        if not isinstance(data["sub_regions"], list) or len(data["sub_regions"]) < 2:
            issues.append("Need at least 2 sub_regions")
        for i, sr in enumerate(data.get("sub_regions", [])):
            if not sr.get("name"):
                issues.append(f"sub_regions[{i}] missing 'name'")
            if not sr.get("description"):
                issues.append(f"sub_regions[{i}] missing 'description'")

    if "expert_tips" in data:
        if not isinstance(data["expert_tips"], list) or len(data["expert_tips"]) < 6:
            issues.append("Need at least 6 expert_tips")

    if "key_insights" in data:
        for field in ["accessibility", "optimal_timing", "budgeting", "legal_facts"]:
            if not data["key_insights"].get(field):
                issues.append(f"key_insights.{field} is empty")

    if "faqs" in data:
        if not isinstance(data["faqs"], list) or len(data["faqs"]) < 6:
            issues.append("Need at least 6 FAQs")

    if "hidden_costs" in data:
        if not isinstance(data["hidden_costs"], list) or len(data["hidden_costs"]) < 3:
            issues.append("Need at least 3 hidden_costs")

    return issues