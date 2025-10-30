from dataclasses import dataclass


@dataclass(frozen=True)
class ALGORITHMS :
    DEFAULT_ALGORITHM : str =  "DEFAULT"
    STABLE_TOPOSORT_ALGORITHM : str = "STABLE_TOPOSORT"