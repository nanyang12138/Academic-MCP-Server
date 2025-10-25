"""
arXiv Adapter
Provides access to arXiv preprint server for physics, math, CS, etc.
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
from urllib.parse import quote
from .base_adapter import BaseAdapter


class ArXivAdapter(BaseAdapter):
    """Adapter for arXiv preprint server"""
    
    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"
    
    def get_source_name(self) -> str:
        return "arxiv"
    
    def search_by_keywords(self, keywords: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search arXiv by keywords
        
        Args:
            keywords: Search query string
            num_results: Number of results to return
            
        Returns:
            List of standardized paper dictionaries
        """
        try:
            # arXiv search query
            search_query = f"all:{quote(keywords)}"
            params = {
                "search_query": search_query,
                "start": 0,
                "max_results": num_results,
                "sortBy": "relevance",
                "sortOrder": "descending"
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            
            if response.status_code != 200:
                print(f"Error: arXiv API returned status {response.status_code}")
                return []
            
            return self._parse_arxiv_response(response.text)
            
        except Exception as e:
            print(f"Error searching arXiv: {e}")
            return []
    
    def search_advanced(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Advanced search in arXiv
        
        Args:
            title: Search in title
            author: Author name
            abstract: Search in abstract
            category: arXiv category (e.g., "cs.AI", "physics.comp-ph")
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            num_results: Number of results
            
        Returns:
            List of standardized paper dictionaries
        """
        try:
            query_parts = []
            
            if kwargs.get('title'):
                query_parts.append(f"ti:{quote(kwargs['title'])}")
            if kwargs.get('author'):
                query_parts.append(f"au:{quote(kwargs['author'])}")
            if kwargs.get('abstract'):
                query_parts.append(f"abs:{quote(kwargs['abstract'])}")
            if kwargs.get('category'):
                query_parts.append(f"cat:{quote(kwargs['category'])}")
            
            if not query_parts:
                # If no specific fields, use general search
                if kwargs.get('term'):
                    query_parts.append(f"all:{quote(kwargs['term'])}")
                else:
                    return []
            
            search_query = "+AND+".join(query_parts)
            
            num_results = kwargs.get('num_results', 10)
            
            params = {
                "search_query": search_query,
                "start": 0,
                "max_results": num_results,
                "sortBy": "submittedDate",
                "sortOrder": "descending"
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            
            if response.status_code != 200:
                return []
            
            results = self._parse_arxiv_response(response.text)
            
            # Filter by date if provided
            if kwargs.get('start_date') or kwargs.get('end_date'):
                results = self._filter_by_date(results, kwargs.get('start_date'), kwargs.get('end_date'))
            
            return results
            
        except Exception as e:
            print(f"Error in advanced arXiv search: {e}")
            return []
    
    def get_metadata(self, identifier: str) -> Dict[str, Any]:
        """
        Get metadata for an arXiv article by ID
        
        Args:
            identifier: arXiv ID (e.g., "2301.00001" or "arXiv:2301.00001")
            
        Returns:
            Standardized metadata dictionary
        """
        try:
            # Clean arXiv ID
            arxiv_id = identifier.replace("arXiv:", "").strip()
            
            params = {
                "id_list": arxiv_id,
                "max_results": 1
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            
            if response.status_code != 200:
                return {"error": f"Could not retrieve metadata for arXiv ID: {identifier}"}
            
            results = self._parse_arxiv_response(response.text)
            
            if results:
                return results[0]
            
            return {"error": f"No metadata found for arXiv ID: {identifier}"}
            
        except Exception as e:
            return {"error": f"Error fetching metadata: {str(e)}"}
    
    def download_pdf(self, identifier: str) -> str:
        """
        Download PDF for an arXiv article
        
        Args:
            identifier: arXiv ID
            
        Returns:
            Status message
        """
        try:
            # Clean arXiv ID
            arxiv_id = identifier.replace("arXiv:", "").strip()
            
            # arXiv PDF URL
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            
            response = requests.get(pdf_url, timeout=30)
            
            if response.status_code != 200:
                return f"Error: Unable to download PDF (status code: {response.status_code})"
            
            # Save PDF
            filename = f"arxiv_{arxiv_id.replace('/', '_')}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            return f"PDF downloaded successfully as {filename}"
            
        except Exception as e:
            return f"Error downloading PDF: {str(e)}"
    
    def _parse_arxiv_response(self, xml_text: str) -> List[Dict[str, Any]]:
        """
        Parse arXiv API XML response
        
        Args:
            xml_text: XML response from arXiv API
            
        Returns:
            List of standardized result dictionaries
        """
        try:
            root = ET.fromstring(xml_text)
            
            # arXiv uses Atom namespace
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            results = []
            
            for entry in root.findall('atom:entry', ns):
                # Extract arXiv ID from the id URL
                id_elem = entry.find('atom:id', ns)
                arxiv_id = id_elem.text.split('/abs/')[-1] if id_elem is not None else ""
                
                # Title
                title_elem = entry.find('atom:title', ns)
                title = title_elem.text.strip() if title_elem is not None else ""
                
                # Authors
                authors = []
                for author in entry.findall('atom:author', ns):
                    name_elem = author.find('atom:name', ns)
                    if name_elem is not None:
                        authors.append(name_elem.text)
                authors_str = ", ".join(authors)
                
                # Abstract
                summary_elem = entry.find('atom:summary', ns)
                abstract = summary_elem.text.strip() if summary_elem is not None else ""
                
                # Publication date
                published_elem = entry.find('atom:published', ns)
                pub_date = published_elem.text[:10] if published_elem is not None else ""
                
                # Category
                category_elem = entry.find('atom:category', ns)
                category = category_elem.get('term') if category_elem is not None else ""
                
                result = {
                    "id": arxiv_id,
                    "title": title,
                    "authors": authors_str,
                    "abstract": abstract,
                    "publication_date": pub_date,
                    "journal": f"arXiv preprint ({category})",
                    "url": f"https://arxiv.org/abs/{arxiv_id}",
                    "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                    "source": "arxiv"
                }
                
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error parsing arXiv response: {e}")
            return []
    
    def _filter_by_date(self, results: List[Dict[str, Any]], 
                       start_date: Optional[str], 
                       end_date: Optional[str]) -> List[Dict[str, Any]]:
        """
        Filter results by date range
        
        Args:
            results: List of results
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Filtered results
        """
        filtered = []
        
        for result in results:
            pub_date = result.get("publication_date", "")
            
            if start_date and pub_date < start_date:
                continue
            if end_date and pub_date > end_date:
                continue
            
            filtered.append(result)
        
        return filtered

