
import pandas as pd

# Load the original dataset
df = pd.read_csv("data/data.csv")

print("Original dataset shape:", df.shape)

# 1. Check missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# 2. Check duplicate rows
print("\nNumber of duplicate rows:", df.duplicated().sum())

# 3. Check data types
print("\nColumn data types:")
print(df.dtypes)

# 4. Check unique values in important columns
print("\nMachine type counts:")
print(df["Type"].value_counts())

print("\nMachine failure counts:")
print(df["Machine failure"].value_counts())

# 5. Check numeric ranges
print("\nNumeric summary:")
print(df.describe().T)
