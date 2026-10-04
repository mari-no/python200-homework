#Task 5: The Test Suite

# 
# to_readings returns one reading per hour, in order (check the first and last timestamps).
# The values in reading i match index i of each input list. This test catches the case where readings are paired with the wrong timestamps.
# Two HourlyReading objects with identical fields compare equal.

from weatherkit.records import HourlyReading, to_readings
from weatherkit.schemas import WeatherResponse

def test_to_readings_returns_one_reading_per_hour():
    test_data = {
                    "latitude":20.0,
                    "longitude":10.0,
                    "timezone": "CST",
                    "elevation": 32.0,
                    "hourly":{
                        "time": ["2026-09-29T10:00","2026-09-29T10:20", "2026-09-29T11:00", "2026-09-29T12:00"],
                        "temperature_2m":[15.0, 18.0, 27.0, 26],
                        "precipitation":[0.8,0.9, 0, 0.3],
                    }
                }
    response = WeatherResponse.model_validate(test_data)

    readings = to_readings(response)

    assert(len(readings)==4)
    assert readings[0].timestamp == "2026-09-29T10:00"
    assert readings[3].timestamp == "2026-09-29T12:00"



def test_readings_values_i_match_each_i_input():
    test_data = {
                    "latitude":20.0,
                    "longitude":10.0,
                    "timezone": "CST",
                    "elevation": 32.0,
                    "hourly":{
                        "time": ["2026-09-29T09:00","2026-09-29T10:00", "2026-09-29T11:00", "2026-09-29T12:00"],
                        "temperature_2m":[15.0, 18.0, 27.0, 26],
                        "precipitation":[0.8,0.9, 0, 0.3],
                    }
                }
    response = WeatherResponse.model_validate(test_data)

    readings = to_readings(response)

    for i, reading in enumerate(readings):
        assert reading.timestamp == response.hourly.time[i]
        assert reading.temperature_c == response.hourly.temperature_2m[i]
        assert reading.precipitation_mm == response.hourly.precipitation[i]


def test_identical_hourly_readings_are_equal():
    reading1 = HourlyReading(timestamp="2026-09-29T09:00",
                            temperature_c=20.0,
                            precipitation_mm = 0.3,
    )
    reading2 = HourlyReading(timestamp="2026-09-29T09:00",
                                temperature_c=20.0,
                                precipitation_mm = 0.3,
        )

    assert reading1 == reading2