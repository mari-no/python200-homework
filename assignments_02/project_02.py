#Task 1: Fetch the Data

import requests
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
   
    "latitude": 30.2672,
    "longitude": -97.7431,
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "wind_speed_10m_max",
    ],
    "timezone": "America/Chicago",
}
response = requests.get(url, params=params)
response.raise_for_status()
df = pd.DataFrame(response.json()["daily"])
df["date"] = pd.to_datetime(df["time"])
df = df.drop("time", axis=1)
print("Dataset shape:", df.shape)
print("First 5 rows:",df.head())
#Austin, Texas

#Task 2: Look at the Features


print("Descriptive statistics:")
print(df.describe())

# Check for missing values in each column
print("Missing values:")
print(df.isna().sum())

# No missing values, no need to remove/handle them 


# Correlation with Daily High

target = "temperature_2m_max"

correlations = (
    df.select_dtypes(include="number")
    .corr()[target]
    .drop(target)
    .sort_values(ascending=False)
)

print("\nCorrelation with daily high, sorted:")
print(correlations)

# The feature with the largest positive correlation is the one
# most strongly positively related to the daily high.
print("Most strongly positively correlated feature:")
print(correlations.idxmax())


#  Create and Save a Plot

output_dir = Path("outputs")
output_dir.mkdir(parents=True, exist_ok=True)

plt.figure(figsize=(8, 5))
plt.scatter(
    df["temperature_2m_min"],
    df["temperature_2m_max"],
    alpha=0.6,
)

plt.xlabel("Daily Low Temperature (°C)")
plt.ylabel("Daily High Temperature (°C)")
plt.title("Austin: Daily Low vs. Daily High Temperature (2023)")
plt.tight_layout()

plt.savefig(output_dir / "austin_low_vs_high.png", dpi=150)
plt.show()


# The daily minimum temperature has a strong positive correlation
# with the daily maximum temperature (0.9415).

# Maximum wind speed has a weak positive correlation with the daily high (0.1044).

# Precipitation has a weak negative correlation with the daily high (-0.1407).

# The scatter plot shows a strong positive relationship:
# days with higher minimum temperatures generally have higher maximum temperatures.


# Task 3: Engineer a Feature

# Create a binary feature: 1 for summer (June, July, August), 0 otherwise
df["is_summer"] = df["date"].dt.month.isin([6, 7, 8]).astype(int)

# Count summer and non-summer days
print("Summer and non-summer days:")
print(df["is_summer"].value_counts().rename(index={0: "Non-summer", 1: "Summer"}))

# I expect is_summer to help predict the daily high because Austin
# generally has hotter temperatures in summer than in other seasons.


# Task 4: Baseline Model



# Feature (X): daily minimum temperature
X = df[["temperature_2m_min"]]

# Target (y): daily maximum temperature
y = df["temperature_2m_max"]

# Split the data: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Print the slope
print("Task 4: Baseline Model")
print("Slope:", model.coef_[0])

# Calculate RMSE and R²
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("Test RMSE:", rmse)
print("Test R²:", r2)

#The test RMSE is approximately 3.26°C, meaning the model's
# prediction errors are typically around 3.26°C in size.
# The test R² of 0.876 indicates that the model explains 
# 87.6% of the variation in daily high temperatures.


#Task 5: Full Model

# Four features to predict the daily maximum temperature
feature_cols = [
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
    "is_summer",
]

X = df[feature_cols].values
y = df["temperature_2m_max"].values

# Split the data into 80% training and 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Evaluate the model
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

print("Task 5: Full Model")
print(f"Train R²: {train_r2:.3f}")
print(f"Test R²:  {test_r2:.3f}")
print(f"Test RMSE: {rmse:.3f}°C")

# Print each feature's coefficient
print("Feature coefficients:")
for name, coef in zip(feature_cols, model.coef_):
    print(f"{name:22s}: {coef:+.3f}")

# Compare the full model with the Task 4 baseline.
baseline_test_r2 = 0.8763974930210267
improvement = test_r2 - baseline_test_r2

print(f"Baseline test R²: {baseline_test_r2:.3f}")
print(f"Full model test R²: {test_r2:.3f}")
print(f"Change in test R²: {improvement:+.3f}")


# The full model's test R² (0.891) is higher than the baseline
# test R² (0.876), an improvement of 0.015.
# Test RMSE decreased from 3.2569°C to 3.055°C, so the full model
# makes more accurate predictions on the test set.
# Daily minimum temperature and is_summer have positive coefficients,
# meaning higher values increase the predicted daily high when other
# features are constant.
# Precipitation has a negative coefficient, meaning more precipitation
# decreases the predicted high when other features are constant.
# Wind speed has a small positive coefficient, which is surprising,
# but its effect is weak.
# Train R² (0.907) is slightly higher than test R² (0.891).
# The gap is small (0.016), suggesting the model generalizes reasonably
# well to the held-out test data, with no obvious sign of severe overfitting.


# Task 6: Evaluate and Summarize

# Create a predicted vs actual plot for the full model on the test set
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_test_pred, alpha=0.7)

# Add diagonal reference line for perfect predictions
min_value = min(y_test.min(), y_test_pred.min())
max_value = max(y_test.max(), y_test_pred.max())
plt.plot(
    [min_value, max_value],
    [min_value, max_value],
    linestyle="--",
    color="red"
)

plt.title("Predicted vs Actual (Full Model)")
plt.xlabel("Actual Daily High Temperature (°C)")
plt.ylabel("Predicted Daily High Temperature (°C)")
plt.tight_layout()
plt.savefig(output_dir / "predicted_vs_actual_high.png", dpi=150)
plt.show()
plt.close()

#The model appears to struggle more with predictions in the mid-to-high
#temperature range (approximately 15–35°C), where the errors seem larger.

# Dataset size: 365 days; test set: 73 days (20% of the dataset).
# The full model's test RMSE is approximately 3.055°C, meaning
# prediction errors are typically around 3°C in size.
# The test R² is approximately 0.891, meaning the model explains
# about 89.1% of the variation in daily high temperatures.

# Daily minimum temperature has the largest coefficient (+0.951),
# so higher minimum temperatures increase the predicted daily high
# when the other features are held constant.

# One surprising result is that wind speed has a small positive
# coefficient (+0.043), although its correlation with daily high
# temperature is weak.


