import csv
import datetime

input_file = r'c:\Users\Hesara\Desktop\Airflow-DBT-Databricks-Data-Engineering-Project\Dataset\data\stores.csv'
output_file = r'c:\Users\Hesara\Desktop\Airflow-DBT-Databricks-Data-Engineering-Project\Dataset\data\ingestion_stores.csv'

now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)
    fieldnames = reader.fieldnames

# Update existing data
for row in rows:
    if row['store_id'] == '1':
        row['store_name'] = 'Walmart Store 1 - Renovated'
        row['updated_timestamp'] = now_str
    elif row['store_id'] == '2':
        row['is_active'] = 'N'
        row['updated_timestamp'] = now_str

# Add new data
rows.append({
    'store_id': '26',
    'store_name': 'Walmart Store 26',
    'city': 'Toronto',
    'province': 'Ontario',
    'country': 'Canada',
    'created_timestamp': now_str,
    'updated_timestamp': now_str,
    'is_active': 'Y'
})

rows.append({
    'store_id': '27',
    'store_name': 'Walmart Store 27',
    'city': 'Vancouver',
    'province': 'British Columbia',
    'country': 'Canada',
    'created_timestamp': now_str,
    'updated_timestamp': now_str,
    'is_active': 'Y'
})

with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Successfully generated {output_file}")
