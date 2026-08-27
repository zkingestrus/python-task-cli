from models import Task
from service import add_task


def test_add_task():
    tasks = []

    task = add_task(tasks, "学习 Python", "high")

    assert task is not None
    assert task.title == "学习 Python"
    assert task.priority == "high"
    assert task.done is False
    assert len(tasks) == 1

from service import (
    add_task,
    complete_task,
    delete_task,
    find_task_by_id,
    generate_task_id,
    get_incomplete_tasks,
)


def test_generate_task_id():
    tasks = [
        Task(1, "任务一"),
        Task(3, "任务三"),
    ]

    assert generate_task_id(tasks) == 4


def test_add_empty_task():
    tasks = []

    task = add_task(tasks, "")

    assert task is None
    assert tasks == []


def test_find_task_by_id():
    tasks = [Task(1, "学习 Python")]

    assert find_task_by_id(tasks, 1) == tasks[0]
    assert find_task_by_id(tasks, 99) is None


def test_complete_task():
    tasks = [Task(1, "学习 Python")]

    task = complete_task(tasks, 1)

    assert task is not None
    assert task.done is True


def test_complete_missing_task():
    tasks = [Task(1, "学习 Python")]

    assert complete_task(tasks, 99) is None


def test_get_incomplete_tasks():
    tasks = [
        Task(1, "已完成", done=True),
        Task(2, "未完成", done=False),
    ]

    result = get_incomplete_tasks(tasks)

    assert result == [tasks[1]]


def test_delete_task():
    tasks = [
        Task(1, "任务一"),
        Task(2, "任务二"),
    ]

    deleted = delete_task(tasks, 1)

    assert deleted == tasks[0] or deleted is not None
    assert len(tasks) == 1
    assert tasks[0].id == 2