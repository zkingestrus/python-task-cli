from models import Task


def generate_task_id(tasks: list[Task]) -> int:
    """生成新的任务 ID。"""
    return max((task.id for task in tasks), default=0) + 1


def find_task_by_id(
    tasks: list[Task],
    task_id: int,
) -> Task | None:
    """根据 ID 查找任务。"""
    for task in tasks:
        if task.id == task_id:
            return task

    return None


def add_task(
    tasks: list[Task],
    title: str,
    priority: str = "medium",
) -> Task | None:
    """新增任务，不负责输入和保存文件。"""
    title = title.strip()

    if title == "":
        return None

    task = Task(
        id=generate_task_id(tasks),
        title=title,
        priority=priority,
    )

    tasks.append(task)
    return task


def complete_task(
    tasks: list[Task],
    task_id: int,
) -> Task | None:
    """完成任务，不负责输入和保存文件。"""
    task = find_task_by_id(tasks, task_id)

    if task is None or task.done:
        return None

    task.done = True
    return task


def delete_task(
    tasks: list[Task],
    task_id: int,
) -> Task | None:
    """删除任务，不负责输入和保存文件。"""
    task = find_task_by_id(tasks, task_id)

    if task is None:
        return None

    tasks.remove(task)
    return task


def get_incomplete_tasks(tasks: list[Task]) -> list[Task]:
    """返回所有未完成任务。"""
    return [task for task in tasks if not task.done]