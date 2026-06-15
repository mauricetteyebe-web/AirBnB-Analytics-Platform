SELECT
    CAST(full_moon_date AS DATE) AS date_day
FROM {{ ref('bronze_seed_full_moon_dates') }}