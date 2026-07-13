{{ config(materialized="incremental", unique_key="product_id") }}

select *, current_timestamp() as processed_at
from {{ source("ghost_db", "products") }}

{% if is_incremental() %}
    where
        updated_timestamp
        > (select coalesce(max(updated_timestamp), '1900-01-01') from {{ this }})
{% endif %}
