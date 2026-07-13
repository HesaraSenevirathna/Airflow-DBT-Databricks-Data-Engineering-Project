import pendulum
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator

# This is the path to your DBT project inside the Airflow Docker container
DBT_PROJECT_DIR = "/opt/airflow/Airflow_DBT_Databricks_Data_Engineering_Project"

@dag(
    dag_id="orchestrate",
    schedule="0 11 * * *", #cron syntax 11am daily (minute, hour, day of month, month, day of week)
    catchup=False,
    start_date=pendulum.datetime(2026,7,10, tz="UTC"), #pendulam is a library for date and time
)
def orchestrate():
    
    # 00. Run Databricks Job directly via WorkspaceClient
    @task
    def run_databricks_job():
        from databricks.sdk import WorkspaceClient
        ws = WorkspaceClient(
            host="https://dbc-97b5e1b9-f7e2.cloud.databricks.com",
            token="<DATABRICKS_TOKEN>"
        )
        print("Triggering Databricks Job 296372939303741...")
        job_trigger = ws.jobs.run_now(job_id=296372939303741)
        # .result() waits for the job to complete on Databricks before moving on
        job_trigger.result()
        print("Databricks Job Completed!")
        
    databricks_job = run_databricks_job()
    
    # 0. Clean stale cache (important when moving between Windows and Docker!) and install deps
    dbt_init = BashOperator(
        task_id="dbt_init",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt clean --profiles-dir . && dbt deps --profiles-dir ."
    )
    
    # 1. Capture Slowly Changing Dimensions (SCD) changes via Snapshots
    ingest_cdc = BashOperator(
        task_id="ingest_cdc",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt snapshot --profiles-dir ."
    )
    
    # 2. Run the Bronze Layer (Raw Data / Cleansing)
    source_cleansing = BashOperator(
        task_id="source_cleansing",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt run --select bronze --profiles-dir ."
    )
    
    # 3. Run the Silver Layer (Transformations & Joins)
    transform_silver = BashOperator(
        task_id="transform_silver",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt run --select silver --profiles-dir ."
    )
    
    # 4. Run the Gold Layer (Aggregations & Business Logic)
    transform_gold = BashOperator(
        task_id="transform_gold",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt run --select gold --profiles-dir ."
    )
    
    # 5. Run Tests and Ensure Data Quality (Optional but recommended)
    test_data = BashOperator(
        task_id="test_data",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt test --profiles-dir ."
    )
    
    # Set the execution order (dependencies)
    databricks_job >> dbt_init >> source_cleansing >> transform_silver >> ingest_cdc >> transform_gold >> test_data

# Instantiate the DAG
orchestrate()