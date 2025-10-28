from quasar.model.task_model import TaskModel
from quasar.services.task_registry import TaskRegistry


class DepsChecker:

    def __init__(self, task_registry: TaskRegistry) -> None:
        self.task_registry = task_registry

    def check_deps(self, tasks: list[TaskModel] | None = None) -> dict[str, list] | None:

        if tasks is None:
            tasks = self.task_registry.tasks

        results = {"errors": [], "warnings": []}
        has_root_task = False

        if not tasks:
            return results

        for task in tasks:
            if not task.depends_on:
                has_root_task = True
            for dep in task.depends_on:

                # WARNINGS
                if not self.task_registry.is_in_task_registry_by_name(dep):
                    results["warnings"].append({
                        "task": task.name,
                        "dependency": dep,
                        "issue": f"Orphan dependency '{dep}' not found in task registry."
                    })
                    continue

                # ERRORS
                if dep == task.name:
                    results["errors"].append({
                        "task": task.name,
                        "dependency": dep,
                        "issue": "Task name conflict: a task cannot depend on itself."
                    })

        if not has_root_task:
            results["errors"].append({
                "task": "ALL",
                "issue": "Circular dependency detected: no task can start."
            })

        return results