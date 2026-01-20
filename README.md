## Architecture
```
[User Question] 
    ↓
[Planning Agent] → Creates research plan
    ↓
[Search Agent] → Calls Tavily for sources
    ↓
[Synthesis Agent] → Combines findings
    ↓
[Quality Agent] → Validates citations
    ↓
[Final Answer with Sources]
```

## Results
- Reduces research time from hours to minutes
- Automatically cites all sources
- Pulls from trusted, up-to-date web sources

## Technical Implementation

**Agent Orchestration:** LangGraph for workflow management  
**LLM:** Claude Sonnet 4 for reasoning and synthesis  
**Search:** Tavily API for real-time web search  
**RAG:** Hybrid retrieval combining semantic search and keyword matching  

**Key Features:**
- Parallel agent execution for speed
- Citation validation to prevent hallucinations
- Fallback handling for API errors
