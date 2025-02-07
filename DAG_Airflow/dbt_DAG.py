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
    "dbt_kubernetes_dag",
    default_args=default_args,
    schedule_interval="@daily",  # Chạy DAG mỗi ngày
    catchup=False,
)

# Tạo Task sử dụng KubernetesPodOperator để chạy 
dbt_run_task = KubernetesPodOperator(  
    image="phong192016/my-dbt-project:v2",  # Image dbt từ Docker Hub
    cmds=["dbt", "run"],  # Chạy lệnh dbt run
    arguments=["--profiles-dir", "."],
    name="dbt-run-pod",
    task_id="dbt_run",
    get_logs=True,  # Lấy logs từ Kubernetes để hiển thị trong Airflow
    is_delete_operator_pod=False,  # Tự động xóa Pod sau khi chạy xong
    in_cluster=True,  # Nếu Airflow chạy trong Kubernetes, đặt là True
    dag=dag,
)

dbt_run_task  # Kết nối Task vào DAG
