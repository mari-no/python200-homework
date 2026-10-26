# Task 5: The Script
# Uses real saved model in models/weather_classifier.pkl



from weather_model import WeatherClassifier


def main():
    """Predict if days are good for running."""

    model_path = "models/weather_classifier.pkl"
    classifier = WeatherClassifier(model_path)

    # Four days: good, bad, and borderline conditions.
    days = [
        {
            "temperature_2m_max": 22,
            "temperature_2m_min": 12,
            "precipitation_sum": 0,
            "wind_speed_10m_max": 10,
        },
        {
            "temperature_2m_max": 3,
            "temperature_2m_min": -4,
            "precipitation_sum": 12,
            "wind_speed_10m_max": 40,
        },
        {
            "temperature_2m_max": 27,
            "temperature_2m_min": 19,
            "precipitation_sum": 0,
            "wind_speed_10m_max": 15,
        },
        {
            "temperature_2m_max": 15,
            "temperature_2m_min": 8,
            "precipitation_sum": 2,
            "wind_speed_10m_max": 25,
        },
    ]

    predictions = classifier.predict(days)

    for i, prediction in enumerate(predictions):
        day = days[i]

        print(
            f"Day {i + 1}: "
            f"high={day['temperature_2m_max']}°C, "
            f"low={day['temperature_2m_min']}°C, "
            f"rain={day['precipitation_sum']} mm, "
            f"wind={day['wind_speed_10m_max']} km/h | "
            f"Prediction: {prediction.label}, "
            f"probability of good: {prediction.probability:.2%}"
        )


if __name__ == "__main__":
   # Without this guard, importing this module would automatically
    # run the entire script instead of allowing its functions
    # to be reused without running the predictions.
    main()
