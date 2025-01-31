from redis import asyncio as Redis
from schema.task import Task

class CacheTask:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self, user_id: int) -> list[Task] | None:
        async with self.redis as redis:
            if tasks_json := await redis.lrange(f"tasks:{user_id}", 0, -1):
                return [Task.model_validate_json(task_json) for task_json in tasks_json]
        return None

    async def set_tasks(self, tasks: list[Task]):
        tasks_json = [task.model_dump_json() for task in tasks]
        async with self.redis as redis:
            await redis.rpush("tasks", *tasks_json)
