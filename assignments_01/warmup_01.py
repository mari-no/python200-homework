####### Classes WarmUp

## Classes Question 1


class Thermometer:
    def __init__(self, location, temp_readings = None):
        self.location = location
        self.temp_readings = temp_readings if temp_readings is not None else []


    def add(self, reading):
        self.temp_readings.append(reading)

    def average(self):
        return sum(self.temp_readings)/len(self.temp_readings) if self.temp_readings else None

    def hottest(self):
        return max(self.temp_readings) if self.temp_readings else None


austin = Thermometer("Austin", [32, 28, 30, 35, 36, 29])
austin.add(32)
austin.add(37)
austin.add(25)
austin.add(31)


print(f'Average, Celsius: {austin.average()}')

print(f'Hottest, Celsius: {austin.hottest()}')
###Comment that explains why we need None
### why does average() need to handle the empty case?
# because without that handling Python would try divide 0/0
#  What would happen without that check?
#Without that check Python would raise ZeroDivisionError: division by zero
# Classes Question 2

class Thermometer:
    def __init__(self, location, temp_readings = None):
        self.location = location
        self.temp_readings = temp_readings if temp_readings is not None else []


    def add(self, reading):
        self.temp_readings.append(reading)

    def average(self):
        return sum(self.temp_readings)/len(self.temp_readings) if self.temp_readings else None

    def hottest(self):
        return max(self.temp_readings) if self.temp_readings else None

    def __repr__(self):
        return (
            f"Thermometer(location={self.location!r}, n_readings={len(self.temp_readings)}, "
            f"average={self.average()})"
        )


austin = Thermometer("Austin", [32, 28, 30, 35, 36, 29])
print(austin)
destin = Thermometer("Destin",[30, 29, 32, 31, 34])
print([austin, destin])

###comment explaining what Python displays when 
# a class has no __repr__, and why that is unhelpful when debugging.
#Without __repr__, Python displays a default representation of the object,
# including its class name and memory address. This is unhelpful when debugging
# because it does not show the object's useful data



# Classes Question 3
class TemperatureAlert:
    def __init__(self, threshold = 30):
        self.threshold = threshold

        
        

        self.threshold=threshold
    def breaches(self, thermometer):
        list_above_threshold=[]
        for temp_reading in thermometer.temp_readings:
            if temp_reading > self.threshold:
                list_above_threshold.append(temp_reading)

        return list_above_threshold

low_threshold = TemperatureAlert(30)
high_threshold = TemperatureAlert(33)

print(f"Low threshold: {low_threshold.breaches(destin)}")

print(f"High threshold: {high_threshold.breaches(destin)}")


###comment answering these questions: why is the threshold stored on TemperatureAlert rather than passed as an argument to breaches()? 
# What advantage does that give you if you have twenty thermometers to check?
# The threshold is stored in TemperatureAlert to make the alert easier to use and modify.
# We can create multiple alert objects with different thresholds and reuse them
# across many thermometers without passing the threshold each time.
# This is especially useful when checking many thermometers or when we need
# several different threshold settings.


##### Dataclasses, Type Hints, and Docstrings
## Dataclass Question 1

from dataclasses import dataclass
@dataclass
class Station:
  """Represents a weather station and its location information"""
  station_id :str
  name :str 
  latitude : float
  longitude : float
  elevation : float
station_a = Station("01","Austin","1.23","24.56","0.8")
station_b = Station("01","Austin","1.23","24.56","0.8")
print(station_a == station_b)
###comment explaining why the result is what it is, 
# and what it would have been with the original hand-written class.

#Result is True, because dataclass automatically creates __eq__ method that compares each
#field value of two objects and values are the same. With hand written cklass without dataclass 
#result would have been false because Python would compare two different objects, not their 
#field values

# Dataclass Question 2
# Make Station frozen. Then:
# Show that assigning to a field now raises FrozenInstanceError 
# (catch it and print the message -- do not let the script crash).
# Build a set containing three Station objects where two are identical, 
# and print the length.
# Add a comment: what does frozen=True give you besides immutability, 
# and why is that useful here?
from dataclasses import dataclass, FrozenInstanceError
@dataclass(frozen=True)
class Station:
  """Represents a weather station and its location information"""
  station_id :str
  name :str 
  latitude : float
  longitude : float
  elevation : float
station_a = Station("01","Austin","1.23","24.56","0.8")
station_b = Station("01","Austin","1.23","24.56","0.8")

station_c = Station("02","Dallas","1.8","44.58","70.8")
try:
    station_a.name="Changed name"
except FrozenInstanceError as error:
    print(f"Sorry, Station is immutable: {error}")

stations = {station_a, station_b, station_c}
print(f"Number of stations in a set: {len(stations)}")
###comment explaining
###frozen=True makes object immutable and now they can be stored in a set
#Station a ans station b considered the same because they have identical field values and that's why 
#the length of the set will be 2, not 3


# Dataclass Question 3
# Write a dataclass StationBatch 

from dataclasses import dataclass, field, FrozenInstanceError
@dataclass
class StationBatch:
    """Represents a set of weather stations"""
    region: str
    stations:list[Station] = field(default_factory=list)

    ### stations:list[Station] = []--that is a mistake
    #Python raises: ValueError: mutable default 
    # <class 'list'> for field stations is not allowed: use default_factory
    #A single mutable default would be shared across all instances, 
    # so appending to one object's list would change every other object's list.
    #  Dataclasses raise a `ValueError` rather than let you make that mistake. 
    # `field(default_factory=list)` calls `list()` fresh for each new instance.

    def add(self, station: Station) -> None:
        self.stations.append(station)

    def highest(self)->Station|None:
        if not self.stations:
            return None
        highest_station= self.stations[0]
        for station in self.stations:
            if station.elevation > highest_station.elevation:
                highest_station=station
        return highest_station

###Pydantic
#Pydantic Question 1
from pydantic import BaseModel, Field
class Reading(BaseModel):
    station_id: str = Field(min_length=3)
    timestamp:str
    temperature_c:float= Field(ge = -90,le=60)
    humidity: float = Field(ge=0,le=100)


reading = Reading( station_id="001",timestamp="2026-10-01",
                  temperature_c = 26.8, humidity = 78.0 )

print(reading)


# Pydantic Question 2

from pydantic import BaseModel, Field, ValidationError


class Reading(BaseModel):
    station_id: str = Field(min_length=3)
    timestamp: str
    temperature_c: float = Field(ge=-90, le=60)
    humidity: float = Field(ge=0, le=100)


try:
    reading = Reading(
        station_id="002",
        #missing timestamp
        temperature_c=25.5,
        humidity=65
    )
except ValidationError as error:
    print(error)


try:
    reading = Reading(
        station_id="003",
        timestamp="2026-10-01",
        temperature_c=150.0, #temperature outside of allowed range
        humidity=65
    )
except ValidationError as error:
    print(error)



try:
    reading = Reading(
        station_id="004",
        timestamp="2026-10-01",
        temperature_c=25.5,
        humidity="very humid" #humidity is string instead of a float
    )
except ValidationError as error:
    print(error)



reading = Reading(
    station_id="005",
    timestamp="2026-10-01",
    temperature_c="21.5",#can convert compatible values to the type required by the model
    humidity=40
)

print(reading)
print(type(reading.temperature_c))
print(type(reading.humidity))

# Pydantic accepts "21.5" because the string contains a value that can be
# converted to a float. It rejects "very humid" because that text can't
# be converted to a float. Pydantic can convert a value
# when it is compatible with the field's required type.

#Pydantic Question 3

try:
    reading = Reading(
        station_id="0", #too short station_id

        #missing timestamp
        temperature_c="very hot", #non-numeric temperature
        humidity=50
    )

except ValidationError as e:
    print(f"{e.error_count()} problems found\n")
    for err in e.errors():
        print(f"  field={err['loc']}  type={err['type']}  msg={err['msg']}")
### Three problems were reported at once:

# 3 problems found

#   field=('station_id',)  type=string_too_short  msg=String should have at least 3 characters
#   field=('timestamp',)  type=missing  msg=Field required
#   field=('temperature_c',)  type=float_parsing  msg=Input should be a valid number, unable to parse string as a number

# When you are debugging a malformed API payload under time pressure, 
# receiving the whole list at once instead of fixing the problems one at 
# a time saves a great deal of effort.

### Pydantic Question 4

from pydantic import BaseModel, Field, ValidationError, model_validator


class Reading(BaseModel):
    station_id: str = Field(min_length=3)
    timestamp:str
    temperature_c:float= Field(ge = -90,le=60)
    humidity: float = Field(ge=0,le=100)
  
    @model_validator(mode="after")
    def check_sensor_health(self):
        if self.humidity == 0.0 and self.temperature_c < -40:
            raise ValueError(
                "Humidity=0.0 and temperature below -40 indicate a failed sensor"
            )

        return self


#Valid reading still constructs
try:
    valid_reading = Reading(
    station_id="001",
    timestamp="2026-10-01",
    temperature_c=-20.0,
    humidity=0.0
)
    print(valid_reading)
except ValidationError as e:
    print(e)




#rejected combination 
try:
    rejected_reading = Reading(
        station_id="002",
        timestamp="2026-10-01",
        temperature_c=-50.0,
        humidity=0.0
    )
    print(rejected_reading)
except ValidationError as e:
    print(e)

#This rule needs model_validator because Field can only 
# check one field at a time, but this rule depends on the combination
#of two fields, which exactly what model_validator can do

### pytest


#pytest Question 1

import pytest

def celsius_to_fahrenheit(celsius: float) -> float :
    """Converts Celsius to Farenheit."""
    return celsius*9/5+32
def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(0)==32
    assert celsius_to_fahrenheit(100)==212
    assert celsius_to_fahrenheit(37)== pytest.approx(98.6)


#pytest Question 2
def mean(values: list[float]) -> float:
    """Returns mean of a list of values"""
    if not values:
        raise ValueError("List can not be empty")
    return sum(values)/len(values)
def test_mean_of_empty_raises():
    with pytest.raises(ValueError, match="can not be empty"):
        mean([])
####
# The match= argument checks the error message against a
#  regular expression, and you should use it.
#  Without match, pytest.raises(ValueError) passes if 
# any ValueError occurs, including one caused by a typo
#  in a test setup. 
# That produces a test that passes for the wrong reason.


##pytest Question 3
@pytest.mark.parametrize("values, expected",
                         [
                             ([10], 10),
                             ([10,20], 15),
                             ([-10,-20], -15),
                             ([1,2,3,4], 2.5)
                         ])

def test_mean_values(values, expected):
    assert mean(values) == expected


### summary line:
# rootdir: /Users/marinam/python200-homework/assignments_01
# collected 6 items                                                                 

# warmup_01.py::test_celsius_to_fahrenheit PASSED                             [ 16%]
# warmup_01.py::test_mean_of_empty_raises PASSED                              [ 33%]
# warmup_01.py::test_mean_values[values0-10] PASSED                           [ 50%]
# warmup_01.py::test_mean_values[values1-15] PASSED                           [ 66%]
# warmup_01.py::test_mean_values[values2--15] PASSED                          [ 83%]
# warmup_01.py::test_mean_values[values3-2.5] PASSED                          [100%]

# ================================ 6 passed in 0.19s ================================

# One parametrized test with four cases better than four nearly identical test functions, 
# because it's easier to maintain, change and add more cases if needed, 
# it also helps us to avoid repetitions of the same code


## pytest Question 4
#Deliberately break celsius_to_fahrenheit 
# (for example, change 9 / 5 to 9 / 4). 
# Run your test again and paste the failure output into a comment:
# 
# ==================================== FAILURES =====================================
# ___________________________ test_celsius_to_fahrenheit ____________________________

#     def test_celsius_to_fahrenheit():
#         assert celsius_to_fahrenheit(0)==32
# >       assert celsius_to_fahrenheit(100)==212
# E       assert 257.0 == 212
# E        +  where 257.0 = celsius_to_fahrenheit(100)

# warmup_01.py:365: AssertionError
# ============================= short test summary info =============================
# FAILED warmup_01.py::test_celsius_to_fahrenheit - assert 257.0 == 212

### Pytest showed that celsius_to_fahrenheit(100) returned 257.0, 
# but the expected value was 212. 
# This is more useful than a bare “assertion failed”
#  because we can see the exact actual and expected 
# values and immediately understand that the calculation is wrong.


