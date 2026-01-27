"""
Usage:
    python test1.py                    # Check environment
    python test1.py path/to/contract.pdf  # Test extraction
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_environment():
    print("-" * 60)
    print("ENVIRONMENT TEST")
    print("-" * 60)
    print()
    
    all_good = True
    
    # Check Python version
    print(f" Python version: {sys.version.split()[0]}")
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f" OpenAI API key found: {api_key[:15]}...")
    else:
        print(" OpenAI API key NOT found!")
        print(" Add OPENAI_API_KEY to your .env file")
        all_good = False
    
    # Check imports
    try:
        from extract_thinker import Extractor
        print(" ExtractThinker installed")
    except ImportError:
        print(" ExtractThinker NOT installed")
        print(" Run: pip install extract-thinker")
        all_good = False
    
    try:
        import openai
        print(" OpenAI package installed")
    except ImportError:
        print(" OpenAI package NOT installed")
        print(" Run: pip install openai")
        all_good = False
    
    try:
        import streamlit
        print(" Streamlit installed")
    except ImportError:
        print(" Streamlit NOT installed")
        print(" Run: pip install streamlit")
        all_good = False
    
    print()
    
    if all_good:
        print("-" * 60)
        print(" ENVIRONMENT READY!")
        print("-" * 60)
        return True
    else:
        print("-" * 60)
        print("FIX THE ISSUES ABOVE")
        print("-" * 60)
        return False


def extract_sample(pdf_path):
    """Extract from a sample contract"""
    from src.simple_extractor import extract_contract_simple as extract_contract
    from src.database import ContractDatabase
    
    print()
    print("-" * 60)
    print("EXTRACTING CONTRACT DATA")
    print("-" * 60)
    print(f"File: {pdf_path}")
    print()
    
    try:
        # Extract data
        print("Step 1: Extracting data from PDF...")
        data = extract_contract(pdf_path)
        
        print(" Extraction successful!")
        print()
        
        # Display extracted data
        print("EXTRACTED DATA:")
        print("-" * 60)
        for field, value in data.items():
            # Truncate long values for display
            display_value = str(value)[:100] if value else "N/A"
            print(f"{field:20s}: {display_value}")
        print("-" * 60)
        print()
        
        # Save to database
        print("Step 2: Saving to database...")
        db = ContractDatabase()
        filename = os.path.basename(pdf_path)
        contract_id = db.insert_contract(filename, data)
        print(f"Saved with ID: {contract_id}")
        
        # Show total contracts
        total = db.get_contract_count()
        print(f" Total contracts in database: {total}")
        
        db.close()
        print()
        print("-" * 60)
        print(" SUCCESS! Contract extracted and saved!")
        print("-" * 60)
        
        return data
        
    except FileNotFoundError:
        print(f" ERROR: File not found: {pdf_path}")
        print()
        print("Make sure:")
        print("File path is correct")
        print("File exists in data/contracts/")
        return None
        
    except Exception as e:
        print(f"ERROR: {e}")
        print()
        print("Common issues:")
        print("  - PDF is corrupted or can't be read")
        print("  - OpenAI API key is invalid")
        print("  - Network connection issue")
        return None


if __name__ == "__main__":
    # Test environment first
    if not test_environment():
        print("\n Fix the issues above and try again")
        sys.exit(1)
    
    # If PDF provided, extract it
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
        extract_sample(pdf_file)
    else:
        print()
        print(" To test extraction, run:")
        print("   python test1.py path/to/contract.pdf")
        print()
        print("Example:")
        print("   python test1.py data/contracts/sample_contract.pdf")