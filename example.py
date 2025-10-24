
TASKS = {}


def main():
    for name, t in TASKS.items():
        deps = t["depends_on"]
        if all(dep not in TASKS or TASKS[dep].get("done") for dep in deps):
            t["done"] = False
            t["func"]()
            t["done"] = True


if __name__ == '__main__':
    main()
