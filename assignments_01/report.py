## Task 2: The Boundary -- weatherkit/schemas.py
#load weather_raw.json and validate


import json
from weatherkit.schemas import WeatherResponse
from dataclasses import dataclass
from weatherkit.summarize import DailyAggregator
from weatherkit.records import to_readings
import pandas as pd

def main():


#Load weather json
    with open("weather_raw.json","r") as file:
        raw_data = json.load(file)
#Validate raw_data
    weather = WeatherResponse.model_validate(raw_data)

    print(f"Latitude: {weather.latitude}")
    print(f"Timezone: {weather.timezone}")
    print(f"The number of hourly observations: {len(weather.hourly.time)}")


### Task 3: Inside the Boundary -- weatherkit/records.py

#Convert hourly data into HourlyReading 
    readings =to_readings(weather)
   # print(readings)


### Task 4: The Aggregation -- weatherkit/summarize.py
#Aggregate the readings into DailySummary objects


    aggregator = DailyAggregator()

    summaries = aggregator.summarize(readings)

    print(f"Number of summaries: {len(summaries)}")

#Print the table and create df for that 
    df = pd.DataFrame([

        {
            "date": summary.date,
            "temp_max": summary.temp_max,
            "temp_min": summary.temp_min,
            "precipitation_sum": summary.precipitation_sum,
            "temperature_reange": summary.temp_range(),
            "hours_observed": summary.hours_observed,

        }
         for summary in summaries
    ])
   
    print(df.to_string(index=False))


#Find days that were dropped because they had fewer than 24 readings 
    incomplete_days = aggregator.incomplete_days(readings)
    if incomplete_days:

        print()
        print(
            "Incomplete days dropped", incomplete_days
        )
#Without this guard, imoprting report would automativsally 
# run the entire report 
# instead of only allowing its functions to be reused
if __name__ == "__main__":
    main()



#Task 7: Reflection 
# 
# 1. WeatherResponse rejects the entire file if any temperature is null. 
# # I think this is the right behavior when temperature data is critical and
# # the pipeline needs reliable, complete data. For example, if the data is 
# # used for safety decisions or an important weather analysis, it may 
# # be better to reject the file rather than use incomplete data. 
# # On the other hand, I would rather tolerate a missing temperature if the weather 
# # service sometimes has temporary gaps and I still want to process the 
# # other valid hourly observations. To tolerate null values, I would change 
# # the temperature field in the schema to optional[float] 
# # (or float | None). Then the pipeline could skip or handle readings with missing temperatures 
# # instead of rejecting the entire file. 
# 2. DailyAggregator.min_hours defaults to 24. If the pipeline runs at noon, 
# # the current day can have only about 12 hours of observations. The aggregator would treat that
# # day as incomplete and would not create a DailySummary for it. 
# # incomplete_days() helps by identifying the dates that were dropped because 
# # they have fewer observations than min_hours. This makes it clear that the 
# # missing summary is intentional because the day is not yet complete. 
# 3. Writing weatherkit as a package makes it easier to organize related
# # functionality into separate modules. When needed, I can import only the function or class I need
# # from the appropriate module instead of putting all the code in one large file.