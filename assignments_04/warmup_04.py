# Part 1: Warmup Exercises
# Pytest will not discover warmup_04.py on its own,
#  because the filename does not match test_*.py.
#  Run its tests explicitly with:
# pytest warmup_04.py -v
## Warmup Question 1
# Write a class ModelInfo that reads a JSON file
#  once in __init__ and stores its contents. 

import pandas as pd
import json
from dataclasses import dataclass
class ModelInfo():
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def feature_count(self) -> int:
        return len(self.data["features"])

# Create a small JSON file with a "features" list
sample_data = {
    "features": ["temp_max", "temp_min", "humidity", "clouds"]
}

with open("model.json", "w", encoding="utf-8") as file:
    json.dump(sample_data, file, indent=4)

# Load the file once when creating the object.
model = ModelInfo("model.json")

# Print the number of features.
print(model.feature_count())  # Output: 4

#Why is loading the file in __init__ better than loading
#  it inside feature_count() if the method is called many times?
# Loading the file in __init__ means the JSON file is read only once when 
# the ModelInfo object is created. The feature_count() method can then access 
# the data already stored in self.data without reopening and rereading the file
#  every time it is called.


# Warmup Question 2

# Create two DayForecast objects and print each summary.
@dataclass
class DayForecast:
    date: str
    high_c: float
    will_rain: bool

    def summary(self) -> str:
        if self.will_rain == True:
            return f"{self.date}: high {self.high_c}, rain expected"
        else: 
            return f"{self.date}: high {self.high_c}, no rain expected"

# Two DayForecast objects
forecast1 = DayForecast("2026-10-26", 28.0, True)
forecast2 = DayForecast("2026-10-27", 30.0, False)
print(forecast1.summary())
print(forecast2.summary())

#The @dataclass decorator automatically generated the __init__() method, 
# so I didn't have to write the constructor and assign each attribute 
# manually.

## Warmup Question 3
# Write a function parse_temperature(text: str) -> float that converts
#  a string like "24.1" to a float, and raises a ValueError with a message
#  containing the word "temperature" when the text is not a number.


import pytest

def parse_temperature(text: str) -> float:
    try:
        return float(text)
    except ValueError:
        raise ValueError(
            f"Invalid temperature: '{text}' is not a number"
        )


def test_parse_temperature_valid():
    assert parse_temperature("24.1") == pytest.approx(24.1)


def test_parse_temperature_bad_input_raises():
    with pytest.raises(ValueError, match="temperature"):
        parse_temperature("hot")
# Test with simply pytest.raises(ValueError) without match would 
# fail to catch wrong error message.
#It could catch any other VallueError exception and pass,
#  without checking this one we're expecting to see.