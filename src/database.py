"""
Database Module
SQLite database operations for storing and querying contract data
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ContractDatabase:
    """
    SQLite database manager for contract data.
    """
    
    def __init__(self, db_path: str = "data/contracts.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.create_tables()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection (creates if needed)."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return self.conn
    
    def create_tables(self):
        """Create database tables if they don't exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                vendor_name TEXT,
                contract_number TEXT,
                effective_date TEXT,
                expiration_date TEXT,
                total_amount TEXT,
                payment_terms TEXT,
                contract_type TEXT,
                key_deliverables TEXT,
                UNIQUE(filename, upload_date)
            )
        """)
        
        conn.commit()
        logger.info(f"Database initialized: {self.db_path}")
    
    def insert_contract(self, filename: str, contract_data: dict) -> int:
        """
        Insert a new contract into the database.
        
        Args:
            filename: Name of the contract file
            contract_data: Dictionary with extracted fields
            
        Returns:
            ID of inserted row
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO contracts (
                filename, vendor_name, contract_number,
                effective_date, expiration_date, total_amount,
                payment_terms, contract_type, key_deliverables
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            filename,
            contract_data.get('vendor_name'),
            contract_data.get('contract_number'),
            contract_data.get('effective_date'),
            contract_data.get('expiration_date'),
            contract_data.get('total_amount'),
            contract_data.get('payment_terms'),
            contract_data.get('contract_type'),
            contract_data.get('key_deliverables')
        ))
        
        conn.commit()
        contract_id = cursor.lastrowid
        logger.info(f"Inserted contract: {filename} (ID: {contract_id})")
        
        return contract_id
    
    def get_all_contracts(self) -> List[Dict]:
        """
        Get all contracts from database.
        
        Returns:
            List of dictionaries with contract data
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM contracts
            ORDER BY upload_date DESC
        """)
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_contract_by_id(self, contract_id: int) -> Optional[Dict]:
        """
        Get a specific contract by ID.
        
        Args:
            contract_id: Contract ID
            
        Returns:
            Dictionary with contract data or None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM contracts WHERE id = ?", (contract_id,))
        row = cursor.fetchone()
        
        return dict(row) if row else None
    
    def search_contracts(self, search_term: str) -> List[Dict]:
        """
        Search contracts by vendor name or contract number.
        
        Args:
            search_term: Search string
            
        Returns:
            List of matching contracts
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{search_term}%"
        cursor.execute("""
            SELECT * FROM contracts
            WHERE vendor_name LIKE ? OR contract_number LIKE ?
            ORDER BY upload_date DESC
        """, (search_pattern, search_pattern))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_contract_count(self) -> int:
        """Get total number of contracts."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM contracts")
        return cursor.fetchone()[0]
    
    def delete_contract(self, contract_id: int) -> bool:
        """
        Delete a contract by ID.
        
        Args:
            contract_id: Contract ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM contracts WHERE id = ?", (contract_id,))
        conn.commit()
        
        deleted = cursor.rowcount > 0
        if deleted:
            logger.info(f"Deleted contract ID: {contract_id}")
        
        return deleted
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None