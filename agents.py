import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from tavily import TavilyClient

# Load API keys
load_dotenv()

# Initialize Claude
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    max_tokens=4096
)

# Initialize Tavily for web search
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# ============================================
# AGENT 1: RESEARCHER
# ============================================

def researcher_agent(question: str) -> dict:
    """
    Searches the web for information about the question.
    Returns: Dictionary with search results and sources
    """
    print("🔍 Researcher Agent: Searching the web...")
    
    # Search the web using Tavily
    search_results = tavily_client.search(
        query=question,
        max_results=5
    )
    
    # Format the results
    formatted_results = []
    for result in search_results.get('results', []):
        formatted_results.append({
            'title': result.get('title', 'No title'),
            'url': result.get('url', ''),
            'content': result.get('content', '')
        })
    
    return {
        'question': question,
        'search_results': formatted_results,
        'status': 'research_complete'
    }


# ============================================
# AGENT 2: ANALYST
# ============================================

def analyst_agent(research_data: dict) -> dict:
    """
    Analyzes the research data and extracts key insights.
    Returns: Dictionary with structured analysis
    """
    print("🧠 Analyst Agent: Analyzing research data...")
    
    # Build the context from search results
    context = ""
    for idx, result in enumerate(research_data['search_results'], 1):
        context += f"\n\nSource {idx}: {result['title']}\n{result['content']}\n"
    
    analyst_prompt = f"""You are an expert analyst. Your job is to analyze research data and extract key insights.

Research Question: {research_data['question']}

Research Data:
{context}

Your task:
1. Identify the 3-5 most important insights from this research
2. Organize them into clear themes
3. Note any conflicting information
4. Highlight gaps in the research

Format your response as:
- Key Insight 1: [insight]
- Key Insight 2: [insight]
- etc.

Be concise but thorough."""

    response = llm.invoke(analyst_prompt)
    
    return {
        'question': research_data['question'],
        'search_results': research_data['search_results'],
        'analysis': response.content,
        'status': 'analysis_complete'
    }


# ============================================
# AGENT 3: WRITER
# ============================================

def writer_agent(analysis_data: dict) -> dict:
    """
    Takes the analysis and writes a clean, formatted report.
    Returns: Dictionary with final report
    """
    print("✍️ Writer Agent: Creating final report...")
    
    writer_prompt = f"""You are an expert technical writer. Your job is to create a clear, well-structured research report.

Research Question: {analysis_data['question']}

Analysis:
{analysis_data['analysis']}

Your task:
Write a professional research report with these sections:
1. Executive Summary (2-3 sentences)
2. Key Findings (organized by theme)
3. Detailed Insights (expand on the findings)
4. Conclusion (1-2 sentences)

Use clear headers, bullet points where helpful, and maintain a professional tone.
Make it easy to scan and understand."""

    response = llm.invoke(writer_prompt)
    
    # Format sources
    sources_text = "\n\n## Sources\n"
    for idx, result in enumerate(analysis_data['search_results'], 1):
        sources_text += f"{idx}. [{result['title']}]({result['url']})\n"
    
    final_report = response.content + sources_text
    
    return {
        'question': analysis_data['question'],
        'report': final_report,
        'sources': analysis_data['search_results'],
        'status': 'report_complete'
    }


# ============================================
# AGENT 4: QUALITY CHECKER
# ============================================

def quality_checker_agent(report_data: dict) -> dict:
    """
    Reviews the report for quality, completeness, and accuracy.
    Returns: Dictionary with quality score and feedback
    """
    print("✅ Quality Checker Agent: Reviewing report...")
    
    checker_prompt = f"""You are a quality assurance expert. Your job is to review research reports for quality and completeness.

Research Question: {report_data['question']}

Report:
{report_data['report']}

Your task:
Evaluate this report on:
1. Completeness - Does it fully answer the question?
2. Clarity - Is it easy to understand?
3. Structure - Is it well-organized?
4. Accuracy - Are claims supported by the research?

Provide:
- A quality score (1-10)
- 2-3 specific strengths
- 2-3 specific improvements (if score < 8)

Format:
Score: [X/10]
Strengths: [list]
Improvements: [list if needed]"""

    response = llm.invoke(checker_prompt)
    
    return {
        'question': report_data['question'],
        'report': report_data['report'],
        'sources': report_data['sources'],
        'quality_review': response.content,
        'status': 'quality_check_complete'
    }
