from fastapi import APIRouter

task_router = APIRouter(prefix="/v1/tasks", tags=["task"])
"""
Endpoints for manage Tasks.
"""
