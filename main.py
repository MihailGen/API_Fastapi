import asyncio
import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()
tasks = {}

class Task(BaseModel):
    duration: int


async def task_worker(task_id, duration):
    await asyncio.sleep(duration)
    tasks[task_id] = "done"
    print(task_id)


@app.post("/task", response_model=dict)
async def create_task(task: Task):
    # Генерируем уникальный идентификатор для задачи
    task_id = str(uuid.uuid4())
    # Устанавливаем статус задачи как "running"
    tasks[task_id] = "running"
    # Создаем асинхронную задачу для выполнения
    asyncio.create_task(task_worker(task_id, task.duration))
    # Возвращаем уникальный идентификатор задачи
    return JSONResponse(content={"task_id": task_id})


@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    return JSONResponse(content={"status": tasks[task_id]})