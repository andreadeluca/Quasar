import uuid
from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class TaskModel:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str | None = None
    func: Callable = None
    depends_on: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, task_dict: dict):
        return cls(
            id=task_dict.get("id", uuid.uuid4()),
            name=task_dict.get("name") or task_dict["func"].__name__,
            func=task_dict["func"],
            depends_on=task_dict.get("depends_on", []),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name or self.func.__name__,
            "func": self.func,
            "depends_on": self.depends_on,
        }


