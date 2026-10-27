
import sqlite3
from pathlib import Path

database_path = Path(__file__).parent / "maintenance.db"

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

cursor.execute("PRAGMA table_info(predictions)")
columns = cursor.fetchall()

print("Columns in predictions table:")

for column in columns:
    print(column[1])

connection.close()
