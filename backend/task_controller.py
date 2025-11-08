import logging
from fastapi import APIRouter, HTTPException, Depends
from models.start_task import StartTaskRequest, StartTaskResponse
from task_service import get_task_service, TaskService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/start", response_model=StartTaskResponse)
async def start_task(request: StartTaskRequest, task_service: TaskService = Depends(get_task_service)):
    """
    Main endpoint: accepts task text, launches automation, and returns workflow steps
    
    Example:
        POST /tasks/start
        {
            "site_url": "https://notion.so",
            "login_url": "https://notion.so/login",
            "session_path": "session.json"
            "task": "How do I create a project in Notion?"
        }
    """
    try:
        return await task_service.start_task(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task execution failed: {str(e)}")