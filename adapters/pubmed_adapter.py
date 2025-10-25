"""
PubMed Adapter
Provides access to PubMed database using integrated utilities
"""

from typing import List, Dict, Any, Optional

# Import PubMed utilities from local utils module
from utils.pubmed_utils import (
    search_key_words,
    search_advanced,
    get_pubmed_metadata,
    download_full_text_pdf,
    deep_paper_analysis as pubmed_deep_analysis
)

from .base_adapter import BaseAdapter


class PubMedAdapter(BaseAdapter):
    """Adapter for PubMed database using integrated PubMed utilities"""
    
    def get_source_name(self) -> str:
        return "pubmed"
    
    def search_by_keywords(self, keywords: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search PubMed using keywords
        
        Args:
            keywords: Search query string
            num_results: Number of results to return
            
        Returns:
            List of standardized paper dictionaries
        """
        try:
            results = search_key_words(keywords, num_results)
            return [self._format_result(r) for r in results]
        except Exception as e:
            print(f"Error searching PubMed: {e}")
            return []
    
    def search_advanced(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Advanced search in PubMed
        
        Args:
            title: Search in title
            author: Author name
            journal: Journal name
            start_date: Start date (YYYY/MM/DD)
            end_date: End date (YYYY/MM/DD)
            term: General search term
            num_results: Number of results
            
        Returns:
            List of standardized paper dictionaries
        """
        try:
            term = kwargs.get('term')
            title = kwargs.get('title')
            author = kwargs.get('author')
            journal = kwargs.get('journal')
            start_date = kwargs.get('start_date')
            end_date = kwargs.get('end_date')
            num_results = kwargs.get('num_results', 10)
            
            results = search_advanced(
                term=term,
                title=title,
                author=author,
                journal=journal,
                start_date=start_date,
                end_date=end_date,
                num_results=num_results
            )
            return [self._format_result(r) for r in results]
        except Exception as e:
            print(f"Error in advanced PubMed search: {e}")
            return []
    
    def get_metadata(self, identifier: str) -> Dict[str, Any]:
        """
        Get metadata for a PubMed article by PMID
        
        Args:
            identifier: PMID of the article
            
        Returns:
            Standardized metadata dictionary
        """
        try:
            metadata = get_pubmed_metadata(str(identifier))
            if metadata:
                return self._format_result(metadata)
            return {"error": f"No metadata found for PMID: {identifier}"}
        except Exception as e:
            return {"error": f"Error fetching metadata: {str(e)}"}
    
    def download_pdf(self, identifier: str) -> str:
        """
        Attempt to download PDF for a PubMed article
        
        Args:
            identifier: PMID of the article
            
        Returns:
            Status message
        """
        try:
            return download_full_text_pdf(str(identifier))
        except Exception as e:
            return f"Error downloading PDF: {str(e)}"
    
    def deep_analysis(self, identifier: str) -> str:
        """
        Generate deep analysis prompt for a PubMed article
        
        Args:
            identifier: PMID of the article
            
        Returns:
            Analysis prompt string
        """
        try:
            metadata = get_pubmed_metadata(str(identifier))
            if metadata:
                return pubmed_deep_analysis(metadata)
            return "Error: Could not retrieve metadata for analysis"
        except Exception as e:
            return f"Error generating analysis: {str(e)}"
    
    def _format_result(self, pubmed_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert PubMed format to standardized format
        
        Args:
            pubmed_result: Result from PubMed API
            
        Returns:
            Standardized result dictionary
        """
        if "error" in pubmed_result:
            return pubmed_result
            
        pmid = pubmed_result.get("PMID", "")
        return {
            "id": pmid,
            "title": pubmed_result.get("Title", "No title available"),
            "authors": pubmed_result.get("Authors", "No authors available"),
            "abstract": pubmed_result.get("Abstract", "No abstract available"),
            "publication_date": pubmed_result.get("Publication Date", ""),
            "journal": pubmed_result.get("Journal", ""),
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "pdf_url": None,  # PMC PDF URLs need to be determined separately
            "source": "pubmed"
        }

