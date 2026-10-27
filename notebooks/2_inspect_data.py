
import pandas as pd

# Load the downloaded dataset
df = pd.read_csv("data/data.csv")

# 1. Display the number of rows and columns
print("Dataset shape:")
print(df.shape) # Prints the Number of observations and columns

# 2. Display column names
print("\nColumn names:")
print(df.columns.tolist())

# 3. Display the first five rows
print("\nFirst five rows:")
print(df.head())

# 4. Display data types and non-null counts
print("\nDataset information:")
df.info()

# 5. Display summary statistics
print("\nSummary statistics:")
print(df.describe())

# 6. Check missing values in each column
print("\nMissing values:")
print(df.isnull().sum())

# 7. Check duplicate rows
print("\nNumber of duplicate rows:")
print(df.duplicated().sum())
