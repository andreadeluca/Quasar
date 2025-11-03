from typing import Callable

from quasar.model.task_model import TaskModel
from quasar.services.task_registry import TaskRegistry
from quasar.utils.logging_factory import get_logger

TASK_REGISTRY = TaskRegistry()

logger = get_logger(__name__)

def task(depends_on=None, retries=0):
    depends_on = depends_on or []

    def decorator(func: Callable):
        t = TaskModel(func=func, name=func.__name__, depends_on=depends_on, module=func.__module__, retries=retries | 0)
        TASK_REGISTRY.register(t)
        return func

    return decorator
