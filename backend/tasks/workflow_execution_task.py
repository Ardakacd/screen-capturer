"""
Workflow Execution Task - Orchestrates UI automation workflows.

This task is responsible for:
- Analyzing UI snapshots
- Planning and executing action sequences
- Documenting workflows with screenshots
- Providing comprehensive explanations
"""

import yaml
from crewai import Task, Agent
from models.task_config import TaskConfig
from models.workflow_executor_output import WorkflowExecutorOutput

class WorkflowExecutionTask:
    """
    Workflow Execution Task class for creating workflow execution tasks.
    
    This class handles:
    - Loading task configuration from YAML
    - Creating and configuring the CrewAI Task
    """
    
    def __init__(self, agent: Agent, tools: list, url_finding_task: Task):
        """
        Initialize the Workflow Execution Task.
        
        Args:
            agent: The WorkflowExecutorAgent instance that will execute this task
            tools: List of tools available for this task
        """
        self.agent = agent
        self.tools = tools
        self.url_finding_task = url_finding_task
        self.config = self._load_config()
        self.task = self._create_task()
    
    def _load_config(self) -> TaskConfig:
        """
        Load task configuration from YAML file.
        
        Returns:
            TaskConfig object with description and expected output
        """
        with open("configs/tasks/workflow_execution_task.yaml", "r") as f:
            yaml_data = yaml.safe_load(f)
            config = TaskConfig(**yaml_data["workflow_execution_task"])
        return config
    
    def _create_task(self) -> Task:
        """
        Create and configure the CrewAI Task.
        
        Returns:
            Configured CrewAI Task ready to execute workflows
        """
        
        task = Task(
            description=self.config.description,
            expected_output=self.config.expected_output,
            agent=self.agent,
            tools=self.tools,
            context=[self.url_finding_task],
            output_pydantic=WorkflowExecutorOutput,
        )
        
        return task
    
    def get_task(self) -> Task:
        """
        Get the underlying CrewAI Task instance.
        
        Returns:
            The configured CrewAI Task
        """
        return self.task


