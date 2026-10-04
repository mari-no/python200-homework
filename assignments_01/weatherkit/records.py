### Task 3: Inside the Boundary -- weatherkit/records.py

from dataclasses import dataclass
from weatherkit.schemas import WeatherResponse

@dataclass
class HourlyReading:
    """Represents hourly weather timestamp, temperature, precipitation"""
    timestamp: str
    temperature_c: float
    precipitation_mm: float
def to_readings(response: WeatherResponse) -> list[HourlyReading]:
    """
    Converts the columnar hourly block into one HourlyReading per hour, preserving order. 
    Args: response: validated WeatherResponse with hourly weather data
    Returns: list of HourlyReading objects in the same order as a source data
    """

    readings = []
    for i in range(len(response.hourly.time)): 
        reading = HourlyReading( 
            timestamp=response.hourly.time[i],
            temperature_c=response.hourly.temperature_2m[i],
            precipitation_mm=response.hourly.precipitation[i], )
        readings.append(reading)
    return readings 
### why is HourlyReading a dataclass rather than a Pydantic model, 
# when WeatherResponse is a Pydantic model? Be specific. 
# A good answer identifies where the boundary is.

# WeatherResponse is a Pydantic model because it sits at the boundary
#  where external API data enters our program and needs validation. 
# HourlyReading is  a dataclass because it is an internal application
#  object created from data that has already been validated

