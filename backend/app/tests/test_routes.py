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
            "priority": "High"
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

if __name__ == "__main__":
    unittest.main()