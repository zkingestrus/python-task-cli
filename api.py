from fastapi import FastAPI, HTTPException
from storage import load_tasks, save_tasks
from service import add_task
from dataclasses import asdict
from pydantic import BaseModel
from typing import Literal


app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    priority: Literal["low", "medium", "high"] = "medium"

@app.get("/health")
def health_check():
    return {"status": "running"}



@app.get("/tasks")
def list_tasks():
    tasks = load_tasks()
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