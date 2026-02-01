# tests/test_api_smoke.py

"""
BASIC TESTING IDEA (Python unittest):

- A test is just a normal Python function that checks expectations.
- If an assertion fails, the test fails.
- If all assertions pass, the test passes.
- unittest automatically runs methods whose names start with `test_`.
"""

import unittest
import os
import time
import subprocess
import urllib.request


class TestApiSmoke(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.port = "8000"

        env = os.environ.copy()
        env["PORT"] = cls.port

        cls.proc = subprocess.Popen(
            ["python", "app.py"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        try:
            cls.proc.wait(timeout=3)
        except Exception:
            cls.proc.kill()

    def test_api_patients_returns_200(self):
        """
        This test checks one thing:
        - When we call /api/patients, the server responds correctly
        """

        # Build the API URL using the test server port
        url = f"http://127.0.0.1:{self.port}/api/patients"

        # Make an HTTP GET request to the API
        with urllib.request.urlopen(url) as resp:

            # Assert that HTTP status code is 200 (success)
            # Asset means “Check and complain if it’s not true”
            self.assertEqual(resp.status, 200)

            # Read the response body returned by the API
            body = resp.read().decode("utf-8")

            # Assert that the response body is not empty
            # (means API returned some data)
            self.assertTrue(len(body) > 0)