
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "maintenance.db"


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
    machine_id=None
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
