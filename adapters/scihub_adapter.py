"""
Sci-Hub Adapter
Provides access to Sci-Hub for academic paper retrieval
"""

from typing import List, Dict, Any, Optional
import requests
from .base_adapter import BaseAdapter

class SciHubAdapter(BaseAdapter):
    """Adapter for Sci-Hub paper search and retrieval"""
    
    def __init__(self):
        """Initialize Sci-Hub adapter"""
        self.source_name = "scihub"
        try:
            from scihub import SciHub
            self.sh = SciHub()
            self.sh.timeout = 30
            self.available = True
        except ImportError:
            print("Warning: scihub library not available. Install with: pip install scihub")
            self.available = False
    
    def search_by_keywords(self, keywords: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search papers by keywords using CrossRef API + Sci-Hub
        
        Args:
            keywords: Search query
            num_results: Number of results to return
            
        Returns:
            List of paper dictionaries
        """
        if not self.available:
            return [{"error": "Sci-Hub library not available"}]
        
        papers = []
        try:
            # Use CrossRef API for keyword search
            url = f"https://api.crossref.org/works?query={keywords}&rows={num_results}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for item in data['message']['items'][:num_results]:
                    doi = item.get('DOI')
                    if doi:
                        # Get paper info from Sci-Hub
                        paper_info = self._fetch_from_scihub(doi)
                        if paper_info:
                            # Combine CrossRef metadata with Sci-Hub data
                            title = item.get('title', [''])[0] if item.get('title') else ''
                            authors = self._format_authors(item.get('author', []))
                            
                            papers.append({
                                'id': doi,
                                'title': title,
                                'authors': authors,
                                'abstract': item.get('abstract', 'N/A'),
                                'publication_date': self._format_date(item.get('created', {})),
                                'journal': item.get('container-title', [''])[0] if item.get('container-title') else 'N/A',
                                'url': f"https://doi.org/{doi}",
                                'pdf_url': paper_info.get('url', ''),
                                'source': 'scihub'
                            })
        except Exception as e:
            print(f"Error searching Sci-Hub by keywords: {e}")
        
        return papers
    
    def search_advanced(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        journal: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        term: Optional[str] = None,
        num_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Advanced search using CrossRef API
        
        Args:
            title: Paper title
            author: Author name
            journal: Journal name
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            term: General search term
            num_results: Number of results
            
        Returns:
            List of paper dictionaries
        """
        if not self.available:
            return [{"error": "Sci-Hub library not available"}]
        
        # Build CrossRef query
        query_parts = []
        if title:
            query_parts.append(f"title:{title}")
        if author:
            query_parts.append(f"author:{author}")
        if journal:
            query_parts.append(f"container-title:{journal}")
        if term:
            query_parts.append(term)
        
        query = " ".join(query_parts) if query_parts else "research"
        
        # Use keyword search with the constructed query
        return self.search_by_keywords(query, num_results)
    
    def get_metadata(self, identifier: str) -> Dict[str, Any]:
        """
        Get metadata for a paper by DOI
        
        Args:
            identifier: DOI of the paper
            
        Returns:
            Dictionary with paper metadata
        """
        if not self.available:
            return {"error": "Sci-Hub library not available"}
        
        try:
            # Get from Sci-Hub
            result = self._fetch_from_scihub(identifier)
            if result:
                # Also get CrossRef metadata for more details
                crossref_url = f"https://api.crossref.org/works/{identifier}"
                response = requests.get(crossref_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()['message']
                    
                    return {
                        'id': identifier,
                        'title': data.get('title', [''])[0] if data.get('title') else result.get('title', ''),
                        'authors': self._format_authors(data.get('author', [])),
                        'abstract': data.get('abstract', 'N/A'),
                        'publication_date': self._format_date(data.get('created', {})),
                        'journal': data.get('container-title', [''])[0] if data.get('container-title') else 'N/A',
                        'url': f"https://doi.org/{identifier}",
                        'pdf_url': result.get('url', ''),
                        'source': 'scihub'
                    }
            
            return {"error": f"Paper with DOI {identifier} not found"}
        except Exception as e:
            return {"error": f"Error retrieving metadata: {str(e)}"}
    
    def download_pdf(self, identifier: str, output_path: str = None) -> str:
        """
        Download PDF from Sci-Hub
        
        Args:
            identifier: DOI of the paper
            output_path: Path to save the PDF
            
        Returns:
            Status message
        """
        if not self.available:
            return "Error: Sci-Hub library not available"
        
        try:
            result = self._fetch_from_scihub(identifier)
            if result and result.get('url'):
                if output_path is None:
                    output_path = f"paper_{identifier.replace('/', '_')}.pdf"
                
                self.sh.download(result['url'], path=output_path)
                return f"PDF successfully downloaded to {output_path}"
            else:
                return f"Error: Could not find PDF for DOI {identifier}"
        except Exception as e:
            return f"Error downloading PDF: {str(e)}"
    
    def _fetch_from_scihub(self, doi: str) -> Optional[Dict[str, Any]]:
        """
        Fetch paper from Sci-Hub
        
        Args:
            doi: DOI of the paper
            
        Returns:
            Dictionary with paper info or None
        """
        try:
            result = self.sh.fetch(doi)
            return result
        except Exception as e:
            print(f"Error fetching from Sci-Hub: {e}")
            return None
    
    def _format_authors(self, authors: List[Dict]) -> str:
        """Format author list from CrossRef data"""
        if not authors:
            return "N/A"
        
        author_names = []
        for author in authors[:5]:  # Limit to first 5 authors
            given = author.get('given', '')
            family = author.get('family', '')
            if given or family:
                author_names.append(f"{given} {family}".strip())
        
        result = ", ".join(author_names)
        if len(authors) > 5:
            result += " et al."
        
        return result if result else "N/A"
    
    def _format_date(self, date_dict: Dict) -> str:
        """Format date from CrossRef data"""
        if not date_dict:
            return "N/A"
        
        date_parts = date_dict.get('date-parts', [[]])
        if date_parts and date_parts[0]:
            parts = date_parts[0]
            if len(parts) >= 1:
                year = parts[0]
                month = parts[1] if len(parts) >= 2 else 1
                day = parts[2] if len(parts) >= 3 else 1
                return f"{year}-{month:02d}-{day:02d}"
        
        return "N/A"
    
    def get_source_name(self) -> str:
        """
        Get the name of the data source
        
        Returns:
            String name of the database
        """
        return self.source_name
    
    def search_by_title(self, title: str) -> Dict[str, Any]:
        """
        Search for a paper by title using CrossRef + Sci-Hub
        
        Args:
            title: Paper title
            
        Returns:
            Dictionary with paper info
        """
        if not self.available:
            return {"error": "Sci-Hub library not available"}
        
        try:
            # Search CrossRef for the title
            url = f"https://api.crossref.org/works?query.title={title}&rows=1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data['message']['items']:
                    item = data['message']['items'][0]
                    doi = item.get('DOI')
                    
                    if doi:
                        # Get full metadata
                        return self.get_metadata(doi)
            
            return {"error": f"Paper with title '{title}' not found"}
        except Exception as e:
            return {"error": f"Error searching by title: {str(e)}"}

