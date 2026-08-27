from models import Task
from service import (
    add_task,
    complete_task,
    delete_task,
    get_incomplete_tasks,
)
from storage import load_tasks, save_tasks


def print_tasks(tasks: list[Task]) -> None:
    """显示任务列表。"""
    if not tasks:
        print("没有任务。")
        return

    for task in tasks:
        status = "已完成" if task.done else "未完成"
        print(f"{task.id}. {task.title} [{status}]")


def read_task_id(message: str) -> int | None:
    """读取用户输入的任务 ID。"""
    try:
        task_id = int(input(message).strip())
    except ValueError:
        print("任务 ID 必须是数字。")
        return None

    if task_id <= 0:
        print("任务 ID 必须是正整数。")
        return None

    return task_id


def main() -> None:
    """程序入口。"""
    tasks = load_tasks()

    while True:
        print("\n===== 任务管理器 =====")
        print("1. 新增任务")
        print("2. 查看全部任务")
        print("3. 查看未完成任务")
        print("4. 完成任务")
        print("5. 删除任务")
        print("6. 退出")

        choice = input("请选择操作：").strip()

        if choice == "1":
            title = input("请输入任务标题：")
            task = add_task(tasks, title)

            if task is None:
                print("任务标题不能为空。")
            else:
                save_tasks(tasks)
                print(f"任务添加成功：{task.title}")

        elif choice == "2":
            print_tasks(tasks)

        elif choice == "3":
            incomplete_tasks = get_incomplete_tasks(tasks)

            if not incomplete_tasks:
                print("没有未完成的任务。")
            else:
                print_tasks(incomplete_tasks)

        elif choice == "4":
            task_id = read_task_id("请输入要完成的任务 ID：")

            if task_id is not None:
                task = complete_task(tasks, task_id)

                if task is None:
                    print("任务不存在，或任务已经完成。")
                else:
                    save_tasks(tasks)
                    print(f"任务完成成功：{task.title}")

        elif choice == "5":
            task_id = read_task_id("请输入要删除的任务 ID：")

            if task_id is not None:
                task = delete_task(tasks, task_id)

                if task is None:
                    print("任务不存在。")
                else:
                    save_tasks(tasks)
                    print(f"任务删除成功：{task.title}")

        elif choice == "6":
            print("退出程序。")
            break

        else:
            print("无效的选择，请重新输入。")


if __name__ == "__main__":
    main()