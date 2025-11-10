"""
URL Finding Task - Discovers and navigates to the correct starting page.

This task is responsible for:
- Searching the web for relevant URLs
- Navigating to candidate pages
- Verifying the correct starting point
- Confirming navigation to the verified URL
"""

import yaml
from crewai import Task, Agent
from models.task_config import TaskConfig
from models.url_finder_agent_output import URLFinderOutput


class URLFindingTask:
    """
    URL Finding Task class for creating tasks that discover workflow starting points.
    
    This class handles:
    - Loading task configuration from YAML
    - Creating and configuring the CrewAI Task
    """
    
    def __init__(self, agent: Agent, tools: list):
        """
        Initialize the URL Finding Task.
        
        Args:
            agent: The URLFinderAgent instance that will execute this task
            tools: List of tools available for this task
        """
        self.agent = agent
        self.tools = tools
        self.config = self._load_config()
        self.task = self._create_task()
    
    def _load_config(self) -> TaskConfig:
        """
        Load task configuration from YAML file.
        
        Returns:
            TaskConfig object with description and expected output
        """
        with open("configs/tasks/url_finding_task.yaml", "r") as f:
            yaml_data = yaml.safe_load(f)
            config = TaskConfig(**yaml_data["url_finding_task"])
        return config
    
    def _create_task(self) -> Task:
        """
        Create and configure the CrewAI Task.
        
        Returns:
            Configured CrewAI Task ready to find and verify URLs
        """
        
        task = Task(
            description=self.config.description,
            expected_output=self.config.expected_output,
            agent=self.agent,
            tools=self.tools,
            output_pydantic=URLFinderOutput,
        )
        
        return task
    
    def get_task(self) -> Task:
        """
        Get the underlying CrewAI Task instance.
        
        Returns:
            The configured CrewAI Task
        """
        return self.task

