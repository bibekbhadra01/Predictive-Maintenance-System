
import joblib
import pandas as pd

# Load the saved model pipeline
model = joblib.load("../models/random_forest_model.pkl")

# Create one sample of sensor readings
sample = pd.DataFrame([{
    "Type": "M",
    "Air temperature": 300.0,
    "Process temperature": 310.0,
    "Rotational speed": 1500,
    "Torque": 40.0,
    "Tool wear": 100
}])

# Predict machine failure
prediction = model.predict(sample)

print("Predicted machine failure:", prediction[0])

if prediction[0] == 1:
    print("Alert: Potential machine failure detected!")
else:
    print("No machine failure predicted.")
