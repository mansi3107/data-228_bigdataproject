from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'sanjaybharvad',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': ['sanjaybharvad@sjsu.edu'],
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

    # REAL Task 1 - Actually connects to HDFS and checks file exists
    check_hdfs = BashOperator(
        task_id='check_hdfs',
        bash_command='''
            export HADOOP_HOME=/opt/homebrew/opt/hadoop/libexec &&
            export PATH=$PATH:$HADOOP_HOME/bin &&
            hdfs dfs -ls /user/accidents/raw/ &&
            hdfs dfs -du -h /user/accidents/raw/ &&
            echo "HDFS check passed"
        ''',
    )

    # REAL Task 2 - Actually checks Spark version
    check_spark = BashOperator(
        task_id='check_spark',
        bash_command='''
            export SPARK_HOME=/opt/homebrew/opt/apache-spark/libexec &&
            export PATH=$PATH:$SPARK_HOME/bin &&
            spark-submit --version &&
            echo "Spark check passed"
        ''',
    )

    # REAL Task 3 - Actually verifies raw data on HDFS
    data_ingestion = BashOperator(
        task_id='data_ingestion',
        bash_command='''
            export HADOOP_HOME=/opt/homebrew/opt/hadoop/libexec &&
            export PATH=$PATH:$HADOOP_HOME/bin &&
            hdfs dfs -test -e /user/accidents/raw/US_Accidents_March23.csv &&
            hdfs dfs -du -h /user/accidents/raw/US_Accidents_March23.csv &&
            echo "Raw data verified on HDFS" &&
            echo "Data ingestion complete"
        ''',
    )

    # REAL Task 4 - Actually runs Spark cleaning script
    spark_cleaning = BashOperator(
        task_id='spark_cleaning',
        bash_command='''
            export SPARK_HOME=/opt/homebrew/opt/apache-spark/libexec &&
            export HADOOP_HOME=/opt/homebrew/opt/hadoop/libexec &&
            export PATH=$PATH:$SPARK_HOME/bin:$HADOOP_HOME/bin &&
            spark-submit \
                --master spark://localhost:7077 \
                --executor-memory 4g \
                --driver-memory 2g \
                /Users/sanjaybharvad/us_accidents_project/scripts/2_clean.py &&
            echo "Cleaning complete"
        ''',
    )

    # REAL Task 5 - Actually runs Spark EDA script
    spark_eda = BashOperator(
        task_id='spark_eda',
        bash_command='''
            export SPARK_HOME=/opt/homebrew/opt/apache-spark/libexec &&
            export HADOOP_HOME=/opt/homebrew/opt/hadoop/libexec &&
            export PATH=$PATH:$SPARK_HOME/bin:$HADOOP_HOME/bin &&
            spark-submit \
                --master spark://localhost:7077 \
                --executor-memory 4g \
                --driver-memory 2g \
                /Users/sanjaybharvad/us_accidents_project/scripts/3_eda.py &&
            echo "EDA complete"
        ''',
    )

    # REAL Task 6 - Actually trains ML models via Spark
    ml_models = BashOperator(
        task_id='ml_models',
        bash_command='''
            export SPARK_HOME=/opt/homebrew/opt/apache-spark/libexec &&
            export HADOOP_HOME=/opt/homebrew/opt/hadoop/libexec &&
            export PATH=$PATH:$SPARK_HOME/bin:$HADOOP_HOME/bin &&
            spark-submit \
                --master spark://localhost:7077 \
                --executor-memory 4g \
                --driver-memory 2g \
                /Users/sanjaybharvad/us_accidents_project/scripts/4_ml.py &&
            echo "ML models complete"
        ''',
    )

    # REAL Task 7 - Actually verifies all outputs exist on HDFS
    pipeline_complete = BashOperator(
        task_id='pipeline_complete',
        bash_command='''
            export HADOOP_HOME=/opt/homebrew/opt/hadoop/libexec &&
            export PATH=$PATH:$HADOOP_HOME/bin &&
            echo "Verifying all outputs..." &&
            hdfs dfs -ls /user/accidents/cleaned/ &&
            hdfs dfs -ls /user/accidents/outputs/ &&
            hdfs dfs -ls /user/accidents/ml_ready/ &&
            hdfs dfs -du -h /user/accidents/ &&
            echo "========================================" &&
            echo "US Accidents Pipeline Complete!" &&
            echo "All data verified on HDFS"
            echo "========================================"
        ''',
    )

    check_hdfs >> check_spark >> data_ingestion >> spark_cleaning >> spark_eda >> ml_models >> pipeline_complete