"""
URL Finder Agent - Discovers and verifies starting URLs for workflows.

This agent is responsible for:
- Searching the web for relevant URLs based on task descriptions
- Navigating to candidate pages
- Verifying the correct starting point through UI inspection
- Returning the verified full URL
"""

import yaml
from crewai import Agent, LLM
from models.agent_config import AgentConfig


class URLFinderAgent:
    """
    URL Finder Agent class for discovering and verifying workflow starting points.
    
    This class handles:
    - Loading agent configuration from YAML
    - Generating comprehensive backstories
    - Creating and configuring the CrewAI Agent
    - Managing agent lifecycle
    """
    
    def __init__(self):
        """
        Initialize the URL Finder Agent.
        """
        self.config = self._load_config()
        self.agent = self._create_agent()
    
    def _load_config(self) -> AgentConfig:
        """
        Load agent configuration from YAML file.
        
        Returns:
            AgentConfig object with all configuration parameters
        """
        with open("configs/agents/url_finder_agent.yaml", "r") as f:
            yaml_data = yaml.safe_load(f)
            config = AgentConfig(**yaml_data["url_finder_agent"])
        return config
    
    def _create_agent(self) -> Agent:
        """
        Create and configure the CrewAI Agent with all parameters.
        
        Returns:
            Configured CrewAI Agent ready to find and verify URLs
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

