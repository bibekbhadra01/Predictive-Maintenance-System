
from db_operations import save_prediction

record_id = save_prediction(
    "M",
    300.0,
    310.0,
    1500,
    40.0,
    100,
    0,
    "No failure predicted"
)

print("Prediction saved with ID:", record_id)
