from pydantic import BaseModel, Field
from typing import Optional, List


class StartTaskRequest(BaseModel):
    login_url: Optional[str] = Field(None, description="The login URL to navigate to.")
    session_path: str = Field(..., description="The path to store the session.")
    task: str = Field(..., description="The task to complete.")
    task_id: str = Field(..., description="The ID of the task.")


class StartTaskResponse(BaseModel):
    paths: List[str] = Field(..., description="List of saved screenshot paths showing the completed workflow.")
    explanation: str = Field(..., description="Step-by-step explanation of how the workflow was completed.")