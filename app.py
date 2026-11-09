
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import importlib.util
import sys

app = Flask(__name__)
CORS(app)

PROJECT_ROOT = Path(__file__).resolve().parent

# Load the ML prediction function
prediction_file = PROJECT_ROOT / "notebooks" / "13_prediction_function.py"

spec = importlib.util.spec_from_file_location(
    "prediction_module",
    prediction_file
)

prediction_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prediction_module)

predict_machine_failure = prediction_module.predict_machine_failure

# Load database operation
sys.path.insert(0, str(PROJECT_ROOT / "database"))

from db_operations import save_prediction


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Please send sensor readings as JSON."
            }), 400

        machine_type = data.get("machine_type", data.get("type"))

        air_temperature = data.get(
            "air_temperature",
            data.get("airTemperature")
        )

        process_temperature = data.get(
            "process_temperature",
            data.get("processTemperature")
        )

        rotational_speed = data.get(
            "rotational_speed",
            data.get("rotationalSpeed")
        )

        torque = data.get("torque")

        tool_wear = data.get(
            "tool_wear",
            data.get("toolWear")
        )

        # Get the ML prediction
        result = predict_machine_failure(
            machine_type,
            air_temperature,
            process_temperature,
            rotational_speed,
            torque,
            tool_wear
        )

        # Save the prediction to the database
        prediction_id = save_prediction(
            machine_type,
            float(air_temperature),
            float(process_temperature),
            float(rotational_speed),
            float(torque),
            float(tool_wear),
            result["predicted_failure"],
            result["status"]
        )

        # Return the prediction to the frontend
        return jsonify({
            "prediction_id": prediction_id,
            **result
        }), 200

    except (ValueError, TypeError) as error:
        return jsonify({
            "error": str(error)
        }), 400

    except Exception:
        app.logger.exception("Prediction failed")

        return jsonify({
            "error": "Prediction failed. Check the backend terminal."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
