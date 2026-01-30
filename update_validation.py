"""
Auto-fill validation results for manually checked contracts
Supports both perfect matches and contracts with specific field corrections
"""

import csv

print("=" * 60)
print("UPDATING VALIDATION SPREADSHEET")
print("=" * 60)
print()

# Contracts where ALL fields matched perfectly (auto-fill from Extracted_Value)
perfect_matches = [
    'European_Format_Contract.pdf',
    'Ambiguous_Dates_Contract.pdf'
]

# Contracts with specific field corrections
# Format: {filename: {field_name: (actual_value, match_result)}}
field_corrections = {
    'Informal_Contract.pdf': {
        'vendor_name': ('QuickDeal Suppliers', 'TRUE'),
        'contract_number': ('None', 'TRUE'),
        'effective_date': ('None', 'TRUE'),
        'expiration_date': ('one year', 'FALSE'),
        'total_amount': ('around $20k give or take', 'FALSE'),
        'payment_terms': ('we\'ll invoice monthly', 'TRUE'),
        'contract_type': ('Purchase Order', 'TRUE'),
        'key_deliverables': ('office stuff and supplies', 'TRUE')
    },
    'Confusing_Amounts_Contract.pdf': {
        'vendor_name': ('MultiPrice Solutions LLC', 'TRUE'),
        'contract_number': ('MULTI-2024-999', 'FALSE'),
        'effective_date': ('2024-07-01', 'TRUE'),
        'expiration_date': ('2025-07-01', 'TRUE'),
        'total_amount': ('$47,000', 'TRUE'),
        'payment_terms': ('Setup fee upfront, monthly thereafter', 'TRUE'),
        'contract_type': ('Software Subscription Agreement', 'TRUE'),
        'key_deliverables': ('SaaS platform and support', 'TRUE')
    },
    'Amendment_Contract.pdf': {
        'vendor_name': ('TechCorp Solutions', 'TRUE'),
        'contract_number': ('SVC-2023-500-AMD2', 'FALSE'),
        'effective_date': ('2024-11-15', 'TRUE'),
        'expiration_date': ('None', 'TRUE'),
        'total_amount': ('$125,000', 'TRUE'),
        'payment_terms': ('NET 45 days', 'TRUE'),
        'contract_type': ('Amendment to Service Agreement', 'FALSE'),
        'key_deliverables': ('Cloud migration services', 'TRUE')
    }
}

# Read validation CSV
csv_path = 'data/validation.csv'
rows = []
updated_count = 0

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    for row in reader:
        filename = row['Filename']
        field_name = row['Field_Name']
        
        # Handle perfect matches
        if filename in perfect_matches:
            row['Actual_Value'] = row['Extracted_Value']
            row['Match'] = 'TRUE'
            row['Notes'] = 'Manually Verified'
            updated_count += 1
        
        # Handle specific field corrections
        elif filename in field_corrections:
            if field_name in field_corrections[filename]:
                actual_value, match = field_corrections[filename][field_name]
                row['Actual_Value'] = actual_value
                row['Match'] = match
                row['Notes'] = 'Manually verified' if match == 'TRUE' else 'Correction applied'
                updated_count += 1
        
        rows.append(row)

# Write updated data back
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f" Updated {updated_count} fields")
print()
print("VALIDATED CONTRACTS:")
print()
print("Perfect Matches (100%):")
for contract in perfect_matches:
    print(f"  • {contract}")
print()
print("Partial Matches (with corrections):")
for contract in field_corrections.keys():
    print(f"  • {contract}")
print()
print(f" Updated file: {csv_path}")
print()
