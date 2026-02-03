# Feature: URL router — maps HTTP paths to services/controllers and serves SPA/static assets. Connects: core, services, frontend.
# router.py

from datetime import datetime
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

# reports and controllers are imported lazily inside handlers to avoid import-time errors


# Clinic controllers are handled via services (lazy import inside handlers)

from core.static import serve_static
from core.responses import send_404, send_json
from core.middleware import add_cors_headers


# -------------------------------
# UI ROUTER (SPA shell + static)
# -------------------------------

FRONTEND_ROUTES = {
    "/", "/home",
    "/reports/enrollments",
    "/docs/flow", "/docs",
    "/profiles",
    # Clinic pages
    "/patients", "/doctors", "/billing",
}

def handle_ui_routes(handler, path):
    # Exact SPA routes
    if path in FRONTEND_ROUTES:
        serve_static(handler, "frontend/pages/index.html")
        return True

    # Allow /something.html to map to SPA routes too
    if path.endswith(".html"):
        stripped = path.replace(".html", "")
        if stripped in FRONTEND_ROUTES:
            serve_static(handler, "frontend/pages/index.html")
            return True

    # Serve assets at /assets/... -> frontend/assets/...
    if path.startswith("/assets/"):
        serve_static(handler, "frontend" + path)
        return True

    # Serve anything under /frontend/ directly
    if path.startswith("/frontend/"):
        serve_static(handler, path.lstrip("/"))
        return True

    if path == "/openapi.yaml":
        serve_static(handler, "openapi.yaml")
        return True

    # Dynamic SPA routes (profiles pages)
    # e.g. /profiles/1 should still load index.html and let the SPA router decide
    if path.startswith("/profiles/"):
        serve_static(handler, "frontend/pages/index.html")
        return True

    return False


# -------------------------------
# Helpers
# -------------------------------

def _last_path_id_or_404(handler, path):
    """
    Extract the last path segment and ensure it's a number.
    If it's not a number, return None after sending 404 (no crash).
    """
    last = path.split("/")[-1]
    if not last.isdigit():
        send_404(handler)
        return None
    return int(last)


# -------------------------------
# MAIN ROUTER CLASS
# -------------------------------

class PatientRouter(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        add_cors_headers(self)
        self.end_headers()

    # ---------------------------
    # READ (GET)
    # ---------------------------
    def do_GET(self):
        path = urlparse(self.path).path

        # 1) UI routes first (SPA + static)
        if handle_ui_routes(self, path):
            return


        # ---------------------------
        # REPORTS (JOIN)
        # ---------------------------
        if path == "/api/reports/enrollments":
            from services.report_service import service_get_enrollment_report
            return send_json(self, 200, service_get_enrollment_report())

        # Clinic reports
        if path == "/api/reports/billing":
            # Return all invoices as a basic billing report
            from services.invoice_service import service_get_all as service_get_all_invoices
            return send_json(self, 200, service_get_all_invoices())

        # ---------------------------
        # PATIENTS
        # ---------------------------
        if path == "/api/patients":
            from services.patient_service import service_get_all
            return send_json(self, 200, service_get_all())

        if path.startswith("/api/patients/"):
            patient_id = _last_path_id_or_404(self, path)
            if patient_id is None:
                return
            from services.patient_service import service_get_one
            patient = service_get_one(patient_id)
            if not patient:
                return send_404(self)
            return send_json(self, 200, patient)

        # ---------------------------
        # DOCTORS
        # ---------------------------
        if path == "/api/doctors":
            from services.doctor_service import service_get_all
            return send_json(self, 200, service_get_all())

        if path.startswith("/api/doctors/"):
            doctor_id = _last_path_id_or_404(self, path)
            if doctor_id is None:
                return
            from services.doctor_service import service_get_one
            doctor = service_get_one(doctor_id)
            if not doctor:
                return send_404(self)
            return send_json(self, 200, doctor)

        # ---------------------------
        # BILLING
        # ---------------------------
        if path == "/api/billing":
            from services.billing_service import service_get_all
            return send_json(self, 200, service_get_all())

        if path.startswith("/api/billing/"):
            billing_id = _last_path_id_or_404(self, path)
            if billing_id is None:
                return
            from services.billing_service import service_get_one
            billing = service_get_one(billing_id)
            if not billing:
                return send_404(self)
            return send_json(self, 200, billing)

        # ---------------------------
        # INVOICES
        # ---------------------------
        if path == "/api/invoices":
            from services.invoice_service import service_get_all
            return send_json(self, 200, service_get_all())

        if path.startswith("/api/invoices/"):
            invoice_id = _last_path_id_or_404(self, path)
            if invoice_id is None:
                return
            from services.invoice_service import service_get_one
            invoice = service_get_one(invoice_id)
            if not invoice:
                return send_404(self)
            return send_json(self, 200, invoice)

        # If the path doesn't belong to the API or static assets, serve the SPA
        # This helps deep-linking like /profiles/123 work even when the server only
        # sees the direct request (typical in some deployment setups).
        if not path.startswith("/api/") and not path.startswith("/assets/") and not path.startswith("/frontend/") and path != "/openapi.yaml":
            serve_static(self, "frontend/pages/index.html")
            return

        return send_404(self)

    # ---------------------------
    # CREATE (POST)
    # ---------------------------
    def do_POST(self):
        path = urlparse(self.path).path


        # ---------------------------
        # PATIENTS
        # ---------------------------
        if path == "/api/patients":
            from core.request import parse_json_body
            from services.patient_service import service_create
            data = parse_json_body(self)
            created = service_create(data)
            return send_json(self, 201, created)

        # ---------------------------
        # DOCTORS
        # ---------------------------
        if path == "/api/doctors":
            from core.request import parse_json_body
            from services.doctor_service import service_create
            data = parse_json_body(self)
            created = service_create(data)
            return send_json(self, 201, created)

        # ---------------------------
        # BILLING
        # ---------------------------
        if path == "/api/billing":
            from core.request import parse_json_body
            from services.billing_service import service_create
            data = parse_json_body(self)
            created = service_create(data)
            return send_json(self, 201, created)

        # ---------------------------
        # INVOICES
        # ---------------------------
        if path == "/api/invoices":
            from core.request import parse_json_body
            from services.invoice_service import service_create
            data = parse_json_body(self)
            created = service_create(data)
            return send_json(self, 201, created)

        return send_404(self)

    # ---------------------------
    # UPDATE (PUT)
    # ---------------------------
    def do_PUT(self):
        path = urlparse(self.path).path

        # ---------------------------
        # PATIENTS
        # ---------------------------
        if path.startswith("/api/patients/"):
            patient_id = _last_path_id_or_404(self, path)
            if patient_id is None:
                return
            return update_patient(self, patient_id)

        # ---------------------------
        # DOCTORS
        # ---------------------------
        if path.startswith("/api/doctors/"):
            doctor_id = _last_path_id_or_404(self, path)
            if doctor_id is None:
                return
            return update_doctor(self, doctor_id)

        # ---------------------------
        # BILLING
        # ---------------------------
        if path.startswith("/api/billing/"):
            billing_id = _last_path_id_or_404(self, path)
            if billing_id is None:
                return
            return update_billing(self, billing_id)

        # ---------------------------
        # INVOICES
        # ---------------------------
        if path.startswith("/api/invoices/"):
            invoice_id = _last_path_id_or_404(self, path)
            if invoice_id is None:
                return
            return update_invoice(self, invoice_id)

        return send_404(self)

    # ---------------------------
    # DELETE (DELETE)
    # ---------------------------
    def do_DELETE(self):
        path = urlparse(self.path).path


        # ---------------------------
        # PATIENTS
        # ---------------------------
        if path.startswith("/api/patients/"):
            patient_id = _last_path_id_or_404(self, path)
            if patient_id is None:
                return
            return delete_patient(self, patient_id)

        # ---------------------------
        # DOCTORS
        # ---------------------------
        if path.startswith("/api/doctors/"):
            doctor_id = _last_path_id_or_404(self, path)
            if doctor_id is None:
                return
            return delete_doctor(self, doctor_id)

        # ---------------------------
        # BILLING
        # ---------------------------
        if path.startswith("/api/billing/"):
            billing_id = _last_path_id_or_404(self, path)
            if billing_id is None:
                return
            return delete_billing(self, billing_id)

        # ---------------------------
        # INVOICES
        # ---------------------------
        if path.startswith("/api/invoices/"):
            invoice_id = _last_path_id_or_404(self, path)
            if invoice_id is None:
                return
            return delete_invoice(self, invoice_id)

        return send_404(self)

    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [Server] {format % args}")


# ---------------------------
# Handlers for UPDATE / DELETE
# ---------------------------

def update_patient(handler, patient_id):
    from core.request import parse_json_body
    from services.patient_service import service_get_one, service_update

    data = parse_json_body(handler) or {}

    # Ensure we don't clobber required fields when a partial payload is sent.
    existing = service_get_one(patient_id)
    if not existing:
        return send_404(handler)

    allowed = ["first_name", "last_name", "age", "gender", "phone"]
    merged = {k: data.get(k, existing.get(k)) for k in allowed}

    updated = service_update(patient_id, merged)
    if not updated:
        return send_404(handler)
    return send_json(handler, 200, updated)


def delete_patient(handler, patient_id):
    from services.patient_service import service_delete

    deleted = service_delete(patient_id)
    if not deleted:
        return send_404(handler)
    return send_json(handler, 200, deleted)


def update_doctor(handler, doctor_id):
    from core.request import parse_json_body
    from services.doctor_service import service_update

    data = parse_json_body(handler)
    updated = service_update(doctor_id, data)
    if not updated:
        return send_404(handler)
    return send_json(handler, 200, updated)


def delete_doctor(handler, doctor_id):
    from services.doctor_service import service_delete

    deleted = service_delete(doctor_id)
    if not deleted:
        return send_404(handler)
    return send_json(handler, 200, deleted)


def update_billing(handler, billing_id):
    from core.request import parse_json_body
    from services.billing_service import service_update

    data = parse_json_body(handler)
    updated = service_update(billing_id, data)
    if not updated:
        return send_404(handler)
    return send_json(handler, 200, updated)


def delete_billing(handler, billing_id):
    from services.billing_service import service_delete

    deleted = service_delete(billing_id)
    if not deleted:
        return send_404(handler)
    return send_json(handler, 200, deleted)


def update_invoice(handler, invoice_id):
    from core.request import parse_json_body
    from services.invoice_service import service_update

    data = parse_json_body(handler)
    updated = service_update(invoice_id, data)
    if not updated:
        return send_404(handler)
    return send_json(handler, 200, updated)


def delete_invoice(handler, invoice_id):
    from services.invoice_service import service_delete

    deleted = service_delete(invoice_id)
    if not deleted:
        return send_404(handler)
    return send_json(handler, 200, deleted)
