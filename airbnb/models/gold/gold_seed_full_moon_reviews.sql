SELECT
    fr.*,
    CASE
        WHEN fm.date_day IS NULL THEN 'not full moon'
        ELSE 'full moon'
    END AS is_full_moon
FROM {{ ref('gold_fact_reviews') }} fr
LEFT JOIN {{ ref('silver_seed_full_moon_dates') }} fm
    ON CAST(fr.review_date AS DATE) = fm.date_day + INTERVAL '1' DAY