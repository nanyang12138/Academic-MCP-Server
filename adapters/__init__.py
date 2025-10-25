"""
Academic MCP Server - Adapters Package
Provides unified interfaces for multiple academic databases
"""

from .base_adapter import BaseAdapter
from .pubmed_adapter import PubMedAdapter
from .biorxiv_adapter import BioRxivAdapter
from .arxiv_adapter import ArXivAdapter
from .semantic_scholar_adapter import SemanticScholarAdapter

__all__ = [
    'BaseAdapter',
    'PubMedAdapter',
    'BioRxivAdapter',
    'ArXivAdapter',
    'SemanticScholarAdapter'
]

