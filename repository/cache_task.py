from redis import Redis
from schema.task import Task

class CacheTask:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> list[Task] | None:
        if tasks_json := self.redis.lrange("tasks", 0, -1):
            return [Task.model_validate_json(task_json) for task_json in tasks_json]
        return None

    def set_tasks(self, tasks: list[Task]):
        tasks_json = [task.model_dump_json() for task in tasks]
        self.redis.rpush("tasks", *tasks_json)
