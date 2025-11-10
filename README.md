# Agent B - AI Workflow Capture System

An AI-powered system that autonomously navigates web applications and captures step-by-step workflow documentation. Built with a multi-agent CrewAI architecture.

## 🎯 Overview

Agent B understands natural language requests like "How do I invite a teammate in Notion?" and automatically:

- Finds the correct starting URL using web search
- Navigates the application autonomously
- Captures screenshots at each step
- Generates human-readable explanations
- Handles logins with session management

## ✨ Key Features

- **🤖 AI-Powered Navigation** - Uses GPT-4 to understand and navigate any web application
- **🔍 Smart URL Finding** - Automatically discovers the right starting point for your task
- **📸 Visual Documentation** - Captures every UI state including modals and dynamic content
- **🔐 Session Management** - Login once, reuse session for multiple workflows
- **🎨 Modern UI** - Beautiful Next.js frontend with dark mode support
- **🔧 Multi-Agent System** - Coordinated AI agents working together using CrewAI

## 🏗️ Architecture

### Multi-Agent System (CrewAI)

The system uses two specialized AI agents working in sequence:

```
┌──────────────────────┐
│  URL Finder Agent    │ ──► Finds starting URL via web search
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Workflow Executor    │ ──► Navigates UI and captures screenshots
│      Agent           │
└──────────────────────┘
```

**URL Finder Agent:**

- Uses OpenAI's web search to find the application URL
- Verifies the URL by navigating to it
- Returns the base domain for the workflow

**Workflow Executor Agent:**

- Analyzes UI using intelligent DOM snapshots
- Plans and executes actions (clicks, typing, navigation)
- Captures screenshots before/after each interaction
- Generates step-by-step explanations

### Tools

Five specialized tools available to agents:

1. **web_search_url_tool** - Searches the web to find URLs
2. **navigate_page_and_take_screenshot_tool** - Navigates to URLs and takes screenshots
3. **capture_ui_snapshot_tool** - Captures semantic UI snapshots (buttons, inputs, links)
4. **click_element_and_take_screenshot_tool** - Clicks elements and takes screenshots
5. **fill_input_and_take_screenshot_tool** - Fills form fields and takes screenshots

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

### Backend Setup

```bash
cd backend

# Run automated setup script
chmod +x setup.sh
./setup.sh

# Create .env file and add your API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Start the server
source venv/bin/activate
python main.py
```

Backend runs at: `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Run automated setup script
chmod +x setup.sh
./setup.sh

# Start the development server
npm run dev
```

Frontend runs at: `http://localhost:3000`

### First Workflow

1. Open http://localhost:3000
2. Enter a task: "How to connect your Slack account in Notion?"
3. Set login URL: `https://www.notion.so/login`
4. Set session file name: `notion_session.json`
5. Click "Start Capture"
6. **First time only**: Playwright opens a browser - log in manually within 60 seconds
7. Watch as Agent B captures your workflow!

## 📡 API

### POST `/tasks/start`

Start a new workflow capture task.

**Request:**

```json
{
  "task": "How to invite a teammate in Notion?",
  "login_url": "https://www.notion.so/login",
  "session_path": "notion_session.json",
  "task_id": "2025-11-09T12:00:00.000Z"
}
```

**Response:**

```json
{
  "paths": [
    "screenshots/2025-11-09T12:00:00.000Z/after_navigate_001.png",
    "screenshots/2025-11-09T12:00:00.000Z/before_click_002.png",
    "screenshots/2025-11-09T12:00:00.000Z/final_state_003.png"
  ],
  "explanation": "1) Navigated to Notion workspace. 2) Clicked 'Share' button. 3) Entered teammate email and sent invite."
}
```

## 🛠️ Tech Stack

### Backend

- **FastAPI** - Modern async Python web framework
- **CrewAI** - Multi-agent orchestration framework
- **Playwright** - Browser automation
- **OpenAI GPT-4** - AI reasoning and web search
- **Pydantic** - Data validation

### Frontend

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling

## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Multi-agent system architecture
- **[SETUP.md](SETUP.md)** - Comprehensive setup guide for both backend and frontend
- **[backend/ENV.md](backend/ENV.md)** - Environment variables reference

## 🔐 Session Management

Agent B uses session files to avoid repeated logins:

1. **First task**: Provide `login_url` - Playwright opens browser, you log in manually
2. **Session saved**: Cookies stored in session file (e.g., `notion_session.json`)
3. **Subsequent tasks**: Omit `login_url`, use same `session_path` - automatic login!

Different applications use different session files:

- Notion: `notion_session.json`
- Linear: `linear_session.json`
- GitHub: `github_session.json`

## 🚀 Future Enhancements

- **MCP Servers** - Integrate Model Context Protocol for enhanced tool management and extensibility
- **S3 Storage** - Move screenshots to S3 buckets for scalability and better performance

## 🙏 Acknowledgments

- [CrewAI](https://www.crewai.com/) for multi-agent orchestration
- [OpenAI](https://openai.com/) for GPT-4 API and web search
- [Playwright](https://playwright.dev/) for browser automation
- [FastAPI](https://fastapi.tiangolo.com/) and [Next.js](https://nextjs.org/) communities
