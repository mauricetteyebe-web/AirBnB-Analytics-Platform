SELECT
    listing_id,
    review_date,
    reviewer_name,
    review_text,
    sentiment
FROM {{ ref('silver_reviews') }}
ORDER BY review_date DESC