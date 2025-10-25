# Academic MCP Server

🔍 A unified Model Context Protocol (MCP) server that provides AI assistants access to multiple academic databases through a single, consistent interface.

## 🌟 Features

### Supported Databases

- **PubMed** 🏥 - Biomedical and life sciences literature (NCBI)
- **bioRxiv** 🧬 - Biology preprints
- **medRxiv** 💊 - Medical preprints  
- **arXiv** 🔬 - Physics, mathematics, computer science, and more
- **Semantic Scholar** 🤖 - AI-powered academic search across disciplines

### Core Capabilities

- ✅ **Unified Search**: Search across all databases with a single query
- ✅ **Advanced Filtering**: Filter by title, author, date, journal, and more
- ✅ **Metadata Access**: Retrieve detailed paper information
- ✅ **PDF Download**: Download open access papers when available
- ✅ **Deep Analysis**: Generate comprehensive paper analysis prompts
- ✅ **Standardized Output**: Consistent data format across all sources

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- FastMCP library
- Internet connection

### Installation

**✅ Already Installed!** Your Academic MCP Server is fully configured and ready to use.

If you need to set it up on another machine:

1. Clone or download this repository:
   ```bash
   cd Academic-MCP-Server
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**Note:** All PubMed functionality is integrated locally. No external dependencies required!

### Configuration for Cursor

This project provides **TWO MCP servers** with complementary features:

1. **`academic`** - Basic search, metadata retrieval, and PDF downloads across 5 databases
2. **`academic-research`** - Advanced features including citation analysis, paper impact evaluation, local PDF analysis, and complete research workflows

Add this configuration to your MCP settings file (`~/.cursor/mcp.json` or `C:\Users\YOUR_USERNAME\.cursor\mcp.json`):

**Windows:**
```json
{
  "mcpServers": {
    "academic": {
      "command": "C:\\Users\\YOUR_USERNAME\\path\\to\\Academic-MCP-Server\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YOUR_USERNAME\\path\\to\\Academic-MCP-Server\\academic_server.py"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": []
    },
    "academic-research": {
      "command": "C:\\Users\\YOUR_USERNAME\\path\\to\\Academic-MCP-Server\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YOUR_USERNAME\\path\\to\\Academic-MCP-Server\\academic_research_advanced.py"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Mac/Linux:**
```json
{
  "mcpServers": {
    "academic": {
      "command": "/path/to/Academic-MCP-Server/venv/bin/python",
      "args": [
        "/path/to/Academic-MCP-Server/academic_server.py"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": []
    },
    "academic-research": {
      "command": "/path/to/Academic-MCP-Server/venv/bin/python",
      "args": [
        "/path/to/Academic-MCP-Server/academic_research_advanced.py"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Note:** Replace `YOUR_USERNAME` and `path/to` with your actual paths.

## 📖 Usage

### Search Papers

Search across all databases:
```python
search_papers(
    keywords="UCAR-T",
    source="all",
    num_results=15
)
```

Search specific database:
```python
search_papers(
    keywords="machine learning",
    source="arxiv",
    num_results=10
)
```

### Advanced Search

```python
search_papers_advanced(
    title="neural networks",
    author="Hinton",
    start_date="2020-01-01",
    end_date="2024-12-31",
    source="semantic_scholar",
    num_results=10
)
```

PubMed-specific advanced search:
```python
search_papers_advanced(
    title="CAR-T",
    author="Wang",
    journal="Nature",
    start_date="2024/01/01",  # PubMed uses YYYY/MM/DD
    end_date="2025/12/31",
    source="pubmed",
    num_results=10
)
```

### Get Paper Metadata

```python
# PubMed
get_paper_metadata(identifier="40883768", source="pubmed")

# bioRxiv
get_paper_metadata(identifier="10.1101/2024.01.001", source="biorxiv")

# arXiv
get_paper_metadata(identifier="2301.00001", source="arxiv")

# Semantic Scholar (Paper ID or DOI)
get_paper_metadata(identifier="DOI:10.1038/s41586-020-1234-5", source="semantic_scholar")
```

### Download PDF

```python
download_paper_pdf(identifier="2301.00001", source="arxiv")
```

### List Available Sources

```python
list_available_sources()
# Returns: ["pubmed", "biorxiv", "medrxiv", "arxiv", "semantic_scholar"]
```

### Deep Paper Analysis

```python
deep_paper_analysis(identifier="40883768", source="pubmed")
```

## 🛠 MCP Tools Reference

### Server: `academic` (Basic Search & Retrieval)

#### 1. `search_papers`
Search for papers using keywords.

**Parameters:**
- `keywords` (str): Search query
- `source` (str): "all", "pubmed", "biorxiv", "medrxiv", "arxiv", or "semantic_scholar"
- `num_results` (int): Number of results per source (default: 10)

#### 2. `search_papers_advanced`
Advanced search with multiple filters.

**Parameters:**
- `title` (str, optional): Search in titles
- `author` (str, optional): Author name
- `journal` (str, optional): Journal name
- `start_date` (str, optional): Start date
- `end_date` (str, optional): End date
- `term` (str, optional): General search term
- `source` (str): Database source
- `num_results` (int): Number of results

#### 3. `get_paper_metadata`
Get detailed metadata for a specific paper.

**Parameters:**
- `identifier` (str): Paper ID (PMID, DOI, arXiv ID, etc.)
- `source` (str): Database source

#### 4. `download_paper_pdf`
Download PDF for a paper.

**Parameters:**
- `identifier` (str): Paper ID
- `source` (str): Database source

#### 5. `list_available_sources`
List all available databases.

#### 6. `deep_paper_analysis`
Generate comprehensive analysis prompt.

**Parameters:**
- `identifier` (str): Paper ID
- `source` (str): Database source

### Server: `academic-research` (Advanced Analysis & Research)

#### 1. `analyze_citation_network`
Analyze paper's citation network.

**Parameters:**
- `paper_id` (str): Paper identifier (DOI, PMID, etc.)
- `source` (str): Data source (default: "semantic_scholar")
- `max_depth` (int): Network depth 1-3 layers (default: 2)

#### 2. `evaluate_paper_impact`
Evaluate academic impact of a paper.

**Parameters:**
- `paper_id` (str): Paper identifier
- `source` (str): Data source (default: "semantic_scholar")

#### 3. `recommend_related_papers`
Recommend related papers using multiple strategies.

**Parameters:**
- `paper_id` (str): Source paper identifier
- `source` (str): Data source (default: "semantic_scholar")
- `num_recommendations` (int): Number of recommendations (default: 10)
- `strategy` (str): "comprehensive", "citations", "similar", or "influential"

#### 4. `research_workflow_complete`
**⭐ Recommended Core Feature** - Complete research workflow: retrieve → analyze → read → summarize

**Parameters:**
- `topic` (str): Research topic (e.g., "CRISPR gene editing")
- `num_papers` (int): Number of papers to retrieve (default: 5)
- `include_analysis` (bool): Include deep analysis (default: true)
- `include_summary` (bool): Include auto-summary (default: true)

#### 5. `analyze_local_paper`
Comprehensively analyze local or online PDF papers.

**Parameters:**
- `pdf_path` (str): PDF file path (local or URL)
- `include_figures` (bool): Analyze figures (default: true)
- `include_summary` (bool): Generate summary (default: true)

#### 6. `list_all_figures`
List all figures from a PDF paper.

**Parameters:**
- `pdf_path` (str): PDF file path (local or URL)

#### 7. `explain_specific_figure`
Explain a specific figure from a PDF.

**Parameters:**
- `pdf_path` (str): PDF file path (local or URL)
- `figure_number` (int): Figure number (e.g., 1, 2, 3)
- `provide_context` (bool): Include context paragraphs (default: true)

## 📊 Standardized Output Format

All search results return papers in this standardized format:

```python
{
    "id": "Unique identifier (PMID, DOI, arXiv ID, etc.)",
    "title": "Paper title",
    "authors": "Author names (comma-separated)",
    "abstract": "Paper abstract",
    "publication_date": "Publication date",
    "journal": "Journal or venue name",
    "url": "Link to paper",
    "pdf_url": "PDF link (if available)",
    "source": "Database source (pubmed/biorxiv/arxiv/etc.)"
}
```

Semantic Scholar results include additional fields:
- `citation_count`: Number of citations
- `reference_count`: Number of references
- `fields_of_study`: Research areas

## 🔧 Architecture

### Adapter Pattern

Each database is wrapped in an adapter that implements a common interface:

```
Academic-MCP-Server/
├── academic_server.py          # Main MCP server
├── adapters/                   # Database adapters
│   ├── base_adapter.py        # Abstract base class
│   ├── pubmed_adapter.py      # PubMed wrapper
│   ├── biorxiv_adapter.py     # bioRxiv/medRxiv
│   ├── arxiv_adapter.py       # arXiv
│   └── semantic_scholar_adapter.py
├── utils/                      # Helper functions
└── requirements.txt
```

### Adding New Databases

To add a new database:

1. Create a new adapter in `adapters/`
2. Inherit from `BaseAdapter`
3. Implement all required methods
4. Register in `academic_server.py`

Example:
```python
# adapters/new_database_adapter.py
from .base_adapter import BaseAdapter

class NewDatabaseAdapter(BaseAdapter):
    def search_by_keywords(self, keywords, num_results):
        # Implementation
        pass
    # ... implement other methods

# In academic_server.py
from adapters.new_database_adapter import NewDatabaseAdapter

adapters = {
    # ... existing adapters
    "new_database": NewDatabaseAdapter()
}
```

## 🎯 Use Cases

### For Researchers
- Search across multiple preprint servers simultaneously
- Find papers by specific authors or topics
- Download open access papers automatically
- Generate literature review materials

### For AI Assistants
- Access comprehensive academic knowledge
- Provide up-to-date research information
- Help with citation and reference management
- Analyze research trends and findings

## ⚠️ Limitations & Notes

### API Rate Limits
- **PubMed**: No API key required, but rate-limited
- **bioRxiv/medRxiv**: No authentication required
- **arXiv**: Rate-limited (1 request per 3 seconds recommended)
- **Semantic Scholar**: Free tier has rate limits; get API key for higher limits at https://www.semanticscholar.org/product/api

### PDF Availability
- **PubMed**: Only PMC open access articles
- **bioRxiv/medRxiv**: All articles are open access
- **arXiv**: All articles are open access
- **Semantic Scholar**: Depends on publisher policies

### Date Formats
- **PubMed**: `YYYY/MM/DD`
- **Others**: `YYYY-MM-DD`

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new database adapters
- Improve existing functionality
- Fix bugs
- Enhance documentation

## 📄 License

This project builds upon the PubMed-MCP-Server and follows similar open-source principles.

## 🙏 Acknowledgments

- PubMed-MCP-Server for the original PubMed integration
- NCBI E-utilities
- bioRxiv/medRxiv API
- arXiv API
- Semantic Scholar API
- FastMCP framework

## 📞 Support

For issues or questions:
1. Check the documentation above
2. Review error messages in logs
3. Ensure all dependencies are installed
4. Verify your MCP configuration

---

**Happy researching! 📚🔬**

