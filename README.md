# US Accidents Big Data Analysis

## Team
Mansi Deshmukh · Md. Faiq Salman · Sanjay Bharvad · Sharan Patil

## Course
CMPE/DATA 228 — Big Data Technologies · SJSU · Spring 2026

## Tech Stack
- Apache Hadoop HDFS 3.5.0
- Apache Spark 4.1.1 (PySpark)
- Apache Airflow 2.9.0 (Docker)
- Spark MLlib
- Flask (Python)

## Dataset
US Accidents 2016-2023 — 7.49M records — Kaggle (sobhanmoosavi)

## Project Structure
- notebooks/Main.ipynb — Full pipeline: EDA + Cleaning + ML Models
- airflow-docker/dags/ — Airflow DAG
- demo/ — Flask live demo app
- charts/ — Generated visualizations

## Results
- Random Forest Accuracy: 80.17%
- 3 ML Models trained on 7.49M records
- 7-task Airflow DAG pipeline
- 2 interactive dashboards
