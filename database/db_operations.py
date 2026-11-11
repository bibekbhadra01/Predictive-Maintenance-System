
import sqlite3
from db_config import DATABASE_PATH


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def get_machines():
    connection = get_connection()
    try:
        rows = connection.execute("""
            SELECT machine_id, machine_type
            FROM machines
            ORDER BY machine_id
        """).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def get_machine(machine_id):
    connection = get_connection()
    try:
        row = connection.execute("""
            SELECT machine_id, machine_type
            FROM machines
            WHERE machine_id = ?
        """, (machine_id,)).fetchone()

        if not row:
            return None

        machine = dict(row)

        latest = connection.execute("""
            SELECT *
            FROM predictions
            WHERE machine_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT 1
        """, (machine_id,)).fetchone()

        machine["latest_prediction"] = (
            dict(latest) if latest else None
        )
        return machine
    finally:
        connection.close()


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def get_machines():
    connection = get_connection()
    try:
        rows = connection.execute("""
            SELECT machine_id, machine_type
            FROM machines
            ORDER BY machine_id
        """).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def get_machine(machine_id):
    connection = get_connection()
    try:
        row = connection.execute("""
            SELECT machine_id, machine_type
            FROM machines
            WHERE machine_id = ?
        """, (machine_id,)).fetchone()

        if not row:
            return None

        machine = dict(row)

        latest = connection.execute("""
            SELECT *
            FROM predictions
            WHERE machine_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT 1
        """, (machine_id,)).fetchone()

        machine["latest_prediction"] = (
            dict(latest) if latest else None
        )
        return machine
    finally:
        connection.close()


def save_prediction(
    machine_type,
    air_temperature,
    process_temperature,
    rotational_speed,
    torque,
    tool_wear,
    predicted_failure,
    prediction_status,
<<<<<<< HEAD
    machine_id=None
=======
    machine_id=None,
    confidence=None
>>>>>>> 3198136 (Update database setup and testing)
):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO predictions (
                machine_id,
                machine_type,
                air_temperature,
                process_temperature,
                rotational_speed,
                torque,
                tool_wear,
                predicted_failure,
                prediction_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            machine_id,
            machine_type,
            air_temperature,
            process_temperature,
            rotational_speed,
            torque,
            tool_wear,
            predicted_failure,
            prediction_status
        ))

        connection.commit()
        return cursor.lastrowid
<<<<<<< HEAD
    finally:
        connection.close()


def get_predictions(limit=100):
    connection = get_connection()
    try:
        rows = connection.execute("""
            SELECT
                p.*,
                m.machine_id AS selected_machine
            FROM predictions p
            LEFT JOIN machines m
                ON p.machine_id = m.machine_id
            ORDER BY p.created_at DESC, p.id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]
=======
>>>>>>> 3198136 (Update database setup and testing)
    finally:
        connection.close()


def get_predictions(limit=100):
    connection = get_connection()
    try:
        rows = connection.execute("""
            SELECT
                p.*,
                m.machine_id AS selected_machine
            FROM predictions p
            LEFT JOIN machines m
                ON p.machine_id = m.machine_id
            ORDER BY p.created_at DESC, p.id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]
    finally:
        connection.close()


def save_alert(machine_id, prediction_id, message):
    connection = get_connection()
    try:
        cursor = connection.execute(
            "INSERT INTO alerts (machine_id, prediction_id, message) VALUES (?, ?, ?)",
            (machine_id, prediction_id, message),
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def get_alerts(limit=50):
    connection = get_connection()
    try:
        rows = connection.execute(
            "SELECT * FROM alerts ORDER BY created_at DESC, id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        connection.close()        
