import joblib
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
    confusion_matrix,
    classification_report
)

# 1. Load dataset
df = pd.read_csv("../data/data.csv")

print("Columns in dataset:")
print(df.columns.tolist()) # displays all column names


# 2. Separate features and target

y = df["Machine failure"]

columns_to_drop = [
    "UDI",
    "Product ID",
    "Machine failure",
    "TWF",
    "HDF",
    "PWF",
    "OSF",
    "RNF"
]

# Drop only columns that actually exist
X = df.drop(
    columns=[col for col in columns_to_drop if col in df.columns]
)

print("\nFeature columns:")
print(X.columns.tolist())

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 4. Identify feature types
numerical_features = X.select_dtypes(include=["number"]).columns.tolist() # selects columns with only numerical data type and displays it's column name
categorical_features = X.select_dtypes(exclude=["number"]).columns.tolist() # excludes numerical columns and returns the names of remaining columns

# 5. Define preprocessing
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numerical_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
])

# 6. Define models
models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
}

# 7. Train and evaluate
results = []

for name, classifier in models.items():
    model = Pipeline([
        ("preprocessing", preprocessor),
        ("classifier", classifier)
    ])

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    if name == "Random Forest":
        os.makedirs("../models", exist_ok=True)
        joblib.dump(model, "../models/random_forest_model.pkl")
        print("Random Forest model saved successfully!")

    print(f"\n{'=' * 45}")
    print(name)
    print("=" * 45)

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred, labels=[0, 1]))

    print("\nClassification Report:")
    print(classification_report(
        y_test, y_pred,
        labels=[0, 1],
        target_names=["No Failure", "Failure"],
        zero_division=0
    ))

    results.append({
        "Model": name,
        "Precision (Failure)": precision_score(
            y_test, y_pred, zero_division=0
        ),
        "Recall (Failure)": recall_score(
            y_test, y_pred, zero_division=0
        ),
        "F1-score (Failure)": f1_score(
            y_test, y_pred, zero_division=0
        ),
        "Accuracy": accuracy_score(y_test, y_pred)
    })

# 8. Display and save comparison
results_df = pd.DataFrame(results)

print("\nMODEL COMPARISON")
print(results_df.round(4).to_string(index=False))

results_df.to_csv("../models/model_comparison.csv", index=False)
print("\nResults saved to models/model_comparison.csv")

best_model = results_df.loc[
    results_df["Recall (Failure)"].idxmax(), "Model"
]

print("\nBest model by failure recall:")
print(best_model)