from pydantic import BaseModel, Field


class TaskConfig(BaseModel):
    description: str = Field(..., description="The task description and instructions.")
    expected_output: str = Field(..., description="The expected output format for the task.")

