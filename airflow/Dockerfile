FROM apache/airflow:2.8.0-python3.11

USER airflow
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
