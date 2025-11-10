"""
Workflow Executor Agent - Main orchestrator for UI automation workflows.

This agent is responsible for:
- Analyzing UI snapshots
- Planning action sequences
- Executing browser interactions
- Documenting workflows with screenshots
"""

import yaml
from crewai import Agent, LLM
from models.agent_config import AgentConfig


class WorkflowExecutorAgent:
    """
    Workflow Executor Agent class for creating and managing the main workflow orchestrator.
    
    This class handles:
    - Loading agent configuration from YAML
    - Generating comprehensive backstories
    - Creating and configuring the CrewAI Agent
    - Managing agent lifecycle
    """
    
    def __init__(self):
        """
        Initialize the Workflow Executor Agent.
        """
        self.config = self._load_config()
        self.agent = self._create_agent()
    
    def _load_config(self) -> AgentConfig:
        """
        Load agent configuration from YAML file.
        
        Returns:
            AgentConfig object with all configuration parameters
        """
        with open("configs/agents/workflow_executor_agent.yaml", "r") as f:
            yaml_data = yaml.safe_load(f)
            config = AgentConfig(**yaml_data["workflow_executor_agent"])
        return config
     
    def _create_agent(self) -> Agent:
        """
        Create and configure the CrewAI Agent with all parameters.
        
        Returns:
            Configured CrewAI Agent ready to execute workflows
        """

        
        agent = Agent(
            role=self.config.role,
            goal=self.config.goal,
            backstory=self.config.backstory,
            verbose=self.config.verbose,
            allow_delegation=self.config.allow_delegation,
            llm=LLM(model=self.config.llm),
            cache=False,  # Disable agent-level tool caching otherwise it does not take the latest snapshot
        )
        
        return agent
    
    def get_agent(self) -> Agent:
        """
        Get the underlying CrewAI Agent instance.
        
        Returns:
            The configured CrewAI Agent
        """
        return self.agent

