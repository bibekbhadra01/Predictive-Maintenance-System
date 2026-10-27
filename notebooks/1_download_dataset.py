from ucimlrepo import fetch_ucirepo #importing the dataset from UCI Machine Learning Repository
import pandas as pd # manipulates data to tables 
from pathlib import Path # manages file and folders paths

# Create the data folder if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Fetch the dataset from UCI
dataset = fetch_ucirepo(id=601)

# Combine input features and target columns
X = dataset.data.features
y = dataset.data.targets

df = pd.concat([X, y], axis=1) # combines the inputs and the target

df.to_csv(data_dir / "data.csv", index=False) # Save the complete original dataset

print("Dataset downloaded successfully!")
print("Shape:", df.shape)
print("Saved to:", data_dir / "data.csv")
print("\nFirst five rows:")
print(df.head())