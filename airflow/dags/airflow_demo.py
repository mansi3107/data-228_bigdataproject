from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'sanjaybharvad',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='us_accidents_pipeline',
    default_args=default_args,
    description='US Accidents Big Data Pipeline - HDFS + Spark',
    schedule_interval='@weekly',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['bigdata', 'spark', 'hdfs'],
) as dag:

    check_hdfs = BashOperator(
        task_id='check_hdfs',
        bash_command='hdfs dfs -ls /user/accidents/raw/ && echo "HDFS is running"',
    )

    check_spark = BashOperator(
        task_id='check_spark',
        bash_command='spark-submit --version && echo "Spark is running"',
    )

    data_ingestion = BashOperator(
        task_id='data_ingestion',
        bash_command='hdfs dfs -ls /user/accidents/raw/US_Accidents_March23.csv && echo "Raw data verified on HDFS"',
    )

    spark_cleaning = BashOperator(
        task_id='spark_cleaning',
        bash_command='hdfs dfs -ls /user/accidents/cleaned/ && echo "Cleaned data verified on HDFS"',
    )

    spark_eda = BashOperator(
        task_id='spark_eda',
        bash_command='hdfs dfs -ls /user/accidents/outputs/ && echo "EDA outputs verified on HDFS"',
    )

    ml_models = BashOperator(
        task_id='ml_models',
        bash_command='hdfs dfs -ls /user/accidents/ml_ready/ && echo "ML ready data verified on HDFS"',
    )

    

    check_hdfs >> check_spark >> data_ingestion >> spark_cleaning >> spark_eda >> ml_models >> pipeline_complete
