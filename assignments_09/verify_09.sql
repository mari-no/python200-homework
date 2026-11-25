--Step 5: Verify with SQL

-- Query 1: Row count and date range

SELECT
    COUNT(*) AS total_rows,
    MIN(date) AS earliest_date,
    MAX(date) AS latest_date
FROM weather_raw;

-- Result:
--total_rows:    365
--earliest_date: 2023-01-01
--latest_date:   2023-12-31
-- Query 2: Count rows with missing weather values

SELECT
    COUNT(*) AS rows_with_missing_values
FROM weather_raw
WHERE
    temperature_2m_max IS NULL
    OR temperature_2m_min IS NULL
    OR precipitation_sum IS NULL
    OR wind_speed_10m_max IS NULL;

   -- Result:
   -- rows_with_missing_values: 0
   /*
The SQL results match my Python verification results.
The table contains exactly 365 records, covering the
full year of 2023.
There are no missing values in the four weather columns.
The latest date is 2023-12-31, as expected.
Running the pipeline twice did not create duplicate
records because upsert uses date as the conflict key.
This confirms that the pipeline is idempotent.*/