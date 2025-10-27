from collections import defaultdict, deque

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

        #execute tasks
        for task in _execution_list:
            task.func()


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


    @staticmethod
    def _resolve_execution_order(tasks: list[TaskModel]) -> list[TaskModel]:
        task_map = {t.name: t for t in tasks}
        deps = {t.name: set(t.depends_on) for t in tasks}
        ready = [name for name, d in deps.items() if not d]
        order = []

        if not ready:
            raise RuntimeError("No root tasks found! Circular dependency detected.")
            #TODO maybe it would be better to specify a specific error for this case... "CircularDependencyError"
        while ready:
            current = ready.pop(0)
            order.append(task_map[current])
            for name, d in deps.items():
                if current in d:
                    d.remove(current)
                    if not d and name not in [t.name for t in order] and name not in ready:
                        ready.append(name)
            deps[current].clear()

        if any(deps.values()):
            raise RuntimeError("Circular dependency detected.")

        return order

    '''
    Method that needs to be tested.
    #TODO in the future, it would be nice that it would be possible to choose between algorithms.
    '''

    @staticmethod
    def stable_toposort(tasks, deps):
        indegree = {t: 0 for t in tasks}
        graph = defaultdict(set)

        # Costruisci grafo e indegree
        for task in tasks:
            for d in deps.get(task, ()):
                graph[d].add(task)
                indegree[task] += 1

        # Coda stabile (ordine di inserimento)
        q = deque([t for t in tasks if indegree[t] == 0])
        out = []

        while q:
            t = q.popleft()
            out.append(t)

            for v in graph[t]:
                indegree[v] -= 1
                if indegree[v] == 0:
                    q.append(v)  # mantiene ordine originale
        if len(out) != len(tasks):
            raise ValueError("Ciclo di dipendenze rilevato")
        return out