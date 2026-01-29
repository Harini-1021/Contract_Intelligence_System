"""
Generate Validation Spreadsheet
Creates CSV with all extracted data ready for manual verification
"""

from src.database import ContractDatabase
import csv

print("=" * 60)
print("VALIDATION SPREADSHEET GENERATOR")
print("=" * 60)
print()

# Connect to database
db = ContractDatabase()

# Get all contracts
contracts = db.get_all_contracts()
print(f"Found {len(contracts)} contracts in database")
print()

# Prepare rows for CSV
rows = []

# Header row
header = [
    'Contract_ID',
    'Filename', 
    'Field_Name',
    'Extracted_Value',
    'Actual_Value',
    'Match',
    'Notes'
]

rows.append(header)

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

# Generate rows for each contract
contract_id = 1
for contract in contracts:
    filename = contract['filename']
    
    for field in fields:
        extracted_value = contract.get(field, 'NULL')
        
        # Truncate very long values
        if extracted_value and len(str(extracted_value)) > 100:
            extracted_value = str(extracted_value)[:100] + "..."
        
        row = [
            contract_id,
            filename,
            field,
            extracted_value,
            '',  # Actual_Value - YOU WILL FILL THIS
            '',  # Match - YOU WILL FILL THIS  
            ''   # Notes - OPTIONAL
        ]
        rows.append(row)
    
    contract_id += 1

# Write to CSV
csv_path = 'data/validation.csv'

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f" Generated validation spreadsheet: {csv_path}")
print()
print(f" Total rows: {len(rows) - 1} (header not counted)")
print(f" Contracts: {len(contracts)}")
print(f" Fields per contract: {len(fields)}")
print(f" Total checks needed: {len(contracts) * len(fields)}")
print()
print("NEXT STEPS:")
print("1. Open data/validation.csv in Excel or Google Sheets")
print("2. For each row, check the PDF and fill in 'Actual_Value' column")
print("3. Mark 'Match' as TRUE or FALSE")
print("4. Add any notes if needed")
print()

db.close()