"""
FastAPI Backend for AI Multi-Agent Workflow Capture System
Coordinates agents, runs Playwright automation, and exposes REST APIs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv
from task_controller import router as task_controller_router

load_dotenv()

app = FastAPI(
    title="Agent B - Workflow Capture System",
    description="AI-driven system for autonomous web app navigation and workflow capture",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount screenshots directory
os.makedirs("screenshots", exist_ok=True)
app.mount("/screenshots", StaticFiles(directory="screenshots"), name="screenshots")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Agent B - Workflow Capture System",
        "status": "running",
        "version": "1.0.0"
    }


app.include_router(task_controller_router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

