import uuid
from datetime import datetime, timedelta

# In-memory storage for Sprint 1
TASKS = []

PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}
SCHEDULE_START_HOUR = 9

def create_task(title: str, due_date: str, priority: str, duration_minutes: int):
    task = {
        "id": str(uuid.uuid4()),
        "title": title.strip(),
        "status": "Pending",
        "due_date": due_date.strip(),   # frontend sends "YYYY-MM-DD HH:MM"
        "priority": priority.strip(),   # "Low"|"Medium"|"High"
        "duration_minutes": duration_minutes
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

def _parse_due_date(value: str) -> datetime | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M")
    except (TypeError, ValueError):
        return None

def _format_schedule_time(value: datetime | None) -> str | None:
    if value is None:
        return None

    return value.strftime("%I:%M %p").lstrip("0")

def generate_schedule():
    valid_groups = {}
    invalid_tasks = []

    for task in TASKS:
        due_dt = _parse_due_date(task.get("due_date"))
        duration_minutes = task.get("duration_minutes")

        if due_dt is None or not isinstance(duration_minutes, int) or duration_minutes <= 0:
            invalid_tasks.append(task)
            continue

        valid_groups.setdefault(due_dt.date(), []).append((task, due_dt))

    scheduled_tasks = []
    for day in sorted(valid_groups):
        current_start = datetime.combine(day, datetime.min.time()).replace(hour=SCHEDULE_START_HOUR)
        day_tasks = sorted(
            valid_groups[day],
            key=lambda item: (
                PRIORITY_ORDER.get(item[0]["priority"], 99),
                item[1],
                item[0]["title"].lower()
            )
        )

        for task, due_dt in day_tasks:
            scheduled_start = current_start
            scheduled_end = scheduled_start + timedelta(minutes=task["duration_minutes"])
            scheduled_tasks.append({
                **task,
                "scheduled_start": scheduled_start.strftime("%Y-%m-%d %H:%M"),
                "scheduled_end": scheduled_end.strftime("%Y-%m-%d %H:%M"),
                "display_time_range": (
                    f"{_format_schedule_time(scheduled_start)} - "
                    f"{_format_schedule_time(scheduled_end)}"
                ),
                "scheduled_date": due_dt.strftime("%Y-%m-%d"),
                "is_scheduled": True
            })
            current_start = scheduled_end

    for task in invalid_tasks:
        scheduled_tasks.append({
            **task,
            "scheduled_start": None,
            "scheduled_end": None,
            "display_time_range": "Time unavailable",
            "scheduled_date": None,
            "is_scheduled": False
        })

    scheduled_tasks.sort(
        key=lambda task: (
            task["scheduled_date"] is None,
            task["scheduled_date"] or "",
            task["scheduled_start"] or "",
            PRIORITY_ORDER.get(task["priority"], 99),
            task["title"].lower()
        )
    )

    return scheduled_tasks
