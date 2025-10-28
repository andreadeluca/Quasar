import pytest

from quasar.model.task_model import TaskModel
from quasar.services.task_registry import TaskRegistry
from orchestrator.task_runner import TaskOrchestrator


@pytest.fixture
def complex_tasks():
    """
    Crea il DAG complesso da usare per i test.
    """
    return [
        TaskModel(name="setup_env", depends_on=[]),
        TaskModel(name="init_db", depends_on=[]),
        TaskModel(name="load_config", depends_on=["setup_env"]),
        TaskModel(name="seed_db", depends_on=["init_db"]),
        TaskModel(name="start_services", depends_on=["load_config", "seed_db"]),
        TaskModel(name="run_integration_tests", depends_on=["start_services"]),
        TaskModel(name="build_frontend", depends_on=["start_services"]),
        TaskModel(name="prepare_artifacts", depends_on=["start_services"]),
        TaskModel(name="deploy_staging", depends_on=["run_integration_tests", "build_frontend", "prepare_artifacts"]),
        TaskModel(name="smoke_test", depends_on=["deploy_staging"]),
        TaskModel(name="notify_team", depends_on=["deploy_staging"]),
        TaskModel(name="promote_to_production", depends_on=["smoke_test", "notify_team"]),
    ]


def test_execution_order_is_valid(complex_tasks):
    """
    Verifica che il resolver restituisca un ordine coerente con le dipendenze.
    """
    registry = TaskRegistry()
    registry.tasks = complex_tasks
    runner = TaskOrchestrator(task_registry=registry)

    # Costruisco grafo e ordine di esecuzione
    graph = runner._build_graph(complex_tasks)
    execution_order = runner._resolve_execution_order(graph, complex_tasks)

    # Estraggo solo i nomi
    ordered_names = [t.name for t in execution_order]

    # --- 1️⃣ Assicuro che siano tutti i task ---
    assert set(ordered_names) == {t.name for t in complex_tasks}, "Alcuni task mancano nell'ordine finale"

    # --- 2️⃣ Ogni task deve comparire dopo le sue dipendenze ---
    index = {name: i for i, name in enumerate(ordered_names)}
    for task in complex_tasks:
        for dep in task.depends_on:
            assert index[dep] < index[task.name], (
                f"Task '{task.name}' eseguito prima della sua dipendenza '{dep}'"
            )


def test_detects_circular_dependency():
    """
    Verifica che venga segnalata una dipendenza circolare.
    """
    registry = TaskRegistry()
    registry.tasks = [
        TaskModel(name="a", depends_on=["b"]),
        TaskModel(name="b", depends_on=["a"]),
    ]
    runner = TaskOrchestrator(task_registry=registry)
    graph = runner._build_graph(registry.tasks)

    with pytest.raises(RuntimeError):
        runner._resolve_execution_order(graph, registry.tasks)
