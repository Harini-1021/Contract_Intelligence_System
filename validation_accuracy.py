"""
Accuracy Calculator
Analyzes validation results and generates accuracy report
"""

import csv
from collections import defaultdict

print("=" * 60)
print("ACCURACY VALIDATION REPORT")
print("=" * 60)
print()

# Read validation CSV
csv_path = 'data/validation.csv'

# Track results
total_checked = 0
total_correct = 0
field_stats = defaultdict(lambda: {'total': 0, 'correct': 0})
contract_stats = defaultdict(lambda: {'total': 0, 'correct': 0})

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        # Skip rows that haven't been validated yet
        if not row['Match']:
            continue
        
        total_checked += 1
        field_name = row['Field_Name']
        contract_id = row['Contract_ID']
        match = row['Match'].upper()
        
        # Update totals
        field_stats[field_name]['total'] += 1
        contract_stats[contract_id]['total'] += 1
        
        if match == 'TRUE':
            total_correct += 1
            field_stats[field_name]['correct'] += 1
            contract_stats[contract_id]['correct'] += 1

# Calculate overall accuracy
if total_checked > 0:
    overall_accuracy = (total_correct / total_checked) * 100
else:
    print("⚠️  No validated rows found!")
    print("Make sure you filled in the 'Match' column (TRUE/FALSE)")
    exit()

# Display results
print(f" OVERALL METRICS")
print("-" * 60)
print(f"Total Fields Validated:  {total_checked}")
print(f"Correct Extractions:     {total_correct}")
print(f"Incorrect Extractions:   {total_checked - total_correct}")
print(f"Overall Accuracy:        {overall_accuracy:.1f}%")
print()

# Per-field accuracy
print(f" PER-FIELD ACCURACY")
print("-" * 60)
print(f"{'Field Name':<25} {'Correct':<10} {'Total':<10} {'Accuracy':<10}")
print("-" * 60)

for field, stats in sorted(field_stats.items()):
    accuracy = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
    print(f"{field:<25} {stats['correct']:<10} {stats['total']:<10} {accuracy:>6.1f}%")

print("-" * 60)
print()

# Per-contract accuracy
print(f" PER-CONTRACT ACCURACY")
print("-" * 60)
print(f"{'Contract ID':<15} {'Correct':<10} {'Total':<10} {'Accuracy':<10}")
print("-" * 60)

for contract_id, stats in sorted(contract_stats.items(), key=lambda x: int(x[0])):
    accuracy = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
    print(f"{contract_id:<15} {stats['correct']:<10} {stats['total']:<10} {accuracy:>6.1f}%")

print("-" * 60)
print()

# Summary
print(" VALIDATION COMPLETE!")
print()
print(f"Validated {len(contract_stats)} contracts with {overall_accuracy:.1f}% accuracy")