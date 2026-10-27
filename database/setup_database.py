
import sqlite3
from pathlib import Path

# Locate the database file in the current folder
database_path = Path(__file__).parent / "maintenance.db"

# Connect to the database
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

# Create a table for machine readings and predictions
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_type TEXT NOT NULL,
    air_temperature REAL NOT NULL,
    process_temperature REAL NOT NULL,
    rotational_speed INTEGER NOT NULL,
    torque REAL NOT NULL,
    tool_wear INTEGER NOT NULL,
    predicted_failure INTEGER NOT NULL,
    prediction_status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Save the changes and close the connection
connection.commit()
connection.close()

print("Database created successfully!")
print(f"Location: {database_path}")
