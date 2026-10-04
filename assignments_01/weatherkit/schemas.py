##Task 2: The Boundary -- weatherkit/schemas.py
# Write Pydantic models describing the API response.

from pydantic import BaseModel, Field, model_validator

class HourlyBlock(BaseModel):
    """ Provides hourly temperature and precipitation"""
    time: list[str]
    temperature_2m: list[float]
    precipitation: list[float]

    @model_validator(mode="after")

    def same_length_lists(self):
        if not(
            len(self.time)==len(self.precipitation)==len(self.temperature_2m)
        ):
            raise ValueError ("The three lists are not all the same length, response is corrupt.")
        return self
class WeatherResponse(BaseModel):

    """Top-level metadata: latitude, longitude, elevation"""
    latitude: float = Field (ge = -90, le=90)
    longitude: float = Field (ge = -180, le=180)
    timezone: str
    elevation: float
    hourly: HourlyBlock

