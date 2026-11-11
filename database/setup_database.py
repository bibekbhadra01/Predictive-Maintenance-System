
import sqlite3
from db_config import DATABASE_PATH

<<<<<<< HEAD
DATABASE_PATH = Path(__file__).parent / "maintenance.db"

MACHINES = [
    ("MCH-001", "L"),
    ("MCH-002", "M"),
    ("MCH-003", "H"),
    ("MCH-004", "L"),
    ("MCH-005", "M"),
    ("MCH-006", "H"),
]

=======
MACHINES = [
    ("MCH-001", "L"),
    ("MCH-002", "M"),
    ("MCH-003", "H"),
    ("MCH-004", "L"),
    ("MCH-005", "M"),
    ("MCH-006", "H"),
]

>>>>>>> 3198136 (Update database setup and testing)
connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS machines (
    machine_id TEXT PRIMARY KEY,
    machine_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

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

<<<<<<< HEAD
=======
cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id TEXT NOT NULL,
    prediction_id INTEGER,
    message TEXT NOT NULL,
    is_resolved INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

>>>>>>> 3198136 (Update database setup and testing)
# Add machine_id to an existing predictions table if necessary.
columns = [
    row[1] for row in cursor.execute(
        "PRAGMA table_info(predictions)"
    ).fetchall()
]

if "machine_id" not in columns:
    cursor.execute(
        "ALTER TABLE predictions ADD COLUMN machine_id TEXT"
    )

<<<<<<< HEAD
=======
if "confidence" not in columns:
    cursor.execute("ALTER TABLE predictions ADD COLUMN confidence REAL")    

>>>>>>> 3198136 (Update database setup and testing)
# Insert the six profiles without overwriting existing records.
cursor.executemany("""
INSERT OR IGNORE INTO machines (machine_id, machine_type)
VALUES (?, ?)
""", MACHINES)

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_predictions_machine
ON predictions(machine_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_predictions_created
ON predictions(created_at)
""")

connection.commit()
connection.close()

print("Database setup successful!")
print("Six machine profiles are ready.")
print(f"Database location: {DATABASE_PATH}")
