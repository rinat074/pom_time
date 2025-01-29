from fastapi import APIRouter, HTTPException, status, Depends
from exception import TaskNotFoundError
from schema import Task, TaskCreateSchema
from repository import TaskRepository
from dependency import get_task_service, get_tasks_repository, get_cache_task, get_request_user_id
from service import TaskService

from typing import Annotated

router = APIRouter(prefix="/task", tags=["task"])


@router.get(
        "/all",
        response_model=list[Task]
        )
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
    ):
    return task_service.get_tasks(user_id)


@router.post("/")
async def create_task(
    body: TaskCreateSchema, 
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
    ):
    task = task_service.create_task(body, user_id)
    return {"message": task.id}

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
async def patch_task(
    task_id: int, 
    name: str, 
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
    ):
    try:
        task = task_service.update_task_name(task_id, name, user_id)
        return task
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)

@router.delete(
        "/{task_id}",
        status_code=status.HTTP_204_NO_CONTENT
        )
async def delete_task(
    task_id: int, 
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
    ):
    try:
        task_service.delete_task(task_id, user_id)
        return {"message": "task deleted"}
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)