import uuid

# In-memory storage for Sprint 1
TASKS = []

PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

def create_task(title: str, due_date: str, priority: str):
    task = {
        "id": str(uuid.uuid4()),
        "title": title.strip(),
        "status": "Pending",
        "due_date": due_date.strip(),   # frontend sends "YYYY-MM-DD HH:MM"
        "priority": priority.strip()     # "Low"|"Medium"|"High"
    }
    TASKS.append(task)
    return task

def get_all_tasks(sort_by: str | None = None):
    tasks = list(TASKS)

    if sort_by == "date":
        # Works correctly if due_date format is consistent: "YYYY-MM-DD HH:MM"
        tasks.sort(key=lambda t: t["due_date"])
    elif sort_by == "priority":
        tasks.sort(key=lambda t: PRIORITY_ORDER.get(t["priority"], 99))

    return tasks