import argparse

from models import Task
from service import (
    add_task,
    complete_task,
    get_incomplete_tasks,
)
from storage import load_tasks, save_tasks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="命令行任务管理器"
    )

    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser(
        "add",
        help="新增任务",
    )
    add_parser.add_argument(
        "title",
        help="任务标题",
    )
    add_parser.add_argument(
        "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="任务优先级",
    )

    subparsers.add_parser(
        "list",
        help="查看全部任务",
    )

    done_parser = subparsers.add_parser(
        "done",
        help="完成任务",
    )
    done_parser.add_argument(
        "task_id",
        type=int,
        help="任务 ID",
    )

    return parser


def print_tasks(tasks: list[Task]) -> None:
    if not tasks:
        print("没有任务。")
        return

    for task in tasks:
        status = "已完成" if task.done else "未完成"
        print(
            f"{task.id}. {task.title} "
            f"[{status}] 优先级：{task.priority}"
        )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    tasks = load_tasks()

    if args.command == "add":
        task = add_task(
            tasks,
            args.title,
            args.priority,
        )

        if task is None:
            print("任务标题不能为空。")
        else:
            save_tasks(tasks)
            print(f"任务添加成功：{task.title}")

    elif args.command == "list":
        print_tasks(tasks)

    elif args.command == "done":
        task = complete_task(
            tasks,
            args.task_id,
        )

        if task is None:
            print("任务不存在，或已经完成。")
        else:
            save_tasks(tasks)
            print(f"任务完成成功：{task.title}")


if __name__ == "__main__":
    main()