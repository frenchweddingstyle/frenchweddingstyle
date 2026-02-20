#!/usr/bin/env python3
"""Build venues.json for Paris / Ile-de-France location page."""
import json
import re
import unicodedata
import os

INPUT_PATH = r'C:\Users\LFoul\.claude\projects\c--Users-LFoul-Desktop-fws-content\08097e90-66e7-44ce-9745-9ef951b11c74\tool-results\mcp-airtable-list_records-1771397160679.txt'
OUTPUT_PATH = r'c:\Users\LFoul\Desktop\fws_content\workflows\location-page-gen\working\paris-ile-de-france\venues.json'

# --- Load data ---
with open(INPUT_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

records = data.get('records', [])


# --- Helpers ---
def slugify(text):
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text.strip())
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def make_cta_name(name):
    prefixes = [
        "Chateau du Prieure d'", "Chateau du Prieure d\u2019",
        "\u00c2Ch\u00e2teau du Prieur\u00e9 d\u2019",
        "Ch\u00e2teau du Prieur\u00e9 d\u2019",
        "Ch\u00e2teau du ", "Chateau du ",
        "Ch\u00e2teau de la ", "Chateau de la ",
        "Ch\u00e2teau de l'", "Chateau de l'",
        "Ch\u00e2teau d'", "Chateau d'",
        "Ch\u00e2teau de ", "Chateau de ",
        "Ch\u00e2teau des ", "Chateau des ",
        "Domaine du ", "Domaine de la ", "Domaine de l'", "Domaine d'",
        "Domaine de ", "Domaine des ",
        "H\u00f4tel ", "Hotel ",
        "Le Moulin de ", "Le Moulin du ",
        "Le ", "La ", "Les "
    ]
    for prefix in prefixes:
        if name.startswith(prefix):
            remainder = name[len(prefix):]
            return remainder
    return name


def parse_full_venue_json(raw):
    if not raw:
        return None
    fixed = raw.replace('\\_', '_')
    try:
        return json.loads(fixed)
    except json.JSONDecodeError:
        return None


def determine_sub_region(name, address, venue_address, closest_town):
    all_text = "{} {} {} {}".format(name, address, venue_address, closest_town).lower()

    paris_indicators = [
        '75001', '75002', '75003', '75004', '75005', '75006',
        '75007', '75008', '75009', '75010', '75011', '75012', '75013',
        '75014', '75015', '75016', '75017', '75018', '75019', '75020',
        'avenue montaigne', 'place vendome', 'place vend\u00f4me',
        'av. montaigne', 'av. junot', 'avenue kl\u00e9ber', 'av. kl\u00e9ber',
        "av. d'i\u00e9na", "rue de l'arcade"
    ]
    for p in paris_indicators:
        if p in all_text:
            return "Central Paris"

    yvelines_indicators = [
        '78430', '78460', '78740', 'louveciennes',
        'chevreuse', 'versailles', 'yvelines',
        'evecquemont', '\u00e9vecquemont'
    ]
    for y in yvelines_indicators:
        if y in all_text:
            return "Versailles & Yvelines"

    sem_indicators = [
        '77120', '77164', '77710', 'seine-et-marne',
        'ferrieres-en-brie', 'ferri\u00e8res-en-brie',
        'aulnoy', 'treuzy', 'fontainebleau'
    ]
    for s in sem_indicators:
        if s in all_text:
            return "Seine-et-Marne"

    vdo_indicators = [
        '95270', '95450', '95570', "val-d'oise", "val d'oise",
        'bouffemont', 'bouff\u00e9mont', 'saint-martin-du-tertre',
        'champlatreux', '\u00e9pinay-champl\u00e2treux',
        'condecourt', 'cond\u00e9court'
    ]
    for v in vdo_indicators:
        if v in all_text:
            return "Val-d'Oise & Northern \u00cele-de-France"

    if closest_town and 'paris' in closest_town.lower():
        return "Central Paris"
    if 'paris' in name.lower():
        return "Central Paris"

    return "\u00cele-de-France"


def infer_venue_type(name):
    name_lower = name.lower()
    if 'chateau' in name_lower or 'ch\u00e2teau' in name_lower:
        return "chateau"
    elif 'hotel' in name_lower or 'h\u00f4tel' in name_lower:
        return "hotel"
    elif 'moulin' in name_lower:
        return "moulin"
    elif 'domaine' in name_lower:
        return "domaine"
    elif 'manoir' in name_lower:
        return "manoir"
    return "venue"


def derive_tags(venue_type, sub_region, name, capacity, sleeping, price_min, venue_type_style):
    tags = []
    styles = venue_type_style if isinstance(venue_type_style, list) else []

    # Size-based first (determines Grand vs Intimate)
    is_intimate = capacity and capacity <= 80
    is_grand = capacity and capacity >= 300

    if venue_type in ('chateau', 'castle'):
        tags.append("Historic")
    if venue_type == 'hotel':
        if is_grand:
            tags.append("Grand")
        elif is_intimate:
            tags.append("Intimate")
        else:
            tags.append("Historic")
    if 'Historical' in styles and "Historic" not in tags:
        tags.append("Historic")

    # Add size tag if not already present
    if is_intimate and "Intimate" not in tags:
        tags.append("Intimate")
    elif is_grand and "Grand" not in tags:
        tags.append("Grand")

    if sub_region == "Seine-et-Marne":
        tags.append("Countryside")
    if 'Garden' in styles:
        tags.append("Romantic")

    if sleeping and sleeping >= 30 and "Grand" not in tags and "Intimate" not in tags:
        tags.append("Family-Friendly")

    if venue_type == 'moulin':
        tags.append("Countryside")
        tags.append("Romantic")

    # Deduplicate and remove contradictions
    seen = set()
    unique_tags = []
    for t in tags:
        if t not in seen:
            # Don't add Grand if Intimate already present, and vice versa
            if t == "Grand" and "Intimate" in seen:
                continue
            if t == "Intimate" and "Grand" in seen:
                continue
            seen.add(t)
            unique_tags.append(t)

    defaults_for_type = {
        "chateau": ["Historic", "Romantic"],
        "hotel": ["Romantic", "Historic"],
        "moulin": ["Countryside", "Romantic"],
        "domaine": ["Countryside", "Romantic"],
        "venue": ["Romantic", "Historic"],
    }
    fallbacks = defaults_for_type.get(venue_type, ["Romantic", "Historic"])
    for fb in fallbacks:
        if fb not in seen:
            unique_tags.append(fb)
            seen.add(fb)
        if len(unique_tags) >= 2:
            break

    return unique_tags[:2]


# Hand-written descriptions (no forbidden words)
DESCRIPTIONS = {
    "Chateau de Bonaventure": (
        "A historic chateau in the Brie region of Seine-et-Marne, offering private-hire "
        "celebrations for up to 150 guests. Set within sprawling grounds just an hour from "
        "Paris, with 36 beds on-site for weekend wedding stays."
    ),
    "Hotel Plaza Athenee": (
        "A landmark hotel on Avenue Montaigne in the heart of Paris, known for its "
        "red-geranium facade and views of the Eiffel Tower. Hosts refined wedding "
        "receptions for up to 80 guests with world-class catering and full hotel accommodation."
    ),
    "Hotel Particulier Montmartre": (
        "A private mansion hidden behind a cobbled lane in Montmartre, one of Paris's "
        "most characterful neighbourhoods. Offers an intimate garden setting and five "
        "suites for wedding celebrations of up to 120 guests."
    ),
    "Chateau de Meridon": (
        "A 13th-century estate rebuilt in the 19th century, set in the Chevreuse Valley "
        "just 40 minutes from Paris. Surrounded by parkland in the Yvelines, it hosts "
        "weddings for up to 150 guests with 42 beds on-site."
    ),
    "Ch\u00e2teau du Prieur\u00e9 d\u2019\u00c9vecquemont": (
        "A private estate in the Yvelines countryside, perched above a bend in the "
        "Seine with views across the valley. Welcomes intimate weddings of up to 70 "
        "guests with 30 sleeping on-site."
    ),
    "Chateau de Frenneville (Chateau de Paris)": (
        "A 13th-century fortified estate located 45 minutes south of Paris, offering "
        "exclusive hire for large-scale celebrations. Accommodates up to 400 guests "
        "for dinner and 90 overnight, set within a walled domain."
    ),
    "Hotel Shangri-la Paris": (
        "A former Napoleonic palace in Paris's 16th arrondissement, with direct views "
        "of the Eiffel Tower and the Seine. Hosts wedding receptions for up to 300 "
        "guests across grand reception rooms with period detailing."
    ),
    "Chateau de Prunay": (
        "A hillside chateau in Louveciennes, just west of Paris in the Yvelines "
        "department. Offers ceremony and reception spaces for up to 140 guests, "
        "surrounded by private gardens and a historic orangerie."
    ),
    "Le Moulin de Launoy": (
        "An 18th-century watermill in Treuzy-Levelay, one hour from Paris and 20 "
        "minutes from Fontainebleau. Once the studio of artist Bernard Boutet de "
        "Monvel, it now hosts weddings for up to 150 guests with 28 beds on-site."
    ),
    "Chateau Bouffemont": (
        "A 19th-century chateau in Val-d'Oise, 30 minutes north of Paris near "
        "Charles de Gaulle Airport. Built for the Marquise of Preignes, it offers "
        "exclusive-hire weddings for up to 150 guests with 30 sleeping on-site."
    ),
    "Alfred Sommier Hotel": (
        "A 19th-century hotel particulier steps from La Madeleine in central Paris, "
        "built in 1860. Features grand reception rooms and a garden courtyard for "
        "weddings of up to 180 guests."
    ),
    "Hotel Peninsula Paris": (
        "A grand hotel on Avenue Kleber in the 16th arrondissement, a short walk "
        "from the Arc de Triomphe. Hosts wedding celebrations for up to 100 guests "
        "in ornate period salons with rooftop views across Paris."
    ),
    "Chateau de Champlatreux": (
        "An 18th-century estate 30 minutes north of Paris and 15 minutes from CDG "
        "Airport, built between 1751 and 1757. Its formal gardens and grand interiors "
        "host weddings for up to 500 guests."
    ),
    "Chateau de Villette": (
        "Known as 'Le Petit Versailles,' this 17th-century chateau in Condecourt sits "
        "40 minutes northwest of Paris. Designed by Francois Mansart, it offers exclusive "
        "hire for weddings of up to 400 guests across its formal salons and 60-hectare grounds."
    ),
    "Hotel Ritz Paris": (
        "Situated at 15 Place Vendome in the 1st arrondissement, the Ritz Paris is one "
        "of the world's most recognized hotels. Offers wedding receptions for up to 400 "
        "guests in gilded salons, with a legendary bar and full hotel service."
    ),
}


def get_description(name, venue_type, sub_region, fvj):
    if fvj:
        desc = fvj.get('identity', {}).get('short_description', '')
        if desc:
            return desc
    if name in DESCRIPTIONS:
        return DESCRIPTIONS[name]
    return "A {} in the {} area of Ile-de-France, near Paris. Available for private-hire wedding celebrations.".format(
        venue_type, sub_region
    )


def format_price(min_price, max_price):
    if min_price and min_price > 0:
        return "From \u20ac{:,.0f}".format(min_price)
    return "On request"


def get_airport(sub_region, venue_address, fvj_data):
    if fvj_data:
        airports = fvj_data.get('location', {}).get('nearest_airports', [])
        if airports and isinstance(airports, list) and len(airports) > 0:
            first = airports[0]
            aname = first.get('name', '')
            dist = first.get('distance_text', '')
            if aname and dist:
                return "{} ({})".format(aname, dist)
            elif aname:
                return aname

    if sub_region == "Central Paris":
        return "Paris CDG / Orly"
    elif "Val-d'Oise" in sub_region or "Northern" in sub_region:
        return "Paris CDG (15-30 min)"
    elif sub_region == "Seine-et-Marne":
        return "Paris CDG / Orly"
    elif sub_region == "Versailles & Yvelines":
        return "Paris Orly / CDG"
    return "Paris CDG / Orly"


# --- Process all records ---
venues = []

for rec in records:
    fields = rec.get('fields', {})
    name = fields.get('venue_name', '')
    fvj_raw = fields.get('full_venue_json', '')
    fvj = parse_full_venue_json(fvj_raw)
    image_url = fields.get('image_url', '')
    fws_url = fields.get('fws_url', '')
    fws_review = fields.get('FWS Review', '')
    real_weddings = fields.get('Real Weddings', [])
    region = fields.get('region', '')
    closest_town = fields.get('Closest Town/ City', '')
    fws_member = fields.get('FWS Member', '')
    venue_address = fields.get('venue_address', '')
    min_price = fields.get('min_from_price_eur', None)
    max_price = fields.get('max_from_price_eur', None)
    max_cap = fields.get('max_guest_capacity', None)
    sleeping = fields.get('guest_sleep_onsite', None)
    venue_type_style = fields.get('venue_type_style', [])

    # venue_type
    if fvj:
        venue_type = fvj.get('identity', {}).get('venue_type', infer_venue_type(name))
    else:
        venue_type = infer_venue_type(name)

    # sub_region
    if fvj and fvj.get('location', {}).get('sub_region'):
        fvj_sub = fvj['location']['sub_region']
        if fvj_sub == "Seine-et-Marne":
            sub_region = "Seine-et-Marne"
        else:
            sub_region = determine_sub_region(name, '', venue_address, closest_town)
    else:
        sub_region = determine_sub_region(name, '', venue_address, closest_town)

    # Override for Chateau de Villette (fvj says Burgundy but Airtable says IDF)
    if name == "Chateau de Villette":
        sub_region = determine_sub_region(name, '', venue_address, closest_town)

    # Override for Frenneville - no address data, but it's in Essonne (south IDF)
    # Name contains "Chateau de Paris" which falsely triggers Central Paris
    if "Frenneville" in name:
        sub_region = "Seine-et-Marne"

    # Description
    # For Chateau de Villette: fvj is from a DIFFERENT property (Burgundy) so skip fvj desc
    if name == "Chateau de Villette":
        desc = get_description(name, venue_type, sub_region, None)
    else:
        desc = get_description(name, venue_type, sub_region, fvj)

    # Capacity
    # For Chateau de Villette: fvj capacity (22) is from wrong property, use Airtable (400)
    if name == "Chateau de Villette" and max_cap:
        capacity_num = max_cap
        sleeping_num = sleeping
    elif fvj:
        fvj_max = fvj.get('overview', {}).get('max_guests', None)
        fvj_sleeping = fvj.get('overview', {}).get('max_sleeping_guests', None)
        capacity_num = fvj_max or max_cap
        sleeping_num = fvj_sleeping if fvj_sleeping is not None else sleeping
    else:
        capacity_num = max_cap
        sleeping_num = sleeping

    # Price
    if fvj:
        fvj_price = fvj.get('overview', {}).get('min_price_eur', None)
        price_num = fvj_price or min_price
    else:
        price_num = min_price

    # Airport
    airport = get_airport(sub_region, venue_address, fvj)

    # Tags
    tags = derive_tags(
        venue_type, sub_region, name, capacity_num, sleeping_num,
        price_num, venue_type_style if isinstance(venue_type_style, list) else []
    )

    venue_card = {
        "name": name,
        "slug": slugify(name),
        "venue_type": venue_type,
        "description": desc,
        "price": format_price(price_num, max_price),
        "min_price_eur": price_num if price_num and price_num > 0 else None,
        "capacity": str(capacity_num) if capacity_num else "TBC",
        "max_guests": capacity_num,
        "max_sleeping_guests": sleeping_num if sleeping_num and sleeping_num > 0 else None,
        "airport": airport,
        "sub_region": sub_region,
        "location": sub_region,
        "image_url": image_url or "",
        "cta_name": make_cta_name(name),
        "explore_url": fws_url or "",
        "review_url": fws_review or "",
        "real_weddings_linked": real_weddings or [],
        "tags": tags
    }
    venues.append(venue_card)

# --- Group by sub_region ---
grouped = {
    "Central Paris": [],
    "Versailles & Yvelines": [],
    "Seine-et-Marne": [],
    "Val-d'Oise & Northern \u00cele-de-France": []
}

for v in venues:
    sr = v["sub_region"]
    if sr in grouped:
        grouped[sr].append(v)
    elif "Paris" in sr:
        grouped["Central Paris"].append(v)
    elif "Yvelines" in sr or "Versailles" in sr:
        grouped["Versailles & Yvelines"].append(v)
    elif "Seine-et-Marne" in sr:
        grouped["Seine-et-Marne"].append(v)
    elif "Val-d'Oise" in sr or "Northern" in sr:
        grouped["Val-d'Oise & Northern \u00cele-de-France"].append(v)
    else:
        # Fallback
        grouped["Central Paris"].append(v)
        v["sub_region"] = "Central Paris"
        v["location"] = "Central Paris"

# --- Cost tiers ---
priced_venues = sorted(
    [v for v in venues if v["min_price_eur"]],
    key=lambda x: x["min_price_eur"]
)

if len(priced_venues) >= 6:
    third = len(priced_venues) // 3
    tier1 = priced_venues[:third]
    tier2 = priced_venues[third:2*third]
    tier3 = priced_venues[2*third:]
elif len(priced_venues) >= 3:
    # Split as evenly as possible
    n = len(priced_venues)
    s1 = n // 3
    s2 = n // 3
    s3 = n - s1 - s2
    if s1 == 0:
        s1 = 1
        s3 = n - s1 - s2
    tier1 = priced_venues[:s1]
    tier2 = priced_venues[s1:s1+s2]
    tier3 = priced_venues[s1+s2:]
else:
    tier1 = []
    tier2 = []
    tier3 = []

if tier1 and tier2 and tier3:
    cost_tiers = [
        {
            "tier": 1,
            "label": "The Chic Boutique",
            "range": "\u20ac{:,.0f} \u2013 \u20ac{:,.0f}".format(
                tier1[0]['min_price_eur'], tier1[-1]['min_price_eur']
            ),
            "min": tier1[0]["min_price_eur"],
            "max": tier1[-1]["min_price_eur"],
            "venues": [v["name"] for v in tier1]
        },
        {
            "tier": 2,
            "label": "The Heritage Grandeur",
            "range": "\u20ac{:,.0f} \u2013 \u20ac{:,.0f}".format(
                tier2[0]['min_price_eur'], tier2[-1]['min_price_eur']
            ),
            "min": tier2[0]["min_price_eur"],
            "max": tier2[-1]["min_price_eur"],
            "venues": [v["name"] for v in tier2]
        },
        {
            "tier": 3,
            "label": "The Ultra Luxe",
            "range": "\u20ac{:,.0f}+".format(tier3[0]['min_price_eur']),
            "min": tier3[0]["min_price_eur"],
            "max": tier3[-1]["min_price_eur"],
            "venues": [v["name"] for v in tier3]
        }
    ]
else:
    cost_tiers = [
        {"tier": 1, "label": "The Chic Boutique", "range": "\u20ac5,000 \u2013 \u20ac10,000", "min": 5000, "max": 10000, "venues": []},
        {"tier": 2, "label": "The Heritage Grandeur", "range": "\u20ac12,000 \u2013 \u20ac25,000", "min": 12000, "max": 25000, "venues": []},
        {"tier": 3, "label": "The Ultra Luxe", "range": "\u20ac30,000+", "min": 30000, "max": None, "venues": []}
    ]

# --- Build output ---
output = {
    "venues": venues,
    "grouped": grouped,
    "cost_tiers": cost_tiers
}

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("Wrote {} venues to {}".format(len(venues), OUTPUT_PATH))
print()

# Summary
print("=== SUMMARY ===")
print("Total venues: {}".format(len(venues)))
print()
for sr, vlist in grouped.items():
    print("{}: {} venues".format(sr, len(vlist)))
    for v in vlist:
        has_fvj = "YES" if any(
            r.get('fields', {}).get('full_venue_json')
            for r in records
            if r.get('fields', {}).get('venue_name') == v['name']
        ) else "NO"
        print("  - {} (price: {}, capacity: {}, tags: {}, full_venue_json: {})".format(
            v['name'], v['price'], v['capacity'], v['tags'], has_fvj
        ))
    print()

print("=== COST TIERS ===")
for t in cost_tiers:
    print("Tier {}: {} -- {}".format(t['tier'], t['label'], t['range']))
    for vn in t['venues']:
        print("  - {}".format(vn))
    print()
