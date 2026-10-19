import requests
import pandas as pd

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
#Austin, Texas
response = requests.get(url, params=params)
response.raise_for_status()
df = pd.DataFrame(response.json()["daily"])
df["date"] = pd.to_datetime(df["time"])
df = df.drop("time", axis=1)

print("Dataset shape:", df.shape)
print("First 5 rows:",df.head())

## Task 2: Engineer the Label
#Create a good_for_running column that is 1 when a day is good
#  and 0 otherwise. A day is good when the high is between 7 
# and 26 degrees, the low is at least 0, precipitation is under
#  3 mm, and the maximum wind is under 30 km/h. 

df["good_for_running"] = (
    (df["temperature_2m_max"] >= 7) &
    (df["temperature_2m_max"] <= 26) &
    (df["temperature_2m_min"] >= 0) &
    (df["precipitation_sum"] < 3) &
    (df["wind_speed_10m_max"] < 30)
).astype(int)

good_days = (df["good_for_running"] == 1).sum()
skip_days = (df["good_for_running"] == 0).sum()
good_fraction = good_days / len(df)

print("Good days:", good_days)
print("Skip days:", skip_days)
print(f"Fraction of good days: {good_fraction:.2%}")
# #Class balance:
# 109 good days and 256 skip days.
# About 30% of days are good for running. 
# This seems reasonable for Austin, where summer heat and occasional rain or strong winds can make running
# less comfortable under our chosen thresholds.
# The classes are somewhat imbalanced, so accuracy alone may be misleading.
# I will pay particular attention to precision, recall, F1-score, and the
# confusion matrix to evaluate how well the model identifies good running days.

## Task 3: Build and Evaluate a KNN Classifier


from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

features = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
]

X = df[features]
y = df["good_for_running"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

knn_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier())
])

# Try at least five values of k using 5-fold cross-validation.
param_grid = {
    "knn__n_neighbors": [3, 5, 7, 9, 11, 15, 21]
}

knn_search = GridSearchCV(
    knn_pipeline,
    param_grid,
    cv=5,
    scoring="f1",
    n_jobs=-1
)

knn_search.fit(X_train, y_train)

best_knn = knn_search.best_estimator_
knn_predictions = best_knn.predict(X_test)

knn_accuracy = accuracy_score(y_test, knn_predictions)

print("Best k:", knn_search.best_params_["knn__n_neighbors"])
print("Best cross-validation F1:", round(knn_search.best_score_, 4))
print("KNN test accuracy:", round(knn_accuracy, 4))
print(classification_report(
    y_test,
    knn_predictions,
    target_names=["Skip", "Good for running"],
    zero_division=0
))

## Task 4: Build and Evaluate a Logistic Regression Classifier
#Build a Pipeline of StandardScaler and LogisticRegression(max_iter=1000).
#  Fit it and print its test accuracy, precision, recall, F1, and classification report.

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score

logistic_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("logistic", LogisticRegression(max_iter=1000))
])

logistic_pipeline.fit(X_train, y_train)
logistic_predictions = logistic_pipeline.predict(X_test)

logistic_accuracy = accuracy_score(y_test, logistic_predictions)
logistic_precision = precision_score(
    y_test, logistic_predictions, zero_division=0
)
logistic_recall = recall_score(
    y_test, logistic_predictions, zero_division=0
)
logistic_f1 = f1_score(
    y_test, logistic_predictions, zero_division=0
)

print("Logistic regression test accuracy:", round(logistic_accuracy, 4))
print("Precision:", round(logistic_precision, 4))
print("Recall:", round(logistic_recall, 4))
print("F1:", round(logistic_f1, 4))

print(classification_report(
    y_test,
    logistic_predictions,
    target_names=["Skip", "Good for running"],
    zero_division=0
))

# Print coefficients from the fitted logistic regression model.
logistic_model = logistic_pipeline.named_steps["logistic"]

for feature, coefficient in zip(features, logistic_model.coef_[0]):
    print(f"{feature}: {coefficient:.4f}")


# Negative coefficients push predictions toward "skip".
#temperature_2m_max: -0.8280
# temperature_2m_min: -1.7494
# precipitation_sum: -3.0324
# wind_speed_10m_max: -0.8347
# temperature_2m_min: -1.7494 and precipitation_sum push most strongly toward "skip".

## Task 5: Compare and Choose
# Logistic Regression had higher test accuracy (93.15%) than KNN (91.78%).
# Logistic Regression also had a slightly higher F1-score for good running
# days (0.8718 vs. 0.86).

# For a running app, I would prioritize precision if the main goal is to
# avoid recommending bad weather. A false positive means the app
# recommends running on a day that does not meet our weather criteria.
# A false negative means the app misses a good running day. If encouraging
# users to run on as many suitable days as possible is more important,
# recall would deserve more weight.

# I would deploy Logistic Regression because it achieved higher accuracy
# and F1-score on the test set. It also supports predict_proba() to estimate the probability
# of a good running day. Its precision was 1.0 on this test set, although
# this does not guarantee perfect precision on future data.
# KNN achieved higher recall (0.86 vs. 0.7727), so I would consider it
# if identifying more good running days became the main priority.
#Logistic regression's probabilities, interpretability, and small size are real advantages when a model has to run in a pipeline

## Task 6: Save the Model

# Save Logistic Regression 
import os
import json
import sys
import sklearn
import joblib
from pathlib import Path
os.makedirs("models", exist_ok=True)
# Choose Logistic Regression explicitly
chosen_model = logistic_pipeline
chosen_name = "Logistic Regression"
chosen_accuracy = logistic_accuracy
chosen_f1 = logistic_f1

output_dir = Path("models")

model_path = output_dir / "weather_classifier.pkl"
metadata_path = output_dir / "weather_classifier_metadata.json"

# Save the fitted pipeline, including StandardScaler
joblib.dump(chosen_model, model_path)

metadata = {
    "python_version": sys.version,
    "scikit_learn_version": sklearn.__version__,
    "joblib_version": joblib.__version__,
    "model_name": chosen_name,
    "feature_names": features,
    "label_name": "good_for_running",
    "label_rule": {
        "temperature_2m_max": "7 <= value <= 26 degrees Celsius",
        "temperature_2m_min": "value >= 0 degrees Celsius",
        "precipitation_sum": "value < 3 mm",
        "wind_speed_10m_max": "value < 30 km/h"
    },
    "city": "Austin, Texas, USA",
    "test_accuracy": float(chosen_accuracy),
    "test_f1": float(chosen_f1),
    "random_state": 42,
    "test_size": 0.2
}

with open(metadata_path, "w", encoding="utf-8") as file:
    json.dump(metadata, file, indent=4)

print(f"Model saved to: {model_path}")
print(f"Metadata saved to: {metadata_path}")
print(f"Chosen model: {chosen_name}")
print("Both files were written successfully.")
