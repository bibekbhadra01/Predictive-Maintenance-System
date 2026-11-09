

const predictionForm = document.getElementById("predictionForm");
const predictionResult = document.getElementById("predictionResult");

if (predictionForm && predictionResult) {
    predictionForm.addEventListener("submit", async function (event) {
        // Prevent the page from refreshing
        event.preventDefault();

        const machineTypeField = document.getElementById("machineType");
        const airTemperatureField = document.getElementById("airTemperature");
        const processTemperatureField = document.getElementById("processTemperature");
        const rotationalSpeedField = document.getElementById("rotationalSpeed");
        const torqueField = document.getElementById("torque");
        const toolWearField = document.getElementById("toolWear");

        // Check that all required fields exist
        if (
            !machineTypeField ||
            !airTemperatureField ||
            !processTemperatureField ||
            !rotationalSpeedField ||
            !torqueField ||
            !toolWearField
        ) {
            showResult("Error: One or more form fields are missing from index.html.", "error");
            return;
        }

        const machineType = machineTypeField.value;
        const airTemperature = Number(airTemperatureField.value);
        const processTemperature = Number(processTemperatureField.value);
        const rotationalSpeed = Number(rotationalSpeedField.value);
        const torque = Number(torqueField.value);
        const toolWear = Number(toolWearField.value);

        // Validate machine type
        if (!["L", "M", "H"].includes(machineType)) {
            showResult("Please select a machine type: L, M, or H.", "error");
            return;
        }

        // Validate that all fields have values
        if (
            airTemperatureField.value.trim() === "" ||
            processTemperatureField.value.trim() === "" ||
            rotationalSpeedField.value.trim() === "" ||
            torqueField.value.trim() === "" ||
            toolWearField.value.trim() === ""
        ) {
            showResult("Please fill in all five sensor readings.", "error");
            return;
        }

        // Validate sensor readings
        if (
            !Number.isFinite(airTemperature) ||
            !Number.isFinite(processTemperature) ||
            !Number.isFinite(rotationalSpeed) ||
            !Number.isFinite(torque) ||
            !Number.isFinite(toolWear) ||
            airTemperature <= 0 ||
            processTemperature <= 0 ||
            rotationalSpeed <= 0 ||
            torque < 0 ||
            toolWear < 0
        ) {
            showResult("Please enter valid readings. Temperatures and speed must be positive; torque and tool wear cannot be negative.", "error");
            return;
        }

        showResult("Analyzing machine condition. Please wait...", "loading");

        const submitButton = predictionForm.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = "Analyzing...";
        }

        try {
            console.log("Sending prediction request to Flask backend...");

            const response = await fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    machine_type: machineType,
                    air_temperature: airTemperature,
                    process_temperature: processTemperature,
                    rotational_speed: rotationalSpeed,
                    torque: torque,
                    tool_wear: toolWear
                })
            });

            const result = await response.json();

            console.log("Backend response:", result);

            if (!response.ok) {
                throw new Error(result.error || `Server error: ${response.status}`);
            }

            const failureDetected = Number(result.predicted_failure) === 1;

            // Build the prediction result
            predictionResult.replaceChildren();

            const heading = document.createElement("h3");
            heading.textContent = failureDetected
                ? "⚠️ Potential Machine Failure"
                : "✅ No Failure Predicted";

            const details = [
                ["Status", result.status],
                ["Prediction ID", result.prediction_id],
                ["Machine Type", machineType],
                ["Air Temperature", `${airTemperature} K`],
                ["Process Temperature", `${processTemperature} K`],
                ["Rotational Speed", `${rotationalSpeed} RPM`],
                ["Torque", `${torque} Nm`],
                ["Tool Wear", `${toolWear} minutes`]
            ];

            predictionResult.appendChild(heading);

            details.forEach(([label, value]) => {
                const paragraph = document.createElement("p");
                const strong = document.createElement("strong");

                strong.textContent = `${label}: `;
                paragraph.appendChild(strong);
                paragraph.appendChild(document.createTextNode(String(value)));

                predictionResult.appendChild(paragraph);
            });

            styleResult(failureDetected ? "failure" : "success");

            // Bring the result into view
            predictionResult.scrollIntoView({
                behavior: "smooth",
                block: "nearest"
            });

        } catch (error) {
            console.error("Prediction error:", error);

            showResult(
                `Prediction failed: ${error.message}. Check that the backend is running and the database is set up.`,
                "error"
            );

        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = "Check Machine Health";
            }
        }
    });
}

function showResult(message, type) {
    predictionResult.textContent = message;
    styleResult(type);
}

function styleResult(type) {
    predictionResult.style.display = "block";
    predictionResult.style.padding = "20px";
    predictionResult.style.marginTop = "20px";
    predictionResult.style.borderRadius = "10px";
    predictionResult.style.border = "1px solid";
    predictionResult.style.lineHeight = "1.6";

    if (type === "success") {
        predictionResult.style.color = "#166534";
        predictionResult.style.backgroundColor = "#f0fdf4";
        predictionResult.style.borderColor = "#bbf7d0";
    } else if (type === "failure" || type === "error") {
        predictionResult.style.color = "#b91c1c";
        predictionResult.style.backgroundColor = "#fef2f2";
        predictionResult.style.borderColor = "#fecaca";
    } else {
        predictionResult.style.color = "#1d4ed8";
        predictionResult.style.backgroundColor = "#eff6ff";
        predictionResult.style.borderColor = "#bfdbfe";
    }
}
