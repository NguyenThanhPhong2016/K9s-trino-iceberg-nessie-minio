from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

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
    trino_query

