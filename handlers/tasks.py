from fastapi import APIRouter, status, Depends
from schema.task import Task
from repository import TaskRepository
from database.models import Tasks
from dependency import get_task_service, get_tasks_repository, get_cache_task
from service import TaskService

from typing import Annotated

router = APIRouter(prefix="/task", tags=["task"])


@router.get(
        "/all",
        response_model=list[Task]
        )
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)]
    ):
    return task_service.get_tasks()


@router.post("/")
async def create_task(task: Task, tasks_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    task_id = tasks_repository.create_task(task)
    return {"message": task_id}

@router.get(
        "/{task_id}",
        response_model=Task
        )
async def get_task(task_id: int, tasks_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    return tasks_repository.get_task(task_id)

@router.patch(
        "/{task_id}",
        response_model=Task
        )
async def patch_task(task_id: int, name: str, tasks_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    task = tasks_repository.update_task_name(task_id, name)
    return task

@router.delete(
        "/{task_id}",
        status_code=status.HTTP_204_NO_CONTENT
        )
async def delete_task(task_id: int, tasks_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    tasks_repository.delete_task(task_id)
    return {"message": "task deleted"}
