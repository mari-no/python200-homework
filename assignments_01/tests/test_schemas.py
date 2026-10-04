# Task 5: The Test Suite
#
# A valid response validates, and hourly.time has 168 entries. 
# Load the real JSON file for this one.
# A latitude of 200.0 raises ValidationError.
# Mismatched list lengths raise ValidationError. Build a small hand-written dict for this -- three or four entries is plenty, and one list one element short.
# A null inside temperature_2m raises ValidationError.



from pathlib import Path
import pytest
from pydantic import ValidationError
from weatherkit.schemas import WeatherResponse


def test_valid_response_168_entries():

    # path works regardless of the directory pytest is run from, 
    # plain relative path is unreliable because it depends on the current
    #working directory

    path = Path(__file__).parent.parent/"weather_raw.json"
    response = WeatherResponse.model_validate_json(path.read_text())

    assert len(response.hourly.time) == 168


def test_latitude_200_enties_negative():
    test_data = {
        "latitude":200,
        "longitude":10.0,
        "timezone": "CST",
        "elevation": 32.0,
        "hourly":{
            "time": ["2026-09-29T12:20"],
            "temperature_2m":[15.0],
            "precipitation":[0.8],
        }
    }
    with pytest.raises(ValidationError):
        WeatherResponse.model_validate(test_data)


def test_mismatched_lists_length_negative():
    test_data = {
            "latitude":20.9,
            "longitude":10.0,
            "timezone": "CST",
            "elevation": 32.0,
            "hourly":{
                "time": ["2026-09-29T12:20", "2026-09-29T11:20", "2026-09-29T13:20"],
                "temperature_2m":[15.0, 27.0],
                "precipitation":[0.8, 0, 0.3],
            }
        }
    with pytest.raises(ValidationError):
        WeatherResponse.model_validate(test_data)

def test_null_temperature_negative():
    test_data = {
                "latitude":20.0,
                "longitude":10.0,
                "timezone": "CST",
                "elevation": 32.0,
                "hourly":{
                    "time": ["2026-09-29T12:20", "2026-09-29T11:20", "2026-09-29T13:20"],
                    "temperature_2m":[15.0, 27.0, None],
                    "precipitation":[0.8, 0, 0.3],
                }
            }
    with pytest.raises(ValidationError):
        WeatherResponse.model_validate(test_data)
    
    ### To check if the tests work, def same_length_lists(self) validator
    #was deliberately commented out, and after that test_mismatched_lists_length_negative FAILED :
#     # marinam@macbookair assignments_01 % pytest tests/test_schemas.py -v
# ============================= test session starts ==============================
# platform darwin -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0 -- /Users/marinam/python200-homework/.venv/bin/python
# cachedir: .pytest_cache
# rootdir: /Users/marinam/python200-homework/assignments_01
# collected 4 items                                                              

# tests/test_schemas.py::test_valid_response_168_entries PASSED            [ 25%]
# tests/test_schemas.py::test_latitude_200_enties_negative PASSED          [ 50%]
# tests/test_schemas.py::test_mismatched_lists_length_negative FAILED      [ 75%]
# tests/test_schemas.py::test_null_temperature_negative PASSED             [100%]

# =================================== FAILURES ===================================
# ____________________ test_mismatched_lists_length_negative _____________________

#     def test_mismatched_lists_length_negative():
#         test_data = {
#                 "latitude":20.9,
#                 "longitude":10.0,
#                 "timezone": "CST",
#                 "elevation": 32.0,
#                 "hourly":{
#                     "time": ["2026-09-29T12:20", "2026-09-29T11:20", "2026-09-29T13:20"],
#                     "temperature_2m":[15.0, 27.0],
#                     "precipitation":[0.8, 0, 0.3],
#                 }
#             }
# >       with pytest.raises(ValidationError):
#              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# E       Failed: DID NOT RAISE ValidationError

# tests/test_schemas.py:60: Failed
# =========================== short test summary info ============================
# FAILED tests/test_schemas.py::test_mismatched_lists_length_negative - Failed: DID NOT RAISE ValidationError
# ========================= 1 failed, 3 passed in 0.43s ==========================