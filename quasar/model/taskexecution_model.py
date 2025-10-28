import datetime
import uuid
from dataclasses import dataclass, field

from quasar.model.task_model import TaskModel


class TaskExecutionStatus:
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"


@dataclass
class TaskExecutionModel:
    execution_id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: str = TaskExecutionStatus.UNKNOWN
    started_at: datetime.datetime | None = None
    finished_at: datetime.datetime | None = None
    retry: bool = False
    attempt_count: int | None = None
    related_task: TaskModel | None = None
    failing_reason: str | None = None

    def __init__(self, task: TaskModel):
        self.related_task = task
        self.execution_id = uuid.uuid4()
        self.status = TaskExecutionStatus.PENDING
        self.started_at = None
        self.finished_at = None
