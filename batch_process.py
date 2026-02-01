
import os
from pathlib import Path
from src.simple_extractor import extract_contract_simple
from src.database import ContractDatabase

# Define the contracts folder
CONTRACTS_FOLDER = "data/contracts"

print("=" * 60)
print("BATCH CONTRACT PROCESSOR")
print("=" * 60)
print()

# Get all PDF files
pdf_files = list(Path(CONTRACTS_FOLDER).glob("*.pdf"))
total_files = len(pdf_files)

print(f"Found {total_files} PDF files to process")
print()

# Initialize database
db = ContractDatabase()

# Track results
results = {
    'successful': [],
    'failed': []
}

# Process each contract
for i, pdf_file in enumerate(pdf_files, 1):
    filename = pdf_file.name
    
    print(f"[{i}/{total_files}] Processing: {filename}")
    
    try:
        # Extract data
        data = extract_contract_simple(str(pdf_file))
        
        # Save to database
        contract_id = db.insert_contract(filename, data)
        
        # Track success
        results['successful'].append({
            'filename': filename,
            'id': contract_id,
            'vendor': data.get('vendor_name', 'Unknown')
        })
        
        print(f"Saved (ID: {contract_id}) - {data.get('vendor_name', 'N/A')}")
        
    except Exception as e:
        # Track failure
        results['failed'].append({
            'filename': filename,
            'error': str(e)
        })
        
        print(f"Failed - {str(e)[:60]}")
    
    print()

# Close database
db.close()

# Display summary
print("=" * 60)
print("BATCH PROCESSING COMPLETE")
print("=" * 60)
print()
print(f"Successful: {len(results['successful'])}")
print(f"Failed:     {len(results['failed'])}")
print(f"Total:      {total_files}")
print()

if results['successful']:
    print("Successful extractions:")
    for item in results['successful']:
        print(f"  • {item['filename']} → {item['vendor']}")
    print()

if results['failed']:
    print("Failed extractions:")
    for item in results['failed']:
        print(f"  • {item['filename']}")
        print(f"    Error: {item['error'][:80]}")
    print()

# Final database count
db = ContractDatabase()
total_in_db = db.get_contract_count()
db.close()

print(f"Total contracts in database: {total_in_db}")
print()
print("Batch processing complete!")
