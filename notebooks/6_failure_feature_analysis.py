import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("../data/data.csv")

# Select the sensor features we want to compare
features = [
    "Air temperature",
    "Process temperature",
    "Rotational speed",
    "Torque",
    "Tool wear"
]

# Compare average sensor readings for failure vs no failure
print("Average sensor readings by machine failure:")
print(df.groupby("Machine failure")[features].mean().T) # separates rows into 2 groups - Failure and No Failure

# Visualize the distributions for each failure category
for feature in features:
    plt.figure(figsize=(7, 4))

    sns.boxplot(
        data=df,
        x="Machine failure",
        y=feature
    )

    plt.title(f"{feature} by Machine Failure")
    plt.xlabel("Machine Failure (0 = No, 1 = Yes)")
    plt.tight_layout()
    plt.show()
