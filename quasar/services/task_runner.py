from quasar.model.task_model import TaskModel
from quasar.services.task_registry import TaskRegistry


class Runner:
    def __init__(self, task_registry: TaskRegistry):
        self.task_registry = task_registry

    def run_tasks(self, tasks: list[TaskModel] | None = None) -> None:
        _tasks_graph = {}
        if tasks is None:
            tasks = self.task_registry.tasks

        results = self._check_deps(tasks)
        if results["errors"]:
            print("[ERROR] Dependency validation failed.")
            for e in results["errors"]:
                print(f"  - {e['task']} → {e['issue']}")
            return
        if results["warnings"]:
            print("[WARNING] Some dependencies are missing, but execution can continue.")
            for w in results["warnings"]:
                print(f"  - {w['task']} → {w['issue']}")
        # procedo a costruire il grafo
        _tasks_graph = self._build_graph(tasks)
        _execution_list = self._resolve_execution_order(_tasks_graph, tasks)

        print("[INFO] Task execution order:")
        [print(f"{e}") for e in _execution_list]



    def _check_deps(self, tasks: list[TaskModel]) -> dict[str, list]:
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

    @staticmethod
    def _build_graph(tasks: list[TaskModel]) -> dict[str, list]:
        return {task.name: list(task.depends_on) for task in tasks}

    def _resolve_execution_order(self, graph: dict[str, list[str]], tasks: list[TaskModel]) -> list[TaskModel]:
        task_map = {t.name: t for t in tasks}
        g = {name: set(deps) for name, deps in graph.items()}  # usare set per performance
        ready = [name for name, deps in g.items() if not deps]
        execution_order: list[TaskModel] = []

        if not ready:
            print("[ERROR] No root tasks found! Circular dependency detected.")
            return []

        while ready:
            current = ready.pop(0)  # FIFO
            execution_order.append(task_map[current])

            for name, deps in g.items():
                if current in deps:
                    deps.remove(current)
                    if not deps and name not in [t.name for t in execution_order] and name not in ready:
                        ready.append(name)

            g[current].clear()

        if any(g[name] for name in g):
            print("[ERROR] Circular dependency detected: some tasks could not be resolved.")

        return execution_order

