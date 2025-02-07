from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator


def process_response(**kwargs):
    ti = kwargs["ti"]
    response_data = ti.xcom_pull(task_ids="get_post")  #  Lấy dữ liệu từ XCom
    print("📌 Response từ API:", response_data)


# Khai báo DAG
default_args = {"owner": "airflow", "start_date": days_ago(1)}


with DAG("http_operator_example", default_args=default_args, schedule_interval=None) as dag:

    get_post = SimpleHttpOperator(
        task_id="get_post",
        method="GET",
        http_conn_id="http_connect",  # 🟢 Không dùng Connection
        endpoint="",  # 🟢 Truyền URL trực tiếp
        log_response=True,  # 🟢 Ghi log phản hồi từ API
        do_xcom_push=True,
    )
    process_task = PythonOperator(
        task_id="process_response",
        python_callable=process_response,
        provide_context=True,
    )
    get_post >> process_task

