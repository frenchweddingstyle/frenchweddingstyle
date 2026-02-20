"""
Tone Checker — scans text for forbidden words from the FWS tone-of-voice guide.

Returns a list of violations with context. Used as a validation step in the
pipeline: if violations found, AI rewrites the offending text.
"""

import re

# Forbidden words and phrases from context/tone-of-voice.md
FORBIDDEN_WORDS = [
    # AI Writing Red Flags
    "timeless", "timelessness",
    "sophistication", "sophisticated",
    "nestled", "nestling",
    "opulent", "opulence",
    "meticulous", "meticulously",
    "effortless", "effortlessly",
    "curated",
    "boasts", "boasting",
    "stunning",
    "breathtaking",
    "exquisite",
    "impeccable", "flawless",
    "ethereal", "whimsical",
    "enchanting", "magical",
    "captivating", "mesmerizing",
    # Generic Luxury Language
    "luxe", "luxury",
    "elegant", "elegance",
    "glamorous", "glam",
    "lavish",
    "sumptuous", "decadent",
    "extravagant",
    "high-end", "upscale",
    "exclusive", "premier",
    # Trendy/Buzzy
    "trendy", "on-trend",
    "viral", "buzzy",
    "hyped",
    "must-have", "must-see",
    "of-the-moment",
    "cutting-edge",
    "next-level",
    # Vague Descriptors
    "beautiful", "gorgeous", "lovely",
    "amazing", "incredible", "awesome",
    "perfect",
    "unique",
    "special", "memorable",
    "dream", "dreamy",
    "unforgettable",
    "ultimate", "definitive",
]

# Build regex pattern — match whole words, case-insensitive
_PATTERN = re.compile(
    r'\b(' + '|'.join(re.escape(w) for w in FORBIDDEN_WORDS) + r')\b',
    re.IGNORECASE
)


def check_text(text: str) -> list[dict]:
    """
    Scan text for forbidden words.

    Returns list of dicts: [{"word": str, "position": int, "context": str}]
    Empty list means the text passes tone checking.
    """
    violations = []
    for match in _PATTERN.finditer(text):
        start = max(0, match.start() - 40)
        end = min(len(text), match.end() + 40)
        context = text[start:end].replace('\n', ' ')
        violations.append({
            "word": match.group(),
            "position": match.start(),
            "context": f"...{context}...",
        })
    return violations


def check_dict_values(data: dict, path: str = "") -> list[dict]:
    """
    Recursively scan all string values in a dict/list structure.

    Returns violations with the JSON path where each was found.
    """
    violations = []

    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            violations.extend(check_dict_values(value, current_path))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            violations.extend(check_dict_values(item, f"{path}[{i}]"))
    elif isinstance(data, str):
        text_violations = check_text(data)
        for v in text_violations:
            v["path"] = path
        violations.extend(text_violations)

    return violations


def format_report(violations: list[dict]) -> str:
    """Format violations into a readable report string."""
    if not violations:
        return "PASS — No forbidden words found."

    lines = [f"FAIL — {len(violations)} forbidden word(s) found:\n"]
    for v in violations:
        path_info = f" at {v['path']}" if v.get('path') else ""
        lines.append(f"  - \"{v['word']}\"{path_info}")
        lines.append(f"    Context: {v['context']}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Quick self-test
    sample = (
        "This stunning château is nestled in the rolling hills of Provence. "
        "The venue boasts elegant interiors and timeless sophistication."
    )
    violations = check_text(sample)
    print(format_report(violations))