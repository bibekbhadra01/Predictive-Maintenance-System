import pandas as pd
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv("../data/data.csv")

# Separate features and target
X = df.drop(columns=[
    "Machine failure",
    "TWF", "HDF", "PWF", "OSF", "RNF"
])

y = df["Machine failure"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y # Python tries to maintain the same percentages of failed and non-failed machines in both sets.
)

# Display the sizes
print("Training features:", X_train.shape)
print("Testing features:", X_test.shape)
print("Training target:", y_train.shape)
print("Testing target:", y_test.shape)

print("\nFailure distribution in training data:")
print(y_train.value_counts())

print("\nFailure distribution in testing data:")
print(y_test.value_counts())