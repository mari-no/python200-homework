#Task 5: The Test Suite

#Use a @pytest.fixture for shared input.
# Grouping works: a hand-built 
# list spanning two dates produces two summaries.
# temp_max and temp_min are correct for a known small input.
# precipitation_sum adds up correctly. Use pytest.approx.
# A day with fewer than min_hours readings is dropped,
#  and its date appears in incomplete_days().
# Lowering min_hours causes that same day to be kept --
#  proving the parameter is actually consulted rather than ignored.
# At least one test must use @pytest.mark.parametrize.

import pytest
from weatherkit.records import HourlyReading
from weatherkit.summarize import DailyAggregator

@pytest.fixture
def shared_input():
    return[HourlyReading(timestamp="2026-09-29T09:00",
                            temperature_c=20.0,
                            precipitation_mm = 0.1,
    ),
    HourlyReading(timestamp="2026-09-29T10:00",
                            temperature_c=21.0,
                            precipitation_mm = 0.9,
    ),
    HourlyReading(timestamp="2026-09-29T11:00",
                            temperature_c=23.0,
                            precipitation_mm = 0.3,
    ),
    HourlyReading(timestamp="2026-09-30T09:00",
                            temperature_c=30.0,
                            precipitation_mm = 1.0,
    ),
    HourlyReading(timestamp="2026-09-30T10:00",
                            temperature_c=34.0,
                            precipitation_mm = 0.2,
    )]


def test_grouping_by_dates(shared_input):
    aggregator = DailyAggregator(min_hours=1)
    summaries=aggregator.summarize(shared_input)

    assert len(summaries)==2
    assert(summaries[0].date =="2026-09-29")
    assert(summaries[1].date =="2026-09-30")


@pytest.mark.parametrize(
    "date, expected_max, expected_min",
    [
        ("2026-09-29", 23.0, 20.0),
        ("2026-09-30",34.0, 30.0),

    ])

def test_temp_max_and_min(
    shared_input, date, expected_max, expected_min
):

    aggregator = DailyAggregator(min_hours=1)
    summaries = aggregator.summarize(shared_input)

    for item in summaries:
        if item.date == date:
            summary = item
            break

    assert summary.temp_max == expected_max
    assert summary.temp_min == expected_min



def test_precipitation_sum(shared_input):
    aggregator = DailyAggregator(min_hours=1)
    summaries = aggregator.summarize(shared_input)

    assert summaries[0].precipitation_sum == pytest.approx(1.3)
    assert summaries[1].precipitation_sum == pytest.approx(1.2)


def test_with_fewer_than_min_hours_dropped(shared_input):

    aggregator = DailyAggregator(min_hours=3)
    summaries = aggregator.summarize(shared_input)
    fewer_than_min_hours = aggregator.incomplete_days(shared_input)

    assert len(summaries) == 1
    assert summaries[0].date == "2026-09-29"
    assert "2026-09-30" in fewer_than_min_hours

def test_keep_days_by_lowering_min_hours(shared_input):
    aggregator = DailyAggregator(min_hours=2)
    summaries = aggregator.summarize(shared_input)

    assert len(summaries) == 2
    assert summaries[1].date == "2026-09-30"
    

