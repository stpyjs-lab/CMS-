from database.queries import (
    invoices_get_all,
    invoices_get_one,
    invoices_create,
    invoices_update,
    invoices_delete,
)


def service_get_all():
    return invoices_get_all()


def service_get_one(invoice_id):
    return invoices_get_one(invoice_id)


def service_create(data):
    return invoices_create(data)


def service_update(invoice_id, data):
    return invoices_update(invoice_id, data)


def service_delete(invoice_id):
    return invoices_delete(invoice_id)
