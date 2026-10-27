
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "maintenance.db"


def save_prediction(
    machine_type,
    air_temperature,
    process_temperature,
    rotational_speed,
    torque,
    tool_wear,
    predicted_failure,
    prediction_status
):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO predictions (
                machine_type,
                air_temperature,
                process_temperature,
                rotational_speed,
                torque,
                tool_wear,
                predicted_failure,
                prediction_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
