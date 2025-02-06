from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime

# Sử dụng image có sẵn SciPy từ Docker Hub
IMAGE_NAME = "jupyter/scipy-notebook"  # Image chứa SciPy, NumPy

PYTHON_SCRIPT = """
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import solve

def objective_function(x):
    return (x - 3) ** 5 + x + 2

def my_task():
    A = np.array([[3, 2], [1, 4]])  # Ma trận hệ số
    b = np.array([5, 6])  # Vector hằng số

    x = solve(A, b)  # Giải hệ phương trình Ax = b
    print("Nghiệm của hệ phương trình tuyến tính:", x)

    result = minimize(objective_function, x0=0)  # Bắt đầu từ x0 = 0
    print("Giá trị x tối ưu:", result.x)
    print("Giá trị nhỏ nhất của hàm:", result.fun)

my_task()
"""

# Tạo DAG
with DAG(
    dag_id="test3",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,  # Chạy thủ công
    catchup=False,
) as dag1:

    # Tạo task chạy container từ Docker Hub với image có SciPy
    dockerhub_k8s = KubernetesPodOperator(
        namespace="phong-movedata-database-minio",
        image=IMAGE_NAME,  # Image có SciPy
        cmds=["python", "-c"],
        arguments=[PYTHON_SCRIPT],  # Chạy script Python trong container
        labels={"app": "airflow"},
        name="airflow-dockerhub-pod",
        task_id="task-dockerhub",
        on_finish_action="delete_pod",
        in_cluster=True,
        get_logs=True,
    )

    dockerhub_k8s  # Gán task vào DAG
