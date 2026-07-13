import os
from databricks import sql

# Connection details from profiles.yml
server_hostname = "dbc-97b5e1b9-f7e2.cloud.databricks.com"
http_path = "/sql/1.0/warehouses/ecef9781dd216b7e"
access_token = "<DATABRICKS_TOKEN>"

try:
    with sql.connect(server_hostname=server_hostname,
                     http_path=http_path,
                     access_token=access_token) as connection:

        with connection.cursor() as cursor:
            # Query Gold layer
            cursor.execute("SELECT store_id, store_name, store_is_active, dbt_valid_from, dbt_valid_to FROM ghost.gold.dim_stores WHERE store_id IN (1, 2, 26, 27) ORDER BY store_id, dbt_valid_from;")
            gold_results = cursor.fetchall()
            print("\n--- GOLD LAYER (SCD Type 2) ---")
            for row in gold_results:
                print(f"Store {row.store_id}: '{row.store_name}' | Active? {row.store_is_active} | Valid From: {row.dbt_valid_from} | Valid To: {row.dbt_valid_to}")

except Exception as e:
    print(f"Error querying Databricks: {e}")
