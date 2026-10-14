#Part 1: Warmup Exercises


#The scikit-learn API
#scikit-learn Question 1

import numpy as np
from sklearn.linear_model import LinearRegression

temp_min = np.array([1, 4, 8, 12, 16, 20]).reshape(-1, 1)
temp_max = np.array([8, 10, 15, 18, 23, 27])

#Create the model

model = LinearRegression()

#Fit the model to the data

model.fit(temp_min, temp_max)

#  Predict the high for a day with a low of 6 degrees 
# and a day with a low of 18 degrees
predictions = model.predict(np.array([6,18]).reshape(-1,1))
#Print the slope (model.coef_[0]), 
# the intercept (model.intercept_),
#  and the two predictions.

print("Slope:", model.coef_[0])
print("Intercept:", model.intercept_)

print("Predicted high for a low of 6 degrees: ", predictions[0])
print("Predicted high for a low of 18 degrees: ", predictions[1])


#scikit-learn Question 2
#scikit-learn requires the feature array X to be 2D even when you only have one feature.
#1D array:
x = np.array([10, 20, 30, 40, 50])

print("Original shape:", x.shape)
#convert it to a 2D array
x_reshaped= x.reshape(-1, 1)
print("Reshaped:", x_reshaped.shape) 

# why scikit-learn needs X to be 2D?
#because scikit-learn treats data as rows(number of observations, samples)
#and columns(features)


#Linear Regression
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import os
os.makedirs("outputs", exist_ok=True)
rng = np.random.default_rng(42)
num_days  = 120
temp_min  = rng.uniform(-5, 22, num_days)
is_rainy  = rng.integers(0, 2, num_days).astype(float)
temp_max  = 1.0 * temp_min + 6 - 4 * is_rainy + rng.normal(0, 2, num_days)

#Linear Regression Question 1
# Plot daily low vs high temperature, colored by rain status 
plt.scatter(temp_min, temp_max, c=is_rainy, cmap="coolwarm") 
plt.title("Daily High vs Low")
plt.xlabel("Minimum Temperature") 
plt.ylabel("Maximum Temperature") 
plt.savefig("outputs/high_vs_low.png") 
plt.show()
# Observation: Two visible groups appear because rainy days tend
#  to have lower maximum temperatures than dry days at
#  similar minimum temperatures.  This suggests that is_rainy
#  affects the relationship between low and high temperatures.


#Linear Regression Question 2
# Use temp_min as the only feature 
X = temp_min.reshape(-1, 1) 
# Use temp_max as the target 
y = temp_max 
# Split into training and test sets (80/20) 
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=42 )
 # Print the shapes of all four arrays 
print("X_train shape:", X_train.shape) 
print("X_test shape:", X_test.shape) 
print("y_train shape:", y_train.shape) 
print("y_test shape:", y_test.shape)

#Linear Regression Question 3

# Create and fit the model using the training data
model = LinearRegression()
model.fit(X_train, y_train)

# Print the slope and intercept
print("Slope:", model.coef_[0])
print("Intercept:", model.intercept_)

# Predict high temperatures using the test data
y_pred = model.predict(X_test)

# Calculate RMSE and R²
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = model.score(X_test, y_test)

print("RMSE:", rmse)
print("R² on test set:", r2)

# Interpretation: For each 1-degree increase in daily low temperature,
# the predicted daily high increases by approximately the slope amount 0.944


# Linear Regression Question 4

# Added is_rainy as a second feature
X_full = np.column_stack([temp_min, is_rainy])

# Split the data into training and test sets
X_full_train, X_full_test, y_full_train, y_full_test = train_test_split(
    X_full, temp_max, test_size=0.2, random_state=42
)

# Create and fit a new model
model_full = LinearRegression()
model_full.fit(X_full_train, y_full_train)

# Calculate test R²
r2_full = model_full.score(X_full_test, y_full_test)

print("R² without rain:", r2)
print("R² with rain:", r2_full)

# Print both coefficients
print("temp_min coefficient:", model_full.coef_[0])

print("is_rainy coefficient:", model_full.coef_[1])


# When the minimum temperature is the same, the model predicts that 
# a rainy day will have a maximum temperature about 2.919 degrees lower 
# than a dry day because is_rainy changes from 0 (dry) to 1 (rainy), and its coefficient is -2.919


# Linear Regression Question 5

# Predict using the two-feature model from Question 4
y_full_pred = model_full.predict(X_full_test)

# Create the predicted vs actual plot
plt.figure(figsize=(8, 6))
plt.scatter(y_full_pred, y_full_test)

# Add the diagonal reference line (perfect predictions)
min_val = min(y_full_pred.min(), y_full_test.min())
max_val = max(y_full_pred.max(), y_full_test.max())
plt.plot([min_val, max_val], [min_val, max_val], "r--")

plt.title("Predicted vs Actual")
plt.xlabel("Predicted High Temperature")
plt.ylabel("Actual High Temperature")

plt.savefig("outputs/predicted_vs_actual_warmup.png")
plt.show()

# Interpretation:
# Points above the diagonal represent underpredictions:
# actual temperatures are higher than predicted.
# Points below the diagonal represent overpredictions:
# actual temperatures are lower than predicted.
