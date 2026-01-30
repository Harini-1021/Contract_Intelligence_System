"""
Contract Data Validation Rules
Validates extracted contract data for common errors and format issues
"""

from datetime import datetime
import re


class ContractValidator:
    """Validates extracted contract data"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate(self, contract_data):
        """
        Validate all fields in contract data
        Returns: (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Run all validation checks
        self._validate_required_fields(contract_data)
        self._validate_dates(contract_data)
        self._validate_amount(contract_data)
        self._validate_date_logic(contract_data)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_required_fields(self, data):
        """Check required fields are present"""
        if not data.get('vendor_name') or data['vendor_name'] == 'NULL':
            self.errors.append("CRITICAL: Missing vendor name (required field)")
    
    def _validate_dates(self, data):
        """Validate date formats"""
        date_fields = ['effective_date', 'expiration_date']
        
        for field in date_fields:
            date_value = data.get(field)
            if date_value and date_value != 'NULL':
                # Check if it's in YYYY-MM-DD format
                if not self._is_valid_date_format(date_value):
                    self.warnings.append(f"{field}: Invalid format '{date_value}' (expected YYYY-MM-DD)")
    
    def _validate_amount(self, data):
        """Validate amount field"""
        amount = data.get('total_amount')
        
        if amount and amount != 'NULL':
            # Check if amount contains at least one number
            if not re.search(r'\d', amount):
                self.warnings.append(f"total_amount: No numeric value found in '{amount}'")
            
            # Check if amount is suspiciously low or high
            numeric_amount = self._extract_numeric_amount(amount)
            if numeric_amount:
                if numeric_amount < 100:
                    self.warnings.append(f"total_amount: Unusually low amount ${numeric_amount}")
                elif numeric_amount > 10000000:
                    self.warnings.append(f"total_amount: Unusually high amount ${numeric_amount}")
    
    def _validate_date_logic(self, data):
        """Validate date relationships"""
        effective = data.get('effective_date')
        expiration = data.get('expiration_date')
        
        if effective and expiration and effective != 'NULL' and expiration != 'NULL':
            try:
                effective_dt = datetime.strptime(effective, '%Y-%m-%d')
                expiration_dt = datetime.strptime(expiration, '%Y-%m-%d')
                
                if expiration_dt <= effective_dt:
                    self.errors.append(f"DATE LOGIC ERROR: Expiration date ({expiration}) is before or equal to effective date ({effective})")
            except ValueError:
                # Already caught in format validation
                pass
    
    def _is_valid_date_format(self, date_string):
        """Check if date is in YYYY-MM-DD format"""
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def _extract_numeric_amount(self, amount_string):
        """Extract numeric value from amount string"""
        # Remove common currency symbols and text
        cleaned = re.sub(r'[^\d,.]', '', amount_string)
        cleaned = cleaned.replace(',', '')
        
        try:
            return float(cleaned)
        except ValueError:
            return None
    
    def get_summary(self):
        """Get validation summary"""
        return {
            'has_errors': len(self.errors) > 0,
            'has_warnings': len(self.warnings) > 0,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'errors': self.errors,
            'warnings': self.warnings
        }


def validate_contract(contract_data):
    """
    Convenience function to validate contract data
    
    Args:
        contract_data: Dictionary with extracted contract fields
    
    Returns:
        tuple: (is_valid, errors, warnings)
    """
    validator = ContractValidator()
    return validator.validate(contract_data)


# Example usage
if __name__ == "__main__":
    # Test with sample data
    test_data = {
        'vendor_name': 'TechCorp Solutions',
        'contract_number': 'SVC-2024-001',
        'effective_date': '2024-01-15',
        'expiration_date': '2024-01-10',  # ERROR: before effective
        'total_amount': '$75,000',
        'payment_terms': 'NET 30 days',
        'contract_type': 'Service Agreement',
        'key_deliverables': 'Software development'
    }
    
    is_valid, errors, warnings = validate_contract(test_data)
    
    print("Validation Results:")
    print(f"Valid: {is_valid}")
    print(f"Errors: {errors}")
    print(f"Warnings: {warnings}")