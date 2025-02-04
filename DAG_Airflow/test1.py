from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.operators.bash_operator import BashOperator
from minio import Minio
from minio.sse import SseCustomerKey
from trino.dbapi import connect
def my_task():
    client = Minio(
        "192.168.1.17:30090",  # Địa chỉ API MinIO (cổng 9000)
        access_key="zAibg3ryk50qi0f6oS9T",  # Tài khoản mặc định
        secret_key="P0QX1qz9sBvbfhf4bgEtA6JNJJIyPMkS5PTd20pA", # Mật khẩu mặc định
        secure=False
    )

    bucket_name = "test-minio"  # Tên bucket
    object_name = "trino_data.csv"  # Tên file trên MinIO
    file_path = "trino_data.csv"  # Đường dẫn file cục bộ

    # Ghi dữ liệu vào MinIO
    client.fput_object(bucket_name, object_name, file_path)
    print(f"File '{file_path}' đã được tải lên bucket '{bucket_name}' dưới tên '{object_name}'.")

    x = client.list_buckets()
    for y in x:
        print(y)
with DAG(
    dag_id="test",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,  # Chạy thủ công
    catchup=False,
) as dag:
    task = PythonOperator(
        task_id="print_message",
        python_callable=my_task,
    )
    run_bash_command = BashOperator(
        task_id='run_bash_command',
        bash_command='minio --version'
    )
    run_bash_command1 = BashOperator(
        task_id='run_bash_command1',
        bash_command='python --version'
    )
    task >> run_bash_command >> run_bash_command1

    