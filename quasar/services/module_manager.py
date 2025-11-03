# quasar/core/module_manager.py
import importlib
import importlib.util
from importlib import invalidate_caches
from pathlib import Path
import logging
import typer
import ast

logger = logging.getLogger("quasar.module_manager")


class ModuleManager:
    """
    Gestisce la risoluzione, validazione e import dinamico di un modulo.
    """

    def __init__(self, module_name: str):
        self.module_name = module_name
        self.spec = importlib.util.find_spec(module_name)

        if self.spec is None or self.spec.origin is None:
            raise typer.BadParameter(f"Impossible to find '{module_name}'.")

        self.file_path = Path(self.spec.origin)

    # ----------------------------------------------------------------------

    def _validate_ast(self) -> bool:
        try:
            source = self.file_path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(self.file_path))
            compile(source, str(self.file_path), "exec")  # genera bytecode in memoria
            logger.debug(f"Syntax check OK for '{self.file_path.name}'")
            return True
        except SyntaxError as e:
            logger.error(f"Syntax error in '{self.file_path}': line {e.lineno} → {e.msg}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during AST validation: {e}")
            return False

    # ----------------------------------------------------------------------

    def _check_malicious_imports(self) -> None:
        """
        TODO: implementare controllo AST su import di moduli pericolosi.
        """
        # Placeholder for SafeImportVisitor
        pass

    # ----------------------------------------------------------------------

    def import_module(self) -> bool:
        """
        Valida e importa dinamicamente un modulo Python.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"File '{self.file_path}' does not exists.")

        # Step 1: Syntactic control
        if not self._validate_ast():
            logger.error(f" Blocked import: '{self.module_name}' is not valid.")
            return False

        # Step 2: Check for forbidden imports via AST
        self._check_malicious_imports()

        # Step 3: Actual import
        try:
            invalidate_caches()
            importlib.import_module(self.module_name)
            logger.debug(f"Successfully imported '{self.module_name}'.")
            return True
        except Exception as e:
            logger.error(f"Failed to import '{self.module_name}': {e}")
            return False
