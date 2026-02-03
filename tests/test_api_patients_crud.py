# Feature: integration tests for patient CRUD flows — creates/updates/deletes patients via HTTP. Connects: app.py and patient API endpoints.
import unittest
import os
import time
import subprocess
import urllib.request
import json

class TestApiPatientsCrud(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.port = "8001"

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

    def test_create_update_delete_patient(self):
        base = f"http://127.0.0.1:{self.port}"

        # Create
        data = {
            "first_name": "Test",
            "last_name": "Patient",
            "phone": "123",
            "email": "t@example.com",
        }
        req = urllib.request.Request(f"{base}/api/patients", method="POST", data=json.dumps(data).encode('utf-8'), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 201)
            created = json.loads(resp.read().decode('utf-8'))
            self.assertIn('id', created)
            pid = created['id']

        # Update
        update = { "first_name": "Updated" }
        req = urllib.request.Request(f"{base}/api/patients/{pid}", method="PUT", data=json.dumps(update).encode('utf-8'), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            updated = json.loads(resp.read().decode('utf-8'))
            self.assertEqual(updated['first_name'], 'Updated')

        # Delete
        req = urllib.request.Request(f"{base}/api/patients/{pid}", method="DELETE")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)

        # Ensure 404 on get
        try:
            with urllib.request.urlopen(f"{base}/api/patients/{pid}") as resp:
                self.fail('Expected 404')
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)
