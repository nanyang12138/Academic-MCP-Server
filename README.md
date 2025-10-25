# Academic MCP Server

🔍 A unified Model Context Protocol (MCP) server that provides AI assistants access to multiple academic databases through a single, consistent interface.

## 🌟 Features

### Supported Databases

- **PubMed** 🏥 - Biomedical and life sciences literature (NCBI)
- **bioRxiv** 🧬 - Biology preprints
- **medRxiv** 💊 - Medical preprints  
- **arXiv** 🔬 - Physics, mathematics, computer science, and more
- **Semantic Scholar** 🤖 - AI-powered academic search across disciplines
- **Sci-Hub** 📚 - Comprehensive academic paper access and download

### Core Capabilities

- ✅ **Unified Search**: Search across all databases with a single query
- ✅ **Advanced Filtering**: Filter by title, author, date, journal, and more
- ✅ **Metadata Access**: Retrieve detailed paper information
- ✅ **PDF Download**: Download open access papers when available
- ✅ **Deep Analysis**: Generate comprehensive paper analysis prompts
- ✅ **Local PDF Analysis**: Support for both local and online PDF file analysis
- ✅ **Citation Network Analysis**: Analyze paper citation relationships and impact
- ✅ **Complete Research Workflow**: One-click retrieve→analyze→read→summarize
- ✅ **Standardized Output**: Consistent data format across all sources

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- MCP library
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

1. **`academic`** - Basic search, metadata retrieval, and PDF downloads across 6 databases (PubMed, bioRxiv, medRxiv, arXiv, Semantic Scholar, Sci-Hub)
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
# Returns: ["pubmed", "biorxiv", "medrxiv", "arxiv", "semantic_scholar", "scihub"]
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
- `source` (str): "all", "pubmed", "biorxiv", "medrxiv", "arxiv", "semantic_scholar", or "scihub"
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

#### 8. `extract_text_from_pdf`
Extract text content from PDF (supports both local and online URLs).

**Parameters:**
- `pdf_path` (str): PDF path (local or URL)
- `extract_sections` (bool): Whether to extract by sections
- `page_range` (tuple, optional): Page range, e.g., (1, 10) for pages 1-10

#### 9. `batch_analyze_local_papers`
Batch analyze all PDF papers in a folder (local folders only).

**Parameters:**
- `folder_path` (str): Folder path
- `max_papers` (int): Maximum number of papers to analyze (default: 10)
- `file_pattern` (str): File matching pattern (default: "*.pdf")

#### 10. `compare_papers`
Compare multiple papers.

**Parameters:**
- `paper_ids` (list): List of paper IDs to compare (2-5 papers)
- `comparison_aspects` (list, optional): Comparison dimensions - "methodology", "findings", "impact", "timeline"

#### 11. `extract_key_information`
Extract key information from papers.

**Parameters:**
- `paper_id` (str): Paper identifier
- `source` (str): Data source (default: "semantic_scholar")
- `info_types` (list, optional): List of information types to extract
  - "methodology": Research methods
  - "findings": Main findings
  - "limitations": Study limitations
  - "datasets": Used datasets
  - "metrics": Evaluation metrics
  - "contributions": Main contributions

#### 12. `generate_paper_summary`
Automatically generate paper summaries.

**Parameters:**
- `paper_id` (str): Paper identifier
- `source` (str): Data source (default: "semantic_scholar")
- `summary_type` (str): Summary type
  - "brief": Brief summary (100-200 words)
  - "comprehensive": Comprehensive summary (500-800 words)
  - "technical": Technical details summary
  - "layman": Easy-to-understand version

#### 13. `extract_pdf_fulltext`
Extract full text content from PDF.

**Parameters:**
- `pdf_url` (str): PDF file URL
- `extract_sections` (bool): Whether to identify and extract sections (default: true)

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

### Dual Server Design

This project provides **two complementary MCP servers**:

1. **`academic_server.py`** - Core search and retrieval functionality
2. **`academic_research_advanced.py`** - Advanced analysis and research workflows

### Project Structure

```
Academic-MCP-Server/
├── academic_server.py          # Main MCP server (basic search)
├── academic_research_advanced.py # Advanced research server
├── adapters/                   # Database adapters
│   ├── base_adapter.py        # Abstract base class
│   ├── pubmed_adapter.py      # PubMed wrapper
│   ├── biorxiv_adapter.py     # bioRxiv/medRxiv
│   ├── arxiv_adapter.py       # arXiv
│   ├── semantic_scholar_adapter.py
│   └── scihub_adapter.py      # Sci-Hub
├── utils/                      # Helper functions
│   ├── helpers.py             # General utilities
│   └── pubmed_utils.py        # PubMed-specific utilities
├── requirements.txt           # Dependencies
└── README.md / README_CN.md   # Documentation
```

### Adapter Pattern

Each database is wrapped in an adapter that implements a common interface:

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
- Analyze local PDF collections
- Perform comprehensive citation network analysis
- Generate automated paper summaries

### For AI Assistants
- Access comprehensive academic knowledge
- Provide up-to-date research information
- Help with citation and reference management
- Analyze research trends and findings
- Process and explain figures from academic papers
- Conduct complete research workflows automatically

## ⚠️ Limitations & Notes

### API Rate Limits
- **PubMed**: No API key required, but rate-limited
- **bioRxiv/medRxiv**: No authentication required
- **arXiv**: Rate-limited (1 request per 3 seconds recommended)
- **Semantic Scholar**: Free tier has rate limits; get API key for higher limits at https://www.semanticscholar.org/product/api
- **Sci-Hub**: No authentication required; use responsibly

### PDF Availability
- **PubMed**: Only PMC open access articles
- **bioRxiv/medRxiv**: All articles are open access
- **arXiv**: All articles are open access
- **Semantic Scholar**: Depends on publisher policies
- **Sci-Hub**: Wide coverage of academic papers (use for research purposes only)

### Local PDF Support
- **Full text extraction**: Extract complete text from local or online PDFs
- **Figure analysis**: List and explain figures from PDF papers
- **Section parsing**: Automatically identify and extract paper sections
- **Batch processing**: Analyze multiple PDFs in a folder simultaneously

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
- Sci-Hub MCP Server ([JackKuo666/Sci-Hub-MCP-Server](https://github.com/JackKuo666/Sci-Hub-MCP-Server))
- FastMCP framework

## ⚠️ Disclaimer

The Sci-Hub integration is provided for **research and educational purposes only**. Users are responsible for complying with copyright laws and institutional policies in their jurisdiction. The authors do not endorse or encourage copyright infringement. Please support publishers and authors by obtaining papers through legitimate channels when possible.

## 📊 Project Statistics

- **Supported Databases**: 6 (PubMed, bioRxiv, medRxiv, arXiv, Semantic Scholar, Sci-Hub)
- **MCP Servers**: 2 (academic, academic-research)
- **Basic MCP Tools**: 6
- **Advanced Research Tools**: 15+
- **Lines of Code**: ~3,000
- **Supported Formats**: PDF, metadata, citations, full-text analysis
- **PDF Support**: Both local files and online URLs

## 🚀 Enhanced Features

### Advanced Research Capabilities
- **Citation Network Analysis**: Understand paper relationships and impact
- **Automated Summarization**: Generate summaries in multiple styles
- **Key Information Extraction**: Extract methodology, findings, limitations
- **Complete Research Workflows**: One-click research from topic to summary

### PDF Processing
- **Local and Online Support**: Process PDFs from local storage or URLs
- **Figure Explanation**: AI-powered figure analysis and explanation
- **Section Recognition**: Automatic identification of paper sections
- **Batch Analysis**: Process multiple papers simultaneously

### Smart Search Features
- **Concurrent Database Search**: Search all databases simultaneously
- **Intelligent Result Merging**: Deduplicate and rank results
- **Advanced Filtering**: Multi-parameter search with date ranges
- **Source-Specific Optimization**: Tailored search for each database

## 📞 Support

For issues or questions:
1. Check the documentation above
2. Review error messages in logs
3. Ensure all dependencies are installed
4. Verify your MCP configuration

---

**Happy researching! 📚🔬**

