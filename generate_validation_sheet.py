"""
Generate Validation Spreadsheet
Creates CSV with all extracted data ready for manual verification
Supports appending new contracts without overwriting existing data
"""

from src.database import ContractDatabase
import csv
from pathlib import Path

print("=" * 60)
print("VALIDATION SPREADSHEET GENERATOR")
print("=" * 60)
print()

# Connect to database
db = ContractDatabase()

# Get all contracts from database
contracts = db.get_all_contracts()
print(f"Found {len(contracts)} contracts in database")

# Check if validation.csv already exists
csv_path = 'data/validation.csv'
existing_filenames = set()

if Path(csv_path).exists():
    print(f"Found existing validation.csv")
    # Read existing filenames
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_filenames.add(row['Filename'])
    print(f"Already validated: {len(existing_filenames)} contracts")

# Find NEW contracts not yet in validation
new_contracts = [c for c in contracts if c['filename'] not in existing_filenames]
print(f"New contracts to add: {len(new_contracts)}")
print()

if len(new_contracts) == 0:
    print("✓ All contracts already in validation.csv")
    print("✓ No new contracts to add")
    db.close()
    exit()

# Fields to validate
fields = [
    'vendor_name',
    'contract_number',
    'effective_date',
    'expiration_date',
    'total_amount',
    'payment_terms',
    'contract_type',
    'key_deliverables'
]

# Prepare new rows
new_rows = []

for contract in new_contracts:
    filename = contract['filename']
    print(f"  Adding: {filename}")
    
    for field in fields:
        extracted_value = contract.get(field, 'NULL')
        
        # Truncate very long values
        if extracted_value and len(str(extracted_value)) > 100:
            extracted_value = str(extracted_value)[:100] + "..."
        
        row = [
            contract['id'],
            filename,
            field,
            extracted_value,
            '',  
            '',   
            ''   
        ]
        new_rows.append(row)

# If validation.csv doesn't exist, create it with header
if not Path(csv_path).exists():
    header = [
        'Contract_ID',
        'Filename', 
        'Field_Name',
        'Extracted_Value',
        'Actual_Value',
        'Match',
        'Notes'
    ]
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    print("Created new validation.csv")

# Append new rows
with open(csv_path, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)

print()
print(f" Added {len(new_rows)} rows to validation.csv")
print(f" New contracts added: {len(new_contracts)}")
print()

db.close()
