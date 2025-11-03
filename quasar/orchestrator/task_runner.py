from quasar.model.task_model import TaskModel
from quasar.services.task_registry import TaskRegistry
from quasar.utils.logging_factory import get_logger
from services.deps_checker import DepsChecker
from services.task_executioner import TaskExecutioner
from services.task_resolver import TaskResolver
from utils.const import ALGORITHMS

logger = get_logger(__name__)

class TaskOrchestrator:
    def __init__(self, task_registry: TaskRegistry, algorithm=ALGORITHMS.DEFAULT_ALGORITHM):
        self.task_registry = task_registry
        self.algorithm = algorithm

    def run_tasks(self, tasks: list[TaskModel] | None = None) -> None:
        checker = DepsChecker(self.task_registry)
        solver = TaskResolver(self.task_registry, self.algorithm)

        if tasks is None:
            tasks = self.task_registry.tasks

        results = checker.check_deps(tasks)

        if results["errors"]:
            logger.debug("[ERROR] Dependency validation failed.")
            for e in results["errors"]:
                logger.debug(f"  - {e['task']} → {e['issue']}")
            return
        if results["warnings"]:
            logger.debug("[WARNING] Some dependencies are missing, but execution can continue.")
            for w in results["warnings"]:
                logger.debug(f"  - {w['task']} → {w['issue']}")

        execution_list = solver.resolve_execution_order()
        executioner = TaskExecutioner(execution_list)
        executioner.execute_tasks()

