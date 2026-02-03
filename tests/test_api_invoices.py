# Feature: invoice integration tests — create patients/doctors and invoices. Connects: app.py and invoice API.
import unittest
import os
import time
import subprocess
import urllib.request
import json


class TestApiInvoices(unittest.TestCase):

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

    def _post_json(self, path, payload):
        url = f"http://127.0.0.1:{self.port}{path}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))

    def test_api_invoices_returns_200(self):
        url = f"http://127.0.0.1:{self.port}/api/invoices"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            body = resp.read().decode("utf-8")
            self.assertTrue(len(body) >= 0)

    def test_create_invoice_flow(self):
        # Create patient
        status, patient = self._post_json("/api/patients", {"first_name": "Test", "last_name": "Patient"})
        self.assertEqual(status, 201)

        # Create doctor
        status, doctor = self._post_json("/api/doctors", {"name": "Dr. Who"})
        self.assertEqual(status, 201)

        # Create invoice
        invoice_payload = {
            "patient_id": patient["id"],
            "doctor_id": doctor["id"],
            "amount": 123.45,
            "issued_on": "2025-01-01",
            "description": "Test invoice",
        }

        status, invoice = self._post_json("/api/invoices", invoice_payload)
        self.assertEqual(status, 201)
        self.assertIn("id", invoice)
        self.assertEqual(invoice["patient_id"], patient["id"])
        self.assertEqual(invoice["doctor_id"], doctor["id"])
        self.assertAlmostEqual(invoice["amount"], 123.45)

        # Check invoices list contains the invoice
        url = f"http://127.0.0.1:{self.port}/api/invoices"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            items = json.loads(resp.read().decode("utf-8"))
            ids = [i["id"] for i in items]
            self.assertIn(invoice["id"], ids)
