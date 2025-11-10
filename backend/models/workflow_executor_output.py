from pydantic import BaseModel, Field
from typing import List

class WorkflowExecutorOutput(BaseModel):
    paths: List[str] = Field(..., description="The paths of the screenshots of the effective steps.")
    explanation: str = Field(..., description="The explanation of the steps in the order of the steps.")

