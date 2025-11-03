
import typer

from orchestrator.task_runner import TaskOrchestrator
from quasar.core.task_decorator import TASK_REGISTRY
from quasar.utils.logging_factory import get_logger
from quasar.services.module_manager import ModuleManager
from utils.const import ALGORITHMS

logger = get_logger(__name__)

app = typer.Typer(no_args_is_help=True)


@app.command()
def run(
        algorithm: str | None = typer.Option(ALGORITHMS.DEFAULT_ALGORITHM,"--alg","-a", help="Algorithm used to analyze solve task dependencies and order."),
        path_module: str | None = typer.Argument(None, help="Path to the module to load."),
    ) -> None:
    # TODO da considerare l'async: stiamo leggendo da fs
    # TODO aggiungere logica try except e gestione errori
    # TODO spostare tutto in servizio relativo, forse è più ordinato
    if not (path_module and path_module.strip()):
        raise typer.BadParameter(
            "Please specify a file or a directory. (E.g. 'quasar.examples.example' or 'src/tasks/'")

    module_manager = ModuleManager(path_module)
    module_manager.import_module()
    runner = TaskOrchestrator(TASK_REGISTRY, algorithm)
    runner.run_tasks()


@app.command()
def list() -> None:
    logger.debug("Listo niko")


if __name__ == "__main__":
    app()
