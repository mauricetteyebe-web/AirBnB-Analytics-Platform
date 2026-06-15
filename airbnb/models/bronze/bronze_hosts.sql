SELECT
    id,
    name,
    is_superhost,
    created_at,
    updated_at
FROM {{ ref('hosts') }}