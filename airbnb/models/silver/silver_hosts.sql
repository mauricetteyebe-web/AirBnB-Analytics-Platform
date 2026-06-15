SELECT
    id          AS host_id,
    COALESCE(name, 'Anonymous') AS host_name,
    CAST(is_superhost AS BOOLEAN) AS is_superhost,
    created_at,
    updated_at
FROM {{ ref('bronze_hosts') }}