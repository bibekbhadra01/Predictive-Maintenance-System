import pandas as pd

df = pd.read_csv("../data/data.csv")

# Check missing values
print("Missing values:")
print(df.isnull().sum())

# Check duplicate rows
print("\nDuplicate rows:", df.duplicated().sum())

# Separate input features and target
X = df.drop(columns=[
    "Machine failure",
    "TWF", "HDF", "PWF", "OSF", "RNF"
])

y = df["Machine failure"]

print("\nFeatures shape:", X.shape)
print("Target shape:", y.shape)
print("\nTarget distribution:")
print(y.value_counts())