import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer # applies different preparations to different columns
from sklearn.preprocessing import OneHotEncoder, StandardScaler # OneHotEncoder - converts Machine type into numerical values, StandardScaler - Scles numerical values
# scaling is done by a formula : (original valuee - mean value) / standard deviation
from sklearn.pipeline import Pipeline # used to combine multiple Machine Learning steps into one workflow so they run automatically in the correct order.
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# Load dataset
df = pd.read_csv("../data/data.csv")

# Separate features and target
X = df.drop(columns=[
    "Machine failure",
    "TWF", "HDF", "PWF", "OSF", "RNF"
])
y = df["Machine failure"]

# Identify categorical and numerical features
categorical_features = ["Type"]
numerical_features = [
    "Air temperature",
    "Process temperature",
    "Rotational speed",
    "Torque",
    "Tool wear"
]

# Prepare the features
preprocessor = ColumnTransformer([ # It directs different columns to the appropriate preparation method.
    ("num", StandardScaler(), numerical_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
])

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create the ML pipeline
model = Pipeline([
    ("preprocessing", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))