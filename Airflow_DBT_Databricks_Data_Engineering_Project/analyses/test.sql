select store_id, store_name, updated_timestamp, processed_at
from bronze.bronze_stores
where store_id in (26, 27)
order by processed_at desc
;
