from collections import defaultdict, deque

from model.task_model import TaskModel
from services.task_registry import TaskRegistry
from utils.const import CONST
from utils.errorManager import CircularDependencyError


class TaskResolver:
    def __init__(self, task_registry: TaskRegistry):
        self.task_registry = task_registry
        self.execution_order = []
        self.algorithm = CONST.DEFAULT_ALGORITHM


    def resolve_execution_order(self, tasks: list[TaskModel] | None = None)  -> list[TaskModel] | None:
        if tasks is None:
            tasks = self.task_registry.tasks

        task_map = {t.name: t for t in tasks}
        deps = {t.name: set(t.depends_on) for t in tasks}
        ready = [name for name, d in deps.items() if not d]
        self.execution_order = []

        if not ready:
            raise CircularDependencyError("No root tasks found! Circular dependency detected.")
        while ready:
            current = ready.pop(0)
            self.execution_order.append(task_map[current])
            for name, d in deps.items():
                if current in d:
                    d.remove(current)
                    if not d and name not in [t.name for t in self.execution_order] and name not in ready:
                        ready.append(name)
            deps[current].clear()

        if any(deps.values()):
            raise CircularDependencyError("Circular dependency detected.")

        return self.execution_order

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
            raise CircularDependencyError("Circular dependency detected.")
        return out
