"""
Auto-fill validation results for manually checked contracts
"""

import csv

# Contracts you manually validated
validated_contracts = [
    'Contract_Amendment_Enterprise.pdf',
    'MSA_Global_Consulting.pdf', 
    'PO_TechSupplies.pdf'
]

print("=" * 60)
print("UPDATING VALIDATION SPREADSHEET")
print("=" * 60)
print()

# Read existing validation data
csv_path = 'data/validation.csv'
rows = []

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    for row in reader:
        # If this contract was validated, fill in the columns
        if row['Filename'] in validated_contracts:
            # Actual_Value = Extracted_Value (since everything matched)
            row['Actual_Value'] = row['Extracted_Value']
            # Match = TRUE (you said everything was correct)
            row['Match'] = 'TRUE'
            # Notes = Verified
            row['Notes'] = 'Manually verified'
        
        rows.append(row)

# Write updated data back
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f" Updated validation for {len(validated_contracts)} contracts")
print()
print("Validated contracts:")
for contract in validated_contracts:
    print(f"  • {contract}")
print()
print(f"Updated file: {csv_path}")
print()
