import pandas as pd
import joblib # used to save and load the data model
import math

# Load the saved Random Forest model
model_path = "../models/random_forest_model.pkl"

model = joblib.load(model_path)

print("Model loaded successfully!")




def predict_machine_failure(
    machine_type,
    air_temperature,
    process_temperature,
    rotational_speed,
    torque,
    tool_wear
):
    # Check machine type
    if machine_type not in ["L", "M", "H"]:
        raise ValueError("Type must be L, M, or H.") # stops the function and reports input error

    # Collect numerical sensor readings
    readings = {
        "Air temperature": air_temperature,
        "Process temperature": process_temperature,
        "Rotational speed": rotational_speed,
        "Torque": torque,
        "Tool wear": tool_wear
    }

    # Check that all readings are valid numbers
    for name, value in readings.items():
        if isinstance(value, bool):
            raise ValueError(f"{name} must be a number.")

        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"{name} must be a number.")

        if not math.isfinite(number):
            raise ValueError(f"{name} must be a finite number.")

        readings[name] = number # saves the converted number

    # Check basic physical limits
    if readings["Air temperature"] <= 0:
        raise ValueError("Air temperature must be above 0 K.")

    if readings["Process temperature"] <= 0:
        raise ValueError("Process temperature must be above 0 K.")

    if readings["Rotational speed"] <= 0:
        raise ValueError("Rotational speed must be above zero.")

    if readings["Torque"] < 0:
        raise ValueError("Torque cannot be negative.")

    if readings["Tool wear"] < 0:
        raise ValueError("Tool wear cannot be negative.")



    
    # Prepare one row for the model
    sample = pd.DataFrame([{
        "Type": machine_type,
        **readings
    }])

    # Generate prediction
    prediction = model.predict(sample)

    # Convert the prediction into a simple number
    predicted_failure = int(prediction[0])

    # Prepare the result for the backend
    if predicted_failure == 1:
        status = "Failure predicted"
    else:
        status = "No failure predicted"

    return {
        "predicted_failure": predicted_failure,
        "status": status
    }













# Test 1: Valid inputs
print(predict_machine_failure(
    "M", 300.0, 310.0, 1500, 40.0, 100
))

# Test 2: Invalid machine type
try:
    predict_machine_failure(
        "X", 300.0, 310.0, 1500, 40.0, 100
    )
except ValueError as error:
    print("Input error:", error)

# Test 3: Numeric strings
print(predict_machine_failure(
    "M", "300", "310", "1500", "40", "100"
))


# Test 4: Non-numeric temperature
try:
    predict_machine_failure(
        "M", "hello", 310.0, 1500, 40.0, 100
    )
except ValueError as error:
    print("Test 4:", error)


# Test 5: Negative torque
try:
    predict_machine_failure(
        "M", 300.0, 310.0, 1500, -40.0, 100
    )
except ValueError as error:
    print("Test 5:", error)


# Test 6: Negative tool wear
try:
    predict_machine_failure(
        "M", 300.0, 310.0, 1500, 40.0, -10
    )
except ValueError as error:
    print("Test 6:", error)


# Test 7: Infinite temperature
try:
    predict_machine_failure(
        "M", float("inf"), 310.0, 1500, 40.0, 100
    )
except ValueError as error:
    print("Test 7:", error)