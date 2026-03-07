import unittest
from app import create_app

class ApiTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_and_list_tasks(self):

        # Create task
        res = self.client.post("/api/tasks", json={
            "title": "Math Homework",
            "due_date": "2026-03-01 23:59",
            "priority": "High"
        })

        self.assertEqual(res.status_code, 201)

        # List tasks
        res = self.client.get("/api/tasks")
        self.assertEqual(res.status_code, 200)

        data = res.get_json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Math Homework")
        self.assertEqual(data[0]["status"], "Pending")
        self.assertEqual(data[0]["due_date"], "2026-03-01 23:59")
        self.assertEqual(data[0]["priority"], "High")


    def test_edit_task(self):

        # Create task first
        res = self.client.post("/api/tasks", json={
            "title": "Finish Sprint Report",
            "due_date": "2026-03-10 17:00",
            "priority": "High"
        })

        task = res.get_json()
        task_id = task["id"]

        # Edit task
        res = self.client.put(f"/api/tasks/{task_id}", json={
            "title": "Finish Sprint Report (Updated)",
            "due_date": "2026-03-12 12:00",
            "priority": "Medium",
            "status": "Not Started"
        })

        self.assertEqual(res.status_code, 200)

        # Verify change
        res = self.client.get("/api/tasks")
        data = res.get_json()

        self.assertEqual(data[0]["title"], "Finish Sprint Report (Updated)")
        self.assertEqual(data[0]["priority"], "Medium")
        self.assertEqual(data[0]["status"], "Not Started")


    def test_delete_task(self):

        # Create task
        res = self.client.post("/api/tasks", json={
            "title": "Task To Delete",
            "due_date": "2026-04-01 12:00",
            "priority": "Low"
        })

        task = res.get_json()
        task_id = task["id"]

        # Delete task
        res = self.client.delete(f"/api/tasks/{task_id}")
        self.assertEqual(res.status_code, 200)

        # Verify removal
        res = self.client.get("/api/tasks")
        data = res.get_json()

        self.assertEqual(len(data), 0)


if __name__ == "__main__":
    unittest.main()