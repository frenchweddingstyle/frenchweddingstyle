"""
Batch extract profile image URLs from FWS venue listing pages.

Queries Airtable for venues with an fws_url but no image_url,
fetches each page, extracts the og:image meta tag (or feature_banner_img
fallback), and writes the URL back to image_url.

Usage:
  python scripts/batch_extract_image_urls.py
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

# Fix Windows console encoding
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ─── Configuration ───────────────────────────────────────────────
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = "appFQYNRTuooIRZZz"
AIRTABLE_TABLE = "Venues"

FETCH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) FWSImageExtractor/1.0",
    "Accept": "text/html,application/xhtml+xml",
}

RATE_LIMIT_DELAY = 1.0  # seconds between page fetches


# ─── HTTP Helpers ────────────────────────────────────────────────

def api_request(url, data=None, headers=None, method="GET"):
    """Make HTTP request. Returns (status_code, parsed_response)."""
    if headers is None:
        headers = {}
    body = None
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            error_body = e.read().decode("utf-8")
        except Exception:
            error_body = str(e)
        return e.code, error_body
    except urllib.error.URLError as e:
        return 0, f"Network error: {e.reason}"
    except Exception as e:
        return 0, f"Error: {str(e)}"


def fetch_html(url):
    """Fetch a web page and return the HTML as a string. Returns None on error."""
    req = urllib.request.Request(url, headers=FETCH_HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"    HTTP {e.code} fetching {url}")
        return None
    except urllib.error.URLError as e:
        print(f"    Network error fetching {url}: {e.reason}")
        return None
    except Exception as e:
        print(f"    Error fetching {url}: {e}")
        return None


def airtable_headers():
    return {"Authorization": f"Bearer {AIRTABLE_API_KEY}", "Content-Type": "application/json"}


# ─── Image Extraction ───────────────────────────────────────────

def extract_image_url(html):
    """Extract the profile image URL from FWS venue page HTML.

    Tries og:image meta tag first, then feature_banner_img img src.
    Returns the URL string or None.
    """
    # Strategy 1: og:image meta tag
    # Handles both attribute orderings:
    #   <meta property="og:image" content="URL" />
    #   <meta content="URL" property="og:image" />
    match = re.search(
        r'<meta\s+(?:property=["\']og:image["\']\s+content=["\']([^"\']+)["\']'
        r'|content=["\']([^"\']+)["\']\s+property=["\']og:image["\'])',
        html,
        re.IGNORECASE,
    )
    if match:
        url = match.group(1) or match.group(2)
        if url:
            return url.strip()

    # Strategy 2: feature_banner_img class on an img tag
    match = re.search(
        r'<img\s[^>]*class=["\'][^"\']*feature_banner_img[^"\']*["\'][^>]*src=["\']([^"\']+)["\']',
        html,
        re.IGNORECASE,
    )
    if match:
        return match.group(1).strip()

    # Also try src before class (attribute order can vary)
    match = re.search(
        r'<img\s[^>]*src=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*feature_banner_img[^"\']*["\']',
        html,
        re.IGNORECASE,
    )
    if match:
        return match.group(1).strip()

    return None


# ─── Airtable ────────────────────────────────────────────────────

def fetch_venues_missing_image():
    """Fetch all venue records that have fws_url but no image_url."""
    records = []
    offset = None
    formula = "AND({fws_url} != '', {image_url} = '')"

    while True:
        params = {
            "filterByFormula": formula,
            "fields[]": ["venue_name", "fws_url"],
            "pageSize": "100",
        }
        if offset:
            params["offset"] = offset

        url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE}?{urllib.parse.urlencode(params, doseq=True)}"
        status, resp = api_request(url, headers=airtable_headers(), method="GET")

        if status != 200:
            print(f"ERROR: Airtable query failed ({status}): {resp}")
            sys.exit(1)

        for rec in resp.get("records", []):
            fields = rec.get("fields", {})
            records.append({
                "id": rec["id"],
                "name": fields.get("venue_name", "(unnamed)"),
                "fws_url": fields.get("fws_url", ""),
            })

        offset = resp.get("offset")
        if not offset:
            break

    return records


def update_image_url(record_id, image_url):
    """Write image_url to a single Airtable record."""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE}/{record_id}"
    status, _ = api_request(
        url,
        data={"fields": {"image_url": image_url}},
        headers=airtable_headers(),
        method="PATCH",
    )
    return status == 200


# ─── Main ────────────────────────────────────────────────────────

def main():
    print("Fetching venues with fws_url but no image_url...")
    venues = fetch_venues_missing_image()

    if not venues:
        print("No venues found that need image extraction.")
        return

    print(f"Found {len(venues)} venue(s) to process.\n")

    success = 0
    failed = 0
    skipped = 0

    for i, v in enumerate(venues, 1):
        name = v["name"]
        fws_url = v["fws_url"]

        if not fws_url.strip():
            print(f"  [{i}/{len(venues)}] {name} — SKIP (empty fws_url)")
            skipped += 1
            continue

        print(f"  [{i}/{len(venues)}] {name} — fetching {fws_url}")
        html = fetch_html(fws_url)

        if html is None:
            print(f"    FAIL (could not fetch page)")
            failed += 1
        else:
            image_url = extract_image_url(html)
            if image_url is None:
                print(f"    FAIL (no image found on page)")
                failed += 1
            else:
                ok = update_image_url(v["id"], image_url)
                if ok:
                    print(f"    OK — {image_url}")
                    success += 1
                else:
                    print(f"    FAIL (Airtable write error)")
                    failed += 1

        # Polite crawling delay
        if i < len(venues):
            time.sleep(RATE_LIMIT_DELAY)

    print(f"\nDone. Success: {success} | Failed: {failed} | Skipped: {skipped}")


if __name__ == "__main__":
    main()
