"""
Batch geocode venue addresses from Airtable.

Queries Airtable for venues with a venue_address but no gps_coordinates,
geocodes each via OpenStreetMap Nominatim, and writes "lat, lon" back.

Usage:
  python scripts/batch_geocode.py
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

# ─── Configuration ───────────────────────────────────────────────
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = "appFQYNRTuooIRZZz"
AIRTABLE_TABLE = "Venues"

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_HEADERS = {"User-Agent": "FWSVenueGeocoder/1.0"}

RATE_LIMIT_DELAY = 1.1  # seconds between Nominatim calls


# ─── HTTP Helper ─────────────────────────────────────────────────

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


def airtable_headers():
    return {"Authorization": f"Bearer {AIRTABLE_API_KEY}", "Content-Type": "application/json"}


# ─── Geocoding ───────────────────────────────────────────────────

def geocode_address(address):
    """Geocode an address using OpenStreetMap Nominatim. Returns (lat, lon) or (None, None)."""
    addr = address.strip()
    if "france" not in addr.lower():
        addr = f"{addr}, France"

    params = urllib.parse.urlencode({"q": addr, "format": "json", "limit": "1"})
    url = f"{NOMINATIM_URL}?{params}"

    status, resp = api_request(url, headers=NOMINATIM_HEADERS, method="GET")

    if status == 200 and isinstance(resp, list) and len(resp) > 0:
        lat = resp[0].get("lat")
        lon = resp[0].get("lon")
        if lat and lon:
            return float(lat), float(lon)
    return None, None


# ─── Airtable ────────────────────────────────────────────────────

def fetch_venues_missing_gps():
    """Fetch all venue records that have an address but no GPS coordinates."""
    records = []
    offset = None
    formula = "AND({venue_address} != '', {gps_coordinates} = '')"

    while True:
        params = {
            "filterByFormula": formula,
            "fields[]": ["venue_address", "venue_name"],
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
            records.append({
                "id": rec["id"],
                "name": rec.get("fields", {}).get("venue_name", "(unnamed)"),
                "address": rec.get("fields", {}).get("venue_address", ""),
            })

        offset = resp.get("offset")
        if not offset:
            break

    return records


def update_gps(record_id, coords_str):
    """Write gps_coordinates to a single Airtable record."""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE}/{record_id}"
    status, _ = api_request(
        url,
        data={"fields": {"gps_coordinates": coords_str}},
        headers=airtable_headers(),
        method="PATCH",
    )
    return status == 200


# ─── Main ────────────────────────────────────────────────────────

def main():
    print("Fetching venues with address but no GPS coordinates...")
    venues = fetch_venues_missing_gps()

    if not venues:
        print("No venues found that need geocoding.")
        return

    print(f"Found {len(venues)} venue(s) to geocode.\n")

    success = 0
    failed = 0
    skipped = 0

    for i, v in enumerate(venues, 1):
        name = v["name"]
        address = v["address"]

        if not address.strip():
            print(f"  [{i}/{len(venues)}] {name} — SKIP (empty address)")
            skipped += 1
            continue

        lat, lon = geocode_address(address)

        if lat is None:
            print(f"  [{i}/{len(venues)}] {name} — FAIL (no results for: {address})")
            failed += 1
        else:
            coords = f"{lat}, {lon}"
            ok = update_gps(v["id"], coords)
            if ok:
                print(f"  [{i}/{len(venues)}] {name} — {coords}")
                success += 1
            else:
                print(f"  [{i}/{len(venues)}] {name} — FAIL (Airtable write error)")
                failed += 1

        # Rate limit for Nominatim (max 1 req/sec)
        if i < len(venues):
            time.sleep(RATE_LIMIT_DELAY)

    print(f"\nDone. Success: {success} | Failed: {failed} | Skipped: {skipped}")


if __name__ == "__main__":
    main()
