
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

from airflow.operators.python import PythonOperator
import pendulum 

local_tz = pendulum.timezone('Asia/Ho_Chi_Minh')
def print_hello():
    print("Hello task3 : ")
    for i in range(10):
        print("I : " , i )

# root_file = "IT_Trainning/"
root_file = "/opt/airflow/dags/repo"
PROFILES_DIR = "."
PROJECT_DIR = "."
STAGING_PATH = "./models/staging/exact101"

PROFILES_DIR = root_file +  PROFILES_DIR
PROJECT_DIR = root_file +  PROJECT_DIR
STAGING_PATH = root_file +  STAGING_PATH

PROFILES_DIR = "/opt/airflow/dags/repo"
PROJECT_DIR = "/opt/airflow/dags/repo"
STAGING_PATH = "/opt/airflow/dags/repo/models/staging/exact101"

# PROFILES_DIR = "."
# PROJECT_DIR = "."
# STAGING_PATH = "./models/staging/exact101"


bash_command_staging = f"""dbt run --profiles-dir sunhouse_etl_pipeline\profiles.yml --project-dir sunhouse_etl_pipeline\dbt_project.yml -s path:sunhouse_etl_pipeline\models/staging/exact101/*"""
bash_command_staging = f"""dbt run --profiles-dir {PROFILES_DIR} --project-dir {PROJECT_DIR} --select {STAGING_PATH}"""

bash_command_staging = "ls &&" + bash_command_staging 

# Định nghĩa DAG
with DAG(
    dag_id='example_dag31',  # Tên DAG
    start_date=datetime(2024, 12, 25),  # Ngày bắt đầu
    schedule_interval='27 9 * * *',# Lịch chạy (ở đây là hàng ngày)
    catchup=False,  # Không chạy ngược các ngày cũ
) as dag:
    
    # Task 1: In ra dòng chữ "Hello Airflow"
    task_1 = BashOperator(
        task_id='task1',  # Tên task
        bash_command='echo "Hello Airflow!"',  # Lệnh Bash
    )

    # Task 2: In ra ngày hiện tại
    task_2 = BashOperator(
        task_id='task2',
        bash_command= bash_command_staging,
    )

    task_3 = BashOperator(
        task_id='task3',  # Tên task
        bash_command='dbt --version',  # Lệnh Bash
    )
    task_4 = BashOperator(
        task_id='task4',  # Tên task
        bash_command='pwd',  # Lệnh Bash
    )
    task_5 = BashOperator(
        task_id='task5',  # Tên task
        bash_command='ls',  # Lệnh Bash
    )
    # task_6 = BashOperator(
    #     task_id='task6',  # Tên task
    #     bash_command='dbt run',  # Lệnh Bash
    # )
    # Định nghĩa thứ tự thực thi
    task_1 >> task_2 # task_1 chạy trước, task_2 chạy sau



