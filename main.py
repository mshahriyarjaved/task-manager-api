from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ---------------- DATABASE SETUP ----------------
DATABASE_URL = "sqlite:///./task_manager.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ---------------- DATABASE MODEL ----------------
class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="pending")
    priority = Column(String, default="medium")  # NEW FEATURE

Base.metadata.create_all(bind=engine)

# ---------------- SCHEMAS ----------------
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    priority: Optional[str] = "medium"

class TaskResponse(Task):
    id: int

    class Config:
        orm_mode = True

# ---------------- FASTAPI APP ----------------
app = FastAPI(title="Task Manager Pro API")

# ---------------- CREATE TASK ----------------
@app.post("/tasks", response_model=TaskResponse)
def create_task(task: Task):
    db = SessionLocal()

    new_task = TaskDB(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.close()

    return new_task

# ---------------- GET ALL TASKS ----------------
@app.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks():
    db = SessionLocal()
    tasks = db.query(TaskDB).all()
    db.close()
    return tasks

# ---------------- GET TASK BY ID ----------------
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    db = SessionLocal()
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    db.close()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

# ---------------- UPDATE TASK ----------------
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: Task):
    db = SessionLocal()
    existing_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not existing_task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    existing_task.title = task.title
    existing_task.description = task.description
    existing_task.status = task.status
    existing_task.priority = task.priority

    db.commit()
    db.refresh(existing_task)
    db.close()

    return existing_task

# ---------------- DELETE TASK ----------------
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    db.close()

    return {"message": "Task deleted successfully"}