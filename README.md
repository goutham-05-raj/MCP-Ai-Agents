# 🤖 MCP AI Agents — 5 Intelligent Agents Powered by Model Context Protocol

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=for-the-badge&logo=openai&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-00D4AA?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A collection of 5 production-ready AI agents that use the Model Context Protocol (MCP) to connect GPT-4o with real-world tools — Airbnb, GitHub, Playwright, Notion, Perplexity, and more.**

[🌍 TripCraft](#-tripcraft-ai-travel-planner) • [🐙 RepoLens](#-repolens-github-agent) • [🌐 WebPilot](#-webpilot-browser-agent) • [🚀 Nexus AI](#-nexus-ai-multi-mcp-agent) • [📝 PageMind](#-pagemind-notion-agent)

</div>

---

## 🧠 What Is Model Context Protocol (MCP)?

> **MCP is like a USB-C port for AI agents.** It's an open standard by Anthropic that lets AI models communicate with external tools through a unified interface — so one AI can talk to Airbnb, GitHub, a browser, Notion, and more — all with the same protocol.

```
Your Query → AI Agent → MCP Client → MCP Server → Real API (Airbnb / GitHub / etc.)
                                ↑
              Standardized tool interface
```

Instead of writing custom code to call each API, MCP servers expose tools that any AI agent can call — just like browser extensions, but for AI.

---

## 🗂️ Project Structure

```
mcp_ai_agents/
├── 🌍 ai_travel_planner_mcp_agent_team/   # TripCraft — Streamlit travel planner
│   ├── app.py
│   └── requirements.txt
├── 🐙 github_mcp_agent/                   # RepoLens — GitHub repo analyser
│   ├── github_agent.py
│   └── requirements.txt
├── 🌐 browser_mcp_agent/                  # WebPilot — Playwright browser agent
│   ├── main.py
│   ├── mcp_agent.config.yaml
│   └── requirements.txt
├── 🚀 multi_mcp_agent/                    # Nexus AI — Multi-platform CLI agent
│   ├── multi_mcp_agent.py
│   └── requirements.txt
└── 📝 notion_mcp_agent/                   # PageMind — Notion workspace agent
    ├── notion_mcp_agent.py
    └── requirements.txt
```

---

## 🌍 TripCraft AI Travel Planner

> **Build hyper-detailed travel itineraries using live Airbnb listings + Google Maps + web search**

### ✨ Features
- 🏨 Real-time Airbnb listings with live pricing and availability
- 🗺️ Turn-by-turn directions and distance calculations via Google Maps MCP
- 🔍 Current travel advisories, events, and restaurant reviews via web search
- 📅 Download your itinerary as a `.ics` calendar file

### 🚀 Quick Start
```bash
cd ai_travel_planner_mcp_agent_team
pip install -r requirements.txt
streamlit run app.py
```

### 🔑 Required API Keys
| Key | Where to Get |
|---|---|
| OpenAI API Key | https://platform.openai.com/api-keys |
| Google Maps API Key | https://console.cloud.google.com/apis/credentials |

---

## 🐙 RepoLens — GitHub Agent

> **Query any GitHub repository in plain English — issues, PRs, code activity, health metrics**

### ✨ Features
- 📋 Natural language queries on issues, PRs, branches
- 📊 Repository health analysis and activity trends
- 🔗 Direct links to relevant GitHub pages in every response
- 🐳 Powered by the official GitHub MCP server via Docker

### 🚀 Quick Start
```bash
# Make sure Docker Desktop is running!
cd github_mcp_agent
pip install -r requirements.txt
streamlit run github_agent.py
```

### 🔑 Required API Keys
| Key | Where to Get |
|---|---|
| OpenAI API Key | https://platform.openai.com/api-keys |
| GitHub Token (repo scope) | https://github.com/settings/tokens |

---

## 🌐 WebPilot — Browser Agent

> **Control a real Chromium browser with plain English — navigate, click, scroll, extract**

### ✨ Features
- 🖱️ Full browser control: navigation, clicking, scrolling, typing
- 📸 Screenshots of specific page elements
- 📄 Multi-step browsing workflows
- 🔄 Persistent browser session across multiple commands

### 🚀 Quick Start
```bash
cd browser_mcp_agent
pip install -r requirements.txt
playwright install chromium

# Add your key to mcp_agent.secrets.yaml:
# openai:
#   api_key: "sk-your-key-here"

streamlit run main.py
```

---

## 🚀 Nexus AI — Multi-MCP Agent

> **Terminal AI assistant connected to GitHub + Perplexity + Calendar + Gmail simultaneously**

### ✨ Features
- 🔀 Seamlessly chains multiple MCP tools in one response
- 🧠 Persistent memory across sessions (SQLite)
- 📅 Calendar event creation and management
- 🔍 Real-time web research via Perplexity
- 💬 Streaming terminal chat interface

### 🚀 Quick Start
```bash
cd multi_mcp_agent

# Create .env file:
# OPENAI_API_KEY=sk-your-key
# GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your-token
# PERPLEXITY_API_KEY=pplx-your-key

pip install -r requirements.txt
python multi_mcp_agent.py
```

---

## 📝 PageMind — Notion Agent

> **Read, write, and search your Notion workspace from your terminal**

### ✨ Features
- 📖 Read page content via natural language
- ✏️ Add/update blocks, lists, and tables
- 🔍 Search across your entire workspace
- 💾 Conversation memory (remembers last 5 interactions)

### 🚀 Quick Start
```bash
cd notion_mcp_agent

# Create .env file:
# NOTION_API_KEY=secret_your-integration-token
# OPENAI_API_KEY=sk-your-key

# Get Notion integration: https://www.notion.so/my-integrations

pip install -r requirements.txt
python notion_mcp_agent.py
# Paste your Notion page ID when prompted
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Core language |
| **Agno Framework** | Agent orchestration for Travel, GitHub, Notion, Multi agents |
| **MCP-Agent Framework** | Agent orchestration for Browser agent |
| **OpenAI GPT-4o** | Language model powering all agents |
| **Streamlit** | Web UI for 3 of the 5 agents |
| **Playwright** | Browser automation (WebPilot) |
| **Docker** | GitHub MCP server container |
| **SQLite** | Agent memory persistence |
| **MCP (stdio/npx/Docker)** | Tool communication protocol |

---

## ⚡ Prerequisites

```bash
# Python 3.11+
python --version

# Node.js (for npx MCP servers)
node --version

# Docker Desktop (GitHub agent only)
# https://www.docker.com/products/docker-desktop/
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

Built with ❤️ using **OpenAI GPT-4o**, **MCP**, **Agno**, and **Streamlit**

⭐ Star this repo if you found it useful!

</div>
