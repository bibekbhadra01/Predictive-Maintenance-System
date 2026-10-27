
import sqlite3
from pathlib import Path

database_path = Path(__file__).parent / "maintenance.db"

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

# Insert one sample machine prediction
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
""", ("M", 300.0, 310.0, 1500, 40.0, 100, 0, "No failure predicted"))

connection.commit()

print("Sample prediction saved successfully!")

connection.close()
