"""
Simple Contract Extractor - Direct OpenAI API
Bypasses ExtractThinker to avoid token limit issues
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import logging

load_dotenv()
logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF using PyPDF2"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def extract_contract_simple(pdf_path: str) -> dict:
    """
    Extract contract data using direct OpenAI API call.
    
    Args:
        pdf_path: Path to contract PDF
        
    Returns:
        Dictionary with extracted fields
    """
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    # Extract text from PDF
    logger.info(f"Extracting text from: {pdf_path}")
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Create OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Prompt for extraction
    prompt = f"""
Extract the following information from this contract. Return ONLY valid JSON with these exact field names:

{{
  "vendor_name": "string (required)",
  "contract_number": "string or null",
  "effective_date": "string (YYYY-MM-DD format) or null",
  "expiration_date": "string (YYYY-MM-DD format) or null",
  "total_amount": "string or null",
  "payment_terms": "string or null",
  "contract_type": "string or null",
  "key_deliverables": "string or null"
}}

Contract text:
{pdf_text}

Return ONLY the JSON object, no other text.
"""
    
    # Make API call with safe max_tokens
    logger.info("Calling OpenAI API...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a contract data extraction assistant. Extract information accurately and return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,  # Safe limit
        temperature=0.1
    )
    
    # Parse response
    result_text = response.choices[0].message.content.strip()
    
    # Remove markdown code blocks if present
    if result_text.startswith("```json"):
        result_text = result_text.replace("```json", "").replace("```", "").strip()
    elif result_text.startswith("```"):
        result_text = result_text.replace("```", "").strip()
    
    # Parse JSON
    try:
        data = json.loads(result_text)
        logger.info(f"Successfully extracted: {data.get('vendor_name', 'Unknown')}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        logger.error(f"Response was: {result_text}")
        raise Exception(f"Failed to parse extraction result: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python simple_extractor.py <path_to_contract.pdf>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    try:
        data = extract_contract_simple(pdf_file)
        print("\nExtracted Data:")
        print("-" * 60)
        for field, value in data.items():
            print(f"{field:20s}: {value}")
        print("-" * 60)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)