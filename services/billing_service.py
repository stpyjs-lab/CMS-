# Feature: billing compatibility layer — reuses invoice logic for billing endpoints. Connects: invoice_service, controllers.
# services/billing_service.py
"""
Billing service layer that forwards to the existing invoice service.
This keeps old "appointments" routes renamed to "billing" while reusing
invoice functionality (amounts, issued_on, description, etc.).
"""
from services.invoice_service import (
    service_get_all as _service_get_all_invoices,
    service_get_one as _service_get_one_invoice,
    service_create as _service_create_invoice,
    service_update as _service_update_invoice,
    service_delete as _service_delete_invoice,
)


def service_get_all():
    return _service_get_all_invoices()


def service_get_one(billing_id):
    return _service_get_one_invoice(billing_id)


def service_create(data):
    return _service_create_invoice(data)


def service_update(billing_id, data):
    return _service_update_invoice(billing_id, data)


def service_delete(billing_id):
    return _service_delete_invoice(billing_id)
