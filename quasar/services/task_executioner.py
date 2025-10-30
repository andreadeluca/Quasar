from queue import Queue, LifoQueue
from datetime import datetime
from quasar.model.task_model import TaskModel
from quasar.model.taskexecution_model import TaskExecutionModel
from quasar.utils.logging_factory import get_logger

logger = get_logger(__name__)

class TaskExecutioner:

    execution_queue : LifoQueue[TaskExecutionModel]

    def __init__(self, execution_list: list[TaskModel] | None = None) -> None:
        self.execution_queue: Queue[TaskExecutionModel] = Queue()
        [self.execution_queue.put(TaskExecutionModel(task)) for task in execution_list if task is not None]

    def execute_tasks(self):
        retry_queue = Queue()
        while not self.execution_queue.empty() or not retry_queue.empty():
            if not retry_queue.empty():
                execution = retry_queue.get()
            else:
                execution = self.execution_queue.get()

            task = execution.related_task
            try:
                execution.started_at = datetime.now()
                execution.status = "RUNNING"
                execution.attempt_count += 1
                task.func()
                execution.status = "SUCCESS"
            except Exception as e:
                execution.status = "FAILED"
                execution.failing_reason = str(e)
                logger.error(f"An error occurred while running task {task.name}:{e}")
                if execution.attempt_count <= task.retries:
                    logger.error(f"Task {task.name} failed {execution.attempt_count} time(s)). Will retry.")
                    retry_queue.put(execution)
                #TODO Retry policy, fatal error handling and much more goes here
            finally:
                execution.finished_at = datetime.now()