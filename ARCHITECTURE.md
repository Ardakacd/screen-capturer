# Multi-Agent Architecture

Technical overview of Agent B's CrewAI-based multi-agent system.

## System Overview

Agent B uses **CrewAI** to orchestrate two specialized AI agents that work sequentially to capture web workflows. Each agent has specific tools and responsibilities, and they share context through task dependencies.

## Agent Architecture

### High-Level Flow

```
User Input → URL Finder Agent → Workflow Executor Agent → Screenshots + Explanation
```

The system works in two phases:

1. **URL Discovery Phase** - Find where to start
2. **Workflow Execution Phase** - Navigate and capture

### Agent 1: URL Finder Agent

**Purpose**: Discover and verify the correct starting URL for the workflow.

**Configuration**:

- **Role**: Web URL Discovery Specialist
- **LLM**: GPT-4.1-mini
- **Tools**:
  - `web_search_url_tool` - Find URLs using OpenAI web search
  - `navigate_page_and_take_screenshot_tool` - Navigate to verify the URL
  - `capture_ui_snapshot_tool` - Confirm it's the right application

**Process**:

```
1. Receive user goal: "How to invite a teammate in Notion?"
2. Use web_search_url_tool to find base URL
3. Navigate to the URL to verify
4. Capture snapshot to confirm it's correct
5. Return: "Navigated to https://notion.so"
```

**Output**: Base URL (domain only, no path)

### Agent 2: Workflow Executor Agent

**Purpose**: Execute the workflow by navigating the UI and capturing screenshots.

**Configuration**:

- **Role**: Autonomous UI Workflow Planner and Executor
- **LLM**: GPT-4.1-mini
- **Context**: Receives output from URL Finder Agent
- **Tools**:
  - `capture_ui_snapshot_tool` - Analyze current UI state
  - `navigate_page_and_take_screenshot_tool` - Navigate to different pages
  - `click_element_and_take_screenshot_tool` - Click elements
  - `fill_input_and_take_screenshot_tool` - Fill form fields

**Process**:

```
1. Start from URL provided by URL Finder Agent
2. Loop until goal is achieved:
   a. Capture UI snapshot (analyze buttons, inputs, links)
   b. Decide next action based on goal and current UI
   c. Execute action (click, fill, navigate)
   d. Take screenshot to document the step
   e. Verify action succeeded with another snapshot
3. Return: List of screenshot paths + step-by-step explanation
```

**Output**:

```json
{
  "paths": ["screenshot1.png", "screenshot2.png", ...],
  "explanation": "1) Did X. 2) Did Y. 3) Did Z."
}
```

### Why Two Agents?

**Separation of Concerns**:

- URL Finder: Focuses on research and discovery
- Workflow Executor: Focuses on precise UI interaction

**Better Context Management**:

- URL Finder provides clean starting point
- Workflow Executor receives confirmed URL as context

**Improved Reliability**:

- Each agent has focused, well-defined objectives
- Reduces decision complexity for each agent

## Example: Complete Workflow

**User Input**: "How to invite a teammate in Notion?"

**Phase 1: URL Finding**

```
[URL Finder Agent]
Task: Find Notion application URL
→ web_search_url_tool("Invite a teammate in Notion")
→ Returns: https://notion.so
→ navigate_page_and_take_screenshot_tool("https://notion.so")
→ capture_ui_snapshot_tool() to verify
Output: "Navigated to https://notion.so"
```

**Phase 2: Workflow Execution**

```
[Workflow Executor Agent]
Context: Start from https://notion.so
Goal: Invite a teammate

Step 1:
→ capture_ui_snapshot_tool()
  Sees: "Share" button available
→ click_element_and_take_screenshot_tool("Share" button)
  Screenshot: before_click_001.png

Step 2:
→ capture_ui_snapshot_tool()
  Sees: Modal with "Add emails" input
→ fill_input_and_take_screenshot_tool("Add emails", "teammate@example.com")
  Screenshot: after_fill_002.png

Step 3:
→ capture_ui_snapshot_tool()
  Sees: "Send invite" button
→ click_element_and_take_screenshot_tool("Send invite")
  Screenshot: before_click_003.png

Complete!
Final Screenshot: final_state_004.png

Output: {
  "paths": [
    "before_click_001.png",
    "after_fill_002.png",
    "before_click_003.png",
    "final_state_004.png"
  ],
  "explanation": "1) Clicked Share button. 2) Entered teammate email. 3) Clicked Send invite."
}
```

## Key Design Principles

### 1. Agent Specialization

Each agent has a single, well-defined responsibility. This makes the system more maintainable and the prompts more focused.

### 2. Tool-Based Actions

Agents don't execute browser actions directly. They use tools, which provides:

- Consistent error handling
- Screenshot capture
- Logging and debugging

### 3. Snapshot-Driven Decisions

Before every action, the agent captures a UI snapshot. This ensures:

- Decisions based on current state
- No assumptions about UI structure
- Better handling of dynamic content

### 4. Sequential Execution

Agents run one after another, not in parallel. This:

- Simplifies coordination
- Reduces complexity
- Matches natural workflow discovery → execution flow

### 5. Context Sharing via CrewAI

CrewAI handles passing information between agents automatically through task dependencies.

## Configuration Files

Agent and task configurations are stored in YAML files:

```
configs/
├── agents/
│   ├── url_finder_agent.yaml          # URL Finder configuration
│   └── workflow_executor_agent.yaml   # Workflow Executor configuration
└── tasks/
    ├── url_finding_task.yaml          # URL Finding task definition
    └── workflow_execution_task.yaml   # Workflow Execution task definition
```

This allows easy tuning of:

- Agent roles and backstories
- Task descriptions and expected outputs
- LLM models
- Verbosity settings

## Why CrewAI?

CrewAI provides:

- **Task Dependencies** - Automatic context passing between agents
- **Agent Coordination** - Manages execution order
- **Tool Assignment** - Tools assigned to tasks, not agents
- **Async Support** - Works with async Python operations
- **Flexible Architecture** - Easy to add new agents/tasks

Alternative approaches (custom orchestration loops) would require building all this infrastructure manually.

---

**Summary**: Agent B uses a two-agent CrewAI system where a URL Finder agent discovers the starting point, and a Workflow Executor agent navigates and captures the workflow. Both agents use specialized tools and make decisions based on UI snapshots, with CrewAI handling coordination and context sharing.
