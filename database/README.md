# Predictive Maintenance — Database

## Database Technology
SQLite

## Database File
`maintenance.db`

The database file is created automatically by running:

```bash
python3 database/setup_database.py
```

## Table: `predictions`

Stores machine sensor readings and their predicted failure results.

| Column | Purpose |
|---|---|
| `id` | Unique record ID |
| `machine_type` | Machine type (L, M, or H) |
| `air_temperature` | Air temperature |
| `process_temperature` | Process temperature |
| `rotational_speed` | Rotational speed |
| `torque` | Machine torque |
| `tool_wear` | Tool wear |
| `predicted_failure` | 0 = no failure predicted, 1 = failure predicted |
| `prediction_status` | Text description of prediction |
| `created_at` | Record creation time |

## Saving Predictions

The backend can import the reusable function:

```python
from database.db_operations import save_prediction
```

Call `save_prediction()` after the ML model produces a prediction. Pass the six sensor inputs, the predicted failure value, and its status.

The function saves the record and returns its database ID.

## Important

The backend must use the same database file path as the application. The database currently contains sample records from testing.
