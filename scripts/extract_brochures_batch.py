"""
Batch extract brochure text from Google Drive docs and write to Airtable.
Uses Google Drive API to export docs as plain text, then updates Airtable.
"""
import json
import os
import requests
import re
import time
import sys
import unicodedata

# Configuration
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def requests_get_with_retry(url, **kwargs):
    """Wrapper around requests.get with retry on connection errors."""
    for attempt in range(MAX_RETRIES):
        try:
            return requests.get(url, **kwargs)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt < MAX_RETRIES - 1:
                print(f"\n  [retry {attempt+1}/{MAX_RETRIES} after connection error]", end=" ", flush=True)
                time.sleep(RETRY_DELAY * (attempt + 1))
            else:
                raise
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = "appFQYNRTuooIRZZz"
AIRTABLE_TABLE_ID = "tblIEJQNynXIsD8GL"

TOKEN_FILE = r"C:\Users\LFoul\.config\google-drive-mcp\tokens.json"
CREDS_FILE = r"C:\Users\LFoul\.config\google-drive-creds.json"


def load_tokens():
    with open(TOKEN_FILE) as f:
        return json.load(f)


def load_creds():
    with open(CREDS_FILE) as f:
        return json.load(f)["installed"]


def refresh_access_token():
    tokens = load_tokens()
    creds = load_creds()
    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "refresh_token": tokens["refresh_token"],
        "grant_type": "refresh_token"
    })
    data = resp.json()
    new_token = data.get("access_token")
    if new_token:
        tokens["access_token"] = new_token
        tokens["expiry_date"] = int(time.time() * 1000) + 3500000
        with open(TOKEN_FILE, 'w') as f:
            json.dump(tokens, f, indent=2)
        return new_token
    return None


def get_access_token():
    tokens = load_tokens()
    if tokens.get("expiry_date", 0) < time.time() * 1000 + 60000:
        token = refresh_access_token()
        if token:
            return token
    return tokens["access_token"]


def strip_accents(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def fix_mojibake(s):
    """Fix double-encoded UTF-8 strings."""
    try:
        return s.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return s


def search_google_drive(venue_name, access_token):
    """Search Google Drive for a Google Doc matching the venue name."""
    headers = {"Authorization": f"Bearer {access_token}"}

    # Try to fix mojibake in venue name
    clean_name = fix_mojibake(venue_name)

    # Strategy 1: exact name match
    for search_name in [clean_name, venue_name, strip_accents(clean_name)]:
        escaped = search_name.replace("'", "\\'")
        query = f"name = '{escaped}' and mimeType = 'application/vnd.google-apps.document' and trashed = false"
        params = {"q": query, "fields": "files(id,name)", "pageSize": 5}
        resp = requests_get_with_retry("https://www.googleapis.com/drive/v3/files", headers=headers, params=params)
        if resp.status_code == 200:
            files = resp.json().get("files", [])
            if files:
                return files[0]["id"], files[0]["name"]

    # Strategy 2: name contains (try key words from venue name)
    for search_name in [clean_name, strip_accents(clean_name)]:
        escaped = search_name.replace("'", "\\'")
        query = f"name contains '{escaped}' and mimeType = 'application/vnd.google-apps.document' and trashed = false"
        params = {"q": query, "fields": "files(id,name)", "pageSize": 10}
        resp = requests_get_with_retry("https://www.googleapis.com/drive/v3/files", headers=headers, params=params)
        if resp.status_code == 200:
            files = resp.json().get("files", [])
            # Find best match
            name_lower = clean_name.lower().strip()
            for f in files:
                fname = f["name"].lower().strip()
                if fname == name_lower or name_lower in fname or fname in name_lower:
                    return f["id"], f["name"]
            # If no close match, check if any doc name is similar
            for f in files:
                fname = strip_accents(f["name"].lower().strip())
                sname = strip_accents(name_lower)
                if fname == sname or sname in fname or fname in sname:
                    return f["id"], f["name"]

    # Strategy 3: try shorter name (remove common prefixes)
    short_names = []
    for prefix in ["Chateau ", "Château ", "Domaine ", "Hotel ", "Hôtel ", "Bastide ", "Manoir ", "Abbaye ", "Maison ", "Le ", "La ", "Les "]:
        if clean_name.lower().startswith(prefix.lower()):
            remainder = clean_name[len(prefix):]
            if len(remainder) > 3:
                short_names.append(remainder)

    for short in short_names:
        escaped = short.replace("'", "\\'")
        query = f"name contains '{escaped}' and mimeType = 'application/vnd.google-apps.document' and trashed = false"
        params = {"q": query, "fields": "files(id,name)", "pageSize": 10}
        resp = requests_get_with_retry("https://www.googleapis.com/drive/v3/files", headers=headers, params=params)
        if resp.status_code == 200:
            files = resp.json().get("files", [])
            for f in files:
                fname = f["name"].lower()
                if short.lower() in fname:
                    return f["id"], f["name"]

    return None, None


def export_doc_as_text(doc_id, access_token):
    """Export a Google Doc as plain text via Drive API."""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://www.googleapis.com/drive/v3/files/{doc_id}/export"
    params = {"mimeType": "text/plain"}
    resp = requests_get_with_retry(url, headers=headers, params=params)
    if resp.status_code == 200:
        return resp.text
    return None


def clean_content(text):
    """Clean the exported text content."""
    if not text:
        return None

    # Remove excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove Google Docs export artifacts
    text = re.sub(r'\ufeff', '', text)  # BOM

    # Strip leading/trailing whitespace
    text = text.strip()

    # Truncate at 95,000 chars if needed
    if len(text) > 95000:
        text = text[:95000]
        last_para = text.rfind('\n\n')
        if last_para > 90000:
            text = text[:last_para]
        text += '\n\n[Content truncated at 95,000 characters]'

    return text


def update_airtable(records):
    """Update Airtable records in a batch (max 10)."""
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}"

    payload = {
        "records": [
            {"id": rec["id"], "fields": {"brochure_text": rec["content"]}}
            for rec in records
        ]
    }

    resp = requests.patch(url, headers=headers, json=payload)
    return resp.status_code == 200, resp.status_code, resp.text[:300] if resp.text else ""


def main():
    venues_file = sys.argv[1]
    with open(venues_file) as f:
        venues = json.load(f)

    print(f"Processing {len(venues)} venues...")
    access_token = get_access_token()

    results = []
    batch_for_airtable = []
    consecutive_failures = 0

    for i, venue in enumerate(venues):
        record_id = venue["id"]
        venue_name = venue["name"]

        print(f"\n[{i+1}/{len(venues)}] {venue_name}...", end=" ", flush=True)

        try:
            # Search for Google Doc
            doc_id, doc_name = search_google_drive(venue_name, access_token)

            if not doc_id:
                print("NO DOC FOUND")
                batch_for_airtable.append({
                    "id": record_id,
                    "content": "[ERROR]: Link unreachable."
                })
                results.append({"venue": venue_name, "status": "ERROR", "chars": 0, "reason": "No Google Doc found"})
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    print("\n! 3+ consecutive failures. Refreshing token...")
                    access_token = refresh_access_token() or access_token
                    consecutive_failures = 0
            else:
                print(f"found: '{doc_name}' -> ", end="", flush=True)

                # Export as plain text
                text = export_doc_as_text(doc_id, access_token)

                if not text or len(text.strip()) < 50:
                    print("EMPTY/UNREADABLE")
                    batch_for_airtable.append({
                        "id": record_id,
                        "content": "[ERROR]: Files are images without readable text."
                    })
                    results.append({"venue": venue_name, "status": "ERROR", "chars": 0, "reason": "Empty doc"})
                    consecutive_failures += 1
                else:
                    # Clean and store
                    cleaned = clean_content(text)
                    char_count = len(cleaned)
                    print(f"OK ({char_count:,} chars)")

                    batch_for_airtable.append({"id": record_id, "content": cleaned})
                    results.append({"venue": venue_name, "status": "OK", "chars": char_count, "doc_name": doc_name})
                    consecutive_failures = 0
        except Exception as e:
            print(f"EXCEPTION: {e}")
            batch_for_airtable.append({
                "id": record_id,
                "content": "[ERROR]: Link unreachable."
            })
            results.append({"venue": venue_name, "status": "ERROR", "chars": 0, "reason": str(e)[:100]})
            consecutive_failures += 1

        # Write to Airtable in batches of 10
        if len(batch_for_airtable) >= 10:
            success, status, resp_text = update_airtable(batch_for_airtable)
            if success:
                print(f"  → Airtable batch write: OK ({len(batch_for_airtable)} records)")
            else:
                print(f"  → Airtable batch write: FAILED ({status}) - {resp_text}")
            batch_for_airtable = []
            time.sleep(0.3)

    # Write remaining records
    if batch_for_airtable:
        success, status, resp_text = update_airtable(batch_for_airtable)
        if success:
            print(f"\n  → Airtable final batch: OK ({len(batch_for_airtable)} records)")
        else:
            print(f"\n  → Airtable final batch: FAILED ({status}) - {resp_text}")

    # Summary
    ok = sum(1 for r in results if r["status"] == "OK")
    err = sum(1 for r in results if r["status"] == "ERROR")
    total_chars = sum(r["chars"] for r in results)
    print(f"\n{'='*50}")
    print(f"SUMMARY: {ok} success, {err} errors, {total_chars:,} total chars")
    print(f"{'='*50}")
    for r in results:
        icon = "OK" if r["status"] == "OK" else "ERR"
        reason = f" ({r.get('reason', '')})" if r.get('reason') else ""
        print(f"  [{icon}] {r['venue']}: {r['chars']:,} chars{reason}")

    # Save results
    results_file = venues_file.replace('.json', '_results.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {results_file}")


if __name__ == "__main__":
    main()
