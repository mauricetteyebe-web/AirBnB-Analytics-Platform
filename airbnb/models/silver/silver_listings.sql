SELECT
    id          AS listing_id,
    listing_url,
    name        AS listing_name,
    room_type,
    CASE
        WHEN minimum_nights IS NULL THEN 1
        WHEN minimum_nights = 0     THEN 1
        ELSE minimum_nights
    END         AS minimum_nights,
    host_id,
    CAST(REPLACE(price, '$', '') AS DECIMAL(10,2)) AS price,
    created_at,
    updated_at
FROM {{ ref('bronze_listings') }}