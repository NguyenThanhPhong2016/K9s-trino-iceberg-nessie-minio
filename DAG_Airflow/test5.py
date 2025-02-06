from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago
from airflow.providers.http.sensors.http import HttpSensor



default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1,
}

with DAG(
    "trino_query_pod",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:
    check_website = HttpSensor(
        task_id="check_website",
        http_conn_id="http_connect",  # 🟢 Sử dụng Connection ID từ Airflow UI
        endpoint="",  # 🟢 Để trống nếu kiểm tra trực tiếp host
        method="GET",
        response_check=lambda response: response.status_code == 200,
        poke_interval=10,
        timeout=25,
    )
    check_website1 = HttpSensor(
        task_id="check_website1",
        http_conn_id=None,  # 🟢 Sử dụng Connection ID từ Airflow UI
        endpoint="http://192.168.1.17:31003",  # 🟢 Để trống nếu kiểm tra trực tiếp host
        method="GET",
        response_check=lambda response: response.status_code == 200,
        poke_interval=10,
        timeout=25,
    )

    trino_query = KubernetesPodOperator(
        image="trinodb/trino:latest",  # Sử dụng container Trino CLI
        cmds=["trino"],  # Chạy CLI của Trino
        arguments=[
            "--server", "http://192.168.1.17:31003",  # Địa chỉ Trino Server
            "--catalog", "iceberg",  # Catalog cần query (VD: Hive, Iceberg)
            "--execute", "SELECT * FROM iceberg.my_schema1.table1",  # Truy vấn SQL
        ],
        name="trino-query-task",
        task_id="trino_query_task",
        get_logs=True,
    )
    check_website >>check_website1>>  trino_query

