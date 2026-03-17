import unittest
from app import create_app


class TestMomentumScheduler(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def test_create_task_api(self):
        response = self.app.post("/api/tasks", json={
            "title": "Finish Report",
            "due_date": "2026-03-20 12:00",
            "priority": "High",
            "duration_minutes": 60,
            "effort_level": "Medium",
            "start_after": None,
            "category": "School"
        })

        self.assertEqual(response.status_code, 200)

    def test_create_task_missing_title(self):
        response = self.app.post("/api/tasks", json={
            "title": "",
            "due_date": "2026-03-20 12:00",
            "priority": "High",
            "duration_minutes": 60,
            "effort_level": "Medium",
            "start_after": None,
            "category": "School"
        })

        self.assertNotEqual(response.status_code, 200)

    def test_generate_schedule_api(self):
        response = self.app.post("/api/schedule", json={
            "days": 7,
            "max_tasks_per_day": 3
        })

        self.assertEqual(response.status_code, 200)

    def test_schedule_daily_limit(self):
        response = self.app.post("/api/schedule", json={
            "days": 7,
            "max_tasks_per_day": 2
        })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("schedule", data)

    def test_effort_level_scheduling_order(self):
    same_due_date = "2026-03-20 12:00"

    # Create low-effort task
    low_response = self.app.post("/api/tasks", json={
        "title": "Low Effort Task",
        "due_date": same_due_date,
        "priority": "Medium",
        "duration_minutes": 60,
        "effort_level": "Low",
        "start_after": None,
        "category": "General"
    })
    self.assertEqual(low_response.status_code, 200)

    # Create high-effort task
    high_response = self.app.post("/api/tasks", json={
        "title": "High Effort Task",
        "due_date": same_due_date,
        "priority": "Medium",
        "duration_minutes": 60,
        "effort_level": "High",
        "start_after": None,
        "category": "General"
    })
    self.assertEqual(high_response.status_code, 200)

    # Generate schedule
    schedule_response = self.app.post("/api/schedule", json={
        "days": 7,
        "max_tasks_per_day": 4
    })
    self.assertEqual(schedule_response.status_code, 200)

    data = schedule_response.get_json()
    self.assertIn("schedule", data)

    schedule = data["schedule"]

    # Flatten all scheduled tasks into one list in displayed order
    scheduled_tasks = []
    for day_key in sorted(schedule.keys()):
        scheduled_tasks.extend(schedule[day_key])

    titles = [task["title"] for task in scheduled_tasks]

    self.assertIn("High Effort Task", titles)
    self.assertIn("Low Effort Task", titles)

    # High effort task should appear earlier than low effort task
    self.assertLess(
        titles.index("High Effort Task"),
        titles.index("Low Effort Task")
    )

    def test_delete_task_api(self):
        create_response = self.app.post("/api/tasks", json={
            "title": "Delete Me",
            "due_date": "2026-03-22 10:00",
            "priority": "Low",
            "duration_minutes": 30,
            "effort_level": "Low",
            "start_after": None,
            "category": "General"
        })

        created_task = create_response.get_json()
        task_id = created_task["id"]

        delete_response = self.app.delete(f"/api/tasks/{task_id}")
        self.assertEqual(delete_response.status_code, 200)

    def test_update_task_api(self):
        create_response = self.app.post("/api/tasks", json={
            "title": "Old Task",
            "due_date": "2026-03-22 10:00",
            "priority": "Low",
            "duration_minutes": 30,
            "effort_level": "Low",
            "start_after": None,
            "category": "General"
        })

        created_task = create_response.get_json()
        task_id = created_task["id"]

        update_response = self.app.put(f"/api/tasks/{task_id}", json={
            "title": "Updated Task",
            "due_date": "2026-03-22 12:00",
            "priority": "High",
            "status": "Pending",
            "duration_minutes": 60,
            "effort_level": "High",
            "start_after": None,
            "category": "Work"
        })

        self.assertEqual(update_response.status_code, 200)
    def test_duration_scheduling_sequential_no_overlap(self):
    same_due_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")

    # Create a 30-minute task
    short_response = self.app.post("/api/tasks", json={
        "title": "Short Task",
        "due_date": same_due_date,
        "priority": "Medium",
        "duration_minutes": 30,
        "effort_level": "Medium",
        "start_after": None,
        "category": "General"
    })
    self.assertEqual(short_response.status_code, 200)

    # Create a 90-minute task
    long_response = self.app.post("/api/tasks", json={
        "title": "Long Task",
        "due_date": same_due_date,
        "priority": "Medium",
        "duration_minutes": 90,
        "effort_level": "Medium",
        "start_after": None,
        "category": "General"
    })
    self.assertEqual(long_response.status_code, 200)

    # Generate schedule
    schedule_response = self.app.post("/api/schedule", json={
        "days": 7,
        "max_tasks_per_day": 4
    })
    self.assertEqual(schedule_response.status_code, 200)

    data = schedule_response.get_json()
    self.assertIn("schedule", data)

    schedule = data["schedule"]

    # Flatten scheduled tasks in day order
    scheduled_tasks = []
    for day_key in sorted(schedule.keys()):
        scheduled_tasks.extend(schedule[day_key])

    # Find the tasks we created
    short_task = next(task for task in scheduled_tasks if task["title"] == "Short Task")
    long_task = next(task for task in scheduled_tasks if task["title"] == "Long Task")

    # Helper to convert "9:00 AM" -> datetime object for comparison
    def parse_time(time_str):
        return datetime.strptime(time_str, "%I:%M %p")

    short_start = parse_time(short_task["scheduled_start"])
    short_end = parse_time(short_task["scheduled_end"])
    long_start = parse_time(long_task["scheduled_start"])
    long_end = parse_time(long_task["scheduled_end"])

    # 30-minute task should last 30 minutes
    self.assertEqual(int((short_end - short_start).total_seconds() / 60), 30)

    # 90-minute task should last 90 minutes
    self.assertEqual(int((long_end - long_start).total_seconds() / 60), 90)

    # Tasks should be sequential and not overlap
    first_start = min(short_start, long_start)
    first_end = short_end if short_start < long_start else long_end
    second_start = long_start if short_start < long_start else short_start

    self.assertEqual(first_end, second_start)


if __name__ == "__main__":
    unittest.main()