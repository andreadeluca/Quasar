import importlib

import typer

from orchestrator.task_runner import TaskOrchestrator
from quasar.core.task_decorator import TASK_REGISTRY
from quasar.utils.logging_factory import get_logger

logger = get_logger(__name__)

app = typer.Typer()


@app.command()
def run() -> None:
    # TODO da considerare l'async: stiamo leggendo da fs
    # TODO aggiungere logica try except e gestione errori
    # TODO spostare tutto in servizio relativo, forse è più ordinato
    importlib.invalidate_caches()
    # TODO Leggere da più files.
    importlib.import_module("quasar.examples.example")
    runner = TaskOrchestrator(TASK_REGISTRY)
    runner.run_tasks()


@app.command()
def list() -> None:
    logger.debug("Listo niko")


if __name__ == "__main__":
    app()
