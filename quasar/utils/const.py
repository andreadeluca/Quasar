from dataclasses import dataclass


@dataclass(frozen=True)
class ALGORITHMS :
    DEFAULT_ALGORITHM : str =  "DEFAULT"
    STABLE_TOPOSORT_ALGORITHM : str = "STABLE_TOPOSORT"


'''
This is a list of forbidden import that may ruin your experience.
MODIFY AT YOUR OWN RISK.
'''

FORBIDDEN_IMPORTS = {
    "os",
    "subprocess",
    "sys",
    "shutil",
    "socket",
    "ctypes",
    "multiprocessing",
    "importlib",
    "runpy",
    "pathlib",
    "builtins",
    "eval",
    "exec",
}
