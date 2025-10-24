import uuid
from quasar.model.task_model import TaskModel

class TaskRegistry:
    def __init__(self):
        self.tasks = {}

    def register(self, task: TaskModel) -> TaskModel:
        self.tasks[task.id] = task
        return task

    def get_task_by_id(self, id: uuid.UUID) -> TaskModel:
        return self.tasks[id]

    def get_all(self) -> list[TaskModel]:
        return list(self.tasks.values())

    def clear(self):
        self.tasks.clear()

    def count(self):
        return len(self.tasks)
