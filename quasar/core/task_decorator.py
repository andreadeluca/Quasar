from typing import Callable

from quasar.model.task_model import Task, TaskRegistry

TASK_REGISTRY = TaskRegistry()

def task(depends_on=None):
    depends_on = depends_on or []
    def decorator(func: Callable):
        # TODO Formal control parsing module?
        t = Task(func=func, depends_on=depends_on)
        TASK_REGISTRY.register(t)
        return func
    return decorator


