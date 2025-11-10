from pydantic import BaseModel, Field

class AgentConfig(BaseModel):
    role: str = Field(..., description="The role of the agent.")
    goal: str = Field(..., description="The goal of the agent.")
    backstory: str = Field(..., description="The backstory of the agent.")
    llm: str = Field(..., description="The LLM to use for the agent.")
    verbose: bool = Field(..., description="Whether to print verbose output.")
    allow_delegation: bool = Field(..., description="Whether to allow delegation.")