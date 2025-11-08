import nest_asyncio
import yaml
from crewai import Agent, LLM
from create_tools import create_tools
from datetime import datetime
import json
import os
from session import ensure_session
from models.start_task import StartTaskRequest, StartTaskResponse
from models.agent_config import AgentConfig
from helper.take_screenshot import take_screenshot

nest_asyncio.apply()  

class TaskService:
    async def start_task(self, start_task_request: StartTaskRequest) -> StartTaskResponse:
        """
        Start a new task
        """
        
        with open("configs/planner_agent.yaml", "r") as f:
            yaml_data = yaml.safe_load(f)
            config = AgentConfig(**yaml_data["planner_agent"])

        browser, page = await ensure_session(
            site_url=start_task_request.site_url,
            login_url=start_task_request.login_url,
            session_path=start_task_request.session_path
        )


        id_number = start_task_request.task_id

        # Create tools (passing Playwright page)
        tools = create_tools(page, id_number)

        full_backstory = self._generate_full_backstory(config)
        
        # Initialize CrewAI agent with specific LLM
        planner = Agent(
            role=config.role,
            goal=config.goal,
            backstory=full_backstory,
            verbose=config.verbose,
            allow_delegation=config.allow_delegation,
            tools=tools,
            llm=LLM(
        model=config.llm), 
        )

        result = await planner.kickoff_async(start_task_request.task)

        print("\n=== FINAL RESULT ===")
        
        parsed = json.loads(result.raw)
        paths = parsed.get("paths", [])
        explanation = parsed.get("explanation", "")

        final_screenshot_path = await take_screenshot(page, id_number, tag="final_state")

        paths.append(final_screenshot_path)

        final_result = StartTaskResponse(
            paths=paths,
            explanation=explanation
        )

        print(final_result.model_dump_json())

        await browser.close()

        return final_result

    def _generate_full_backstory(self, config: AgentConfig) -> str:
        full_backstory = (
            config.backstory
            + "\n\n---\n\nTool Usage Guidelines:\n"
            + config.tool_usage_guidelines
            + "\n\n---\n\nReasoning Style:\n"
            + config.reasoning_style
            + "\n\n---\n\nOutput Format Guidelines:\n"
            + config.output_format_guidelines
            + "\n\n---\n\nFew-Shot Examples:\n"
            + config.examples_few_shot
        )
        return full_backstory


def get_task_service() -> TaskService:
    return TaskService()
        
        
        