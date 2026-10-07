from fastapi import FastAPI, HTTPException
from storage import load_tasks, save_tasks
from service import add_task, find_task_by_id, update_task, delete_task
from dataclasses import asdict
from pydantic import BaseModel
from typing import Literal



app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    priority: Literal["low", "medium", "high"] = "medium"

class TaskUpdate(BaseModel):
    title: str | None = None
    priority: Literal["low", "medium", "high"] | None = None
    done: bool | None = None


@app.get("/health")
def health_check():
    return {"status": "running"}



@app.get("/tasks")
def list_tasks(done: bool | None = None):
    tasks = load_tasks()

    if done is not None:
        tasks = [task for task in tasks if task.done == done]

    return [asdict(task) for task in tasks]

@app.post("/tasks", status_code=201)
def create_task(data: TaskCreate):
    tasks = load_tasks()

    task = add_task(
        tasks,
        title=data.title,
        priority=data.priority,
    )

    if task is None:
        raise HTTPException(
            status_code=400,
            detail="任务标题不能为空",
        )

    save_tasks(tasks)
    return asdict(task)


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="任务不存在",
        )

    return asdict(task)

@app.patch("/tasks/{task_id}")
def patch_task(task_id: int, data: TaskUpdate):
    changes = data.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="请至少提供一个要修改的字段",
        )

    if any(value is None for value in changes.values()):
        raise HTTPException(
            status_code=400,
            detail="修改字段不能为 null",
        )

    tasks = load_tasks()

    try:
        task = update_task(tasks, task_id, **changes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="任务不存在",
        )

    save_tasks(tasks)
    return asdict(task)

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    tasks = load_tasks()
    task = delete_task(tasks, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="任务不存在",
        )

    save_tasks(tasks)

    return {
        "message": "任务已删除",
        "task": asdict(task),
    }