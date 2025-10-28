from queue import Queue

from model.task_model import TaskModel
from model.taskexecution_model import TaskExecutionModel


class TaskExecutionService:

    execution_queue : Queue[TaskExecutionModel] = Queue()

    def __init__(self, execution_list: list[TaskModel] | None = None) -> None:
        [self.execution_queue.put(TaskExecutionModel(task)) for task in execution_list if task is not None]

    def execute_tasks(self):
        while not self.execution_queue.empty():
            execution = self.execution_queue.get()
            execution.related_task.func()