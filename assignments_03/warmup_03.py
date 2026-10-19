import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, ConfusionMatrixDisplay, classification_report,
)
import joblib

df = pd.read_csv("/Users/marinam/python200-homework/assignments_03/weather_classification.csv")
numeric = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"]
X = df[numeric]
y = df["good_for_running"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Preprocessing
## Preprocessing Question 1

# Why you fit the scaler on X_train only:
#To prevent data leakage, because using the test data to calculate 
# scaling statistics would allow information from the test set to 
# influence the training process.

scaler = StandardScaler()

# Fit on training data only
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Mean of scaled training data:")
print(pd.Series(X_train_scaled.mean(axis=0), index=numeric))

## Preprocessing Question 2

# Select the season column
X_season = df[["season"]]

# Create the encoder
encoder = OneHotEncoder(sparse_output=False)

# Fit the encoder and transform the data
X_season_encoded = encoder.fit_transform(X_season)
print("Encoded season array shape:")
print(X_season_encoded.shape)
print("Encoded feature names:")
print(encoder.get_feature_names_out(["season"]))

# One column becomes four columns because the dataset
# contains four seasons, and one-hot encoding creates
# one binary column for each unique category.

## Preprocessing Question 3

# Define numeric and categorical columns
numeric = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
]
categorical = ["season"]

# Include both numeric and categorical columns in X
X = df[numeric + categorical]
y = df["good_for_running"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Create a ColumnTransformer.
# StandardScaler scales the numeric columns. 
# OneHotEncoder converts season into binary columns.
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric),
        ("cat", OneHotEncoder(sparse_output=False), categorical),
    ]
)

# Create a Pipeline that preprocesses the data and trains Logistic Regression
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression()),
    ]
)

# Fit the entire pipeline on the training data
pipeline.fit(X_train, y_train)

# Predict labels for the test data
y_pred = pipeline.predict(X_test)

print("Test accuracy:", accuracy_score(y_test, y_pred))

# The pipeline automatically fits the preprocessing steps on
# the training data, applies the same fitted transformations to the test
# data, and passes the transformed features to Logistic Regression.
# It helps to avoid manual scaling and encoding each dataset.


# KNN
## KNN Question 1
#Build a Pipeline of StandardScaler and KNeighborsClassifier(n_neighbors=5). 
# Fit it on the training data and print the test accuracy and the full classification 
# report

# Build a pipeline: scale the data, then train the KNN classifier

# Four numeric features
numeric = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
]

X = df[numeric]
y = df["good_for_running"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

knn_pipeline = Pipeline(
    steps=[
        ("scaler", StandardScaler()),
        ("classifier", KNeighborsClassifier(n_neighbors=5)),
    ]
)

# Train the pipeline using the training data
knn_pipeline.fit(X_train, y_train)

# Predict the target values for the test data
y_pred = knn_pipeline.predict(X_test)

print("KNN Test Accuracy:", accuracy_score(y_test, y_pred))
print("Full KNN Classification Report:")
print(classification_report(y_test, y_pred))


##KNN Question 2
#Loop over k values [1, 3, 5, 7, 9, 11, 15, 21]. For each,
#  build the scaled pipeline and compute the mean 5-fold 
# cross-validation accuracy on the training data. 
# Print each k with its mean CV score. 

k_values = [1, 3, 5, 7, 9, 11, 15, 21]

for k in k_values:
    # Build a pipeline for each k
    knn_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", KNeighborsClassifier(n_neighbors=k)),
    ])

    # Perform 5-fold cross-validation on the training data
    cv_scores = cross_val_score(
        knn_pipeline,
        X_train,
        y_train,
        cv=5,
        scoring="accuracy",
    )
    print(f"k = {k:2d}, Mean cross-validation accuracy = {cv_scores.mean():.4f}")

# I would choose k=11 because it achieves the highest mean
# 5-fold cross-validation accuracy (94.17%). 
# I also chose not to high k, because too high k can make a model to miss 
# important patterns because it takes too many neighbors that may be not similar 
# to the example we're trying to classify

## KNN Question 3
#Fit KNN once without scaling (on raw X_train)
#  and once with scaling, both using n_neighbors=5.
#  Print both test accuracies. 

# Create KNN without scaling
knn_raw = KNeighborsClassifier(n_neighbors=5)

# Fit without scaling
knn_raw.fit(X_train, y_train)

# Predict and calculate test accuracy
y_pred_raw = knn_raw.predict(X_test)
accuracy_raw = accuracy_score(y_test, y_pred_raw)

print("KNN accuracy without scaling:", accuracy_raw)

# Train KNN with scaling on the training data
knn_pipeline.fit(X_train, y_train)

# Predict and calculate test accuracy
y_pred_scaled = knn_pipeline.predict(X_test)
accuracy_scaled = accuracy_score(y_test, y_pred_scaled)

print("KNN accuracy with scaling:", accuracy_scaled)

# did scaling help, and why would scaling matter 
# for a distance-based model?

#Scaling improved test accuracy from 92.50% to 93.33%.
#KNN is a distance-based model, and features with larger numerical
# ranges can dominate distance calculations if the data is not scaled.
# StandardScaler puts numeric features on comparable scales, allowing
# KNN to consider all features more appropriately


# Logistic Regression
## Logistic Regression Question 1
# Build a pipeline: scale the features, then train Logistic Regression
logistic_reg_pipeline = Pipeline(
    steps=[
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=1000)),
    ]
)

# Train the pipeline
logistic_reg_pipeline.fit(X_train, y_train)

# Predict the test labels
y_pred = logistic_reg_pipeline.predict(X_test)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label=1)
recall = recall_score(y_test, y_pred, pos_label=1)
f1 = f1_score(y_test, y_pred, pos_label=1)

print("Logistic Regression Test Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)

## Logistic Regression Question 2
#Print each feature name alongside its coefficient from the fitted logistic regression (use pipeline.named_steps["..."].coef_[0]). 



# Get the feature names (the four numeric features)
feature_names = X_train.columns

# Get the coefficients from the fitted Logistic Regression model
coefficients = logistic_reg_pipeline.named_steps["classifier"].coef_[0]

# Print each feature and its coefficient
for feature, coefficient in zip(feature_names, coefficients):
    print(f"{feature}: {coefficient:.4f}")

#  Wind speed has the strongest negative coefficient (-2.4438),
# followed by precipitation (-1.8891). Both push predictions
# toward class 0 (skip), which matches my intuition that windy
# and rainy weather makes running less comfortable.
# Minimum temperature pushes slightly (0.2563) toward class 1 (good), while maximum
# temperature has a small negative effect(-0.1212). 

## Logistic Regression Question 3

# Get probabilities for the first five test days
probabilities = logistic_reg_pipeline.predict_proba(X_test[:5])

# Find the column corresponding to class 1 ("good")
good_index = list(logistic_reg_pipeline.classes_).index(1)

# Print the probability of "good" for each day
for i, probability in enumerate(probabilities):
    print(f"Test day {i + 1}: P(good) = {probability[good_index]:.2f}")

# Test day 2 has a probability of 0.47, which is close to 0.5.
# This means the model is uncertain about whether the day is good
# for running.


#Evaluation
## Evaluation Question 1

# Generate predictions using the fitted Logistic Regression pipeline
y_pred = logistic_reg_pipeline.predict(X_test)

# Build the confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

# Display and save the confusion matrix
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["skip", "good"]
)

disp.plot()
plt.title("Logistic Regression Confusion Matrix")
plt.tight_layout()
plt.savefig("outputs/logreg_confusion_matrix.png")
plt.show()

# Extract false positives and false negatives
tn, fp, fn, tp = cm.ravel()

print("False positives:", fp)
print("False negatives:", fn)

# The model made 9 false positives and 7 false negatives.
# False positives may matter more because the app could recommend
# running when the weather is bad. 


#joblib
## joblib Question 1
import os
import joblib

# Save the entire fitted pipeline
joblib.dump(logistic_reg_pipeline, "models/warmup_model.pkl")

# Load the saved pipeline
loaded = joblib.load("models/warmup_model.pkl")

# Confirm that predictions are identical
assert (loaded.predict(X_test) == logistic_reg_pipeline.predict(X_test)).all()

print("Predictions match.")

# If we saved only the LogisticRegression step without the scaler,
# raw input data would not be scaled before prediction.
# The model would receive values on different scales than those
# used during training, which might produce incorrect predictions.