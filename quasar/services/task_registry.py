import uuid
from quasar.model.task_model import Task_Model

class TaskRegistry:
    def __init__(self):
        self.tasks: dict[uuid.UUID, Task_Model] = {}

    def register(self, task: Task_Model) -> Task_Model:
        self.tasks[task.id] = task
        return task

    def get_task_by_id(self, id: uuid.UUID) -> Task_Model:
        return self.tasks[id]

    def get_all(self) -> list[Task_Model]:
        return list(self.tasks.values())

    def clear(self):
        self.tasks.clear()

    def count(self):
        return len(self.tasks)
