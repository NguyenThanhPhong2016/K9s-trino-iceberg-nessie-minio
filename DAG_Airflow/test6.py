from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago

# Khai báo DAG
default_args = {"owner": "airflow", "start_date": days_ago(1)}

with DAG("http_operator_example", default_args=default_args, schedule_interval=None) as dag:

    get_post = SimpleHttpOperator(
        task_id="get_post",
        method="GET",
        http_conn_id=None,  # 🟢 Không dùng Connection
        endpoint="http://192.168.1.17:31003",  # 🟢 Truyền URL trực tiếp
        log_response=True,  # 🟢 Ghi log phản hồi từ API
    )

    get_post  # ✅ Kích hoạt task
