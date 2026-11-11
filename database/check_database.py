
import sqlite3
from pathlib import Path

database_path = Path(__file__).parent / "maintenance.db"

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

# 1. Check all tables
cursor.execute("""
SELECT name FROM sqlite_master
WHERE type = 'table'
""")

tables = [row[0] for row in cursor.fetchall()]

print("\n--- DATABASE TABLES ---")

for table in ["machines", "predictions", "alerts"]:
    if table in tables:
        print(f"SUCCESS: {table} table exists")
    else:
        print(f"ERROR: {table} table is missing")

# 2. Check columns in each table
for table in ["machines", "predictions", "alerts"]:
    if table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()

        print(f"\n--- {table.upper()} COLUMNS ---")

        for column in columns:
            print(column[1])

# 3. Check machine records
if "machines" in tables:
    cursor.execute("SELECT * FROM machines")
    machines = cursor.fetchall()

    print("\n--- MACHINE RECORDS ---")
    for machine in machines:
        print(machine)

    print("Total machines:", len(machines))

connection.close()

print("\nDatabase checking completed!")
