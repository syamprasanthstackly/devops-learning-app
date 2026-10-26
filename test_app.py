import json
import threading
import unittest
from http.server import HTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

import app


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), app.AppHandler)
        cls.port = cls.server.server_address[1]

        cls.thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True,
        )
        cls.thread.start()

        cls.base_url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_health_endpoint(self):
        with urlopen(f"{self.base_url}/health") as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))

        self.assertEqual(data["status"], "healthy")

    def test_info_endpoint(self):
        with urlopen(f"{self.base_url}/info") as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))

        self.assertEqual(data["application"], app.APP_NAME)
        self.assertIn("environment", data)
        self.assertEqual(data["version"], "1.0.0")

    def test_homepage(self):
        with urlopen(self.base_url) as response:
            self.assertEqual(response.status, 200)
            content = response.read().decode("utf-8")

        self.assertIn(app.APP_NAME, content)
        self.assertIn("Application is running!", content)

    def test_unknown_endpoint_returns_404(self):
        with self.assertRaises(HTTPError) as error:
            urlopen(f"{self.base_url}/unknown")

        self.assertEqual(error.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
