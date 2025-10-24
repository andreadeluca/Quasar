from quasar.model.task_model import TaskModel
from quasar.model.taskexecution_model import TaskExecutionModel
from quasar.services.task_registry import TaskRegistry


class Runner:
    def __init__(self, task_registry: TaskRegistry):
        self.task_registry = task_registry

    def run_tasks(self, tasks: list[TaskModel] | None = None) -> None:
        if tasks is None:
            tasks = self.task_registry.tasks
        for task in tasks:
            TaskExecutionModel(task)
