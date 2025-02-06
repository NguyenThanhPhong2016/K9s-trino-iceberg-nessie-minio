from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime
with DAG(
    dag_id="test2",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,  # Chạy thủ công
    catchup=False,
) as dag1:
    # Tạo task chạy container từ Docker Hub
    dockerhub_k8s = KubernetesPodOperator(
        namespace="phong-movedata-database-minio",
        image="python:3.9",  # Image từ Docker Hub (public)
        cmds=["python", "-c"],
        arguments=["print('Hello from Docker Hub')"],
        labels={"app": "airflow"},
        name="airflow-dockerhub-pod",
        on_finish_action="delete_pod",
        in_cluster=False,
        task_id="task-dockerhub",
        get_logs=True,
        dag=dag1
    )
    dockerhub_k8s
