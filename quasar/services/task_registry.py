import uuid

from quasar.model.task_model import TaskModel


class TaskRegistry:
    def __init__(self):
        self.tasks = []

    def register(self, task: TaskModel):
        self.tasks.append(task)

    def get_task_by_name(self, name: str) -> TaskModel | None:
        for task in self.tasks:
            if task.name == name:
                return task
        return None

    def is_in_task_registry_by_name(self, name: str) -> bool:
        return True if self.get_task_by_name(name) else False

    def clear(self):
        self.tasks.clear()

    def count(self):
        return len(self.tasks)
