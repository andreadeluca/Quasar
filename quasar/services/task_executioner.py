from queue import Queue
from datetime import datetime
from model.task_model import TaskModel
from model.taskexecution_model import TaskExecutionModel


class TaskExecutioner:

    execution_queue : Queue[TaskExecutionModel]

    def __init__(self, execution_list: list[TaskModel] | None = None) -> None:
        self.execution_queue: Queue[TaskExecutionModel] = Queue()
        [self.execution_queue.put(TaskExecutionModel(task)) for task in execution_list if task is not None]

    def execute_tasks(self):
        while not self.execution_queue.empty():
            execution = self.execution_queue.get()
            task = execution.related_task
            try:
                execution.started_at = datetime.now()
                task.func()
                execution.status = "SUCCESS"
            except Exception as e:
                execution.status = "FAILED"
                execution.failing_reason = str(e)
                #TODO Retry policy, fatal error handling and much more goes here
            finally:
                execution.finished_at = datetime.now()