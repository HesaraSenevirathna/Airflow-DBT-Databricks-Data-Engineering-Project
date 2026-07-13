{{ config(severity="warn") }}

select 1
from {{ ref("obt") }} as obt
where
    obt.order_id is null
    or obt.product_id is null
    or obt.employee_id is null
    or obt.store_id is null
    or obt.order_item_id is null
    or obt.customer_id is null
