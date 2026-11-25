# My video link:https://youtu.be/s9AFGghcuZs
## Part 2: Project — Extract + Load Pipeline


## Step 1: Extract
import os
from pathlib import Path
from datetime import date

import requests
from dotenv import load_dotenv
from supabase import create_client
# Supbase connect
def get_client():
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path, override=True)

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError("Missing Supabase credentials in .env")

    return create_client(supabase_url.strip(), supabase_key.strip())

def extract_weather():
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": 30.2672,
        "longitude": -97.7431,
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max"
        ],
        "timezone": "America/Chicago"
    }

    response = requests.get(url, params=params, timeout=30)

    # Catch HTTP errors early
    response.raise_for_status()

    data = response.json()

    print("Extraction Summary: ")
    print("City: Austin, Texas")
    print("Response status:", response.status_code)
    print("Daily variables:", data["daily"].keys())
    print("Number of dates:", len(data["daily"]["time"]))

    return data


## Step 2: Transform

def transform_weather(data):
    daily = data["daily"]

    records = []
#Convert the API response from columnar format into a list of row dictionaries

    for i, weather_date in enumerate(daily["time"]):
        record = {
            "date": weather_date,
            "temperature_2m_max": daily["temperature_2m_max"][i],
            "temperature_2m_min": daily["temperature_2m_min"][i],
            "precipitation_sum": daily["precipitation_sum"][i],
            "wind_speed_10m_max": daily["wind_speed_10m_max"][i]
        }

        records.append(record)

    print("Transformation Summary: ")
    print("First record:", records[0])
    print("Last record:", records[-1])

    # A full year of 2023 has 365 days (not a leap year).
    # We expect 365 records and should receive 365.
    # A difference could indicate missing dates or incomplete API data.

    print("Expected records: 365")
    print("Actual records:", len(records))

    return records


## Step 3: Load

def load_weather(client, records):
    result = (
        client.table("weather_raw")
        .upsert(records, on_conflict="date")
        .execute()
    )

    print("Load Summary: ")
    print("Rows upserted:", len(result.data))


## Step 4: Verify
def verify_weather(client):
    table = client.table("weather_raw")

    # Total row count
    count_result = table.select("*", count="exact").execute()

    print("\n--- Verification ---")
    print("Total rows in weather_raw:", count_result.count)

    # Earliest date
    earliest = (
        table.select("date")
        .order("date", desc=False)
        .limit(1)
        .execute()
    )

    # Latest date
    latest = (
        table.select("date")
        .order("date", desc=True)
        .limit(1)
        .execute()
    )

    print("Earliest date:", earliest.data[0]["date"])
    print("Latest date:", latest.data[0]["date"])

    # Find July 4, 2023
    july_fourth = (
        table.select("*")
        .eq("date", "2023-07-04")
        .execute()
    )

    if july_fourth.data:
        print("July 4 record:", july_fourth.data[0])
    else:
        # If July 4 is missing, find the closest available date.
        all_rows = table.select("*").execute()

        closest = min(
            all_rows.data,
            key=lambda row: abs(
                (date.fromisoformat(row["date"]) -
                 date(2023, 7, 4)).days
            )
        )

        print("July 4 is missing.")
        print("Nearest date record:", closest)


# Run the pipeline
def main():
    client = get_client()

    # Extract
    data = extract_weather()

    # Transform
    records = transform_weather(data)

    # Load
    load_weather(client, records)

    # Verify
    verify_weather(client)


if __name__ == "__main__":
    main()
# Idempotency:
# Running the pipeline multiple times does not create duplicate rows.
# The date column is the primary key, and upsert updates existing
# records instead of inserting duplicates.