# Feature: doctor service — CRUD logic forwarding to DB queries. Connects: database.queries, controllers.
from database.queries import (
    doctors_get_all,
    doctors_get_one,
    doctors_create,
    doctors_update,
    doctors_delete,
)


def service_get_all():
    return doctors_get_all()


def service_get_one(doctor_id):
    return doctors_get_one(doctor_id)


def service_create(data):
    return doctors_create(data)


def service_update(doctor_id, data):
    return doctors_update(doctor_id, data)


def service_delete(doctor_id):
    return doctors_delete(doctor_id)
