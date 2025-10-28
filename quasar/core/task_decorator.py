from typing import Callable

from quasar.model.task_model import TaskModel
from quasar.services.task_registry import TaskRegistry

TASK_REGISTRY = TaskRegistry()


def task(depends_on=None):
    depends_on = depends_on or []

    def decorator(func: Callable):
        t = TaskModel(func=func, name=func.__name__, depends_on=depends_on, module=func.__module__)
        TASK_REGISTRY.register(t)
        return func

    return decorator
