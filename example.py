from typing import Callable

TASKS = {}


def task(depends_on=None):
    depends_on = depends_on or []

    def decorator(func: Callable):
        TASKS[func.__name__] = {"func": func, "depends_on": depends_on}
        return func

    return decorator


@task()
def first():
    print("Hi! I'm the first task!")


@task(depends_on=["first"])
def second():
    print("Well, I'm the second task!")


def main():
    for name, t in TASKS.items():
        deps = t["depends_on"]
        if all(dep not in TASKS or TASKS[dep].get("done") for dep in deps):
            t["done"] = False
            t["func"]()
            t["done"] = True


if __name__ == '__main__':
    main()
