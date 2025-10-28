from typing import Callable

from quasar.model.task_model import TaskModel
from quasar.services.task_registry import TaskRegistry

TASK_REGISTRY = TaskRegistry()


def task(depends_on=None):
    depends_on = depends_on or []

    def decorator(func: Callable):
        # TODO Formal control parsing module?
        if not TASK_REGISTRY.is_in_task_registry_by_name(func.__name__):
            t = TaskModel(func=func, name=func.__name__, depends_on=depends_on)
            TASK_REGISTRY.register(t)
        else:
            raise RuntimeError(f"Task {func.__name__} already registered, task name must be unique.")
        return func

    return decorator
