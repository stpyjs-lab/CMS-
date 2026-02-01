# database/queries.py
# Actual SQL queries — Create, Read, Update, Delete (CRUD)

from datetime import datetime
from .connection import get_connection





# -----------------------------
# COURSES CRUD
# -----------------------------

# -----------------------------
# COURSES CRUD (UPDATED)
# -----------------------------






# -----------------------------
# PATIENTS CRUD
# -----------------------------

def patients_get_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def patients_get_one(patient_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def patients_create(data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()

    cur = conn.execute(
        """
        INSERT INTO patients (first_name, last_name, dob, phone, email, address, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("first_name"),
            data.get("last_name"),
            data.get("dob"),
            data.get("phone"),
            data.get("email"),
            data.get("address"),
            now,
        ),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return patients_get_one(new_id)


def patients_update(patient_id: int, data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute(
        """
        UPDATE patients
        SET first_name=?, last_name=?, dob=?, phone=?, email=?, address=?, updated_at=?
        WHERE id=?
        """,
        (
            data.get("first_name"),
            data.get("last_name"),
            data.get("dob"),
            data.get("phone"),
            data.get("email"),
            data.get("address"),
            now,
            patient_id,
        ),
    )
    conn.commit()
    conn.close()
    return patients_get_one(patient_id)


def patients_delete(patient_id: int):
    patient = patients_get_one(patient_id)
    if not patient:
        return None

    conn = get_connection()
    conn.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()
    conn.close()
    return patient


# -----------------------------
# DOCTORS CRUD
# -----------------------------

def doctors_get_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM doctors ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def doctors_get_one(doctor_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def doctors_create(data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    cur = conn.execute(
        "INSERT INTO doctors (name, specialty, phone, email, created_at) VALUES (?, ?, ?, ?, ?)",
        (data.get("name"), data.get("specialty"), data.get("phone"), data.get("email"), now),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return doctors_get_one(new_id)


def doctors_update(doctor_id: int, data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute(
        """
        UPDATE doctors
        SET name=?, specialty=?, phone=?, email=?, updated_at=?
        WHERE id=?
        """,
        (data.get("name"), data.get("specialty"), data.get("phone"), data.get("email"), now, doctor_id),
    )
    conn.commit()
    conn.close()
    return doctors_get_one(doctor_id)


def doctors_delete(doctor_id: int):
    doctor = doctors_get_one(doctor_id)
    if not doctor:
        return None

    conn = get_connection()
    conn.execute("DELETE FROM doctors WHERE id=?", (doctor_id,))
    conn.commit()
    conn.close()
    return doctor


# -----------------------------
# APPOINTMENTS CRUD
# -----------------------------

def appointments_get_all():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            a.*,
            p.first_name || ' ' || p.last_name AS patient_name,
            d.name AS doctor_name
        FROM appointments a
        LEFT JOIN patients p ON p.id = a.patient_id
        LEFT JOIN doctors d ON d.id = a.doctor_id
        ORDER BY a.id DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def appointments_get_one(appointment_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def appointments_create(data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    cur = conn.execute(
        "INSERT INTO appointments (patient_id, doctor_id, scheduled_at, reason, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (data["patient_id"], data["doctor_id"], data["scheduled_at"], data.get("reason"), data.get("status", "scheduled"), now),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return appointments_get_one(new_id)


def appointments_update(appointment_id: int, data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute(
        """
        UPDATE appointments
        SET patient_id=?, doctor_id=?, scheduled_at=?, reason=?, status=?, updated_at=?
        WHERE id=?
        """,
        (
            data.get("patient_id"),
            data.get("doctor_id"),
            data.get("scheduled_at"),
            data.get("reason"),
            data.get("status"),
            now,
            appointment_id,
        ),
    )
    conn.commit()
    conn.close()
    return appointments_get_one(appointment_id)


def appointments_delete(appointment_id: int):
    appt = appointments_get_one(appointment_id)
    if not appt:
        return None

    conn = get_connection()
    conn.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
    conn.commit()
    conn.close()
    return appt


# -----------------------------
# INVOICES CRUD
# -----------------------------

def invoices_get_all():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            i.*,
            p.first_name || ' ' || p.last_name AS patient_name,
            d.name AS doctor_name
        FROM invoices i
        LEFT JOIN patients p ON p.id = i.patient_id
        LEFT JOIN doctors d ON d.id = i.doctor_id
        ORDER BY i.id DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def invoices_get_one(invoice_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def invoices_create(data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    cur = conn.execute(
        "INSERT INTO invoices (patient_id, doctor_id, amount, issued_on, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (data["patient_id"], data.get("doctor_id"), data["amount"], data.get("issued_on"), data.get("description"), now)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return invoices_get_one(new_id)


def invoices_update(invoice_id: int, data: dict):
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute(
        """
        UPDATE invoices
        SET patient_id=?, doctor_id=?, amount=?, issued_on=?, description=?, updated_at=?
        WHERE id=?
        """,
        (
            data.get("patient_id"),
            data.get("doctor_id"),
            data.get("amount"),
            data.get("issued_on"),
            data.get("description"),
            now,
            invoice_id,
        ),
    )
    conn.commit()
    conn.close()
    return invoices_get_one(invoice_id)


def invoices_delete(invoice_id: int):
    inv = invoices_get_one(invoice_id)
    if not inv:
        return None

    conn = get_connection()
    conn.execute("DELETE FROM invoices WHERE id=?", (invoice_id,))
    conn.commit()
    conn.close()
    return inv


# -----------------------------
# APPOINTMENT REPORT (JOIN)
# -----------------------------

def appointment_report():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            a.id AS appointment_id,
            a.scheduled_at,
            a.reason,
            a.status,

            p.id AS patient_id,
            p.first_name || ' ' || p.last_name AS patient_name,
            p.phone AS patient_phone,
            p.email AS patient_email,

            d.id AS doctor_id,
            d.name AS doctor_name,
            d.specialty AS doctor_specialty
        FROM appointments a
        JOIN patients p ON p.id = a.patient_id
        JOIN doctors d ON d.id = a.doctor_id
        ORDER BY a.id DESC;
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]
