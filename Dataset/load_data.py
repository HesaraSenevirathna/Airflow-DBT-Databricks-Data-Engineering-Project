import psycopg2
import os

# Database connection string
conn_string = "postgresql://tsdbadmin:no8s66wgi50djzwl@orohr64hrl.mgn8789tdd.db.ghost.build:5432/tsdb?sslmode=require"

# CSV files mapping to staging schema tables
csv_files = {
    "customers.csv": "staging.customers",
    "stores.csv": "staging.stores",
    "products.csv": "staging.products",
    "employees.csv": "staging.employees",
    "orders.csv": "staging.orders",
    "order_items.csv": "staging.order_items",
}

# Data directory
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

conn = None
try:
    # Connect to the database
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    # Load each CSV file into its corresponding table using copy_expert
    for csv_file, table_name in csv_files.items():
        csv_path = os.path.join(data_dir, csv_file)

        if os.path.exists(csv_path):
            print(f"Loading {csv_file} into {table_name}...")

            with open(csv_path, 'r', encoding='utf-8') as f:
                cursor.copy_expert(
                    f"COPY {table_name} FROM STDIN WITH (FORMAT CSV, HEADER TRUE)",
                    f
                )

            conn.commit()

            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"Successfully loaded {csv_file} ({count} rows)")
        else:
            print(f"File not found: {csv_path}")

    cursor.close()
    conn.close()
    print("\nAll data loaded successfully!")

except Exception as e:
    print(f"Error: {e}")
    if conn:
        conn.rollback()
        conn.close()
