from database.queries import (
    patients_get_all,
    patients_get_one,
    patients_create,
    patients_update,
    patients_delete,
)


def service_get_all():
    return patients_get_all()


def service_get_one(patient_id):
    return patients_get_one(patient_id)


def service_create(data):
    return patients_create(data)


def service_update(patient_id, data):
    return patients_update(patient_id, data)


def service_delete(patient_id):
    return patients_delete(patient_id)
