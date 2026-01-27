"""
Contract Data Schema
Defines the structure of data to extract from contracts
"""

from extract_thinker import Contract
from typing import Optional


class ContractData(Contract):
    """
    Schema for contract data extraction.
    
    Each field tells the AI what to look for in the contract.
    """
    
    vendor_name: str
    """The name of the vendor/supplier/service provider"""
    
    contract_number: Optional[str] = None
    """The unique contract identifier or reference number"""
    
    effective_date: Optional[str] = None
    """The date when the contract becomes effective (format: YYYY-MM-DD if possible)"""
    
    expiration_date: Optional[str] = None
    """The date when the contract expires or terminates (format: YYYY-MM-DD if possible)"""
    
    total_amount: Optional[str] = None
    """The total contract value or amount (include currency if specified)"""
    
    payment_terms: Optional[str] = None
    """Payment terms (e.g., NET 30, due upon receipt, monthly installments)"""
    
    contract_type: Optional[str] = None
    """The type of contract (e.g., Service Agreement, Purchase Order, MSA)"""
    
    key_deliverables: Optional[str] = None
    """Main deliverables or services to be provided under this contract"""