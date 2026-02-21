#!/usr/bin/env python3
"""
Update Airtable records from batch4 JSON payload
"""

import json
import subprocess
import sys

# Read the payload file
with open('c:/Users/LFoul/Desktop/fws_content/outputs/at_payload_batch4.json', 'r', encoding='utf-8') as f:
    records = json.load(f)

print(f"Loaded {len(records)} records from JSON file")

# Prepare the MCP command
base_id = "appFQYNRTuooIRZZz"
table_id = "tblIEJQNynXIsD8GL"

# Build the records JSON string for the command
records_json = json.dumps(records)

# Use npx to call the Airtable MCP server directly
# We'll pass the records as a JSON argument
cmd = [
    "npx",
    "-y",
    "airtable-mcp-server",
    "update_records",
    "--baseId", base_id,
    "--tableId", table_id,
    "--records", records_json
]

print("Executing Airtable update...")
print(f"Command: {' '.join(cmd[:7])}... (records JSON truncated)")

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    if result.returncode == 0:
        print("\n✓ Update successful!")
        print(f"Updated {len(records)} records")
        if result.stdout:
            print(f"\nOutput: {result.stdout}")
    else:
        print("\n✗ Update failed!")
        print(f"Return code: {result.returncode}")
        if result.stderr:
            print(f"Error: {result.stderr}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        sys.exit(1)

except subprocess.TimeoutExpired:
    print("\n✗ Command timed out after 60 seconds")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    sys.exit(1)
