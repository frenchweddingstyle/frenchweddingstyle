"""
Unified Venue Processor — Scrape, Clean, Categorize, Combine, Write to Airtable.

Handles the full pipeline for one venue record:
  Part 1: venue_url  → map → scrape pages → clean → categorize
  Part 2: listing URLs → scrape (single-page) → clean
  Part 3: combine under bold headings → truncate → PATCH Airtable

Usage:
  # Full pipeline (scrape + categorize + write):
  python process_venue.py <record_id> <venue_url> <cb_url> <wi_url> <fwv_url> <fc_key> <at_key> <base_id>

  # Scrape only (saves raw files for Claude structuring):
  python process_venue.py --scrape-only <record_id> <venue_url> <cb_url> <wi_url> <fwv_url> <fc_key> <at_key> <base_id>

  # Write structured file to Airtable (used after Task agent structures content):
  python process_venue.py --write-file <record_id> <structured_file> <at_key> <base_id>

  # Geocode venue address to GPS coordinates:
  python process_venue.py --geocode <record_id> <venue_address> <at_key> <base_id>

  # Write venue JSON files to Airtable (full + summary):
  python process_venue.py --write-json <record_id> <full_json_path> <summary_json_path> <at_key> <base_id>

  # Fetch venue_url_scraped + brochure_text from Airtable to temp files:
  python process_venue.py --fetch-json-sources <record_id> <venue_name> <at_key> <base_id>

  Pass "" for any empty listing-site URL.

Output (stdout, single line):
  SUCCESS|<chars>|<venue_pages>+<listing_count>|<sources_csv>
  SCRAPED|<chars>|<pages>+<listings>|<sources_csv>|<listing_chars>
  WRITTEN|<chars>
  JSON_WRITTEN|<full_chars>|<summary_chars>
  FETCHED|<scraped_chars>|<brochure_chars>
  NO_CONTENT|<reason>
  FETCH_ERROR|<reason>
  GEOCODED|<lat>,<lon>
  GEOCODE_FAIL|<reason>
  GEOCODE_SKIP|no address
  MANUAL_CHECK|<reason>|0
  AIRTABLE_ERROR|<reason>|<chars>
"""
import json
import re
import sys
import os
import time
import urllib.parse
import urllib.request
import urllib.error

WORKING_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'working')
PAYLOAD_PATH = os.path.join(WORKING_DIR, 'payload.json')
MAX_CHARS = 95000
RATE_LIMIT_DELAY = 2  # seconds between Firecrawl calls
MAX_PAGES = 20
MIN_CONTENT_CHARS = 500   # Below this, venue content is likely garbage
MIN_CONTENT_WORDS = 50    # Minimum word count for meaningful venue content
MIN_LISTING_CHARS = 200   # Minimum chars for a listing-site scrape to be kept

EXCLUDE_PATTERNS = [
    'sitemap.xml', '/blog/', '/news/', '/press', '/presse',
    '/tag/', '/category/', '/author/', '/cart', '/checkout',
    '/login', '/account', '/privacy', '/terms', '/legal', '/cookie'
]

PRIORITY_KEYWORDS = [
    'wedding', 'mariage', 'accommodation', 'hébergement', 'room', 'chambre',
    'rental', 'location', 'seminar', 'séminaire', 'activities', 'activités',
    'contact', 'pricing', 'tarif', 'gallery', 'galerie', 'event', 'événement'
]

LISTING_SITES = [
    {'arg_index': 2, 'label': '**ChateauBee**', 'short': 'CB'},
    {'arg_index': 3, 'label': '**WedInspire**', 'short': 'WI'},
    {'arg_index': 4, 'label': '**French Wedding Venues**', 'short': 'FWV'},
]

FORM_FIELD_KEYWORDS = [
    'this field is required', 'first name', 'last name', 'phone number',
    'your message', 'send message', 'submit', 'captcha', 'recaptcha',
    'required field', 'champ requis', 'champ obligatoire',
    'nom de famille', 'prénom', 'numéro de téléphone', 'votre message',
    'envoyer', 'soumettre', 'join now', 'send a follow-up',
    'venue id', 'venue title', 'venue slug', 'venue full url',
    'user ip country', 'flexible on dates',
]

FORM_DROPDOWN_RE = re.compile(
    r'^(\d+\s*[-–]\s*\d+\s*(guests?|invités?|personnes?))|'
    r'^(not sure)|'
    r'^(january|february|march|april|may|june|july|august|september|october|november|december|'
    r'janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)$',
    re.IGNORECASE
)

UI_NOISE_WORDS = {
    'menu', 'close', 'search', 'en', 'fr', 'es', 'de', 'it',
    'reserve', 'book', 'read more', 'read less', 'voir plus',
    'voir moins', 'lire la suite', 'back', 'retour', 'next',
    'previous', 'suivant', 'précédent', 'open', 'ouvrir',
    'fermer', 'share', 'partager', 'print', 'imprimer',
    'i get it', 'i refuse', "j'accepte", 'je refuse',
    'got it', 'dismiss', 'subscribe', 'newsletter',
    'toggle navigation', 'toggle menu', 'we value your privacy',
    'number of guests', 'wedding month', 'year',
    "i'm flexible on dates",
}


# ─── HTTP Helper ─────────────────────────────────────────────────

def api_request(url, data=None, headers=None, method='GET'):
    """Make HTTP request. Returns (status_code, parsed_response)."""
    if headers is None:
        headers = {}
    body = None
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            error_body = e.read().decode('utf-8')
        except Exception:
            error_body = str(e)
        return e.code, error_body
    except urllib.error.URLError as e:
        return 0, f"Network error: {e.reason}"
    except Exception as e:
        return 0, f"Error: {str(e)}"


def firecrawl_headers(key):
    return {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}


def airtable_headers(key):
    return {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}


# ─── Geocoding ───────────────────────────────────────────────────

NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search'
NOMINATIM_HEADERS = {'User-Agent': 'FWSVenueGeocoder/1.0'}


def geocode_address(address):
    """Geocode an address using OpenStreetMap Nominatim. Returns (lat, lon) or (None, None)."""
    # Append France if not already present for better accuracy
    addr = address.strip()
    if 'france' not in addr.lower():
        addr = f"{addr}, France"

    params = urllib.parse.urlencode({'q': addr, 'format': 'json', 'limit': '1'})
    url = f'{NOMINATIM_URL}?{params}'

    status, resp = api_request(url, headers=NOMINATIM_HEADERS, method='GET')

    if status == 200 and isinstance(resp, list) and len(resp) > 0:
        lat = resp[0].get('lat')
        lon = resp[0].get('lon')
        if lat and lon:
            return float(lat), float(lon)
    return None, None


# ─── Stage 1: Map & Scrape ──────────────────────────────────────

def map_venue(venue_url, fc_key):
    """Discover all pages on the venue site via Firecrawl /v2/map."""
    status, resp = api_request(
        'https://api.firecrawl.dev/v2/map',
        data={'url': venue_url},
        headers=firecrawl_headers(fc_key),
        method='POST'
    )
    if status == 429:
        log("Rate limited on map, waiting 30s...")
        time.sleep(30)
        status, resp = api_request(
            'https://api.firecrawl.dev/v2/map',
            data={'url': venue_url},
            headers=firecrawl_headers(fc_key),
            method='POST'
        )
    if status != 200 or not isinstance(resp, dict) or not resp.get('success'):
        return None, status
    links = resp.get('links', [])
    if not links:
        return [], status
    return links, status


def filter_urls(links, venue_url):
    """Filter discovered URLs: exclude patterns, prefer English, cap at MAX_PAGES."""
    if not links:
        return [venue_url]

    # Normalize: links can be strings or dicts
    urls = []
    for link in links:
        if isinstance(link, str):
            urls.append(link)
        elif isinstance(link, dict):
            urls.append(link.get('url', ''))

    # Remove excluded patterns
    filtered = []
    for url in urls:
        url_lower = url.lower()
        if any(pat in url_lower for pat in EXCLUDE_PATTERNS):
            continue
        filtered.append(url)

    # Deduplicate French/English: if both /fr/ and /en/ versions exist, prefer /en/
    en_urls = set()
    fr_urls = set()
    for url in filtered:
        url_lower = url.lower()
        if '/en/' in url_lower or '/english/' in url_lower:
            en_urls.add(url)
        elif '/fr/' in url_lower or '/french/' in url_lower:
            fr_urls.add(url)

    if en_urls and fr_urls:
        # Remove French URLs that have English equivalents
        fr_stems = {}
        for url in fr_urls:
            stem = re.sub(r'/fr/|/french/', '/LANG/', url.lower())
            fr_stems[stem] = url
        en_stems = set()
        for url in en_urls:
            stem = re.sub(r'/en/|/english/', '/LANG/', url.lower())
            en_stems.add(stem)
        duplicated_fr = [fr_stems[s] for s in fr_stems if s in en_stems]
        filtered = [u for u in filtered if u not in duplicated_fr]

    # Ensure venue_url is first
    venue_url_normalized = venue_url.rstrip('/')
    filtered_normalized = {u.rstrip('/'): u for u in filtered}
    if venue_url_normalized in filtered_normalized:
        venue_entry = filtered_normalized[venue_url_normalized]
        filtered.remove(venue_entry)
        filtered.insert(0, venue_entry)
    elif venue_url not in filtered:
        filtered.insert(0, venue_url)

    # Prioritize pages with relevant keywords (move them to front, after venue_url)
    def priority_score(url):
        url_lower = url.lower()
        return sum(1 for kw in PRIORITY_KEYWORDS if kw in url_lower)

    if len(filtered) > 1:
        first = filtered[0]
        rest = sorted(filtered[1:], key=priority_score, reverse=True)
        filtered = [first] + rest

    return filtered[:MAX_PAGES]


def scrape_page(url, fc_key):
    """Scrape a single page via Firecrawl /v2/scrape. Returns markdown or None."""
    payload = {
        'url': url,
        'formats': ['markdown'],
        'onlyMainContent': False,
        'timeout': 120000,
        'waitFor': 8000,
    }
    status, resp = api_request(
        'https://api.firecrawl.dev/v2/scrape',
        data=payload,
        headers=firecrawl_headers(fc_key),
        method='POST'
    )
    if status == 429:
        log("Rate limited on scrape, waiting 30s...")
        time.sleep(30)
        status, resp = api_request(
            'https://api.firecrawl.dev/v2/scrape',
            data=payload,
            headers=firecrawl_headers(fc_key),
            method='POST'
        )
    if status in (408, 504) or status >= 500:
        log(f"  Retrying {url} after error {status}...")
        time.sleep(5)
        status, resp = api_request(
            'https://api.firecrawl.dev/v2/scrape',
            data=payload,
            headers=firecrawl_headers(fc_key),
            method='POST'
        )
    if status != 200 or not isinstance(resp, dict) or not resp.get('success'):
        return None
    md = resp.get('data', {}).get('markdown', '')
    return md if md and md.strip() else None


def scrape_venue_pages(venue_url, fc_key):
    """Full map+scrape pipeline for the venue website. Returns (combined_markdown, page_count) or (None, reason)."""
    # Step 1: Map
    links, map_status = map_venue(venue_url, fc_key)

    if links is None:
        # Map failed — fall back to single-page scrape
        log(f"  Map failed ({map_status}), falling back to single scrape")
        links = [venue_url]

    if not links:
        links = [venue_url]

    # Step 2: Filter
    filtered = filter_urls(links, venue_url)
    log(f"  Scraping {len(filtered)} pages...")

    # Step 3: Scrape each page
    parts = []
    for i, url in enumerate(filtered):
        md = scrape_page(url, fc_key)
        if md:
            parts.append(f"## Page: {url}\n\n{md.strip()}")
        if i < len(filtered) - 1:
            time.sleep(RATE_LIMIT_DELAY)

    if not parts:
        return None, "Empty content returned"

    combined = '\n\n---\n\n'.join(parts)
    return combined, len(parts)


# ─── Stage 2: Clean (Noise Removal) ─────────────────────────────

def _remove_cookie_blocks(lines, cookie_keywords):
    """Remove all contiguous cookie consent blocks from lines (any position)."""
    result = []
    i = 0
    while i < len(lines):
        lower = lines[i].lower().strip()
        if any(kw in lower for kw in cookie_keywords):
            block_start = i
            block_end = i
            gap = 0
            j = i + 1
            while j < len(lines):
                jlower = lines[j].lower().strip()
                if any(kw in jlower for kw in cookie_keywords):
                    block_end = j
                    gap = 0
                elif lines[j].strip() == '':
                    gap += 1
                    if gap > 2:
                        break
                else:
                    gap += 1
                    if gap > 2:
                        break
                j += 1
            cookie_line_count = sum(
                1 for k in range(block_start, block_end + 1)
                if any(kw in lines[k].lower().strip() for kw in cookie_keywords)
            )
            if cookie_line_count >= 3:
                i = block_end + 1
                while i < len(lines) and lines[i].strip() == '':
                    i += 1
                continue
            else:
                result.append(lines[i])
                i += 1
        else:
            result.append(lines[i])
            i += 1
    return result


def _remove_nav_menu_blocks(text):
    """Remove repeated nav menu blocks (lists of short links appearing on every page)."""
    # Match blocks of 5+ consecutive nav-style link lines: - [Text](url) or [Text](url)
    nav_block_re = re.compile(
        r'(?:^[ \t]*[-*]?\s*\[.{1,40}\]\([^)]+\)\s*\n){5,}',
        re.MULTILINE
    )
    return nav_block_re.sub('\n', text)


def _remove_footer_boilerplate(text):
    """Remove footer blocks: Contact us + phone + email + address + Follow us + copyright."""
    # Match "Contact" header followed by phone/email/address/social within 15 lines
    footer_re = re.compile(
        r'^#{1,4}\s*Contact.*?\n'
        r'(?:.*?\n){0,15}?'
        r'(?:©|copyright|all rights reserved|tous droits).*$',
        re.MULTILINE | re.IGNORECASE
    )
    return footer_re.sub('', text)


def _remove_cookie_detail_tables(text):
    """Remove cookie detail tables with cookie names, durations, tracker descriptions."""
    cookie_table_re = re.compile(
        r'\|[^\n]*(?:_gcl_au|_ga_|_ga|_fbp|_gid|CookieLawInfo|cookielawinfo|PHPSESSID)[^\n]*\|',
        re.IGNORECASE
    )
    lines = text.split('\n')
    # If we find a cookie detail table, remove the entire table (header + separator + rows)
    result = []
    in_cookie_table = False
    for line in lines:
        if cookie_table_re.search(line):
            in_cookie_table = True
            continue
        if in_cookie_table:
            if line.strip().startswith('|') or line.strip() == '' or re.match(r'^[\s|:-]+$', line.strip()):
                continue
            else:
                in_cookie_table = False
        result.append(line)
    return '\n'.join(result)


def clean_markdown(text):
    """Strip website junk from raw markdown."""

    # --- Pre-pass: remove structural noise blocks before line-by-line ---
    text = _remove_nav_menu_blocks(text)
    text = _remove_footer_boilerplate(text)
    text = _remove_cookie_detail_tables(text)

    lines = text.split('\n')

    # --- Cookie consent banners (multi-pass, any position) ---
    cookie_keywords = [
        'cookie', 'consent', 'gdpr', 'privacy policy', 'accepter', 'rejeter',
        'nous respectons votre vie', 'we use cookies', 'nous utilisons des cookies',
        'sauvegarder mes', 'personnaliser', 'always active', 'toujours actif',
        'cookie-law-info', 'accept all', 'accepter tout', 'reject all',
        'analytics', 'fonctionnels', 'publicit', 'performance',
        'pas de cookies', 'no cookies to display'
    ]

    lines = _remove_cookie_blocks(lines, cookie_keywords)

    # --- Booking engine widgets ---
    booking_keywords = [
        'arrival', 'departure', 'check-in', 'check-out', 'checkin', 'checkout',
        'number of adults', 'number of guests', 'select date', 'book now',
        'book your stay', 'availability', 'réserver', 'arrivée', 'départ',
        "nombre d'adultes", 'rechercher', 'vérifier la disponibilité',
        'check availability', 'select room', 'adults', 'children',
        'promo code', 'discount code', 'best rate'
    ]

    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()

        # Skip empty lines (kept, but don't apply filters)
        if not stripped:
            cleaned_lines.append(line)
            continue

        # Navigation noise: sequences of short links
        if re.match(r'^(\[.{1,20}\]\([^)]+\)\s*\|\s*){2,}', stripped):
            continue

        # "Skip to content" links
        if re.match(r'^\[?(go to |skip to |aller au |passer au )?(main )?content\]?', lower):
            continue

        # Short UI/navigation text (exact match)
        if lower in UI_NOISE_WORDS:
            continue

        # Bare language-switcher links: [en](...) [fr](...) etc.
        if re.match(r'^\[?(en|fr|es|de|it|nl|pt)\]?\s*(\(.*?\))?\s*$', stripped, re.IGNORECASE):
            continue

        # Booking widget controls (short lines only)
        if any(kw in lower for kw in booking_keywords) and len(stripped) < 120:
            continue

        # Contact form fields and labels (short lines only)
        if any(kw in lower for kw in FORM_FIELD_KEYWORDS) and len(stripped) < 80:
            continue

        # Form dropdown options (month names, guest ranges)
        if FORM_DROPDOWN_RE.match(stripped):
            continue

        # SVG data URI images (lazy-load placeholders)
        if 'data:image/svg+xml' in stripped:
            continue

        # Image-only lines (including list-item images)
        if re.match(r'^[-*]?\s*!\[.*?\]\(.*?\)$', stripped) and not re.search(r'[a-zA-Z]{5,}', stripped.split('](')[0]):
            continue

        # Random hex hash strings (form tokens)
        if re.match(r'^[0-9a-f]{16,}$', stripped):
            continue

        # reCAPTCHA and Google privacy/terms boilerplate
        if 'recaptcha' in lower and len(stripped) < 200:
            continue
        if re.match(r'^\[privacy\].*\[terms\]', stripped, re.IGNORECASE):
            continue

        # Cookie consent UI remnants
        if re.match(r'^\[?(manage|gérer)\s+(options|services|consent|cookies|vendors)', lower):
            continue
        if lower in ('gérer le consentement', 'gérer le consentement aux cookies', 'manage consent'):
            continue

        # Long cookie notice paragraphs (single-line blocks that slip past multi-pass)
        if 'cookie' in lower and len(stripped) > 80 and any(
            p in lower for p in ['function properly', 'we use cookies', 'consent',
                                  'nous utilisons', 'fonctionner correctement']
        ):
            continue

        # Placeholder / empty gallery text
        if lower in ('sorry, we have no imagery here.', 'sorry, we have no imagery here',
                      'no imagery available', 'no image available'):
            continue

        # Keyboard shortcut tables (map widgets)
        if re.match(r'^`[←→↑↓\+\-]`$', stripped) or lower in (
            'move left', 'move right', 'move up', 'move down',
            'zoom in', 'zoom out', 'jump left by 75%', 'jump right by 75%',
            'jump up by 75%', 'jump down by 75%', 'keyboard shortcuts',
        ):
            continue

        # Map data attribution strings
        if re.match(r'^map\s*data', lower) or 'geobasis' in lower or 'map data ©' in lower:
            continue

        # Footer boilerplate (short lines only)
        if any(p in lower for p in [
            'all rights reserved', 'tous droits', '© ', 'copyright',
            'follow us on', 'suivez-nous'
        ]) and len(stripped) < 200:
            continue

        # Social media link lists
        if re.match(r'^(\[?(facebook|twitter|instagram|linkedin|youtube|pinterest|tiktok)\]?\s*[\|/,]\s*){2,}', stripped, re.IGNORECASE):
            continue

        # Directory-site boilerplate CTAs
        if lower in (
            'enquire today', 'handpicked for you', 'no added commission',
            'enquire now', 'send enquiry', 'request a quote',
            'similar venues', 'you may also like', 'related venues',
            'other venues nearby', 'more venues in this region',
        ):
            continue

        # Related venue listing blocks (venue name + region + guest count from listing sites)
        if re.match(r'^.{5,60}\s*[-–|]\s*(south of france|provence|languedoc|dordogne|loire|normandy|brittany|bordeaux|champagne|burgundy)', lower):
            continue

        # Instagram link numbers (bare numbers linking to instagram)
        if re.match(r'^\[?\d{1,4}\]?\s*$', stripped) and 'instagram' in line.lower():
            continue

        # Agency credits / website creation
        if any(p in lower for p in [
            'création site internet', 'création site web', 'web design by',
            'designed by', 'powered by', 'website by', 'site réalisé par',
            'agence web', 'made with love'
        ]) and len(stripped) < 150:
            continue

        cleaned_lines.append(line)

    result = '\n'.join(cleaned_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip()


# ─── Stage 3: Categorize (No-Deletion Policy) ───────────────────

CATEGORIES = [
    {
        'header': 'Overview & History',
        'keywords': [
            'history', 'histoire', 'built in', 'construit', 'century', 'siècle',
            'château', 'chateau', 'manor', 'manoir', 'estate', 'domaine',
            'heritage', 'patrimoine', 'architecture', 'style', 'duke', 'duc',
            'founded', 'fondé', 'restored', 'restauré', 'tradition',
            'about us', 'à propos', 'our story', 'notre histoire', 'welcome',
            'bienvenue', 'family', 'famille', 'generation', 'génération',
            'listed', 'classé', 'monument', 'historic', 'historique'
        ]
    },
    {
        'header': 'Event Logistics',
        'keywords': [
            'event', 'événement', 'wedding', 'mariage', 'reception', 'réception',
            'ceremony', 'cérémonie', 'seated', 'assises', 'cocktail', 'standing',
            'debout', 'capacity', 'capacité', 'catering', 'traiteur', 'tent',
            'chapiteau', 'marquee', 'vendor', 'prestataire', 'dj', 'music',
            'musique', 'dance floor', 'piste de danse', 'celebration',
            'banquet', 'dinner', 'dîner', 'lunch', 'déjeuner', 'buffet',
            'seminar', 'séminaire', 'conference', 'corporate', 'entreprise',
            'party', 'fête', 'guests', 'invités', 'fireworks', "feu d'artifice"
        ]
    },
    {
        'header': 'Accommodation Breakdown',
        'keywords': [
            'room', 'chambre', 'suite', 'gîte', 'gite', 'cottage', 'bed',
            'lit', 'bedroom', 'double', 'twin', 'single', 'king', 'queen',
            'sleep', 'coucher', 'accommodation', 'hébergement', 'lodging',
            'guest house', 'maison', 'apartment', 'appartement', 'studio',
            'occupancy', 'capacity', 'bathroom', 'salle de bain', 'shower',
            'douche', 'en-suite', 'overnight', 'nuit', 'stay', 'séjour',
            'person', 'personne', 'people', 'personnes'
        ]
    },
    {
        'header': 'Amenities & Facilities',
        'keywords': [
            'pool', 'piscine', 'tennis', 'spa', 'sauna', 'jacuzzi',
            'garden', 'jardin', 'park', 'parc', 'hectare', 'acre',
            'wifi', 'wi-fi', 'internet', 'parking', 'nespresso', 'coffee',
            'café', 'kitchen', 'cuisine', 'terrace', 'terrasse', 'balcony',
            'balcon', 'air conditioning', 'climatisation', 'heating',
            'chauffage', 'fireplace', 'cheminée', 'gym', 'fitness',
            'playground', 'aire de jeux', 'lake', 'lac', 'river', 'rivière',
            'forest', 'forêt', 'vineyard', 'vignoble', 'wine', 'vin',
            'bar', 'lounge', 'salon', 'library', 'bibliothèque',
            'chapel', 'chapelle', 'orangery', 'orangerie'
        ]
    },
    {
        'header': 'Travel & Contact',
        'keywords': [
            'address', 'adresse', 'contact', 'phone', 'téléphone', 'email',
            'direction', 'how to get', 'comment venir', 'access', 'accès',
            'airport', 'aéroport', 'train', 'gare', 'station', 'highway',
            'autoroute', 'km', 'miles', 'hours from', 'heures de', 'minutes',
            'paris', 'lyon', 'marseille', 'bordeaux', 'toulouse', 'nice',
            'gps', 'coordinates', 'coordonnées', 'map', 'carte', 'location',
            'localisation', 'taxi', 'shuttle', 'navette', 'transfer',
            'transfert', 'nearest', 'plus proche'
        ]
    }
]


def categorize_content(cleaned_text):
    """Categorize cleaned content into structured sections. No-Deletion Policy."""
    lines = cleaned_text.split('\n')

    blocks = []
    current_block = []
    for line in lines:
        if re.match(r'^#{1,3}\s', line):
            if current_block:
                blocks.append('\n'.join(current_block))
                current_block = []
        current_block.append(line)
    if current_block:
        blocks.append('\n'.join(current_block))

    categorized = {cat['header']: [] for cat in CATEGORIES}
    uncategorized = []

    for block in blocks:
        block_lower = block.lower()
        best_category = None
        best_score = 0
        for cat in CATEGORIES:
            score = sum(1 for kw in cat['keywords'] if kw in block_lower)
            if score > best_score:
                best_score = score
                best_category = cat['header']
        if best_category and best_score >= 1:
            categorized[best_category].append(block)
        else:
            uncategorized.append(block)

    output_parts = []
    for cat in CATEGORIES:
        header = cat['header']
        if categorized[header]:
            output_parts.append(f"## {header}\n")
            output_parts.append('\n\n'.join(categorized[header]))
            output_parts.append('')

    if uncategorized:
        output_parts.append("## Additional Information\n")
        output_parts.append('\n\n'.join(uncategorized))
        output_parts.append('')

    result = '\n\n'.join(output_parts)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip()


# ─── Stage 4: Truncation ────────────────────────────────────────

def truncate_content(text):
    """Truncate to MAX_CHARS at last complete paragraph."""
    if len(text) <= MAX_CHARS:
        return text, False
    truncated = text[:MAX_CHARS]
    last_break = truncated.rfind('\n\n')
    if last_break > MAX_CHARS * 0.5:
        truncated = truncated[:last_break]
    truncated += '\n\n[Content truncated at 95,000 characters]'
    return truncated, True


# ─── Airtable Helpers ───────────────────────────────────────────

def write_manual_check(record_id, reason, at_key, base_id):
    """Write MANUAL_CHECK marker to Airtable."""
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    marker = f"MANUAL_CHECK -- {reason} -- {timestamp}"
    url = f'https://api.airtable.com/v0/{base_id}/Venues/{record_id}'
    api_request(url, data={'fields': {'venue_url_scraped': marker}},
                headers=airtable_headers(at_key), method='PATCH')
    print(f"MANUAL_CHECK|{reason}|0")


def write_to_airtable(record_id, content, at_key, base_id):
    """PATCH venue_url_scraped to Airtable. Returns True on success."""
    payload = {'fields': {'venue_url_scraped': content}}

    # Also write payload to file for debugging
    os.makedirs(WORKING_DIR, exist_ok=True)
    with open(PAYLOAD_PATH, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)

    url = f'https://api.airtable.com/v0/{base_id}/Venues/{record_id}'
    status, _ = api_request(url, data=payload, headers=airtable_headers(at_key), method='PATCH')
    return status == 200


# ─── Logging ────────────────────────────────────────────────────

def log(msg):
    """Log to stderr (visible in terminal but not captured as script output)."""
    print(msg, file=sys.stderr)


# ─── Main ───────────────────────────────────────────────────────

def main():
    # ── --write-file mode: read structured file, write to Airtable, delete temps ──
    if '--write-file' in sys.argv:
        # Usage: python process_venue.py --write-file <record_id> <structured_file> <airtable_key> <base_id>
        args = [a for a in sys.argv if a != '--write-file']
        if len(args) < 5:
            print("ERROR|Usage: python process_venue.py --write-file <record_id> <structured_file> <airtable_key> <base_id>")
            sys.exit(1)
        record_id = args[1]
        structured_file = args[2]
        at_key = args[3]
        base_id = args[4]

        if not os.path.exists(structured_file):
            print(f"ERROR|File not found: {structured_file}|0")
            sys.exit(1)

        with open(structured_file, 'r', encoding='utf-8') as f:
            content = f.read()

        char_count = len(content)
        success = write_to_airtable(record_id, content, at_key, base_id)

        if success:
            # Clean up temp files
            os.remove(structured_file)
            raw_path = os.path.join(WORKING_DIR, f'raw_{record_id}.md')
            if os.path.exists(raw_path):
                os.remove(raw_path)
            for short in ['CB', 'WI', 'FWV']:
                listing_path = os.path.join(WORKING_DIR, f'listing_{record_id}_{short}.md')
                if os.path.exists(listing_path):
                    os.remove(listing_path)
            print(f"WRITTEN|{char_count}")
        else:
            print(f"AIRTABLE_ERROR|PATCH failed|{char_count}")
            sys.exit(1)
        return

    # ── --geocode mode: geocode venue address, write GPS to Airtable ──
    if '--geocode' in sys.argv:
        # Usage: python process_venue.py --geocode <record_id> <venue_address> <airtable_key> <base_id>
        args = [a for a in sys.argv if a != '--geocode']
        if len(args) < 5:
            print("ERROR|Usage: python process_venue.py --geocode <record_id> <venue_address> <airtable_key> <base_id>")
            sys.exit(1)
        record_id = args[1]
        venue_address = args[2]
        at_key = args[3]
        base_id = args[4]

        if not venue_address.strip():
            print("GEOCODE_SKIP|no address")
            return

        log(f"Geocoding: {venue_address}")
        lat, lon = geocode_address(venue_address)

        if lat is None or lon is None:
            print(f"GEOCODE_FAIL|no results for: {venue_address}")
            return

        # Write to Airtable gps_coordinates field as "lat, lon"
        coords = f"{lat}, {lon}"
        url = f'https://api.airtable.com/v0/{base_id}/Venues/{record_id}'
        status, _ = api_request(
            url,
            data={'fields': {'gps_coordinates': coords}},
            headers=airtable_headers(at_key),
            method='PATCH'
        )
        if status == 200:
            print(f"GEOCODED|{lat},{lon}")
        else:
            print(f"GEOCODE_FAIL|Airtable PATCH failed ({status})")
        return

    # ── --write-json mode: write full + summary JSON files to Airtable ──
    if '--write-json' in sys.argv:
        # Usage: python process_venue.py --write-json <record_id> <full_json_path> <summary_json_path> <airtable_key> <base_id>
        args = [a for a in sys.argv if a != '--write-json']
        if len(args) < 6:
            print("ERROR|Usage: python process_venue.py --write-json <record_id> <full_json_path> <summary_json_path> <airtable_key> <base_id>")
            sys.exit(1)
        record_id = args[1]
        full_json_path = args[2]
        summary_json_path = args[3]
        at_key = args[4]
        base_id = args[5]

        # Read full JSON
        if not os.path.exists(full_json_path):
            print(f"ERROR|Full JSON not found: {full_json_path}|0")
            sys.exit(1)
        with open(full_json_path, 'r', encoding='utf-8') as f:
            full_json = f.read()

        # Read summary JSON
        if not os.path.exists(summary_json_path):
            print(f"ERROR|Summary JSON not found: {summary_json_path}|0")
            sys.exit(1)
        with open(summary_json_path, 'r', encoding='utf-8') as f:
            summary_json = f.read()

        # PATCH both fields to Airtable in a single request
        url = f'https://api.airtable.com/v0/{base_id}/Venues/{record_id}'
        payload = {
            'fields': {
                'full_venue_json': full_json,
                'summary_venue_json': summary_json
            }
        }
        status, resp = api_request(url, data=payload, headers=airtable_headers(at_key), method='PATCH')

        if status == 200:
            print(f"JSON_WRITTEN|{len(full_json)}|{len(summary_json)}")
        else:
            print(f"AIRTABLE_ERROR|JSON PATCH failed ({status})|{len(full_json)}+{len(summary_json)}")
            sys.exit(1)
        return

    # ── --fetch-json-sources mode: download venue_url_scraped + brochure_text to temp files ──
    if '--fetch-json-sources' in sys.argv:
        # Usage: python process_venue.py --fetch-json-sources <record_id> <venue_name> <airtable_key> <base_id>
        args = [a for a in sys.argv if a != '--fetch-json-sources']
        if len(args) < 5:
            print("ERROR|Usage: python process_venue.py --fetch-json-sources <record_id> <venue_name> <airtable_key> <base_id>")
            sys.exit(1)
        record_id = args[1]
        venue_name = args[2]
        at_key = args[3]
        base_id = args[4]

        log(f"Fetching JSON sources for: {venue_name} ({record_id})")

        # Fetch the record from Airtable (single-record GET doesn't support fields[] filter)
        url = f'https://api.airtable.com/v0/{base_id}/Venues/{record_id}'
        status, resp = api_request(url, headers=airtable_headers(at_key), method='GET')

        if status != 200:
            print(f"FETCH_ERROR|Airtable GET failed ({status})")
            sys.exit(1)

        fields = resp.get('fields', {}) if isinstance(resp, dict) else {}
        scraped = fields.get('venue_url_scraped', '')
        brochure = fields.get('brochure_text', '')

        # Validate: scraped content must exist and not be a manual-check marker
        if not scraped or not scraped.strip():
            print("NO_CONTENT|venue_url_scraped is empty")
            return
        if scraped.strip().startswith('MANUAL_CHECK'):
            print("NO_CONTENT|venue_url_scraped contains MANUAL_CHECK marker")
            return

        os.makedirs(WORKING_DIR, exist_ok=True)

        # Save scraped content
        scraped_path = os.path.join(WORKING_DIR, f'scraped_{record_id}.md')
        with open(scraped_path, 'w', encoding='utf-8') as f:
            f.write(scraped)

        # Save brochure content (only if non-empty and not an error marker)
        brochure_chars = 0
        if brochure and brochure.strip() and not brochure.strip().startswith('[ERROR]'):
            brochure_path = os.path.join(WORKING_DIR, f'brochure_{record_id}.md')
            with open(brochure_path, 'w', encoding='utf-8') as f:
                f.write(brochure)
            brochure_chars = len(brochure)

        print(f"FETCHED|{len(scraped)}|{brochure_chars}")
        return

    # Parse optional flags
    scrape_only = '--scrape-only' in sys.argv
    args = [a for a in sys.argv if a != '--scrape-only']

    if len(args) < 9:
        print("ERROR|Usage: python process_venue.py [--scrape-only] <record_id> <venue_url> <chateaubee_url> <wedinspire_url> <fwv_url> <firecrawl_key> <airtable_key> <base_id>")
        sys.exit(1)

    record_id = args[1]
    venue_url = args[2]
    listing_urls = {
        'CB': args[3] if args[3] else '',
        'WI': args[4] if args[4] else '',
        'FWV': args[5] if args[5] else '',
    }
    fc_key = args[6]
    at_key = args[7]
    base_id = args[8]

    mode_label = "Scraping" if scrape_only else "Processing"
    log(f"{mode_label} {venue_url} ...")

    # ── Part 1: Venue Website (mandatory, multi-page) ──

    result, info = scrape_venue_pages(venue_url, fc_key)

    if result is None:
        write_manual_check(record_id, info, at_key, base_id)
        return

    venue_pages = info  # page count
    cleaned_venue = clean_markdown(result)

    if not cleaned_venue.strip():
        write_manual_check(record_id, "Empty content after cleaning", at_key, base_id)
        return

    venue_char_count = len(cleaned_venue.strip())
    venue_word_count = len(cleaned_venue.split())
    if venue_char_count < MIN_CONTENT_CHARS or venue_word_count < MIN_CONTENT_WORDS:
        write_manual_check(
            record_id,
            f"Low quality content ({venue_char_count} chars, {venue_word_count} words)",
            at_key, base_id
        )
        return

    # ── Part 2: Listing Sites (optional, single-page) ──

    listing_results = {}
    sources = ['Venue']
    listing_count = 0

    for short, url in listing_urls.items():
        if not url.strip():
            continue

        log(f"  Scraping listing: {short} ({url})")
        time.sleep(RATE_LIMIT_DELAY)
        md = scrape_page(url, fc_key)

        if md:
            cleaned = clean_markdown(md)
            if cleaned.strip() and len(cleaned.strip()) >= MIN_LISTING_CHARS:
                listing_results[short] = cleaned
                sources.append(short)
                listing_count += 1
                log(f"  {short}: OK ({len(cleaned)} chars)")
            else:
                log(f"  {short}: empty or too short after cleaning, skipping")
        else:
            log(f"  {short}: scrape failed, skipping")

    # ── Part 3: Output ──

    if scrape_only:
        # Save raw cleaned content to temp files for Claude to structure
        os.makedirs(WORKING_DIR, exist_ok=True)

        raw_path = os.path.join(WORKING_DIR, f'raw_{record_id}.md')
        with open(raw_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_venue)

        for short in ['CB', 'WI', 'FWV']:
            if short in listing_results:
                listing_path = os.path.join(WORKING_DIR, f'listing_{record_id}_{short}.md')
                with open(listing_path, 'w', encoding='utf-8') as f:
                    f.write(listing_results[short])

        sources_csv = ','.join(sources)
        listing_chars = sum(len(v) for v in listing_results.values())
        print(f"SCRAPED|{venue_char_count}|{venue_pages}+{listing_count}|{sources_csv}|{listing_chars}")
        return

    # Full pipeline mode: categorize + combine + write to Airtable
    categorized_venue = categorize_content(cleaned_venue)

    label_map = {'CB': '**ChateauBee**', 'WI': '**WedInspire**', 'FWV': '**French Wedding Venues**'}
    parts = [f"**Venue Website**\n\n{categorized_venue}"]

    for short in ['CB', 'WI', 'FWV']:
        if short in listing_results:
            label = label_map[short]
            parts.append(f"{label}\n\n{listing_results[short]}")

    combined = '\n\n---\n\n'.join(parts)
    final, was_truncated = truncate_content(combined)

    # Write to Airtable
    success = write_to_airtable(record_id, final, at_key, base_id)

    if success:
        char_count = len(final)
        trunc_note = " Truncated" if was_truncated else ""
        sources_csv = ','.join(sources)
        print(f"SUCCESS|{char_count}|{venue_pages}+{listing_count}|{sources_csv}{trunc_note}")
    else:
        print(f"AIRTABLE_ERROR|PATCH failed|0")


if __name__ == '__main__':
    main()
