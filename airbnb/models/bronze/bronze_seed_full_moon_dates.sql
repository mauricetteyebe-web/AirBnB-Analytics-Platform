SELECT
    full_moon_date
FROM {{ ref('seed_full_moon_dates') }}