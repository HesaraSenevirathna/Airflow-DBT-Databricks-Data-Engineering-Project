{{ config(materialized="incremental", unique_key="employee_id") }}

select *, current_timestamp() as processed_at
from {{ source("ghost_db", "employees") }}

{% if is_incremental() %}
    where
        updated_timestamp
        > (select coalesce(max(updated_timestamp), '1900-01-01') from {{ this }})
{% endif %}
