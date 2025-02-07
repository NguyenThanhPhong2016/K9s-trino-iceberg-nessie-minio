from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

# Định nghĩa default_args cho DAG
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# Khởi tạo DAG
dag = DAG(
    "dbt_kubernetes_dag1",
    default_args=default_args,
    schedule_interval="@daily",  # Chạy DAG mỗi ngày
    catchup=False,
)


dbt_run_task = KubernetesPodOperator(  
    image="phong192016/my-dbt-project:v5",  # Image dbt từ Docker Hub
    cmds=["dbt"], 
    arguments=["run", "--profiles-dir", "./project_dbt1/project_dbt", "--project-dir", "./project_dbt1/project_dbt", "-s", "project_dbt1/project_dbt/models/example/*"],  # Thêm đầy đủ các arguments
    name="dbt-run-pod",
    task_id="dbt_run",
    get_logs=True,  # Lấy logs từ Kubernetes để hiển thị trong Airflow
    is_delete_operator_pod=True,  # Giữ lại pod sau khi chạy để debug nếu cần
    in_cluster=True,  # Nếu Airflow chạy trong Kubernetes, đặt là True
    dag=dag,
)


dbt_run_task  # Kết nối Task vào DAG
