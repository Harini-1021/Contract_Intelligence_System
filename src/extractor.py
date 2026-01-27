"""
Contract Extraction Module
Handles PDF processing and data extraction using ExtractThinker + GPT-4o-mini
"""

import os
from typing import Optional
from extract_thinker import Extractor, DocumentLoaderPyPdf, SplittingStrategy
from dotenv import load_dotenv
from src.schema import ContractData
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContractExtractor:
    """
    Main class for extracting data from contract PDFs.
    
    Uses ExtractThinker with GPT-4o-mini, configured for small documents.
    """
    
    def __init__(
        self, 
        model_name: str = "gpt-4o-mini",
        api_key: Optional[str] = None
    ):
        """
        Initialize the extractor.
        
        Args:
            model_name: OpenAI model to use (default: gpt-4o-mini)
            api_key: OpenAI API key (reads from .env if not provided)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. "
                "Set OPENAI_API_KEY in .env file or pass as parameter."
            )
        
        # Set API key in environment
        os.environ["OPENAI_API_KEY"] = self.api_key
        
        # Initialize extractor
        self.extractor = Extractor()
        self.extractor.load_document_loader(DocumentLoaderPyPdf())
        
        # Use NO_SPLIT strategy for small contracts (process in single call)
        # This avoids chunking and concatenation which causes token issues
        self.extractor.load_splitting_strategy(SplittingStrategy.NO_SPLIT)
        
        self.extractor.load_llm(self.model_name)
        
        logger.info(f"ContractExtractor initialized with model: {self.model_name}, splitting: NO_SPLIT")
    
    def extract(self, pdf_path: str) -> ContractData:
        """
        Extract data from a contract PDF.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            ContractData object with extracted fields
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: If extraction fails
        """
        # Validate file exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Processing contract: {pdf_path}")
        
        try:
            # Extract data using ExtractThinker
            result = self.extractor.extract(pdf_path, ContractData)
            
            logger.info(f"Successfully extracted data from: {pdf_path}")
            logger.info(f"Vendor: {result.vendor_name}")
            
            return result
            
        except Exception as e:
            logger.error(f"Extraction failed for {pdf_path}: {str(e)}")
            raise Exception(f"Failed to extract data: {str(e)}")
    
    def extract_to_dict(self, pdf_path: str) -> dict:
        """
        Extract data and return as dictionary.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with extracted fields
        """
        result = self.extract(pdf_path)
        return result.model_dump()


def extract_contract(pdf_path: str) -> dict:
    """
    Convenience function for quick extraction.
    
    Args:
        pdf_path: Path to contract PDF
        
    Returns:
        Dictionary with extracted data
    """
    extractor = ContractExtractor()
    return extractor.extract_to_dict(pdf_path)


# Example usage
if __name__ == "__main__":
    # Test extraction on a sample contract
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python extractor.py <path_to_contract.pdf>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    print(f"\n{'='*60}")
    print("CONTRACT EXTRACTION TEST")
    print(f"{'='*60}\n")
    
    try:
        data = extract_contract(pdf_file)
        
        print("Extracted Data:")
        print("-" * 60)
        for field, value in data.items():
            print(f"{field:20s}: {value}")
        print("-" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: If token errors occur, use simple_extractor.py")
        sys.exit(1)