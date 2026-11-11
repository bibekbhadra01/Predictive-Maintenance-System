
from db_operations import save_prediction, get_predictions

# Insert a sample prediction
prediction_id = save_prediction(
    "L",
    298.1,
    308.6,
    1500,
    40.0,
    100,
    0,
    "No failure predicted",
    "MCH-001"
)

print("Prediction saved successfully!")
print("Prediction ID:", prediction_id)

# Retrieve predictions
predictions = get_predictions()

print("\nSaved predictions:")

for prediction in predictions:
    print(dict(prediction))
