"""
Semantic Scholar Adapter
Provides access to Semantic Scholar's AI-powered academic search
"""

import requests
from typing import List, Dict, Any, Optional
from .base_adapter import BaseAdapter


class SemanticScholarAdapter(BaseAdapter):
    """Adapter for Semantic Scholar API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize adapter
        
        Args:
            api_key: Optional API key for higher rate limits
                    Get one at: https://www.semanticscholar.org/product/api
        """
        self.base_url = "https://api.semanticscholar.org/graph/v1"
        self.api_key = api_key
        self.headers = {}
        if api_key:
            self.headers['x-api-key'] = api_key
    
    def get_source_name(self) -> str:
        return "semantic_scholar"
    
    def search_by_keywords(self, keywords: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search Semantic Scholar by keywords
        
        Args:
            keywords: Search query string
            num_results: Number of results to return
            
        Returns:
            List of standardized paper dictionaries
        """
        try:
            url = f"{self.base_url}/paper/search"
            params = {
                "query": keywords,
                "limit": min(num_results, 100),  # API max is 100
                "fields": "paperId,title,abstract,authors,year,venue,url,openAccessPdf"
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            
            if response.status_code != 200:
                print(f"Semantic Scholar API error: {response.status_code}")
                if response.status_code == 429:
                    print("Rate limit exceeded. Consider using an API key.")
                return []
            
            data = response.json()
            papers = data.get("data", [])
            
            return [self._format_semantic_result(paper) for paper in papers]
            
        except Exception as e:
            print(f"Error searching Semantic Scholar: {e}")
            return []
    
    def search_advanced(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Advanced search in Semantic Scholar
        
        Args:
            term: General search term
            title: Search in title (not directly supported, uses general search)
            author: Author name
            year: Publication year
            venue: Publication venue
            fields_of_study: Field of study (e.g., "Computer Science")
            num_results: Number of results
            
        Returns:
            List of standardized paper dictionaries
        """
        try:
            # Semantic Scholar supports limited advanced search
            # We'll use general search with filtering
            
            query_parts = []
            
            if kwargs.get('term'):
                query_parts.append(kwargs['term'])
            if kwargs.get('title'):
                query_parts.append(kwargs['title'])
            if kwargs.get('author'):
                query_parts.append(kwargs['author'])
            
            if not query_parts:
                return []
            
            query = " ".join(query_parts)
            num_results = kwargs.get('num_results', 10)
            
            url = f"{self.base_url}/paper/search"
            params = {
                "query": query,
                "limit": min(num_results * 2, 100),  # Get extra for filtering
                "fields": "paperId,title,abstract,authors,year,venue,url,openAccessPdf,fieldsOfStudy"
            }
            
            # Add year filter if provided
            if kwargs.get('year'):
                params['year'] = str(kwargs['year'])
            
            # Add venue filter if provided
            if kwargs.get('venue'):
                params['venue'] = kwargs['venue']
            
            # Add fields of study if provided
            if kwargs.get('fields_of_study'):
                params['fieldsOfStudy'] = kwargs['fields_of_study']
            
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            papers = data.get("data", [])
            
            results = [self._format_semantic_result(paper) for paper in papers]
            
            # Additional filtering if needed
            if kwargs.get('author'):
                author_query = kwargs['author'].lower()
                results = [r for r in results if author_query in r.get('authors', '').lower()]
            
            return results[:num_results]
            
        except Exception as e:
            print(f"Error in advanced Semantic Scholar search: {e}")
            return []
    
    def get_metadata(self, identifier: str) -> Dict[str, Any]:
        """
        Get metadata for a paper by Semantic Scholar Paper ID or DOI
        
        Args:
            identifier: Paper ID or DOI
            
        Returns:
            Standardized metadata dictionary
        """
        try:
            # Semantic Scholar accepts both paper IDs and DOIs
            url = f"{self.base_url}/paper/{identifier}"
            params = {
                "fields": "paperId,title,abstract,authors,year,venue,url,openAccessPdf,citationCount,referenceCount"
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            
            if response.status_code != 200:
                return {"error": f"Could not retrieve metadata for ID: {identifier}"}
            
            paper = response.json()
            return self._format_semantic_result(paper)
            
        except Exception as e:
            return {"error": f"Error fetching metadata: {str(e)}"}
    
    def download_pdf(self, identifier: str) -> str:
        """
        Attempt to download PDF for a paper
        
        Note: Semantic Scholar provides links to PDFs when available,
        but doesn't host all PDFs directly
        
        Args:
            identifier: Paper ID or DOI
            
        Returns:
            Status message
        """
        try:
            # First get metadata to find PDF URL
            metadata = self.get_metadata(identifier)
            
            if "error" in metadata:
                return metadata["error"]
            
            pdf_url = metadata.get("pdf_url")
            
            if not pdf_url:
                return f"No open access PDF available for this paper. Try accessing: {metadata.get('url', '')}"
            
            # Download PDF
            response = requests.get(pdf_url, timeout=30)
            
            if response.status_code != 200:
                return f"Error: Unable to download PDF (status code: {response.status_code})"
            
            # Save PDF
            paper_id = metadata.get("id", identifier).replace("/", "_")
            filename = f"semantic_scholar_{paper_id}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            return f"PDF downloaded successfully as {filename}"
            
        except Exception as e:
            return f"Error downloading PDF: {str(e)}"
    
    def _format_semantic_result(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert Semantic Scholar format to standardized format
        
        Args:
            paper: Result from Semantic Scholar API
            
        Returns:
            Standardized result dictionary
        """
        # Extract authors
        authors_list = paper.get("authors", [])
        if authors_list:
            authors_str = ", ".join([author.get("name", "") for author in authors_list])
        else:
            authors_str = "No authors available"
        
        # Extract PDF URL if available
        pdf_info = paper.get("openAccessPdf")
        pdf_url = pdf_info.get("url") if pdf_info else None
        
        paper_id = paper.get("paperId", "")
        
        return {
            "id": paper_id,
            "title": paper.get("title", "No title available"),
            "authors": authors_str,
            "abstract": paper.get("abstract", "No abstract available"),
            "publication_date": str(paper.get("year", "")),
            "journal": paper.get("venue", ""),
            "url": paper.get("url", f"https://www.semanticscholar.org/paper/{paper_id}"),
            "pdf_url": pdf_url,
            "source": "semantic_scholar",
            # Additional Semantic Scholar specific fields
            "citation_count": paper.get("citationCount"),
            "reference_count": paper.get("referenceCount"),
            "fields_of_study": paper.get("fieldsOfStudy")
        }

