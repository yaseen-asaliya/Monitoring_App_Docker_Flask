import unittest
import json
import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_disk_usage(self):
        response = self.app.get("/disk")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("current", data)
        self.assertIn("usage_for_last_24h", data)

    def test_memory_usage(self):
        response = self.app.get("/memory")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("current", data)
        self.assertIn("usage_for_last_24h", data)

    def test_cpu_usage(self):
        response = self.app.get("/cpu")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("current", data)
        self.assertIn("usage_for_last_24h", data)
        
    def test_fail_api(self):
        response = self.app.get("/test")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()

