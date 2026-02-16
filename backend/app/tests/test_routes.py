import unittest
from app import create_app

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_health(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)

    def test_create_task_validation(self):
        res = self.client.post("/api/tasks", json={"title": "", "due_date": "", "priority": "High"})
        self.assertEqual(res.status_code, 400)

if __name__ == "__main__":
    unittest.main()