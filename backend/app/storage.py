import uuid
from datetime import datetime

# Simple in-memory storage for Sprint 0/1
TASKS = []

def create_task(title: str, due_date: str, priority: str):
    task = {
        "id": str(uuid.uuid4()),
        "title": title.strip(),
        "status": "Pending",
        "due_date": due_date,     # keep as string for now (e.g., "2026-03-01 23:59")
        "priority": priority      # "Low" | "Medium" | "High"
    }
    TASKS.append(task)
    return task

def list_tasks(sort_by: str | None = None):
    tasks = list(TASKS)

    if sort_by == "date":
        # naive sort by string; fine for Sprint 1 if you keep a consistent format
        tasks.sort(key=lambda t: t["due_date"])
    elif sort_by == "priority":
        order = {"High": 0, "Medium": 1, "Low": 2}
        tasks.sort(key=lambda t: order.get(t["priority"], 99))

    return tasks