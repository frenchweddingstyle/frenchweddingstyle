#!/usr/bin/env python3
"""
Update Airtable records from batch4 JSON payload using pyairtable
"""

import json
import os
from pyairtable import Api

# Airtable configuration
BASE_ID = "appFQYNRTuooIRZZz"
TABLE_ID = "tblIEJQNynXIsD8GL"

# Get API token from environment
api_token = os.getenv('AIRTABLE_API_KEY')
if not api_token:
    print("ERROR: AIRTABLE_API_KEY environment variable not set")
    exit(1)

# Read the payload file
payload_file = 'c:/Users/LFoul/Desktop/fws_content/outputs/at_payload_batch4.json'
with open(payload_file, 'r', encoding='utf-8') as f:
    records = json.load(f)

print(f"Loaded {len(records)} records from {payload_file}")

# Initialize Airtable API
api = Api(api_token)
table = api.table(BASE_ID, TABLE_ID)

# Update records
print("\nUpdating records...")
updated_count = 0
errors = []

for record in records:
    record_id = record['id']
    fields = record['fields']

    try:
        table.update(record_id, fields)
        updated_count += 1
        print(f"  ✓ Updated record {record_id}")
    except Exception as e:
        error_msg = f"  ✗ Failed to update record {record_id}: {str(e)}"
        print(error_msg)
        errors.append(error_msg)

# Summary
print(f"\n{'='*60}")
print(f"Update complete:")
print(f"  Total records: {len(records)}")
print(f"  Successfully updated: {updated_count}")
print(f"  Errors: {len(errors)}")
print(f"{'='*60}")

if errors:
    print("\nErrors encountered:")
    for error in errors:
        print(error)
    exit(1)
else:
    print("\nAll records updated successfully!")
