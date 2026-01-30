"""
Test Contract Validator
"""

from src.contract_validator import validate_contract

print("=" * 60)
print("TESTING CONTRACT VALIDATOR")
print("=" * 60)
print()

# Test Case 1: Perfect contract
print("Test 1: Perfect Contract")
print("-" * 60)
perfect_data = {
    'vendor_name': 'TechCorp Solutions',
    'contract_number': 'SVC-2024-001',
    'effective_date': '2024-01-15',
    'expiration_date': '2025-01-15',
    'total_amount': '$75,000',
    'payment_terms': 'NET 30 days',
    'contract_type': 'Service Agreement',
    'key_deliverables': 'Software development'
}

is_valid, errors, warnings = validate_contract(perfect_data)
print(f"✓ Valid: {is_valid}")
print(f"  Errors: {len(errors)}")
print(f"  Warnings: {len(warnings)}")
print()

# Test Case 2: Missing vendor (CRITICAL)
print("Test 2: Missing Vendor Name")
print("-" * 60)
no_vendor = perfect_data.copy()
no_vendor['vendor_name'] = None

is_valid, errors, warnings = validate_contract(no_vendor)
print(f"✗ Valid: {is_valid}")
print(f"  Errors: {errors}")
print()

# Test Case 3: Invalid date format
print("Test 3: Invalid Date Format")
print("-" * 60)
bad_date = perfect_data.copy()
bad_date['effective_date'] = '01/15/2024'  # Wrong format

is_valid, errors, warnings = validate_contract(bad_date)
print(f"Valid: {is_valid}")
print(f"  Warnings: {warnings}")
print()

# Test Case 4: Expiration before effective
print("Test 4: Date Logic Error")
print("-" * 60)
bad_logic = perfect_data.copy()
bad_logic['expiration_date'] = '2023-01-15'  # Before effective

is_valid, errors, warnings = validate_contract(bad_logic)
print(f"✗ Valid: {is_valid}")
print(f"  Errors: {errors}")
print()

# Test Case 5: Amount with no numbers
print("Test 5: Invalid Amount")
print("-" * 60)
bad_amount = perfect_data.copy()
bad_amount['total_amount'] = 'To be determined'

is_valid, errors, warnings = validate_contract(bad_amount)
print(f"Valid: {is_valid}")
print(f"  Warnings: {warnings}")
print()

print("=" * 60)
print("VALIDATOR TESTING COMPLETE")
print("=" * 60)