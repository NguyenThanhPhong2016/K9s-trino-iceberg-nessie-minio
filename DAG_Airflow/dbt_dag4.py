from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 3,  # Số lần retry tối đa
    'retry_delay': timedelta(minutes=1),  # Khoảng thời gian giữa các lần retry
}

# Khởi tạo DAG
dag = DAG(
    "dbt_kubernetes_dag6",
    default_args=default_args,
    schedule_interval="@daily",  # Chạy DAG mỗi ngày
    catchup=False,
)


dbt_run_task = KubernetesPodOperator(  
    image="phong192016/my-dbt-project:v10",  # Image dbt từ Docker Hub
    cmds=["bash", "-c"],
    arguments=["cd /project_dbt && dbt run --profiles-dir . --project-dir . -s ./models/example/*"],
    name="dbt-run-pod",
    task_id="dbt_run",
    get_logs=True,  # Lấy logs từ Kubernetes để hiển thị trong Airflow
    is_delete_operator_pod=False,
    in_cluster=True,  # Nếu Airflow chạy trong Kubernetes, đặt là True
    dag=dag,
)


dbt_run_task  # Kết nối Task vào DAG
