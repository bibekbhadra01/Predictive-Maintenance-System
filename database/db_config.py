import os
from pathlib import Path

DATABASE_PATH = Path(
    os.environ.get("MAINTENANCE_DB", Path(__file__).parent / "maintenance.db")
)