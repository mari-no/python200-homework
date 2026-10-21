## Task 7: Load and Predict

import json
import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path("models/weather_classifier.pkl")
METADATA_PATH = Path("models/weather_classifier_metadata.json")

# Give a helpful error if the training script has not created the files.
for path in [MODEL_PATH, METADATA_PATH]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}. "
            "Run train_classifier.py first to train and save the model."
        )

# Load the fitted pipeline and its metadata.
model = joblib.load(MODEL_PATH)

with open(METADATA_PATH, "r", encoding="utf-8") as file:
    metadata = json.load(file)

# Print key model metadata.
print("City:", metadata["city"])
print("Features:", metadata["feature_names"])
print("Test accuracy:", metadata["test_accuracy"])
print("Model:", metadata["model_name"])

# Build four hypothetical weather days.
# Values use the same units as the training dataset.
hypothetical_days = pd.DataFrame([
    {
        "temperature_2m_max": 22,
        "temperature_2m_min": 12,
        "precipitation_sum": 0,
        "wind_speed_10m_max": 10,
    },
    {
        "temperature_2m_max": 38,
        "temperature_2m_min": 25,
        "precipitation_sum": 0,
        "wind_speed_10m_max": 15,
    },
    {
        "temperature_2m_max": 27,
        "temperature_2m_min": 16,
        "precipitation_sum": 0,
        "wind_speed_10m_max": 10,
    },
    {
        "temperature_2m_max": 18,
        "temperature_2m_min": 8,
        "precipitation_sum": 4,
        "wind_speed_10m_max": 12,
    },
])

# Use feature names and ordering from the metadata.
features = metadata["feature_names"]
hypothetical_days = hypothetical_days[features]

# Predict labels and probabilities.
predictions = model.predict(hypothetical_days)
probabilities = model.predict_proba(hypothetical_days)

# Find the column corresponding to label 1 (good for running).
good_class_index = list(model.classes_).index(1)
good_probabilities = probabilities[:, good_class_index]

print("Weather predictions:")

for i, (_, day) in enumerate(hypothetical_days.iterrows()):
    label = "Good for running" if predictions[i] == 1 else "Skip"

    print(f"Day {i + 1}:")
    for feature in features:
        print(f"  {feature}: {day[feature]}")

    print(f"  Prediction: {label}")
    print(f"  Probability of good: {good_probabilities[i]:.2%}")



## Task 8: Reflection
#
# 1. Day 3 is my borderline day. The model predicted "Good for running"
#    with a probability of 58.57%. I consider this prediction less
#    confident than Day 1's prediction of 84.58%. If the model predicts
#    a probability of 0.52, I would treat the result as uncertain because
#    it is very close to the 0.50 classification threshold. I could flag
#    the day for additional review or check it against my original
#    weather rules.
#
# 2. If predict.py runs before train_classifier.py, the saved model and
#    metadata files may not exist. Loading the model would fail with a
#    FileNotFoundError. I can make the error more helpful by checking
#    whether both files exist and telling the user to run
#    train_classifier.py first.
#
# 3. In a cloud pipeline, I would replace the hardcoded hypothetical
#    weather days with actual daily weather data from an API or database.
