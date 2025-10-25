"""
Base Adapter Class
Defines the unified interface that all database adapters must implement
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any


class BaseAdapter(ABC):
    """Abstract base class for all academic database adapters"""
    
    @abstractmethod
    def search_by_keywords(self, keywords: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for papers using keywords
        
        Args:
            keywords: Search query string
            num_results: Maximum number of results to return
            
        Returns:
            List of dictionaries containing standardized paper information
        """
        pass
    
    @abstractmethod
    def search_advanced(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Perform advanced search with multiple parameters
        
        Args:
            **kwargs: Search parameters (title, author, journal, dates, etc.)
            
        Returns:
            List of dictionaries containing standardized paper information
        """
        pass
    
    @abstractmethod
    def get_metadata(self, identifier: str) -> Dict[str, Any]:
        """
        Get metadata for a specific paper
        
        Args:
            identifier: Unique identifier (PMID, DOI, arXiv ID, etc.)
            
        Returns:
            Dictionary containing standardized paper metadata
        """
        pass
    
    @abstractmethod
    def download_pdf(self, identifier: str) -> str:
        """
        Download PDF for a specific paper
        
        Args:
            identifier: Unique identifier (PMID, DOI, arXiv ID, etc.)
            
        Returns:
            Status message indicating success or failure
        """
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """
        Get the name of the data source
        
        Returns:
            String name of the database (e.g., "pubmed", "biorxiv")
        """
        pass
    
    def _format_result(self, raw_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert database-specific format to standardized format
        Should be overridden by subclasses if needed
        
        Args:
            raw_result: Database-specific result
            
        Returns:
            Standardized result dictionary
        """
        return {
            "id": raw_result.get("id", ""),
            "title": raw_result.get("title", ""),
            "authors": raw_result.get("authors", ""),
            "abstract": raw_result.get("abstract", ""),
            "publication_date": raw_result.get("publication_date", ""),
            "journal": raw_result.get("journal", ""),
            "url": raw_result.get("url", ""),
            "pdf_url": raw_result.get("pdf_url", None),
            "source": self.get_source_name()
        }

