import unittest
import os
import time
import subprocess
import urllib.request


class TestApiClinic(unittest.TestCase):

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
        url = f"http://127.0.0.1:{self.port}/api/patients"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            body = resp.read().decode("utf-8")
            self.assertTrue(len(body) > 0)

    def test_api_doctors_returns_200(self):
        url = f"http://127.0.0.1:{self.port}/api/doctors"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            body = resp.read().decode("utf-8")
            self.assertTrue(len(body) > 0)

    def test_api_billing_returns_200(self):
        url = f"http://127.0.0.1:{self.port}/api/billing"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            body = resp.read().decode("utf-8")
            self.assertTrue(len(body) > 0)

    def test_clinic_db_created(self):
        self.assertTrue(os.path.exists("clinic.db"))
