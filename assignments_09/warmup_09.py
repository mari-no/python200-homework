## Part 1: Warmup

## Supabase Connection
# Connection Question 1

# The two pieces of information supabase-py needs to connect to a Supabase project are:

# 1. Project URL – found in the Supabase Dashboard under Project Settings → API.
# 2. API Key (publishable key / anon key) – found in the same API settings section.
# These values should be stored in environment variables (in a .env file) 
# rather than hardcoded in a Python script. This protects sensitive credentials from being 
# accidentally exposed when sharing code or uploading it to GitHub.

# Connection Question 2
import os
from dotenv import load_dotenv
from supabase import create_client
from pathlib import Path


def get_client():
    
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
    print("ENV file exists:", env_path.exists())

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    print("URL loaded:", bool(supabase_url))
    print("URL value:", repr(supabase_url))
    if not supabase_url or not supabase_key:
        raise ValueError(
            "Missing SUPABASE_URL or SUPABASE_KEY in environment variables."
        )

    return create_client(supabase_url, supabase_key)

# Connection Question 3

# Row Level Security (RLS) is a security feature in Supabase
# that controls which rows users can access, read, update, or delete
# based on defined policies.
# I disabled RLS for this course to simplify database access
# and allow Python application to work with the tables
# without setting up additional security policies.
# In a real-world application, such as a banking app or a healthcare
# system, RLS should remain enabled to ensure users can only access
# their own personal or sensitive data.


## supabase-py CRUD
## CRUD Question 1
from datetime import date


def insert_test_record(supabase):
    record = {
        "date": date.today().isoformat(),
        "temperature_2m_max": 27.5,
        "temperature_2m_min": 18.2,
        "precipitation_sum": 0.0,
        "wind_speed_10m_max": 15.3
    }

    response = supabase.table("weather_raw").insert(record).execute()

    print("Inserted record:", response.data)
    return response.data
# If I run this function twice, the second execution will fail
# because the date column is a PRIMARY KEY and cannot contain
# duplicate values.
# To make the function safe to run multiple times, I can replace
# .insert(record) with .upsert(record, on_conflict="date").
# Upsert checks whether the date already exists. If it does,
# it updates the existing record instead of inserting a duplicate.

## CRUD Question 2
def get_records_by_date_range(supabase, start, end):
    response = (
        supabase.table("weather_raw")
        .select("*")
        .gte("date", start)
        .lte("date", end)
        .execute()
    )

    return response.data

## CRUD Question 3
# INSERT adds a new row to the database.
# If a row with the same primary key already exists,
# this operation fails with a duplicate key error.
# UPSERT inserts a new row if it doesn't exist,
# or updates the existing row if there is a conflict.
# Example:
# Use INSERT when adding a new record that should not
#   already exist, such as a new user registration.
# Use UPSERT when importing daily weather data because
#   the same date might already exist and the weather data
#   may need to be updated.
# In our weather_raw table, date is the PRIMARY KEY,
# so we use date as the conflict key for upsert.
def safe_upsert(supabase, records):
    response = (
        supabase.table("weather_raw")
        .upsert(records, on_conflict="date")
        .execute()
    )

    print(f"Rows affected: {len(response.data)}")
    return response.data
if __name__ == "__main__":
    supabase = get_client()

    # CRUD Question 1: Test INSERT
    insert_test_record(supabase)

    # CRUD Question 2: Test date range query
    today = date.today().isoformat()

    records = get_records_by_date_range(
        supabase,
        today,
        today
    )

    print("Records found in date range:")
    print(records)

    # CRUD Question 3: Test UPSERT
    test_records = [
        {
            "date": today,
            "temperature_2m_max": 27.5,
            "temperature_2m_min": 18.2,
            "precipitation_sum": 0.0,
            "wind_speed_10m_max": 15.3
        }
    ]

    safe_upsert(supabase, test_records)
## Idempotency
## Idempotency Question 1

# Idempotency is important in a data pipeline because it ensures
# that running the same operation multiple times produces the
# same result without creating duplicate or incorrect data.

# Pipelines can crash because of network problems, server errors,
# or other unexpected issues. Idempotency allows us to safely
# restart a pipeline without worrying about duplicating data.

# Example:
# If a pipeline downloads daily weather data and inserts 100 rows,
# but crashes after inserting 50 rows, restarting a non-idempotent
# pipeline could insert those same 50 rows again, creating duplicates.
