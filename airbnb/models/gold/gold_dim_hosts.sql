SELECT
    host_id,
    host_name,
    is_superhost,
    created_at,
    updated_at
FROM {{ ref('silver_hosts') }}