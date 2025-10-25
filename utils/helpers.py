"""
Helper functions for the Academic MCP Server
"""

from typing import List, Dict, Any


def format_search_results(results: List[Dict[str, Any]], max_abstract_length: int = 500) -> List[Dict[str, Any]]:
    """
    Format search results for display
    
    Args:
        results: List of search results
        max_abstract_length: Maximum length of abstract to display
        
    Returns:
        Formatted results
    """
    formatted = []
    
    for result in results:
        formatted_result = result.copy()
        
        # Truncate abstract if too long
        abstract = result.get("abstract", "")
        if len(abstract) > max_abstract_length:
            formatted_result["abstract"] = abstract[:max_abstract_length] + "..."
        
        formatted.append(formatted_result)
    
    return formatted


def merge_results_from_sources(results_dict: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Merge results from multiple sources, removing duplicates by DOI/title
    
    Args:
        results_dict: Dictionary mapping source names to their results
        
    Returns:
        Merged list of results
    """
    merged = []
    seen_ids = set()
    seen_titles = set()
    
    for source, results in results_dict.items():
        for result in results:
            result_id = result.get("id", "")
            title = result.get("title", "").lower().strip()
            
            # Skip if we've seen this paper already
            if result_id and result_id in seen_ids:
                continue
            if title and title in seen_titles:
                continue
            
            merged.append(result)
            
            if result_id:
                seen_ids.add(result_id)
            if title:
                seen_titles.add(title)
    
    return merged


def validate_source(source: str, available_sources: List[str]) -> bool:
    """
    Validate that a source name is valid
    
    Args:
        source: Source name to validate
        available_sources: List of available source names
        
    Returns:
        True if valid, False otherwise
    """
    return source in available_sources or source == "all"

