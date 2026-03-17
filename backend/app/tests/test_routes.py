import unittest
from app import create_app
from app.storage import TASKS

class ApiTests(unittest.TestCase):
    def setUp(self):
        TASKS.clear()
        self.client = create_app().test_client()

    def test_create_and_list_tasks(self):
       
        res = self.client.post("/api/tasks", json={
            "title": "Math Homework",
            "due_date": "2026-03-01 23:59",
            "priority": "High",
            "duration_minutes": 60
        })
        self.assertEqual(res.status_code, 201)

        
        res = self.client.get("/api/tasks")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Math Homework")
        self.assertEqual(data[0]["status"], "Pending")
        self.assertEqual(data[0]["due_date"], "2026-03-01 23:59")
        self.assertEqual(data[0]["priority"], "High")
        self.assertEqual(data[0]["duration_minutes"], 60)

    def test_generate_schedule_includes_scheduled_times(self):
        self.client.post("/api/tasks", json={
            "title": "Task A",
            "due_date": "2026-03-01 17:00",
            "priority": "High",
            "duration_minutes": 60
        })
        self.client.post("/api/tasks", json={
            "title": "Task B",
            "due_date": "2026-03-01 18:00",
            "priority": "Medium",
            "duration_minutes": 30
        })

        res = self.client.post("/api/schedule/generate")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["scheduled_start"], "2026-03-01 09:00")
        self.assertEqual(data[0]["scheduled_end"], "2026-03-01 10:00")
        self.assertEqual(data[0]["display_time_range"], "9:00 AM - 10:00 AM")
        self.assertEqual(data[1]["scheduled_start"], "2026-03-01 10:00")
        self.assertEqual(data[1]["scheduled_end"], "2026-03-01 10:30")
        self.assertEqual(data[1]["display_time_range"], "10:00 AM - 10:30 AM")

    def test_generate_schedule_uses_fallback_for_invalid_data(self):
        self.client.post("/api/tasks", json={
            "title": "Task Without Time",
            "due_date": "2026-03-01 17:00",
            "priority": "Low",
            "duration_minutes": 25
        })

        TASKS[0]["due_date"] = "bad-date"

        res = self.client.post("/api/schedule/generate")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        self.assertEqual(data[0]["scheduled_start"], None)
        self.assertEqual(data[0]["scheduled_end"], None)
        self.assertEqual(data[0]["display_time_range"], "Time unavailable")
        self.assertFalse(data[0]["is_scheduled"])

if __name__ == "__main__":
    unittest.main()
