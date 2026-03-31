import asyncio
import json
import os
import sys
import uuid
from textwrap import dedent
from agno.agent import Agent 
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools 
from agno.db.sqlite import SqliteDb
from mcp import StdioServerParameters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def main():
    print("\n=======================================")
    print("    PageMind — Notion MCP Agent")
    print("======================================\n")
    
    # Get configuration from environment or use defaults
    notion_token = NOTION_TOKEN
    openai_api_key = OPENAI_API_KEY
    
    # Prompt for page ID first
    page_id = None
    if len(sys.argv) > 1:
        # Use command-line argument if provided
        page_id = sys.argv[1]
        print(f"Using provided page ID from command line: {page_id}")
    else:
        # Ask the user for the page ID
        print("Please enter your Notion page ID:")
        print("(You can find this in your page URL, e.g., https://www.notion.so/workspace/Your-Page-1f5b8a8ba283...)")
        print("The ID is the part after the last dash and before any query parameters")
        
        user_input = input("> ")
        
        # If user input is empty, prompt again
        if user_input.strip():
            page_id = user_input.strip()
            print(f"Using provided page ID: {page_id}")
        else:
            print("❌ Error: Page ID is required. Please provide a Notion page ID.")
            return
    
    # Generate unique user and session IDs for this terminal session
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    session_id = f"session_{uuid.uuid4().hex[:8]}"
    print(f"User ID: {user_id}")
    print(f"Session ID: {session_id}")
    
    print("\nConnecting to Notion MCP server...\n")
    
    # Configure the MCP Tools
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@notionhq/notion-mcp-server"],
        env={
            "OPENAPI_MCP_HEADERS": json.dumps(
                {"Authorization": f"Bearer {notion_token}", "Notion-Version": "2022-06-28"}
            )
        }
    )
    
    # Start the MCP Tools session
    async with MCPTools(server_params=server_params) as mcp_tools:
        print("Connected to Notion MCP server successfully!")
        db = SqliteDb(db_file="agno.db") # SQLite DB for memory
        # Create the agent
        agent = Agent(
            name="PageMind",
            model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
            tools=[mcp_tools],
            description="PageMind — an intelligent Notion assistant that reads, writes, and organises your Notion workspace via MCP",
            instructions=dedent(f"""
                You are PageMind, an intelligent Notion workspace assistant with full access to Notion via MCP.
                
                CORE RULES:
                1. Use the MCP tools for every Notion operation — never guess or hallucinate content.
                2. Default page ID for all operations: {page_id} (override only if user specifies another).
                3. For read, write, search, or update requests, always invoke the appropriate MCP tool.
                4. After any change, summarise exactly what was modified so the user can verify.
                5. If a tool call fails, explain why and suggest a practical workaround.
                6. Proactively suggest what the user can do next with their Notion content.
                
                Example tasks you can help with:
                - Reading page content
                - Searching for specific information
                - Adding new content or updating existing content
                - Creating lists, tables, and other Notion blocks
                - Explaining page structure
                - Adding comments to specific blocks
                
                The user's current page ID is: {page_id}
            """),
            markdown=True,
            retries=3,
            db=db,
            enable_user_memories=True, # This enables Memory for the Agent
            add_history_to_context=True,  # Include conversation history
            num_history_runs=5,  # Keep track of the last 5 interactions
        )
        
        print("\n\nPageMind is ready! Start chatting with your Notion workspace.\n")
        print("Type 'exit' or 'quit' to end the session.\n")
        
        # Start interactive CLI session with memory and proper session management
        await agent.acli_app(
            user_id=user_id,
            session_id=session_id,
            user="You",
            emoji="🤖",
            stream=True,
            markdown=True,
            exit_on=["exit", "quit", "bye", "goodbye"]
        )

if __name__ == "__main__":
    asyncio.run(main())