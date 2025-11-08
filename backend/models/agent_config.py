from pydantic import BaseModel, Field

class AgentConfig(BaseModel):
    role: str = Field(..., description="The role of the agent.")
    goal: str = Field(..., description="The goal of the agent.")
    backstory: str = Field(..., description="The backstory of the agent.")
    reasoning_style: str = Field(..., description="The reasoning style of the agent.")
    tool_usage_guidelines: str = Field(..., description="The tool usage guidelines of the agent.")
    output_format_guidelines: str = Field(..., description="The output format guidelines of the agent.")
    examples_few_shot: str = Field(..., description="The examples few shot of the agent.")
    llm: str = Field(..., description="The LLM to use for the agent.")
    verbose: bool = Field(..., description="Whether to print verbose output.")
    allow_delegation: bool = Field(..., description="Whether to allow delegation.")