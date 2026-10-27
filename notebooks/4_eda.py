import pandas as pd # manipulates data to tables
import matplotlib.pyplot as plt # creates and displays charts
import seaborn as sns # creates statistical graphs

# Load the dataset
df = pd.read_csv("data/data.csv")

# Part 1: Analyze overall machine failure distribution
failure_counts = df["Machine failure"].value_counts().sort_index() # counts how many timeseach value occurs and sorts the label into numerical order

print("Machine failure counts:")
print(failure_counts)

# Visualize overall failure distribution (Bar Graph)
sns.countplot(data=df, x="Machine failure")

plt.title("Distribution of Machine Failures")
plt.xlabel("Machine Failure (0 = No, 1 = Yes)")
plt.ylabel("Number of Records")
plt.xticks([0, 1], ["No Failure", "Failure"])
plt.tight_layout() # Adusts spacing
plt.show()

# Part 2: Analyze failure counts by machine type
failure_by_type = pd.crosstab( # Creates a frequency table comparing 2 categorical columns
    df["Type"],
    df["Machine failure"]
)

print("\nFailure counts by machine type:")
print(failure_by_type)

# Visualize failures by machine type
sns.countplot(
    data=df,
    x="Type",
    hue="Machine failure"
)

plt.title("Machine Failure Distribution by Type")
plt.xlabel("Machine Type")
plt.ylabel("Number of Records")
plt.legend(
    title="Machine Failure",
    labels=["No Failure", "Failure"]
)
plt.tight_layout()
plt.show()
