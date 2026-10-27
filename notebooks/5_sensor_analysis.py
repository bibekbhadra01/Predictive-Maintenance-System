import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("data/data.csv")

print("Actual column names:")
print(df.columns.tolist())

# Select numerical sensor features to be examined
features = [
    "Air temperature",
    "Process temperature",
    "Rotational speed",
    "Torque",
    "Tool wear"
]

# Display summary statistics for these features
print("Sensor feature summary:")
print(df[features].describe().T) # selects only the features and summarizes their value using statistics

# Plot distributions of sensor features (Histogram)
df[features].hist(figsize=(12, 8), bins=30)  # bins divide each range into 30 intervals

plt.suptitle("Distribution of Sensor Features")
plt.tight_layout()
plt.show()
