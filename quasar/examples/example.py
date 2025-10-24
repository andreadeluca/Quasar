from quasar.core.task_decorator import task


@task()
def first():
    print("Hi, I'm the first task!")


@task(depends_on=["first"])
def second():
    print("I'm the second task, after the first!")


@task(depends_on=["second"])
def third():
    print("And I'm the third task, after the second!")
