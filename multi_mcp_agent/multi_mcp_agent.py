import asyncio
import os
import uuid
from textwrap import dedent
from agno.agent import Agent 
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MultiMCPTools
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

async def main():
    print("\n" + "="*60)
    print("           🚀 Nexus AI — Multi-MCP Assistant 🚀")
    print("="*60)
    print("🔗 Integrations: GitHub • Perplexity • Calendar • Gmail")
    print("💡 Powered by OpenAI GPT-4o with Multi-Platform MCP Tools")
    print("="*60 + "\n")
    
    # Validate required environment variables
    required_vars = {
        "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN,
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "PERPLEXITY_API_KEY": PERPLEXITY_API_KEY,
    }
    
    missing_vars = [name for name, value in required_vars.items() if not value]
    if missing_vars:
        print("❌ ERROR: Missing required environment variables:")
        for var in missing_vars:
            print(f"   • {var}")
        print("\nPlease check your .env file and ensure all required variables are set.")
        return
    
    # Generate unique user and session IDs for this terminal session
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    session_id = f"session_{uuid.uuid4().hex[:8]}"
    print(f"👤 User ID: {user_id}")
    print(f"🔑 Session ID: {session_id}")
    
    print("\n🔌 Initializing MCP server connections...\n")
    
    # Set up environment variables for MCP servers
    env = {
        **os.environ,
        "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN,
        "PERPLEXITY_API_KEY": PERPLEXITY_API_KEY
    }

    mcp_servers = [
        "npx -y @modelcontextprotocol/server-github",
        "npx -y @chatmcp/server-perplexity-ask",
        "npx @gongrzhe/server-calendar-autoauth-mcp",
        "npx @gongrzhe/server-gmail-autoauth-mcp"
    ]
    
    # Setup database for memory
    db = SqliteDb(db_file="tmp/multi_mcp_agent.db")
    
    # Start the MCP Tools session
    async with MultiMCPTools(mcp_servers, env=env) as mcp_tools:
        print("✅ Successfully connected to all MCP servers!")
        
        # Create the agent with comprehensive instructions
        agent = Agent(
            name="NexusAI",
            model=OpenAIChat(id="gpt-4o", api_key=OPENAI_API_KEY),
            tools=[mcp_tools],
            description="Nexus AI — an intelligent multi-platform assistant with GitHub, Perplexity, Calendar, and Gmail integration",
            instructions=dedent(f"""
                You are Nexus AI, a powerful multi-platform assistant built to supercharge productivity. Your mission is to seamlessly connect the user's digital workspace and help them achieve more.

                🎯 CORE CAPABILITIES & INSTRUCTIONS:

                1. 🔧 TOOL MASTERY
                   • You have DIRECT access to GitHub, Notion, Perplexity, and Calendar through MCP tools
                   • ALWAYS use the appropriate MCP tool calls for any requests related to these platforms
                   • Be proactive in suggesting powerful workflows and automations
                   • Chain multiple tool calls together for complex tasks

                2. 📋 GITHUB EXCELLENCE
                   • Repository management: create, clone, fork, search repositories
                   • Issue & PR workflow: create, update, review, merge, comment
                   • Code analysis: search code, review diffs, suggest improvements
                   • Branch management: create, switch, merge branches
                   • Collaboration: manage teams, reviews, and project workflows

                4. 🔍 PERPLEXITY RESEARCH
                   • Real-time web search and research
                   • Current events and trending information
                   • Technical documentation and learning resources
                   • Fact-checking and verification

                5. 📅 CALENDAR INTEGRATION
                   • Event scheduling and management
                   • Meeting coordination and availability
                   • Deadline tracking and reminders

                6. 🎨 INTERACTION PRINCIPLES
                   • Be conversational, helpful, and proactive
                   • Explain what you're doing and why
                   • Suggest follow-up actions and optimizations
                   • Handle errors gracefully with alternative solutions
                   • Ask clarifying questions when needed
                   • Provide rich, formatted responses using markdown

                7. 🚀 ADVANCED WORKFLOWS
                   • Cross-platform automation (e.g., GitHub issues → Notion tasks)
                   • Research-driven development (Perplexity → GitHub)
                   • Project management integration
                   • Documentation and knowledge sharing

                SESSION INFO:
                • User ID: {user_id}
                • Session ID: {session_id}
                 • Active Services: GitHub, Perplexity, Calendar, Gmail

                 REMEMBER: You are Nexus AI — a productivity multiplier. Think across platforms, suggest automations, and help users accomplish more than they thought possible!
            """),
            markdown=True,
            debug_mode=True,
            retries=3,
            db=db,
            enable_user_memories=True,
            add_history_to_context=True,
            num_history_runs=10,  # Increased for better context retention
        )
        
        print("\n" + "🎉 " + "="*54 + " 🎉")
        print("   Nexus AI is READY! Let's get to work!")
        print("🎉 " + "="*54 + " 🎉\n")
        
        print("💡 Try these example commands:")
        print("   • 'Show my recent GitHub repositories'")
        print("   • 'Search for the latest AI developments'")
        print("   • 'Schedule a meeting for next week'")
        
        print("⚡ Type 'exit', 'quit', or 'bye' to end the session\n")
        
        # Start interactive CLI session
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