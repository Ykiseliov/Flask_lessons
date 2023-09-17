from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

app = FastAPI()

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# Создание таблицы задач, если она не существует
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        status BOOLEAN
    )
""")
conn.commit()

# Модель для задач
class Task(BaseModel):
    title: str
    description: str
    status: bool

# Обработчик для корневой директории
@app.get("/")
async def read_root():
    return "Welcome to the Tasks API"

# Точка для получения списка задач
@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return [{"id": task[0], "title": task[1], "description": task[2], "status": task[3]} for task in tasks]

# Точка для получения задачи по ID
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    task = cursor.fetchone()
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return Task(id=task[0], title=task[1], description=task[2], status=bool(task[3]))

# Точка для добавления новой задачи
@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    cursor.execute("INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)", (task.title, task.description, task.status))
    conn.commit()
    task_id = cursor.lastrowid
    return Task(id=task_id, title=task.title, description=task.description, status=task.status)

# Точка для обновления задачи по ID
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    cursor.execute("UPDATE tasks SET title=?, description=?, status=? WHERE id=?", (updated_task.title, updated_task.description, updated_task.status, task_id))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return updated_task

# Точка для удаления задачи по ID
@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"id": task_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)