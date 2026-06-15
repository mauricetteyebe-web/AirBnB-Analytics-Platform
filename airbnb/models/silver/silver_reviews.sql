SELECT
    listing_id,
    date            AS review_date,
    reviewer_name,
    comments        AS review_text,
    sentiment
FROM {{ ref('bronze_reviews') }}
WHERE comments IS NOT NULL