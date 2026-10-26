## Task 4: The Test Suite
import joblib
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from weather_model import WeatherClassifier, Prediction


@pytest.fixture

def model_path(tmp_path):
    """Create and save a tiny model for testing."""

    X = pd.DataFrame(
        [
            [22, 14, 0, 8],
            [24, 16, 0, 10],
            [20, 12, 0.2, 12],
            [2, -4, 12, 40],
            [5, 0, 8, 35],
            [8, 2, 6, 32],
        ],
        columns=WeatherClassifier.FEATURES,
    )

    # 1 means good for running; 0 means skip.
    y = [1, 1, 1, 0, 0, 0]
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000)),
    ])
    pipe.fit(X, y)
   

    model_path = tmp_path / "test_model.pkl"
    joblib.dump(pipe, model_path)

    return model_path
    
@pytest.fixture
def classifier(model_path):
    """A WeatherClassifier loaded from the saved tiny model."""
    return WeatherClassifier(model_path)
    

@pytest.mark.parametrize(
    "day, expected_label",
    [
        (
            {
                "temperature_2m_max": 23,
                "temperature_2m_min": 14,
                "precipitation_sum": 0,
                "wind_speed_10m_max": 8,
            },
            "good",
        ),
        (
            {
                "temperature_2m_max": 4,
                "temperature_2m_min": -2,
                "precipitation_sum": 10,
                "wind_speed_10m_max": 38,
            },
            "skip",
        ),
    ],
)
#     A clearly good day is labeled "good".
# A clearly bad day  is labeled "skip".
def test_good_and_bad_days(classifier, day, expected_label):
    """Check that good weather is labeled good and bad weather skip."""

    # Mutation check: the good-day case catches a classifier
    # that incorrectly labels every day as "skip".
    result = classifier.predict([day])

    assert result[0].label == expected_label


#The returned probability is between 0 and 1.
def test_probability_is_between_zero_and_one(classifier):
    """The returned probability must be between 0 and 1."""

    day = {
        "temperature_2m_max": 23,
        "temperature_2m_min": 14,
        "precipitation_sum": 0,
        "wind_speed_10m_max": 8,
    }

    result = classifier.predict([day])

    assert 0.0 <= result[0].probability <= 1.0

#Passing three days returns three Prediction objects, in order
def test_three_days_return_predictions_in_order(classifier):
    """Return one Prediction object for each input day, in order."""

    days = [
        {
            "temperature_2m_max": 23,
            "temperature_2m_min": 14,
            "precipitation_sum": 0,
            "wind_speed_10m_max": 8,
        },
        {
            "temperature_2m_max": 4,
            "temperature_2m_min": -2,
            "precipitation_sum": 10,
            "wind_speed_10m_max": 38,
        },
        {
            "temperature_2m_max": 22,
            "temperature_2m_min": 13,
            "precipitation_sum": 0,
            "wind_speed_10m_max": 9,
        },
    ]

    result = classifier.predict(days)

    assert len(result) == 3
    assert all(isinstance(item, Prediction) for item in result)
    assert [item.label for item in result] == ["good", "skip", "good"]

#Passing an empty list returns an empty list.
def test_empty_list_returns_empty_list(classifier):
    """An empty input produces an empty result."""

    assert classifier.predict([]) == []


#A day missing a required feature raises ValueError
def test_missing_feature_raises_value_error(classifier):
    """A day missing a required feature raises ValueError."""

    day = {
        "temperature_2m_max": 23,
        # temperature_2m_min is intentionally missing
        "precipitation_sum": 0,
        "wind_speed_10m_max": 8,
    }

    with pytest.raises(ValueError, match="temperature"):
        classifier.predict([day])

#Constructing a WeatherClassifier with a path to a missing file raises FileNotFoundError 

def test_missing_model_file_raises_file_not_found_error(tmp_path):
    """A nonexistent model file raises FileNotFoundError."""

    missing_path = tmp_path / "missing_model.pkl"

    with pytest.raises(FileNotFoundError, match="Model file not found"):
        WeatherClassifier(missing_path)


## After change in classifier.py from skip to skipppp intentionally,
# 2 tests filed:
# =================================== short test summary info ===================================
# FAILED tests/test_classifier.py::test_good_and_bad_days[day1-skip] - AssertionError: assert 'skipppp' == 'skip'
# FAILED tests/test_classifier.py::test_three_days_return_predictions_in_order - AssertionError: assert ['good', 'skipppp', 'good'] == ['good', 'skip', 'good']
# ================================= 2 failed, 5 passed in 2.26s ======