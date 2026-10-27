
import sqlite3
from pathlib import Path

database_path = Path(__file__).parent / "maintenance.db"

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

cursor.execute("SELECT * FROM predictions")
records = cursor.fetchall()

for record in records:
    print(record)

connection.close()
