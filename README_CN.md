# Academic MCP Server - 统一学术文献搜索服务器

🔍 一个统一的模型上下文协议(MCP)服务器，让AI助手能够通过单一、一致的接口访问多个学术数据库。

## 🌟 核心特性

### 支持的数据库

- **PubMed** 🏥 - 生物医学和生命科学文献（NCBI）
- **bioRxiv** 🧬 - 生物学预印本
- **medRxiv** 💊 - 医学预印本  
- **arXiv** 🔬 - 物理、数学、计算机科学等预印本
- **Semantic Scholar** 🤖 - AI驱动的跨学科学术搜索
- **Sci-Hub** 📚 - 全面的学术论文获取和下载

### 主要功能

- ✅ **统一搜索**：一次查询搜索所有数据库
- ✅ **高级过滤**：按标题、作者、日期、期刊等筛选
- ✅ **元数据访问**：获取详细的论文信息
- ✅ **PDF下载**：下载开放获取的论文
- ✅ **深度分析**：生成全面的论文分析提示
- ✅ **本地PDF分析**：支持本地和在线PDF文件分析
- ✅ **引用网络分析**：分析论文引用关系和影响力
- ✅ **完整研究工作流**：一键完成检索→分析→阅读→总结
- ✅ **标准化输出**：所有数据源的一致数据格式

## 🚀 快速开始

### 前提条件

- Python 3.10+
- MCP库
- 互联网连接

### 安装步骤

1. 克隆或下载此仓库
2. 创建虚拟环境：`python -m venv venv`
3. 激活虚拟环境：
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. 安装依赖：`pip install -r requirements.txt`

**注意：** 所有PubMed功能已完全集成到本地，无需外部依赖！

### MCP配置

本项目提供**两个MCP服务器**，功能互补：

1. **`academic`** - 基础搜索、元数据检索和PDF下载（6个数据库：PubMed、bioRxiv、medRxiv、arXiv、Semantic Scholar、Sci-Hub）
2. **`academic-research`** - 高级功能：引用分析、影响力评估、本地PDF分析、完整研究工作流

将以下配置添加到MCP设置文件（`~/.cursor/mcp.json` 或 `C:\Users\YOUR_USERNAME\.cursor\mcp.json`）：

**Windows配置：**
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

**Mac/Linux配置：**
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

**注意：** 请将 `YOUR_USERNAME` 和 `path/to` 替换为实际路径。

### 如何使用

**重启Cursor后**，您可以直接向AI助手提出以下请求：

#### 示例1：搜索所有数据库
```
帮我搜索最新的UCAR-T相关文献，从所有数据库中查找
```

#### 示例2：搜索特定数据库
```
在bioRxiv中搜索关于CRISPR的最新预印本
```

#### 示例3：高级搜索
```
搜索arXiv上Hinton教授关于神经网络的论文，2020年以后的
```

#### 示例4：下载论文
```
帮我下载arXiv论文2301.00001的PDF
```

## 📊 可用的MCP工具

### 服务器：`academic`（基础搜索与检索）

#### 1. search_papers
按关键词搜索论文

**参数：**
- `keywords` (str): 搜索查询词
- `source` (str): 数据源 - "all", "pubmed", "biorxiv", "medrxiv", "arxiv", "semantic_scholar", "scihub"
- `num_results` (int): 每个数据源返回的结果数量（默认：10）

**示例：**
```python
search_papers(keywords="机器学习", source="all", num_results=15)
```

#### 2. search_papers_advanced
多参数高级搜索

**参数：**
- `title` (str, 可选): 在标题中搜索
- `author` (str, 可选): 作者名
- `journal` (str, 可选): 期刊名
- `start_date` (str, 可选): 开始日期
- `end_date` (str, 可选): 结束日期
- `term` (str, 可选): 通用搜索词
- `source` (str): 数据源
- `num_results` (int): 结果数量

**示例：**
```python
search_papers_advanced(
    title="CAR-T",
    author="Wang",
    journal="Nature",
    start_date="2024/01/01",
    source="pubmed",
    num_results=10
)
```

#### 3. get_paper_metadata
获取特定论文的详细元数据

**参数：**
- `identifier` (str): 论文标识符（PMID、DOI、arXiv ID等）
- `source` (str): 数据源

**示例：**
```python
get_paper_metadata(identifier="40883768", source="pubmed")
```

#### 4. download_paper_pdf
下载论文PDF

**参数：**
- `identifier` (str): 论文标识符
- `source` (str): 数据源

**示例：**
```python
download_paper_pdf(identifier="2301.00001", source="arxiv")
```

#### 5. list_available_sources
列出所有可用的数据源

**返回：**
```python
["pubmed", "biorxiv", "medrxiv", "arxiv", "semantic_scholar", "scihub"]
```

#### 6. deep_paper_analysis
生成全面的论文分析提示

**参数：**
- `identifier` (str): 论文标识符
- `source` (str): 数据源

### 服务器：`academic-research`（高级分析与研究）

#### 1. analyze_citation_network
分析论文的引用网络

**参数：**
- `paper_id` (str): 论文标识符（DOI、PMID等）
- `source` (str): 数据源（默认："semantic_scholar"）
- `max_depth` (int): 网络深度1-3层（默认：2）

#### 2. evaluate_paper_impact
评估论文的学术影响力

**参数：**
- `paper_id` (str): 论文标识符
- `source` (str): 数据源（默认："semantic_scholar"）

#### 3. recommend_related_papers
基于多种策略推荐相关文献

**参数：**
- `paper_id` (str): 源论文标识符
- `source` (str): 数据源（默认："semantic_scholar"）
- `num_recommendations` (int): 推荐数量（默认：10）
- `strategy` (str): 推荐策略 - "comprehensive"、"citations"、"similar"或"influential"

#### 4. research_workflow_complete
**⭐ 推荐核心功能** - 完整研究工作流：检索 → 分析 → 阅读 → 总结

**参数：**
- `topic` (str): 研究主题（例如："CRISPR基因编辑"）
- `num_papers` (int): 检索论文数量（默认：5）
- `include_analysis` (bool): 包含深度分析（默认：true）
- `include_summary` (bool): 包含自动摘要（默认：true）

#### 5. analyze_local_paper
全面分析本地或在线PDF论文

**参数：**
- `pdf_path` (str): PDF文件路径（本地或URL）
- `include_figures` (bool): 分析图表（默认：true）
- `include_summary` (bool): 生成摘要（默认：true）

#### 6. list_all_figures
列出PDF论文中的所有图表

**参数：**
- `pdf_path` (str): PDF文件路径（本地或URL）

#### 7. explain_specific_figure
解释PDF中的特定图表

**参数：**
- `pdf_path` (str): PDF文件路径（本地或URL）
- `figure_number` (int): 图表编号（例如：1、2、3）
- `provide_context` (bool): 包含上下文段落（默认：true）

#### 8. extract_text_from_pdf
从PDF提取文本内容（支持本地和在线URL）

**参数：**
- `pdf_path` (str): PDF路径（本地或URL）
- `extract_sections` (bool): 是否按章节提取
- `page_range` (tuple, 可选): 页面范围，如 (1, 10) 表示第1-10页

#### 9. batch_analyze_local_papers
批量分析文件夹中的所有PDF论文（仅支持本地文件夹）

**参数：**
- `folder_path` (str): 文件夹路径
- `max_papers` (int): 最多分析的论文数量（默认：10）
- `file_pattern` (str): 文件匹配模式（默认："*.pdf"）

#### 10. compare_papers
对比多篇论文

**参数：**
- `paper_ids` (list): 要对比的论文ID列表（2-5篇）
- `comparison_aspects` (list, 可选): 对比维度 - "methodology"、"findings"、"impact"、"timeline"

#### 11. extract_key_information
从论文中抽取关键信息

**参数：**
- `paper_id` (str): 论文标识符
- `source` (str): 数据源（默认："semantic_scholar"）
- `info_types` (list, 可选): 要抽取的信息类型列表
  - "methodology": 研究方法
  - "findings": 主要发现
  - "limitations": 研究局限
  - "datasets": 使用的数据集
  - "metrics": 评估指标
  - "contributions": 主要贡献

#### 12. generate_paper_summary
自动生成论文摘要

**参数：**
- `paper_id` (str): 论文标识符
- `source` (str): 数据源（默认："semantic_scholar"）
- `summary_type` (str): 摘要类型
  - "brief": 简短摘要（100-200字）
  - "comprehensive": 综合摘要（500-800字）
  - "technical": 技术细节摘要
  - "layman": 通俗易懂版本

#### 13. extract_pdf_fulltext
从PDF中提取全文内容

**参数：**
- `pdf_url` (str): PDF文件URL
- `extract_sections` (bool): 是否识别并提取各个章节（默认：true）

## 📈 使用场景

### 场景1：文献综述
```
帮我搜索所有数据库中关于"免疫治疗"的最新文献，每个数据库找10篇
```

### 场景2：追踪最新研究
```
搜索bioRxiv和medRxiv上最近6个月关于新冠病毒的预印本
```

### 场景3：跨学科研究
```
同时在arXiv和Semantic Scholar中搜索"深度学习在蛋白质结构预测中的应用"
```

### 场景4：特定作者追踪
```
在所有数据库中查找作者"Zhang Wei"发表的关于肿瘤免疫的论文
```

### 场景5：获取论文详情
```
获取PubMed文章40883768的完整信息
```

## 🎯 数据源选择指南

| 数据源 | 适用领域 | 特点 | 开放程度 |
|--------|----------|------|----------|
| **pubmed** | 生物医学、医学 | 权威、同行评审 | 部分开放 |
| **biorxiv** | 生物学 | 预印本、最新 | 全部开放 |
| **medrxiv** | 医学、临床 | 预印本、最新 | 全部开放 |
| **arxiv** | 物理、数学、CS | 预印本、最新 | 全部开放 |
| **semantic_scholar** | 全学科 | AI驱动、引用分析 | 取决于来源 |
| **scihub** | 全学科 | 广泛覆盖、PDF下载 | 全面覆盖 |
| **all** | 全部 | 一次搜索所有 | 混合 |

## 📋 返回数据格式

所有搜索结果采用统一的标准格式：

```python
{
    "id": "唯一标识符（PMID、DOI、arXiv ID等）",
    "title": "论文标题",
    "authors": "作者列表（逗号分隔）",
    "abstract": "论文摘要",
    "publication_date": "发表日期",
    "journal": "期刊或来源名称",
    "url": "论文链接",
    "pdf_url": "PDF链接（如有）",
    "source": "数据源（pubmed/biorxiv/arxiv等）"
}
```

## 🔧 高级配置

### Semantic Scholar API密钥（可选）

免费API有速率限制。如需更高配额：

1. 访问 https://www.semanticscholar.org/product/api
2. 注册并获取免费API密钥
3. 编辑 `academic_server.py` 第35行：

```python
"semantic_scholar": SemanticScholarAdapter(api_key="YOUR_API_KEY_HERE")
```

## 📁 项目架构

```
Academic-MCP-Server/
├── academic_server.py          # 主MCP服务器
├── academic_research_advanced.py # 高级研究服务器
├── adapters/                   # 数据库适配器
│   ├── base_adapter.py        # 抽象基类
│   ├── pubmed_adapter.py      # PubMed适配器
│   ├── biorxiv_adapter.py     # bioRxiv/medRxiv
│   ├── arxiv_adapter.py       # arXiv
│   ├── semantic_scholar_adapter.py
│   └── scihub_adapter.py      # Sci-Hub适配器
├── utils/                      # 工具函数
├── requirements.txt            # 依赖清单
├── README.md                   # 英文文档
└── README_CN.md                # 本文件
```

## 🐛 故障排除

### 问题：AI无法调用工具

**解决方案：**
1. 重启Cursor
2. 检查MCP配置文件 `mcp.json`
3. 查看Cursor的MCP日志

### 问题：PubMed适配器失败

**解决方案：** 
- PubMed功能已完全整合，无需外部目录
- 运行测试验证： `.\venv\Scripts\python.exe test_server.py`
- 检查网络连接是否正常

### 问题：搜索超时

**原因：** 网络问题或API限制

**解决方案：**
- 检查网络连接
- 减少 `num_results` 参数
- 稍后重试
- 使用特定数据源而非"all"

### 问题：bioRxiv/medRxiv搜索结果少

**原因：** 这些数据库的搜索API需要遍历时间范围

**说明：** 默认搜索最近1年的数据，这是正常的

## ⚡ 性能提示

1. **首次搜索较慢** - 各API需要初始化
2. **并发搜索优化** - `source="all"` 现在真正并发搜索所有数据库（使用 `asyncio.gather`）
3. **超时保护** - 每个数据源有30秒超时限制，避免某个源卡住影响整体
4. **合理设置结果数** - 建议10-20篇，过多会影响速度
5. **指定数据源更快** - 如果知道目标数据库，使用具体的 `source` 会更快

## 🔍 搜索技巧

### 1. 关键词优化
- ✅ 使用专业术语："CAR-T"而非"嵌合抗原受体"
- ✅ 英文搜索效果更好
- ✅ 使用引号精确匹配："machine learning"

### 2. 时间范围
- PubMed使用 `YYYY/MM/DD` 格式
- 其他数据库使用 `YYYY-MM-DD` 格式

### 3. 数据源选择
- 生物医学 → pubmed, biorxiv, medrxiv
- 计算机科学 → arxiv, semantic_scholar
- 物理数学 → arxiv
- 跨学科 → semantic_scholar, all

## 📚 更多资源

- **快速入门**：`QUICKSTART.md`
- **部署总结**：`DEPLOYMENT_SUMMARY.md`
- **测试脚本**：运行 `.\venv\Scripts\python.exe test_server.py`

## 🎯 完全独立部署

Academic MCP Server **完全独立**，不需要任何外部依赖：

### 特点
- ✅ 所有PubMed功能已集成到本地
- ✅ 单一目录，简洁部署
- ✅ 5个数据库统一管理
- ✅ 不依赖外部PubMed-MCP-Server

### 使用方式
- 搜索PubMed → 使用 academic 服务器，source="pubmed"
- 搜索所有数据库 → 使用 academic 服务器，source="all"
- 一个服务器，五个数据库！

## 🎓 实战示例

### 示例1：查找UCAR-T最新进展
```
帮我在所有数据库中搜索UCAR-T的最新研究，重点关注2024年以后的文章
```

AI会：
1. 调用 `search_papers(keywords="UCAR-T", source="all")`
2. 从5个数据库获取结果
3. 自动去重和整理
4. 按相关性排序返回

### 示例2：追踪特定作者
```
搜索Wang教授在Nature发表的关于CAR-T的论文
```

AI会：
```python
search_papers_advanced(
    title="CAR-T",
    author="Wang",
    journal="Nature",
    source="pubmed"
)
```

### 示例3：下载论文合集
```
帮我下载以下arXiv论文：2301.00001, 2302.00123, 2303.00456
```

AI会依次调用：
```python
download_paper_pdf("2301.00001", "arxiv")
download_paper_pdf("2302.00123", "arxiv")
download_paper_pdf("2303.00456", "arxiv")
```

## 🌍 数据库覆盖范围

- 🇺🇸 PubMed - 美国国家医学图书馆
- 🌐 bioRxiv - Cold Spring Harbor Laboratory
- 🌐 medRxiv - Cold Spring Harbor Laboratory
- 🌐 arXiv - Cornell University
- 🌐 Semantic Scholar - Allen Institute for AI

## ✨ 核心优势

1. **一站式搜索** - 无需切换多个网站
2. **AI集成** - 直接在对话中获取文献
3. **标准化数据** - 统一格式便于处理
4. **开放获取** - 优先开放文献，可直接下载
5. **持续更新** - 包含最新预印本
6. **跨学科** - 覆盖生物医学到计算机科学

## 📊 统计数据

- **数据库数量**：6个（PubMed、bioRxiv、medRxiv、arXiv、Semantic Scholar、Sci-Hub）
- **MCP服务器数量**：2个（academic、academic-research）
- **基础MCP工具数量**：6个
- **高级研究工具数量**：15个
- **代码行数**：~3000行
- **支持的文献格式**：PDF、元数据、引用、全文分析
- **PDF支持**：本地文件和在线URL双重支持

## 💡 使用建议

1. **重启Cursor** - 配置更新后需要重启
2. **自然语言** - 直接用中文描述需求即可
3. **明确来源** - 说明想搜索哪个数据库
4. **合理范围** - 指定时间范围获得更精准结果
5. **保存结果** - 重要论文信息及时保存

## 🎉 开始使用

**现在就重启Cursor，开始您的学术探索之旅！**

尝试说：
```
帮我搜索最新的UCAR-T文献，从所有数据库中查找
```

或者：
```
在bioRxiv中找最近3个月关于mRNA疫苗的预印本
```

## 🙏 致谢

- PubMed-MCP-Server - 原始PubMed集成
- NCBI E-utilities
- bioRxiv/medRxiv API
- arXiv API
- Semantic Scholar API
- Sci-Hub MCP Server ([JackKuo666/Sci-Hub-MCP-Server](https://github.com/JackKuo666/Sci-Hub-MCP-Server))
- FastMCP框架

## ⚠️ 免责声明

Sci-Hub集成**仅供研究和教育目的使用**。用户有责任遵守其所在地区的版权法和机构政策。作者不支持或鼓励侵犯版权。在可能的情况下，请通过合法渠道获取论文以支持出版商和作者。

---

**祝您研究顺利！📚🔬🎓**

