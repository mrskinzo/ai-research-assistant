import streamlit as st
from orchestrator import run_research_workflow, get_final_output

# Page config
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# Title and description
st.title("🔍 AI Research Assistant")
st.markdown("""
This multi-agent system uses specialized AI agents to research any topic and produce a comprehensive report.

**How it works:**
1. **Researcher Agent** searches the web
2. **Analyst Agent** extracts key insights
3. **Writer Agent** creates a structured report
4. **Quality Checker Agent** reviews the output
""")

st.markdown("---")

# Input section
st.subheader("What would you like to research?")
question = st.text_input(
    "Enter your research question:",
    placeholder="e.g., What are the latest trends in RAG architecture?"
)

# Button to start research
if st.button("🚀 Start Research", type="primary"):
    if question:
        with st.spinner("🔄 Multi-agent workflow in progress..."):
            try:
                # Run the workflow
                result = run_research_workflow(question)
                
                # Display the formatted output
                st.success("✅ Research Complete!")
                
                # Get formatted output
                output = get_final_output(result)
                
                # Display the report
                st.markdown(output)
                
                # Download button
                st.download_button(
                    label="📥 Download Report",
                    data=output,
                    file_name=f"research_report_{question[:30].replace(' ', '_')}.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("Please check your API keys in the .env file and try again.")
    else:
        st.warning("⚠️ Please enter a research question first.")

# Sidebar with info
with st.sidebar:
    st.header("About")
    st.markdown("""
    ### Multi-Agent System
    
    This project demonstrates:
    - **Multi-agent orchestration**
    - **Web search integration** (Tavily)
    - **LLM-powered analysis** (Claude)
    - **Structured workflow design**
    
    ### Tech Stack
    - LangGraph
    - Claude Sonnet 4
    - Tavily API
    - Streamlit
    - Python
    
    ---
    
    **Built by:** Christi Akinwumi  
    **Portfolio:** [christi.io](https://christi.io)
    """)
