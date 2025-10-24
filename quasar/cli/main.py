import typer
from rich import print
import importlib

app = typer.Typer()

@app.command()
def run() -> None:
    #TODO da considerare l'async: stiamo leggendo da fs
    #TODO aggiungere logica try except e gestione errori
    #TODO spostare tutto in servizio relativo, forse è più ordinato
    importlib.invalidate_caches()
    importlib.import_module("quasar.examples.example")


@app.command()
def list() -> None:
    print("Listo niko")
if __name__ == "__main__":
    app()