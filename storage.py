from models import Task
from dataclasses import asdict
import json
DATA_FILE="tasks.json"
import os

def save_tasks(tasks:list[Task])->None:
    """保存任务列表到文件。"""
    data = [asdict(task) for task in tasks]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



def load_tasks()->list[Task]:
    """从文件加载任务列表。"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data=json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("任务文件损坏，无法加载任务列表。")
        return []
    return [Task(**item) for item in data]