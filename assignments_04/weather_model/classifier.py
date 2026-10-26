from dataclasses import dataclass
from pathlib import Path
import joblib
import pandas as pd

## Task 1: The Prediction Dataclass

# In weather_model/classifier.py, write a dataclass 
# Prediction with two type-hinted fields:
# label (str) -- either "good" or "skip"
# probability (float) -- the probability, from 0 to 1, 
# that the day is good for running
# Give it a docstring.

@dataclass

class Prediction:
    """ Predicts if a day is good for running"""
    label: str 
    probability: float


## Task 2: The WeatherClassifier Class

class WeatherClassifier:
    """Loads a trained model and predicts running weather."""


    FEATURES = [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "wind_speed_10m_max",
    ]

    def __init__(self, model_path:str)->None:
        """ Loads a trained model from a .pkl file.
            Raises: FileNotFoundError if the model file does not exist."""
        path = Path(model_path)

        if not path.is_file():
            raise FileNotFoundError(
                f"Model file not found: {path}"
            )

        self.model = joblib.load(path)

    def predict(
        self, days: list[dict[str, float]]
    ) -> list[Prediction]:
        """ Predicts whether each day is good for running.
            Raises: ValueError if any required feature is missing.
        """
        if not days:
            return []

        for i, day in enumerate(days):
            missing = []
            for feature in self.FEATURES:
                if feature not in day:
                    missing.append(feature)
            if missing:
                raise ValueError(
                    f"Day {i} is missing features: {', '.join(missing)}"
                        )

        X = pd.DataFrame(days, columns=self.FEATURES)

        labels = self.model.predict(X)
        probabilities = self.model.predict_proba(X)[:, 1]
        predictions = []

        for label, probability in zip(labels, probabilities):
            if label == 1:
                label_text = "good"
            else:
                label_text = "skip"

            prediction = Prediction(
                label=label_text,
                probability=float(probability)
            )

            predictions.append(prediction)

        return predictions

        