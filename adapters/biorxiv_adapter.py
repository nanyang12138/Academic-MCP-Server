"""
bioRxiv/medRxiv Adapter
Provides access to bioRxiv and medRxiv preprint servers
"""

import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from .base_adapter import BaseAdapter


class BioRxivAdapter(BaseAdapter):
    """Adapter for bioRxiv and medRxiv preprint servers"""
    
    def __init__(self, server: str = "biorxiv"):
        """
        Initialize adapter
        
        Args:
            server: "biorxiv" or "medrxiv"
        """
        if server not in ["biorxiv", "medrxiv"]:
            raise ValueError("server must be 'biorxiv' or 'medrxiv'")
        self.server = server
        self.base_url = f"https://api.biorxiv.org"
    
    def get_source_name(self) -> str:
        return self.server
    
    def search_by_keywords(self, keywords: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search bioRxiv/medRxiv by keywords
        
        Note: bioRxiv API doesn't support keyword search directly,
        so we fetch recent papers and filter by keywords
        
        Args:
            keywords: Search query string
            num_results: Number of results to return
            
        Returns:
            List of standardized paper dictionaries
        """
        try:
            # Fetch papers from the last year and filter
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            
            date_range = f"{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
            
            all_results = []
            cursor = 0
            keywords_lower = keywords.lower()
            
            # Fetch in batches until we have enough results
            while len(all_results) < num_results and cursor < 10000:
                url = f"{self.base_url}/details/{self.server}/{date_range}/{cursor}"
                response = requests.get(url, timeout=30)
                
                if response.status_code != 200:
                    break
                
                data = response.json()
                collection = data.get("collection", [])
                
                if not collection:
                    break
                
                # Filter by keywords in title or abstract
                for item in collection:
                    title = item.get("title", "").lower()
                    abstract = item.get("abstract", "").lower()
                    
                    if keywords_lower in title or keywords_lower in abstract:
                        all_results.append(self._format_biorxiv_result(item))
                        if len(all_results) >= num_results:
                            break
                
                cursor += len(collection)
            
            return all_results[:num_results]
            
        except Exception as e:
            print(f"Error searching {self.server}: {e}")
            return []
    
    def search_advanced(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Advanced search in bioRxiv/medRxiv
        
        Args:
            title: Search in title
            author: Author name
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            num_results: Number of results
            
        Returns:
            List of standardized paper dictionaries
        """
        try:
            start_date = kwargs.get('start_date')
            end_date = kwargs.get('end_date')
            title_query = kwargs.get('title', '').lower()
            author_query = kwargs.get('author', '').lower()
            num_results = kwargs.get('num_results', 10)
            
            # Default to last year if no dates provided
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            if not start_date:
                start_obj = datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=365)
                start_date = start_obj.strftime('%Y-%m-%d')
            
            date_range = f"{start_date}/{end_date}"
            
            all_results = []
            cursor = 0
            
            while len(all_results) < num_results and cursor < 10000:
                url = f"{self.base_url}/details/{self.server}/{date_range}/{cursor}"
                response = requests.get(url, timeout=30)
                
                if response.status_code != 200:
                    break
                
                data = response.json()
                collection = data.get("collection", [])
                
                if not collection:
                    break
                
                for item in collection:
                    # Filter by title and author
                    title_match = not title_query or title_query in item.get("title", "").lower()
                    author_match = not author_query or author_query in item.get("authors", "").lower()
                    
                    if title_match and author_match:
                        all_results.append(self._format_biorxiv_result(item))
                        if len(all_results) >= num_results:
                            break
                
                cursor += len(collection)
            
            return all_results[:num_results]
            
        except Exception as e:
            print(f"Error in advanced {self.server} search: {e}")
            return []
    
    def get_metadata(self, identifier: str) -> Dict[str, Any]:
        """
        Get metadata for a bioRxiv/medRxiv article by DOI
        
        Args:
            identifier: DOI of the article (e.g., "10.1101/2024.01.001")
            
        Returns:
            Standardized metadata dictionary
        """
        try:
            # Extract DOI suffix if full DOI provided
            doi = identifier.replace("10.1101/", "")
            
            url = f"{self.base_url}/details/{self.server}/{doi}"
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                return {"error": f"Could not retrieve metadata for DOI: {identifier}"}
            
            data = response.json()
            collection = data.get("collection", [])
            
            if collection:
                return self._format_biorxiv_result(collection[0])
            
            return {"error": f"No metadata found for DOI: {identifier}"}
            
        except Exception as e:
            return {"error": f"Error fetching metadata: {str(e)}"}
    
    def download_pdf(self, identifier: str) -> str:
        """
        Download PDF for a bioRxiv/medRxiv article
        
        Args:
            identifier: DOI of the article
            
        Returns:
            Status message
        """
        try:
            # bioRxiv/medRxiv DOI format: 10.1101/YYYY.MM.DD.XXXXXX
            doi = identifier.replace("10.1101/", "")
            
            # PDF URL format
            pdf_url = f"https://www.{self.server}.org/content/{doi}v1.full.pdf"
            
            response = requests.get(pdf_url, timeout=30)
            
            if response.status_code != 200:
                return f"Error: Unable to download PDF (status code: {response.status_code})"
            
            # Save PDF
            filename = f"{self.server}_{doi.replace('/', '_')}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            return f"PDF downloaded successfully as {filename}"
            
        except Exception as e:
            return f"Error downloading PDF: {str(e)}"
    
    def _format_biorxiv_result(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert bioRxiv/medRxiv format to standardized format
        
        Args:
            item: Result from bioRxiv API
            
        Returns:
            Standardized result dictionary
        """
        doi = item.get("doi", "")
        
        return {
            "id": doi,
            "title": item.get("title", ""),
            "authors": item.get("authors", ""),
            "abstract": item.get("abstract", ""),
            "publication_date": item.get("date", ""),
            "journal": f"{self.server} (preprint)",
            "url": f"https://www.{self.server}.org/content/{doi}",
            "pdf_url": f"https://www.{self.server}.org/content/{doi}v1.full.pdf",
            "source": self.server
        }

