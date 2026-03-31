import asyncio
import os
import streamlit as st
from textwrap import dedent
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.tools.mcp import MCPTools
from mcp import StdioServerParameters

st.set_page_config(page_title="🐙 RepoLens — GitHub MCP Agent", page_icon="🐙", layout="wide")

st.markdown("<h1 class='main-header'>🐙 RepoLens — GitHub MCP Agent</h1>", unsafe_allow_html=True)
st.markdown("Query any GitHub repository in plain English using the Model Context Protocol")

with st.sidebar:
    st.header("🔑 Authentication")
    
    openai_key = st.text_input("OpenAI API Key", type="password",
                              help="Required for the AI agent to interpret queries and format results")
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    
    github_token = st.text_input("GitHub Token", type="password", 
                                help="Create a token with repo scope at github.com/settings/tokens")
    if github_token:
        os.environ["GITHUB_TOKEN"] = github_token
    
    st.markdown("---")
    st.markdown("### Example Queries")
    
    st.markdown("**Issues**")
    st.markdown("- List open issues by label")
    st.markdown("- Which issues have the most discussion?")
    
    st.markdown("**Pull Requests**")
    st.markdown("- Which PRs are waiting for review?")
    st.markdown("- Show recently merged PRs")
    
    st.markdown("**Repository**")
    st.markdown("- Give me a health overview of this repo")
    st.markdown("- What are the recent commit trends?")
    
    st.markdown("---")
    st.caption("Tip: Always mention the repository name in your query for best results.")

col1, col2 = st.columns([3, 1])
with col1:
    repo = st.text_input("Repository", placeholder="owner/repo (e.g. microsoft/vscode)", help="Format: owner/repo")
with col2:
    query_type = st.selectbox("Query Type", [
        "Issues", "Pull Requests", "Repository Activity", "Custom"
    ])

if query_type == "Issues":
    query_template = f"Find issues labeled as bugs in {repo}"
elif query_type == "Pull Requests":
    query_template = f"Show me recent merged PRs in {repo}"
elif query_type == "Repository Activity":
    query_template = f"Analyze code quality trends in {repo}"
else:
    query_template = ""

query = st.text_area("Your Query", value=query_template, 
                     placeholder="What would you like to know about this repository?")

async def run_github_agent(message):
    if not os.getenv("GITHUB_TOKEN"):
        return "Error: GitHub token not provided"
    
    if not os.getenv("OPENAI_API_KEY"):
        return "Error: OpenAI API key not provided"
    
    try:
        server_params = StdioServerParameters(
            command="docker",
            args=[
                "run", "-i", "--rm",
                "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
                "-e", "GITHUB_TOOLSETS",
                "ghcr.io/github/github-mcp-server"
            ],
            env={
                **os.environ,
                "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv('GITHUB_TOKEN'),
                "GITHUB_TOOLSETS": "repos,issues,pull_requests"
            }
        )
        
        async with MCPTools(server_params=server_params) as mcp_tools:
            agent = Agent(
                tools=[mcp_tools],
                instructions=dedent("""\
                    You are RepoLens, a GitHub intelligence assistant. Help users understand any repository quickly.
                    - Give structured, data-driven insights from the GitHub API
                    - Use clean markdown formatting and tables for numerical data
                    - Always link to relevant GitHub pages (issues, PRs, commits) where useful
                    - Be concise and highlight the most actionable information first
                """),
                markdown=True,
            )
            
            response: RunOutput = await asyncio.wait_for(agent.arun(message), timeout=120.0)
            return response.content
                
    except asyncio.TimeoutError:
        return "Error: Request timed out after 120 seconds"
    except Exception as e:
        return f"Error: {str(e)}"

if st.button("🚀 Run Query", type="primary", use_container_width=True):
    if not openai_key:
        st.error("Please enter your OpenAI API key in the sidebar")
    elif not github_token:
        st.error("Please enter your GitHub token in the sidebar")
    elif not query:
        st.error("Please enter a query")
    else:
        with st.spinner("Analyzing GitHub repository..."):
            if repo and repo not in query:
                full_query = f"{query} in {repo}"
            else:
                full_query = query
                
            result = asyncio.run(run_github_agent(full_query))
        
        st.markdown("### 🔍 Analysis Results")
        st.markdown(result)

if 'result' not in locals():
    st.markdown(
        """<div class='info-box'>
        <h4>Getting started with RepoLens:</h4>
        <ol>
            <li>Paste your <strong>OpenAI API key</strong> in the sidebar</li>
            <li>Paste your <strong>GitHub Personal Access Token</strong> in the sidebar</li>
            <li>Enter any public repository (e.g., microsoft/vscode)</li>
            <li>Pick a query type or write a custom question</li>
            <li>Click <strong>Run Query</strong> to get your analysis</li>
        </ol>
        <p><strong>How it works:</strong></p>
        <ul>
            <li>Connects to the official GitHub MCP server via Docker for live API access</li>
            <li>OpenAI interprets your natural-language query and selects the right GitHub API calls</li>
            <li>Responses are rendered in clean markdown with tables and direct links</li>
            <li>Best results come from focused questions about issues, PRs, or code activity</li>
        </ul>
        </div>""", 
        unsafe_allow_html=True
    )
