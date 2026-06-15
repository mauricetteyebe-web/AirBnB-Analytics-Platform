SELECT
    listing_id,
    listing_url,
    listing_name,
    room_type,
    minimum_nights,
    host_id,
    price
FROM {{ ref('silver_listings') }}