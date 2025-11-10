import json
from crewai import Crew
from session import ensure_session
from models.start_task import StartTaskRequest, StartTaskResponse
from helper.take_screenshot import take_screenshot
from helper.page_helper import get_current_page
from create_tools import create_tools
from agents.workflow_executor_agent import WorkflowExecutorAgent
from agents.url_finder_agent import URLFinderAgent
from tasks.workflow_execution_task import WorkflowExecutionTask
from tasks.url_finding_task import URLFindingTask

class TaskService:

    async def start_task(self, start_task_request: StartTaskRequest) -> StartTaskResponse:
        """
        Start a new task by coordinating browser session, tools, crew, and execution.
        """
        # Setup browser session
        browser, context = await ensure_session(
            login_url=start_task_request.login_url,
            session_path=start_task_request.session_path
        )

        id_number = start_task_request.task_id

        # Create all available tools
        all_tools = create_tools(context, id_number)
        
        # Separate tools for different tasks
        url_finder_tools = [tool for tool in all_tools if tool.name in ["web_search_url_tool", "navigate_page_and_take_screenshot_tool", "capture_ui_snapshot_tool"]]
        executor_tools = [tool for tool in all_tools if tool.name != "web_search_url_tool"]
        
        
        url_finder_agent = URLFinderAgent().get_agent()
        workflow_executor_agent = WorkflowExecutorAgent().get_agent()
        
        # Create tasks (with tools)
        url_finding_task = URLFindingTask(
            agent=url_finder_agent,
            tools=url_finder_tools
        ).get_task()
        
        workflow_execution_task = WorkflowExecutionTask(
            agent=workflow_executor_agent,
            tools=executor_tools,
            url_finding_task=url_finding_task,
        ).get_task()
        
        # Create crew with agents and tasks
        crew = Crew(
            agents=[url_finder_agent, workflow_executor_agent],
            tasks=[url_finding_task, workflow_execution_task],
            verbose=True,
            cache=False,   # Disable tool result caching otherwise it does not work with the snapshot tool
        )
        
        result = await crew.kickoff_async(inputs={"task_description": start_task_request.task})

        print("\n=== FINAL RESULT ===")
        print(result)
        
        # Finalize workflow result with final screenshot
        final_result = await self._finalize_workflow_result(result, context, id_number)

        await browser.close()

        return final_result

    async def _finalize_workflow_result(
        self, 
        result, 
        context, 
        id_number: str
    ) -> StartTaskResponse:
        """
        Finalize the workflow result by parsing output and capturing final screenshot.
        
        Args:
            result: The CrewAI task result
            context: Browser context for taking final screenshot
            id_number: Task identifier for screenshot naming
            
        Returns:
            StartTaskResponse with paths and explanation
        """
        
        parsed = result.pydantic.model_dump() if hasattr(result, 'pydantic') else json.loads(result.raw)
        paths = parsed.get("paths", [])
        explanation = parsed.get("explanation", "")

        current_page = await get_current_page(context)
        final_screenshot_path = await take_screenshot(current_page, id_number, tag="final_state")

        paths.append(final_screenshot_path)

        return StartTaskResponse(
            paths=paths,
            explanation=explanation
        )
    


def get_task_service() -> TaskService:
    return TaskService()
        
        
        