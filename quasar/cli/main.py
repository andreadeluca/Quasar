import typer
from rich import print
from quasar.core.task_decorator import TASK_REGISTRY
import importlib

app = typer.Typer()

@app.command()
def run() -> None:
    importlib.import_module("quasar.examples.example")

    # ora TASK_REGISTRY è pieno
    print(f"Ciao Niko ora  {len(TASK_REGISTRY.get_all())} tasks.")
@app.command()
def list() -> None:
    print("Listo niko")
if __name__ == "__main__":
    app()