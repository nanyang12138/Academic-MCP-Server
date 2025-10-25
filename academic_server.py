"""
Academic MCP Server
Unified interface for multiple academic databases (PubMed, bioRxiv, arXiv, Semantic Scholar)
"""

from typing import Any, List, Dict, Optional, Union
import asyncio
import logging
from mcp.server.fastmcp import FastMCP

# Import adapters
from adapters.pubmed_adapter import PubMedAdapter
from adapters.biorxiv_adapter import BioRxivAdapter
from adapters.arxiv_adapter import ArXivAdapter
from adapters.semantic_scholar_adapter import SemanticScholarAdapter

# Import utilities
from utils.helpers import merge_results_from_sources

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FastMCP server
mcp = FastMCP("academic")

# Initialize all adapters
adapters = {
    "pubmed": PubMedAdapter(),
    "biorxiv": BioRxivAdapter(server="biorxiv"),
    "medrxiv": BioRxivAdapter(server="medrxiv"),
    "arxiv": ArXivAdapter(),
    "semantic_scholar": SemanticScholarAdapter()  # Add API key if you have one
}

AVAILABLE_SOURCES = list(adapters.keys())


@mcp.tool()
async def search_papers(
    keywords: str,
    source: str = "all",
    num_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Search for academic papers across multiple databases.
    
    Args:
        keywords: Search query string (e.g., "UCAR-T", "machine learning")
        source: Data source to search. Options: "all", "pubmed", "biorxiv", "medrxiv", "arxiv", "semantic_scholar"
        num_results: Number of results to return per source (default: 10)
    
    Returns:
        List of dictionaries containing paper information with standardized fields:
        - id: Unique identifier (PMID, DOI, arXiv ID, etc.)
        - title: Paper title
        - authors: Author names
        - abstract: Paper abstract
        - publication_date: Publication date
        - journal: Journal or venue name
        - url: Link to paper
        - pdf_url: Link to PDF if available
        - source: Database source
    """
    logging.info(f"Searching for papers with keywords: '{keywords}', source: {source}, num_results: {num_results}")
    
    try:
        if source == "all":
            # Search all sources
            all_results = {}
            
            for source_name, adapter in adapters.items():
                try:
                    results = await asyncio.to_thread(
                        adapter.search_by_keywords,
                        keywords,
                        num_results
                    )
                    if results:
                        all_results[source_name] = results
                        logging.info(f"Found {len(results)} results from {source_name}")
                except Exception as e:
                    logging.error(f"Error searching {source_name}: {e}")
            
            # Merge results from all sources
            merged = merge_results_from_sources(all_results)
            logging.info(f"Total unique results: {len(merged)}")
            return merged
        
        elif source in adapters:
            # Search specific source
            adapter = adapters[source]
            results = await asyncio.to_thread(
                adapter.search_by_keywords,
                keywords,
                num_results
            )
            logging.info(f"Found {len(results)} results from {source}")
            return results
        
        else:
            error_msg = f"Invalid source '{source}'. Available sources: {', '.join(AVAILABLE_SOURCES)}, 'all'"
            logging.error(error_msg)
            return [{"error": error_msg}]
    
    except Exception as e:
        error_msg = f"An error occurred while searching: {str(e)}"
        logging.error(error_msg)
        return [{"error": error_msg}]


@mcp.tool()
async def search_papers_advanced(
    title: Optional[str] = None,
    author: Optional[str] = None,
    journal: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    term: Optional[str] = None,
    source: str = "all",
    num_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Perform advanced search for academic papers with multiple parameters.
    
    Args:
        title: Search in paper titles
        author: Author name
        journal: Journal name (primarily for PubMed)
        start_date: Start date (format varies by source: PubMed uses YYYY/MM/DD, others use YYYY-MM-DD)
        end_date: End date
        term: General search term
        source: Data source. Options: "all", "pubmed", "biorxiv", "medrxiv", "arxiv", "semantic_scholar"
        num_results: Number of results to return per source
    
    Returns:
        List of dictionaries containing paper information
    """
    logging.info(f"Advanced search - source: {source}, title: {title}, author: {author}, journal: {journal}")
    
    try:
        search_params = {
            "title": title,
            "author": author,
            "journal": journal,
            "start_date": start_date,
            "end_date": end_date,
            "term": term,
            "num_results": num_results
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        
        if source == "all":
            all_results = {}
            
            for source_name, adapter in adapters.items():
                try:
                    results = await asyncio.to_thread(
                        adapter.search_advanced,
                        **search_params
                    )
                    if results:
                        all_results[source_name] = results
                        logging.info(f"Found {len(results)} results from {source_name}")
                except Exception as e:
                    logging.error(f"Error in advanced search for {source_name}: {e}")
            
            merged = merge_results_from_sources(all_results)
            return merged
        
        elif source in adapters:
            adapter = adapters[source]
            results = await asyncio.to_thread(
                adapter.search_advanced,
                **search_params
            )
            return results
        
        else:
            return [{"error": f"Invalid source '{source}'. Available: {', '.join(AVAILABLE_SOURCES)}, 'all'"}]
    
    except Exception as e:
        return [{"error": f"Error in advanced search: {str(e)}"}]


@mcp.tool()
async def get_paper_metadata(
    identifier: str,
    source: str
) -> Dict[str, Any]:
    """
    Get detailed metadata for a specific paper.
    
    Args:
        identifier: Paper identifier (PMID for PubMed, DOI for bioRxiv, arXiv ID for arXiv, etc.)
        source: Data source. Options: "pubmed", "biorxiv", "medrxiv", "arxiv", "semantic_scholar"
    
    Returns:
        Dictionary containing detailed paper metadata
    
    Examples:
        - PubMed: get_paper_metadata("40883768", "pubmed")
        - bioRxiv: get_paper_metadata("10.1101/2024.01.001", "biorxiv")
        - arXiv: get_paper_metadata("2301.00001", "arxiv")
    """
    logging.info(f"Fetching metadata for {source}:{identifier}")
    
    try:
        if source not in adapters:
            return {"error": f"Invalid source '{source}'. Available: {', '.join(AVAILABLE_SOURCES)}"}
        
        adapter = adapters[source]
        metadata = await asyncio.to_thread(adapter.get_metadata, identifier)
        
        if metadata:
            logging.info(f"Successfully retrieved metadata for {identifier}")
        
        return metadata
    
    except Exception as e:
        return {"error": f"Error fetching metadata: {str(e)}"}


@mcp.tool()
async def download_paper_pdf(
    identifier: str,
    source: str
) -> str:
    """
    Download PDF for a specific paper.
    
    Args:
        identifier: Paper identifier (PMID, DOI, arXiv ID, etc.)
        source: Data source. Options: "pubmed", "biorxiv", "medrxiv", "arxiv", "semantic_scholar"
    
    Returns:
        Status message indicating success or failure
    
    Note:
        - PubMed: Only open access articles from PMC can be downloaded
        - bioRxiv/medRxiv: All articles are open access
        - arXiv: All articles are open access
        - Semantic Scholar: Availability depends on the paper
    """
    logging.info(f"Attempting to download PDF for {source}:{identifier}")
    
    try:
        if source not in adapters:
            return f"Error: Invalid source '{source}'. Available: {', '.join(AVAILABLE_SOURCES)}"
        
        adapter = adapters[source]
        result = await asyncio.to_thread(adapter.download_pdf, identifier)
        
        return result
    
    except Exception as e:
        return f"Error downloading PDF: {str(e)}"


@mcp.tool()
async def list_available_sources() -> List[str]:
    """
    List all available data sources.
    
    Returns:
        List of available source names
    """
    return AVAILABLE_SOURCES


@mcp.prompt()
async def deep_paper_analysis(
    identifier: str,
    source: str
) -> Dict[str, str]:
    """
    Perform comprehensive analysis of a paper (currently only supports PubMed).
    
    Args:
        identifier: Paper identifier
        source: Data source (currently only "pubmed" is fully supported)
    
    Returns:
        Dictionary containing analysis prompt or error message
    """
    logging.info(f"Performing deep analysis for {source}:{identifier}")
    
    try:
        if source == "pubmed":
            adapter = adapters["pubmed"]
            analysis = await asyncio.to_thread(adapter.deep_analysis, identifier)
            return {"analysis_prompt": analysis}
        else:
            # For other sources, generate basic analysis from metadata
            metadata = await get_paper_metadata(identifier, source)
            
            if "error" in metadata:
                return {"error": metadata["error"]}
            
            analysis_prompt = f"""
As an expert in scientific paper analysis, please provide a comprehensive analysis of the following paper:

Title: {metadata.get('title', 'N/A')}
Authors: {metadata.get('authors', 'N/A')}
Journal/Venue: {metadata.get('journal', 'N/A')}
Publication Date: {metadata.get('publication_date', 'N/A')}
Abstract: {metadata.get('abstract', 'N/A')}

Please address the following aspects in your analysis:

1. Research Background and Significance
2. Main Research Questions or Hypotheses
3. Methodology Overview
4. Key Findings and Results
5. Conclusions and Implications
6. Limitations of the Study
7. Future Research Directions
8. Relationship to Other Studies in the Field
9. Overall Evaluation of the Research

Ensure your analysis is thorough, objective, and based on the information provided.
            """
            
            return {"analysis_prompt": analysis_prompt}
    
    except Exception as e:
        return {"error": f"Error performing analysis: {str(e)}"}


if __name__ == "__main__":
    logging.info("Starting Academic MCP Server")
    logging.info(f"Available sources: {', '.join(AVAILABLE_SOURCES)}")
    
    # Initialize and run the server
    mcp.run(transport='stdio')

