"""
Academic Research Advanced MCP Server
专注于深度分析、智能阅读和完整研究工作流
支持本地PDF和在线URL双重输入
"""

from typing import Any, List, Dict, Optional
import asyncio
import logging
from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import os
from pathlib import Path
import io

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FastMCP server
mcp = FastMCP("academic-research")


# ============================================================================
# 本地文件支持函数
# ============================================================================

def _is_local_path(path: str) -> bool:
    """判断是本地路径还是URL"""
    return os.path.exists(path) or (not path.startswith('http'))


async def _read_pdf_content(path_or_url: str) -> io.BytesIO:
    """
    读取PDF内容（支持本地文件和URL）
    
    Args:
        path_or_url: 本地路径或URL
    
    Returns:
        BytesIO对象
    """
    if _is_local_path(path_or_url):
        # 本地文件
        logging.info(f"Reading local PDF: {path_or_url}")
        with open(path_or_url, 'rb') as f:
            return io.BytesIO(f.read())
    else:
        # URL
        logging.info(f"Downloading PDF from: {path_or_url}")
        response = await asyncio.to_thread(requests.get, path_or_url)
        return io.BytesIO(response.content)


# ============================================================================
# 1. 深度分析工具
# ============================================================================

@mcp.tool()
async def analyze_citation_network(
    paper_id: str,
    source: str = "semantic_scholar",
    max_depth: int = 2
) -> Dict[str, Any]:
    """
    分析论文的引用网络
    
    Args:
        paper_id: 论文标识符（DOI、PMID等）
        source: 数据源（semantic_scholar、pubmed等）
        max_depth: 引用网络深度（1-3层）
    
    Returns:
        引用网络图谱，包括：
        - citations: 引用此论文的文章列表
        - references: 此论文引用的文章列表
        - citation_count: 被引次数
        - influential_citations: 有影响力的引用
        - citation_velocity: 引用速度（近期趋势）
    """
    logging.info(f"Analyzing citation network for {paper_id}")
    
    try:
        # 使用Semantic Scholar API
        if source == "semantic_scholar":
            base_url = "https://api.semanticscholar.org/graph/v1"
            
            # 获取论文基本信息和引用
            fields = "title,citations,references,citationCount,influentialCitationCount,year,authors"
            url = f"{base_url}/paper/{paper_id}?fields={fields}"
            
            response = await asyncio.to_thread(requests.get, url)
            
            if response.status_code == 200:
                data = response.json()
                
                result = {
                    "paper_id": paper_id,
                    "title": data.get("title", ""),
                    "year": data.get("year", ""),
                    "citation_count": data.get("citationCount", 0),
                    "influential_citation_count": data.get("influentialCitationCount", 0),
                    "citations": [],
                    "references": [],
                    "citation_network_stats": {
                        "total_citations": data.get("citationCount", 0),
                        "influential_citations": data.get("influentialCitationCount", 0),
                        "influence_rate": 0
                    }
                }
                
                # 计算影响率
                if result["citation_count"] > 0:
                    result["citation_network_stats"]["influence_rate"] = round(
                        result["influential_citation_count"] / result["citation_count"] * 100, 2
                    )
                
                # 处理引用列表
                if "citations" in data and data["citations"]:
                    for citation in data["citations"][:20]:  # 限制20条
                        result["citations"].append({
                            "paperId": citation.get("paperId", ""),
                            "title": citation.get("title", ""),
                            "year": citation.get("year", "")
                        })
                
                # 处理参考文献列表
                if "references" in data and data["references"]:
                    for ref in data["references"][:20]:
                        result["references"].append({
                            "paperId": ref.get("paperId", ""),
                            "title": ref.get("title", ""),
                            "year": ref.get("year", "")
                        })
                
                return result
            else:
                return {"error": f"API error: {response.status_code}"}
        
        return {"error": f"Unsupported source: {source}"}
        
    except Exception as e:
        return {"error": f"Error analyzing citation network: {str(e)}"}


@mcp.tool()
async def evaluate_paper_impact(
    paper_id: str,
    source: str = "semantic_scholar"
) -> Dict[str, Any]:
    """
    评估论文的学术影响力
    
    Args:
        paper_id: 论文标识符
        source: 数据源
    
    Returns:
        影响力评估报告，包括：
        - citation_metrics: 引用指标
        - h_index_contribution: 对作者h-index的贡献
        - field_impact: 领域影响力
        - temporal_impact: 时间维度影响
        - recommendation_score: 推荐分数（0-100）
    """
    logging.info(f"Evaluating impact for {paper_id}")
    
    try:
        base_url = "https://api.semanticscholar.org/graph/v1"
        fields = "title,year,citationCount,influentialCitationCount,citations,references,fieldsOfStudy,publicationDate"
        url = f"{base_url}/paper/{paper_id}?fields={fields}"
        
        response = await asyncio.to_thread(requests.get, url)
        
        if response.status_code == 200:
            data = response.json()
            
            # 计算各项指标
            citation_count = data.get("citationCount", 0)
            influential_count = data.get("influentialCitationCount", 0)
            year = data.get("year", 2024)
            current_year = 2025
            years_since_pub = max(1, current_year - year)
            
            # 引用速度（每年平均引用数）
            citation_velocity = citation_count / years_since_pub
            
            # 影响力评分（0-100）
            impact_score = min(100, (
                citation_count * 0.3 +
                influential_count * 2 +
                citation_velocity * 5
            ))
            
            result = {
                "paper_id": paper_id,
                "title": data.get("title", ""),
                "citation_metrics": {
                    "total_citations": citation_count,
                    "influential_citations": influential_count,
                    "citation_velocity": round(citation_velocity, 2),
                    "years_since_publication": years_since_pub
                },
                "field_impact": {
                    "fields": data.get("fieldsOfStudy", []),
                    "cross_disciplinary": len(data.get("fieldsOfStudy", [])) > 2
                },
                "recommendation_score": round(impact_score, 2),
                "impact_level": "High" if impact_score > 70 else "Medium" if impact_score > 30 else "Emerging",
                "key_insights": []
            }
            
            # 生成关键见解
            if citation_velocity > 10:
                result["key_insights"].append("高引用速度，表明研究热度持续")
            if influential_count / max(citation_count, 1) > 0.3:
                result["key_insights"].append("高比例有影响力引用，表明研究质量优秀")
            if years_since_pub < 2 and citation_count > 50:
                result["key_insights"].append("新近发表但已获高引用，属于快速崛起的重要研究")
            
            return result
        else:
            return {"error": f"API error: {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Error evaluating impact: {str(e)}"}


@mcp.tool()
async def recommend_related_papers(
    paper_id: str,
    source: str = "semantic_scholar",
    num_recommendations: int = 10,
    strategy: str = "comprehensive"
) -> List[Dict[str, Any]]:
    """
    基于多种策略推荐相关文献
    
    Args:
        paper_id: 源论文标识符
        source: 数据源
        num_recommendations: 推荐数量
        strategy: 推荐策略
            - "comprehensive": 综合推荐（引用+被引+相似）
            - "citations": 基于引用关系
            - "similar": 基于内容相似度
            - "influential": 优先推荐高影响力论文
    
    Returns:
        推荐论文列表，每篇包含推荐理由和相关性分数
    """
    logging.info(f"Recommending papers for {paper_id}, strategy: {strategy}")
    
    try:
        base_url = "https://api.semanticscholar.org/graph/v1"
        
        # 获取源论文信息
        fields = "title,citations,references,fieldsOfStudy"
        url = f"{base_url}/paper/{paper_id}?fields={fields}"
        response = await asyncio.to_thread(requests.get, url)
        
        if response.status_code != 200:
            return [{"error": f"Failed to fetch source paper: {response.status_code}"}]
        
        source_paper = response.json()
        recommendations = []
        seen_ids = set()
        
        # 策略1: 基于引用关系
        if strategy in ["comprehensive", "citations"]:
            # 被引用此论文的重要文章
            if "citations" in source_paper:
                for citation in source_paper["citations"][:5]:
                    paper_id_val = citation.get("paperId")
                    if paper_id_val and paper_id_val not in seen_ids:
                        recommendations.append({
                            "paperId": paper_id_val,
                            "title": citation.get("title", ""),
                            "year": citation.get("year", ""),
                            "relevance_score": 0.85,
                            "recommendation_reason": "引用了您关注的论文"
                        })
                        seen_ids.add(paper_id_val)
            
            # 此论文引用的重要文章
            if "references" in source_paper:
                for ref in source_paper["references"][:5]:
                    paper_id_val = ref.get("paperId")
                    if paper_id_val and paper_id_val not in seen_ids:
                        recommendations.append({
                            "paperId": paper_id_val,
                            "title": ref.get("title", ""),
                            "year": ref.get("year", ""),
                            "relevance_score": 0.80,
                            "recommendation_reason": "被您关注的论文引用"
                        })
                        seen_ids.add(paper_id_val)
        
        # 策略2: 基于Semantic Scholar的推荐API
        try:
            rec_url = f"{base_url}/paper/{paper_id}/recommendations?fields=title,year,citationCount&limit={num_recommendations}"
            rec_response = await asyncio.to_thread(requests.get, rec_url)
            
            if rec_response.status_code == 200:
                rec_data = rec_response.json()
                if "recommendedPapers" in rec_data:
                    for rec_paper in rec_data["recommendedPapers"]:
                        paper_id_val = rec_paper.get("paperId")
                        if paper_id_val and paper_id_val not in seen_ids:
                            recommendations.append({
                                "paperId": paper_id_val,
                                "title": rec_paper.get("title", ""),
                                "year": rec_paper.get("year", ""),
                                "citationCount": rec_paper.get("citationCount", 0),
                                "relevance_score": 0.90,
                                "recommendation_reason": "AI算法推荐的相关研究"
                            })
                            seen_ids.add(paper_id_val)
        except Exception as e:
            logging.warning(f"Recommendation API failed: {e}")
        
        # 根据策略排序
        if strategy == "influential":
            recommendations.sort(key=lambda x: x.get("citationCount", 0), reverse=True)
        else:
            recommendations.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return recommendations[:num_recommendations]
        
    except Exception as e:
        return [{"error": f"Error generating recommendations: {str(e)}"}]


# ============================================================================
# 2. 智能阅读工具
# ============================================================================

@mcp.tool()
async def extract_pdf_fulltext(
    pdf_url: str,
    extract_sections: bool = True
) -> Dict[str, Any]:
    """
    从PDF中提取全文内容
    
    Args:
        pdf_url: PDF文件URL
        extract_sections: 是否识别并提取各个章节
    
    Returns:
        提取的文本内容，包括：
        - full_text: 完整文本
        - sections: 各章节内容（如果extract_sections=True）
        - metadata: PDF元数据
        - word_count: 字数统计
    """
    logging.info(f"Extracting fulltext from PDF: {pdf_url}")
    
    try:
        # 注意：实际使用时需要安装 PyPDF2 或 pdfplumber
        # 这里提供一个简化的实现框架
        
        result = {
            "pdf_url": pdf_url,
            "extraction_status": "partial",
            "message": "PDF extraction requires PyPDF2 or pdfplumber library",
            "suggestion": "Install with: pip install PyPDF2 pdfplumber",
            "sections": {
                "abstract": "",
                "introduction": "",
                "methods": "",
                "results": "",
                "discussion": "",
                "conclusion": "",
                "references": ""
            },
            "full_text": "",
            "word_count": 0,
            "metadata": {}
        }
        
        # TODO: 实际的PDF提取逻辑
        # import PyPDF2
        # response = requests.get(pdf_url)
        # pdf_file = io.BytesIO(response.content)
        # pdf_reader = PyPDF2.PdfReader(pdf_file)
        # ...
        
        return result
        
    except Exception as e:
        return {"error": f"Error extracting PDF: {str(e)}"}


@mcp.tool()
async def generate_paper_summary(
    paper_id: str,
    source: str = "semantic_scholar",
    summary_type: str = "comprehensive"
) -> Dict[str, str]:
    """
    自动生成论文摘要
    
    Args:
        paper_id: 论文标识符
        source: 数据源
        summary_type: 摘要类型
            - "brief": 简短摘要（100-200字）
            - "comprehensive": 综合摘要（500-800字）
            - "technical": 技术细节摘要
            - "layman": 通俗易懂版本
    
    Returns:
        生成的摘要和关键信息
    """
    logging.info(f"Generating summary for {paper_id}, type: {summary_type}")
    
    try:
        base_url = "https://api.semanticscholar.org/graph/v1"
        fields = "title,abstract,year,authors,citationCount,fieldsOfStudy,tldr"
        url = f"{base_url}/paper/{paper_id}?fields={fields}"
        
        response = await asyncio.to_thread(requests.get, url)
        
        if response.status_code == 200:
            data = response.json()
            
            # 提取关键信息
            title = data.get("title", "")
            abstract = data.get("abstract", "")
            tldr_obj = data.get("tldr", {})
            tldr_text = tldr_obj.get("text", "") if tldr_obj else ""
            authors = ", ".join([a.get("name", "") for a in data.get("authors", [])[:3]])
            if len(data.get("authors", [])) > 3:
                authors += " 等"
            year = data.get("year", "")
            fields = ", ".join(data.get("fieldsOfStudy", [])[:3])
            citations = data.get("citationCount", 0)
            
            # 生成不同类型的摘要
            summaries = {
                "brief": f"《{title}》({year})由{authors}发表，研究领域：{fields}。已获{citations}次引用。{tldr_text if tldr_text else (abstract[:100] + '...' if abstract else '暂无摘要')}",
                
                "comprehensive": f"""
📄 论文标题：{title}
👥 作者：{authors}
📅 发表年份：{year}
🔬 研究领域：{fields}
📊 引用次数：{citations}

📝 摘要：
{abstract if abstract else '暂无摘要'}

💡 核心要点：
{tldr_text if tldr_text else '暂无TLDR摘要'}

📈 影响力评估：
- 被引用 {citations} 次
- 研究领域：{fields}
- 发表至今：{2025-int(year) if year else 0} 年
                """.strip(),
                
                "technical": f"""
🔧 技术要点总结

研究主题：{title}

核心贡献：
{abstract if abstract else '暂无摘要'}

技术方法：
{tldr_text if tldr_text else '需要完整文本分析'}

研究领域：{fields}
发表时间：{year}
引用情况：{citations}次引用
                """.strip(),
                
                "layman": f"""
📖 通俗解读

这篇论文研究什么：
{title}

简单来说：
{tldr_text if tldr_text else (abstract[:200] + '...' if abstract else '暂无摘要')}

为什么重要：
这项研究已经被其他学者引用了 {citations} 次，说明在学术界受到关注。

研究领域：{fields}
发表时间：{year}年
作者：{authors}
                """.strip()
            }
            
            return {
                "paper_id": paper_id,
                "title": title,
                "summary": summaries.get(summary_type, summaries["comprehensive"]),
                "key_info": {
                    "authors": authors,
                    "year": str(year),
                    "fields": fields,
                    "citations": citations,
                    "tldr": tldr_text
                }
            }
        else:
            return {"error": f"API error: {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Error generating summary: {str(e)}"}


@mcp.tool()
async def extract_key_information(
    paper_id: str,
    source: str = "semantic_scholar",
    info_types: List[str] = None
) -> Dict[str, Any]:
    """
    从论文中抽取关键信息
    
    Args:
        paper_id: 论文标识符
        source: 数据源
        info_types: 要抽取的信息类型列表
            - "methodology": 研究方法
            - "findings": 主要发现
            - "limitations": 研究局限
            - "datasets": 使用的数据集
            - "metrics": 评估指标
            - "contributions": 主要贡献
    
    Returns:
        抽取的各类关键信息
    """
    if info_types is None:
        info_types = ["methodology", "findings", "limitations"]
    
    logging.info(f"Extracting key information from {paper_id}")
    
    try:
        base_url = "https://api.semanticscholar.org/graph/v1"
        fields = "title,abstract,tldr"
        url = f"{base_url}/paper/{paper_id}?fields={fields}"
        
        response = await asyncio.to_thread(requests.get, url)
        
        if response.status_code == 200:
            data = response.json()
            abstract = data.get("abstract", "")
            tldr = data.get("tldr", {})
            
            result = {
                "paper_id": paper_id,
                "title": data.get("title", ""),
                "extracted_info": {}
            }
            
            # TLDR摘要
            if tldr:
                result["tldr"] = tldr.get("text", "")
            
            # 基于摘要的简单信息抽取
            for info_type in info_types:
                if info_type == "methodology":
                    method_keywords = ["method", "approach", "algorithm", "technique", "framework", "model"]
                    methods = []
                    for keyword in method_keywords:
                        if keyword in abstract.lower():
                            sentences = abstract.split('.')
                            for sent in sentences:
                                if keyword in sent.lower():
                                    methods.append(sent.strip())
                    result["extracted_info"]["methodology"] = methods if methods else ["需要完整文本分析"]
                
                elif info_type == "findings":
                    finding_keywords = ["find", "found", "result", "show", "demonstrate", "reveal", "discover"]
                    findings = []
                    for keyword in finding_keywords:
                        if keyword in abstract.lower():
                            sentences = abstract.split('.')
                            for sent in sentences:
                                if keyword in sent.lower():
                                    findings.append(sent.strip())
                    result["extracted_info"]["findings"] = findings if findings else ["需要完整文本分析"]
                
                elif info_type == "limitations":
                    limit_keywords = ["limitation", "challenge", "weakness", "drawback", "constraint"]
                    limitations = []
                    for keyword in limit_keywords:
                        if keyword in abstract.lower():
                            sentences = abstract.split('.')
                            for sent in sentences:
                                if keyword in sent.lower():
                                    limitations.append(sent.strip())
                    result["extracted_info"]["limitations"] = limitations if limitations else ["需要完整文本分析"]
                
                else:
                    result["extracted_info"][info_type] = f"{info_type}信息抽取需要完整PDF文本"
            
            return result
        else:
            return {"error": f"API error: {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Error extracting information: {str(e)}"}


# ============================================================================
# 3. 完整工作流工具
# ============================================================================

@mcp.tool()
async def research_workflow_complete(
    topic: str,
    num_papers: int = 5,
    include_analysis: bool = True,
    include_summary: bool = True
) -> Dict[str, Any]:
    """
    执行完整的研究工作流：检索 → 分析 → 阅读 → 总结
    
    这是推荐的核心功能！一键完成整个研究流程。
    
    Args:
        topic: 研究主题（例如："CRISPR gene editing"、"深度学习"）
        num_papers: 检索论文数量
        include_analysis: 是否包含深度分析
        include_summary: 是否包含自动摘要
    
    Returns:
        完整的研究报告，包括：
        - search_results: 检索结果
        - paper_analyses: 每篇论文的分析
        - summaries: 论文摘要
        - overall_insights: 整体见解
        - recommendations: 进一步阅读推荐
    """
    logging.info(f"Starting complete research workflow for topic: {topic}")
    
    try:
        workflow_result = {
            "topic": topic,
            "timestamp": "2025-10-24",
            "search_results": [],
            "paper_analyses": [],
            "summaries": [],
            "overall_insights": {},
            "recommendations": []
        }
        
        # 步骤1: 检索论文
        logging.info("Step 1: Searching papers...")
        search_url = f"https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": topic,
            "limit": num_papers,
            "fields": "paperId,title,year,citationCount,influentialCitationCount,abstract,authors"
        }
        
        search_response = await asyncio.to_thread(requests.get, search_url, params=params)
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            papers = search_data.get("data", [])
            workflow_result["search_results"] = papers
            
            # 步骤2 & 3: 分析和总结每篇论文
            for paper in papers[:num_papers]:
                paper_id = paper.get("paperId")
                
                if include_analysis:
                    logging.info(f"Analyzing paper: {paper_id}")
                    impact = await evaluate_paper_impact(paper_id)
                    workflow_result["paper_analyses"].append({
                        "paper_id": paper_id,
                        "title": paper.get("title"),
                        "impact_analysis": impact
                    })
                
                if include_summary:
                    logging.info(f"Generating summary for: {paper_id}")
                    summary = await generate_paper_summary(paper_id, summary_type="brief")
                    workflow_result["summaries"].append(summary)
            
            # 步骤4: 生成整体见解
            total_citations = sum(p.get("citationCount", 0) for p in papers)
            avg_citations = total_citations / len(papers) if papers else 0
            years = [p.get("year", 0) for p in papers if p.get("year")]
            
            workflow_result["overall_insights"] = {
                "total_papers_analyzed": len(papers),
                "total_citations": total_citations,
                "average_citations": round(avg_citations, 2),
                "year_range": f"{min(years)} - {max(years)}" if years else "N/A",
                "research_trend": "活跃" if avg_citations > 50 else "新兴",
                "key_observations": [
                    f"在'{topic}'领域找到 {len(papers)} 篇相关论文",
                    f"平均被引 {round(avg_citations, 1)} 次",
                    f"发表年份范围：{min(years) if years else 'N/A'} - {max(years) if years else 'N/A'}",
                    "建议优先阅读高影响力论文"
                ]
            }
            
            # 步骤5: 推荐进一步阅读
            if papers:
                top_paper_id = papers[0].get("paperId")
                workflow_result["recommendations"] = await recommend_related_papers(
                    top_paper_id,
                    num_recommendations=5,
                    strategy="influential"
                )
            
            return workflow_result
        else:
            return {"error": f"Search failed: {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Workflow error: {str(e)}"}


@mcp.tool()
async def compare_papers(
    paper_ids: List[str],
    comparison_aspects: List[str] = None
) -> Dict[str, Any]:
    """
    对比多篇论文
    
    Args:
        paper_ids: 要对比的论文ID列表（2-5篇）
        comparison_aspects: 对比维度
            - "methodology": 研究方法对比
            - "findings": 研究发现对比
            - "impact": 影响力对比
            - "timeline": 时间线对比
    
    Returns:
        详细的对比分析报告
    """
    if comparison_aspects is None:
        comparison_aspects = ["methodology", "findings", "impact"]
    
    logging.info(f"Comparing {len(paper_ids)} papers")
    
    try:
        comparison_result = {
            "papers_compared": len(paper_ids),
            "comparison_aspects": comparison_aspects,
            "papers": [],
            "comparative_analysis": {}
        }
        
        # 获取所有论文的信息
        for paper_id in paper_ids:
            base_url = "https://api.semanticscholar.org/graph/v1"
            fields = "title,year,abstract,citationCount,influentialCitationCount,authors,fieldsOfStudy"
            url = f"{base_url}/paper/{paper_id}?fields={fields}"
            
            response = await asyncio.to_thread(requests.get, url)
            if response.status_code == 200:
                paper_data = response.json()
                comparison_result["papers"].append(paper_data)
        
        # 进行对比分析
        if "impact" in comparison_aspects:
            citations = [p.get("citationCount", 0) for p in comparison_result["papers"]]
            comparison_result["comparative_analysis"]["impact"] = {
                "highest_cited": max(citations) if citations else 0,
                "lowest_cited": min(citations) if citations else 0,
                "citation_range": max(citations) - min(citations) if citations else 0,
                "most_influential_paper": comparison_result["papers"][citations.index(max(citations))].get("title") if citations else None
            }
        
        if "timeline" in comparison_aspects:
            years = [p.get("year", 0) for p in comparison_result["papers"] if p.get("year")]
            comparison_result["comparative_analysis"]["timeline"] = {
                "earliest_year": min(years) if years else None,
                "latest_year": max(years) if years else None,
                "time_span": max(years) - min(years) if years and len(years) > 1 else 0
            }
        
        # 领域对比
        all_fields = set()
        for paper in comparison_result["papers"]:
            all_fields.update(paper.get("fieldsOfStudy", []))
        
        comparison_result["comparative_analysis"]["fields"] = {
            "common_fields": list(all_fields),
            "interdisciplinary": len(all_fields) > 3
        }
        
        return comparison_result
        
    except Exception as e:
        return {"error": f"Comparison error: {str(e)}"}


# ============================================================================
# 4. 本地PDF分析工具（支持本地文件+在线URL）
# ============================================================================

@mcp.tool()
async def list_all_figures(
    pdf_path: str
) -> Dict[str, Any]:
    """
    列出论文中所有图表的标题和基本信息（支持本地PDF和在线URL）
    
    Args:
        pdf_path: PDF文件路径
            - 本地: "C:\\Papers\\paper.pdf" 或 "/home/user/paper.pdf"
            - URL: "https://arxiv.org/pdf/1706.03762.pdf"
    
    Returns:
        所有图表的列表，每个包含编号和标题
    """
    logging.info(f"Listing all figures from {pdf_path}")
    
    try:
        import PyPDF2
        
        # 读取PDF（自动判断本地还是URL）
        pdf_content = await _read_pdf_content(pdf_path)
        pdf_reader = PyPDF2.PdfReader(pdf_content)
        
        # 提取所有文本
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text()
        
        # 查找所有图表标题
        figure_pattern = r'(Figure|Fig\.|图|Table|表)\s*(\d+)[:\.]?\s*([^\n]+)'
        matches = re.findall(figure_pattern, full_text, re.IGNORECASE)
        
        figures_list = []
        seen = set()
        
        for match in matches:
            fig_type, fig_num, caption = match
            fig_id = f"{fig_type.lower()}-{fig_num}"
            
            if fig_id not in seen:
                seen.add(fig_id)
                figures_list.append({
                    "type": fig_type,
                    "number": int(fig_num),
                    "caption": caption.strip()[:200],  # 限制长度
                    "full_id": f"{fig_type} {fig_num}"
                })
        
        # 按编号排序
        figures_list.sort(key=lambda x: (x["type"], x["number"]))
        
        return {
            "source_type": "local" if _is_local_path(pdf_path) else "url",
            "source_path": pdf_path,
            "total_figures": len(figures_list),
            "figures": figures_list,
            "tip": "使用 explain_specific_figure 获取单个图表的详细解释"
        }
        
    except FileNotFoundError:
        return {
            "error": f"文件不存在: {pdf_path}",
            "suggestion": "请检查文件路径是否正确"
        }
    except ImportError:
        return {
            "error": "需要安装 PyPDF2",
            "install_command": "pip install PyPDF2"
        }
    except Exception as e:
        return {"error": f"Error listing figures: {str(e)}"}


@mcp.tool()
async def explain_specific_figure(
    pdf_path: str,
    figure_number: int,
    provide_context: bool = True
) -> Dict[str, Any]:
    """
    解释论文中的特定图表（支持本地PDF和在线URL，仅返回文字解释）
    
    Args:
        pdf_path: PDF文件路径（本地或URL）
        figure_number: 图表编号（如 1, 2, 3）
        provide_context: 是否提供相关段落的上下文
    
    Examples:
        本地文件:
        explain_specific_figure(
            pdf_path="C:\\Papers\\my_paper.pdf",
            figure_number=1
        )
        
        URL:
        explain_specific_figure(
            pdf_path="https://arxiv.org/pdf/1706.03762.pdf",
            figure_number=1
        )
    
    Returns:
        单个图表的详细文字解释
    """
    logging.info(f"Explaining Figure {figure_number} from {pdf_path}")
    
    try:
        import PyPDF2
        
        # 读取PDF
        pdf_content = await _read_pdf_content(pdf_path)
        pdf_reader = PyPDF2.PdfReader(pdf_content)
        
        # 提取文本
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text()
        
        # 查找特定图表
        figure_pattern = rf'(Figure|Fig\.|图)\s*{figure_number}[:\.]?\s*([^\n]+)'
        match = re.search(figure_pattern, full_text, re.IGNORECASE)
        
        if not match:
            return {
                "error": f"未找到Figure {figure_number}",
                "suggestion": "请检查图表编号是否正确，或PDF是否包含可提取的文本"
            }
        
        caption = match.group(2).strip()
        
        # 判断图表类型
        figure_type = "unknown"
        if any(word in caption.lower() for word in ["graph", "plot", "curve", "曲线"]):
            figure_type = "graph/plot"
        elif any(word in caption.lower() for word in ["table", "表格"]):
            figure_type = "table"
        elif any(word in caption.lower() for word in ["diagram", "schematic", "示意图", "流程"]):
            figure_type = "diagram/schematic"
        elif any(word in caption.lower() for word in ["image", "photo", "microscopy", "显微", "照片"]):
            figure_type = "image/photo"
        elif any(word in caption.lower() for word in ["chart", "bar", "柱状", "饼图"]):
            figure_type = "chart"
        
        # 生成详细解释
        explanation = f"""
图{figure_number} 解释：

📊 图表类型: {figure_type}

📝 标题内容: {caption}

🔍 详细分析:
"""
        
        # 基于标题关键词生成针对性解释
        if "comparison" in caption.lower() or "compare" in caption.lower() or "对比" in caption:
            explanation += """
这是一个对比类图表，用于比较不同条件、方法或组别之间的差异。
- 关注各组之间的数值差异
- 注意显著性标记（如 *, **, ***）
- 比较趋势和模式的异同
"""
        
        elif "workflow" in caption.lower() or "pipeline" in caption.lower() or "流程" in caption:
            explanation += """
这是一个工作流程图，展示了研究方法或实验步骤。
- 按照箭头方向理解处理流程
- 注意每个步骤的输入和输出
- 理解各步骤之间的逻辑关系
"""
        
        elif "result" in caption.lower() or "data" in caption.lower() or "结果" in caption:
            explanation += """
这是一个结果展示图，呈现了实验或分析的主要发现。
- 关注数据的趋势和模式
- 注意误差范围或置信区间
- 比对实验组和对照组的差异
"""
        
        elif "structure" in caption.lower() or "model" in caption.lower() or "结构" in caption:
            explanation += """
这是一个结构示意图，展示了系统或模型的组成。
- 理解各个组件的功能和位置
- 注意组件之间的连接关系
- 把握整体架构的设计思路
"""
        
        else:
            explanation += """
根据标题分析，这个图表展示了研究的关键信息。
建议结合论文正文相关段落理解图表的具体含义。
"""
        
        result = {
            "source_type": "local" if _is_local_path(pdf_path) else "url",
            "figure_number": figure_number,
            "caption": caption,
            "figure_type": figure_type,
            "explanation": explanation.strip()
        }
        
        if provide_context:
            result["usage_tips"] = [
                "结合论文Methods部分理解实验设计",
                "对照Results部分的文字描述",
                "注意与其他图表的关联性",
                "关注统计显著性标记"
            ]
        
        return result
        
    except ImportError:
        return {
            "error": "需要安装 PyPDF2",
            "install_command": "pip install PyPDF2"
        }
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


@mcp.tool()
async def analyze_local_paper(
    pdf_path: str,
    include_figures: bool = True,
    include_summary: bool = True
) -> Dict[str, Any]:
    """
    完整分析本地或在线PDF论文
    
    Args:
        pdf_path: PDF文件路径（本地或URL）
        include_figures: 是否分析图表
        include_summary: 是否生成摘要
    
    Returns:
        完整的论文分析报告
    """
    logging.info(f"Analyzing paper: {pdf_path}")
    
    try:
        import PyPDF2
        
        # 读取PDF
        pdf_content = await _read_pdf_content(pdf_path)
        pdf_reader = PyPDF2.PdfReader(pdf_content)
        
        result = {
            "source_type": "local" if _is_local_path(pdf_path) else "url",
            "file_path": pdf_path,
            "file_name": os.path.basename(pdf_path) if _is_local_path(pdf_path) else pdf_path.split('/')[-1],
            "pages": len(pdf_reader.pages),
            "analysis": {}
        }
        
        # 提取文本
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text()
        
        result["word_count"] = len(full_text.split())
        
        # 提取标题（通常在第一页）
        first_page_text = pdf_reader.pages[0].extract_text()
        title_lines = first_page_text.split('\n')[:5]
        result["potential_title"] = " ".join(title_lines)
        
        # 分析图表
        if include_figures:
            figures_data = await list_all_figures(pdf_path)
            result["analysis"]["figures"] = figures_data
        
        # 生成摘要
        if include_summary:
            # 提取摘要部分
            abstract_pattern = r'Abstract[:\.]?\s*(.*?)(?=\n\n|\nIntroduction|\n1\.)'
            abstract_match = re.search(abstract_pattern, full_text, re.IGNORECASE | re.DOTALL)
            
            if abstract_match:
                result["analysis"]["abstract"] = abstract_match.group(1).strip()[:500]
            else:
                result["analysis"]["abstract"] = "未找到摘要部分"
        
        # 提取关键部分
        sections = ["Introduction", "Method", "Result", "Discussion", "Conclusion"]
        found_sections = []
        for section in sections:
            if section.lower() in full_text.lower():
                found_sections.append(section)
        
        result["analysis"]["sections_found"] = found_sections
        
        return result
        
    except FileNotFoundError:
        return {"error": f"文件不存在: {pdf_path}"}
    except ImportError:
        return {
            "error": "需要安装 PyPDF2",
            "install_command": "pip install PyPDF2"
        }
    except Exception as e:
        return {"error": f"Analysis error: {str(e)}"}


@mcp.tool()
async def batch_analyze_local_papers(
    folder_path: str,
    max_papers: int = 10,
    file_pattern: str = "*.pdf"
) -> Dict[str, Any]:
    """
    批量分析文件夹中的所有PDF论文（仅支持本地文件夹）
    
    Args:
        folder_path: 文件夹路径
        max_papers: 最多分析的论文数量
        file_pattern: 文件匹配模式（默认 "*.pdf"）
    
    Returns:
        所有论文的分析结果
    """
    logging.info(f"Batch analyzing papers in: {folder_path}")
    
    if not os.path.exists(folder_path):
        return {"error": f"文件夹不存在: {folder_path}"}
    
    try:
        # 查找所有PDF文件
        pdf_files = list(Path(folder_path).glob(file_pattern))[:max_papers]
        
        if not pdf_files:
            return {
                "error": "未找到PDF文件",
                "folder": folder_path,
                "pattern": file_pattern
            }
        
        result = {
            "folder_path": folder_path,
            "total_files": len(pdf_files),
            "papers": []
        }
        
        # 分析每篇论文
        for pdf_path in pdf_files:
            logging.info(f"Analyzing: {pdf_path.name}")
            
            paper_analysis = await analyze_local_paper(
                str(pdf_path),
                include_figures=True,
                include_summary=True
            )
            
            result["papers"].append(paper_analysis)
        
        return result
        
    except Exception as e:
        return {"error": f"Batch analysis error: {str(e)}"}


@mcp.tool()
async def extract_text_from_pdf(
    pdf_path: str,
    extract_sections: bool = True,
    page_range: Optional[tuple] = None
) -> Dict[str, Any]:
    """
    从PDF提取文本内容（支持本地和在线URL）
    
    Args:
        pdf_path: PDF路径（本地或URL）
        extract_sections: 是否按章节提取
        page_range: 页面范围，如 (1, 10) 表示第1-10页
    
    Returns:
        提取的文本内容
    """
    logging.info(f"Extracting text from: {pdf_path}")
    
    try:
        import PyPDF2
        
        # 读取PDF
        pdf_content = await _read_pdf_content(pdf_path)
        pdf_reader = PyPDF2.PdfReader(pdf_content)
        total_pages = len(pdf_reader.pages)
        
        # 确定页面范围
        if page_range:
            start, end = page_range
            start = max(0, start - 1)  # 转换为0-based索引
            end = min(total_pages, end)
        else:
            start, end = 0, total_pages
        
        # 提取文本
        full_text = ""
        for i in range(start, end):
            full_text += pdf_reader.pages[i].extract_text()
        
        result = {
            "source_type": "local" if _is_local_path(pdf_path) else "url",
            "file_path": pdf_path,
            "total_pages": total_pages,
            "extracted_pages": f"{start+1}-{end}",
            "word_count": len(full_text.split()),
            "full_text": full_text[:5000]  # 限制返回长度，避免过大
        }
        
        # 提取章节
        if extract_sections:
            sections = {}
            section_patterns = {
                "abstract": r'Abstract[:\.]?\s*(.*?)(?=\n\n|\nIntroduction)',
                "introduction": r'Introduction[:\.]?\s*(.*?)(?=\n\n|\nMethod)',
                "methods": r'Method[s]?[:\.]?\s*(.*?)(?=\n\n|\nResult)',
                "results": r'Result[s]?[:\.]?\s*(.*?)(?=\n\n|\nDiscussion)',
                "discussion": r'Discussion[:\.]?\s*(.*?)(?=\n\n|\nConclusion)',
                "conclusion": r'Conclusion[s]?[:\.]?\s*(.*?)(?=\n\n|\nReference)'
            }
            
            for section_name, pattern in section_patterns.items():
                match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
                if match:
                    sections[section_name] = match.group(1).strip()[:1000]  # 限制长度
            
            result["sections"] = sections
        
        return result
        
    except FileNotFoundError:
        return {"error": f"文件不存在: {pdf_path}"}
    except ImportError:
        return {
            "error": "需要安装 PyPDF2",
            "install_command": "pip install PyPDF2"
        }
    except Exception as e:
        return {"error": f"Text extraction error: {str(e)}"}


if __name__ == "__main__":
    logging.info("Starting Academic Research Advanced MCP Server")
    logging.info("Supports both local PDF files and online URLs")
    logging.info("Available tools: citation network, impact evaluation, recommendations, summaries, workflows, local PDF analysis")
    mcp.run(transport='stdio')

