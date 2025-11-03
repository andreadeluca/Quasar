import inspect

from quasar.model.task_model import TaskModel


class TaskRegistry:
    def __init__(self):
        self.tasks = []

    def register(self, task: TaskModel):

        if inspect.iscoroutinefunction(task.func):
            raise RuntimeError('Async function are not supported at the moment')

        if not self.is_in_task_registry_by_name(task.func.__name__):
            self.tasks.append(task)
        else:
            raise RuntimeError(f"Task {task.func.__name__} already registered, task name must be unique.")


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
