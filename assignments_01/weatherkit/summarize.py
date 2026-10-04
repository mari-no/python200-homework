### Task 4: The Aggregation -- weatherkit/summarize.py


from dataclasses import dataclass
from weatherkit.records import HourlyReading
@dataclass
class DailySummary:
    """Summary of weather data observations for one day"""
    date: str
    temp_max: float
    temp_min: float
    precipitation_sum: float
    hours_observed: int
    
    def temp_range(self)->float:

        """Returns the difference between the max and min temperature"""
        return self.temp_max-self.temp_min


class DailyAggregator:
    def __init__(self, min_hours: int = 24):
        self.min_hours = min_hours

    def summarize(self, readings: list[HourlyReading])->list[DailySummary]:
        """Groups readings by calendar date,calculates max and min temperature and a total precipitation"""
#Create dict where date will be the key, 
# and value will be the list of readings for that date
        grouped_by_date={}

        for reading in readings:

#The date is stored
# in first 10 characters of a timestamp, so we slice a string
            date_day = reading.timestamp[:10]

#If date is not already in the dict, create an empty list of values for it
            if date_day not in grouped_by_date:
                grouped_by_date[date_day]=[]
            grouped_by_date[date_day].append(reading)        

# Summarize data by date

        summarized_data = []

        for date_day, day_readings in grouped_by_date.items():
            if len(day_readings)<self.min_hours:
                continue
            temperatures = [
                reading.temperature_c for reading in day_readings
            ]
            precipitation = [
                reading.precipitation_mm for reading in day_readings
            ]

            summarized_data.append(
                DailySummary(
                    date = date_day,
                    temp_max = max(temperatures),
                    temp_min = min(temperatures),
                    precipitation_sum = sum(precipitation),
                    hours_observed = len(day_readings),
                )
                )
        summarized_data.sort(key=lambda summary: summary.date)
        return summarized_data
    def incomplete_days(self, readings: list[HourlyReading]) -> list[str]:
        """Returns dates that were dropped because of having less readings than needed"""

        grouped_by_date = {}

        for reading in readings:
            date = reading.timestamp[:10]
            if date not in grouped_by_date:
                grouped_by_date[date] = []

            grouped_by_date[date].append(reading)


            
        incomplete = []

        for date, day_readings in grouped_by_date.items():
            if len(day_readings)<self.min_hours:
                incomplete.append(date)

        incomplete.sort()

        return incomplete


