# US Accidents Big Data Analysis

**CMPE / DATA 228 — Big Data Technologies**
San José State University · Spring 2026

## Team
| Name | Role |
|------|------|
| Mansi Deshmukh | Data Pipeline & EDA |
| Md. Faiq Salman | ML Models & Evaluation |
| Sanjay Bharvad | Infrastructure & Airflow |
| Sharan Patil | Dashboards & Demo |

---

## Project Overview

A end-to-end big data pipeline that ingests, processes, analyzes, and builds machine learning models on the **US Accidents dataset** — 7.49 million accident records across 49 US states from 2016 to 2023.

The pipeline uses **Apache Hadoop HDFS** for distributed storage, **Apache Spark** for large-scale data processing and ML training, and **Apache Airflow** for automated pipeline orchestration.

---

## Dataset

| Property | Value |
|----------|-------|
| Source | Kaggle — Sobhan Moosavi |
| Period | February 2016 – March 2023 |
| Raw records | 7,728,394 |
| Clean records | 7,493,637 |
| Features | 46 original → 51 engineered |
| Raw size | 3 GB CSV |
| Stored size | 672 MB Parquet (HDFS) |
| States covered | 49 US states |
| Cities covered | 13,679 cities |

**Why this dataset is complex:**
- 7.49M rows exceed single-machine Pandas limits
- Multi-modal features: temporal, geographic, weather, road conditions
- Class imbalance in severity (82% Level 2)
- Missing values across 20+ columns requiring imputation
- Requires distributed computing for efficient processing

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Storage | Apache Hadoop HDFS | 3.5.0 |
| Processing | Apache Spark (PySpark) | 4.1.1 |
| Orchestration | Apache Airflow (Docker) | 2.9.0 |
| ML | Spark MLlib | built-in |
| API | Flask | 3.0 |
| Frontend | HTML + Chart.js | 4.4.1 |
| Language | Python | 3.11 / 3.14 |

---

## Architecture

```
Raw CSV (3GB)
     ↓
HDFS /user/accidents/raw/          ← Hadoop HDFS storage
     ↓
Spark Cleaning & Feature Eng.      ← PySpark ETL
     ↓
HDFS /user/accidents/cleaned/      ← 672MB Parquet
     ↓
Spark EDA & Aggregations           ← 15 output CSVs
     ↓
HDFS /user/accidents/outputs/      ← Analysis results
     ↓
Spark MLlib Training               ← 3 ML models
     ↓
HDFS /user/accidents/ml_ready/     ← 200MB ML dataset
     ↓
Flask Live Demo + Dashboards       ← Visualization
```

---

## HDFS Storage Layout

```
/user/accidents/
├── raw/           2.8 GB   original CSV upload
├── cleaned/       672 MB   cleaned Parquet (snappy)
├── ml_ready/      200 MB   feature-engineered Parquet
└── outputs/        15 MB   15 EDA result CSV files
```

---

## Data Pipeline

### Cleaning Steps
1. Removed exact duplicate rows
2. Dropped rows with null Severity, Start_Time, State, City
3. Filled numeric nulls with median values
4. Filled categorical nulls with Unknown
5. Parsed timestamps to TimestampType
6. Saved to HDFS as Parquet with Snappy compression

### Engineered Features (46 → 51 columns)

| Feature | Source | Description |
|---------|--------|-------------|
| Hour | Start_Time | 0–23 integer |
| Month | Start_Time | 1–12 integer |
| Year | Start_Time | 2016–2023 |
| DayOfWeek | Start_Time | 1(Sun)–7(Sat) |
| DayName | DayOfWeek | Monday … Sunday |
| Duration_Min | Start/End_Time | (End − Start) ÷ 60 |
| Is_RushHour | Hour + DayOfWeek | 1 if 7–9AM or 4–6PM weekday |
| Is_Weekend | DayOfWeek | 1 if Saturday or Sunday |
| TimeOfDay | Hour | Morning/Afternoon/Evening/Night |
| Season | Month | Spring/Summer/Fall/Winter |

---

## EDA Key Findings

| Finding | Value |
|---------|-------|
| Peak accident hour | 7:00 AM (571,624 accidents) |
| Busiest day | Friday (1,325,866 accidents) |
| Top state | California (1,689,207 accidents) |
| Top city | Miami, FL (183,122 accidents) |
| Most common weather | Fair (2,533,374 accidents) |
| Most dangerous season | Winter (2,187,025 accidents) |
| Average severity | 2.21 out of 4.0 |
| Rush hour accidents | 3,034,613 (40.5% of total) |

---

## Machine Learning Models

### Model 1 — Severity Prediction (Random Forest)

| Metric | Value |
|--------|-------|
| Algorithm | Random Forest Classifier |
| Target | Severity Level 1, 2, 3, 4 |
| Trees | 30 |
| Max depth | 8 |
| Train/Test split | 80/20 |
| Accuracy | **80.17%** |
| F1 Score | 0.7242 |
| Baseline | 70% naive |

### Model 2 — Duration Prediction (Linear Regression)

| Metric | Value |
|--------|-------|
| Algorithm | Linear Regression |
| Target | Accident duration (minutes) |
| Max iterations | 10 |
| RMSE | 121.23 minutes |
| MAE | 74.12 minutes |
| R² Score | 0.0379 |

### Model 3 — Rush Hour Prediction (Logistic Regression)

| Metric | Value |
|--------|-------|
| Algorithm | Logistic Regression |
| Target | Is Rush Hour (0 or 1) |
| Max iterations | 10 |
| Accuracy | 59.43% |
| AUC ROC | 0.5521 |
| Best case | 87.1% probability (CA/7AM/Friday) |

---

## Airflow Pipeline

DAG: `us_accidents_pipeline` · Schedule: `@weekly` · Docker · Airflow 2.9.0

```
check_hdfs → check_spark → data_ingestion → spark_cleaning → spark_eda → ml_models → pipeline_complete
```

| Task | Operator | Description |
|------|----------|-------------|
| check_hdfs | BashOperator | Verify HDFS is running |
| check_spark | BashOperator | Verify Spark is running |
| data_ingestion | BashOperator | Verify raw data on HDFS |
| spark_cleaning | BashOperator | Run Spark cleaning job |
| spark_eda | BashOperator | Run Spark EDA job |
| ml_models | BashOperator | Train ML models |
| pipeline_complete | BashOperator | Pipeline completion check |

All 7 tasks completed successfully ✅

---

## Project Structure

```
us_accidents_project/
├── notebooks/
│   └── Main.ipynb                    ← Full pipeline: EDA + ML models
├── airflow-docker/
│   ├── docker-compose.yaml           ← Airflow Docker setup
│   └── dags/
│       └── us_accidents_pipeline.py  ← Airflow DAG definition
├── demo/
│   ├── app.py                        ← Flask live prediction app
│   └── templates/
│       └── index.html                ← Demo frontend
├── charts/
│   ├── accidents_by_year.png
│   ├── accidents_by_hour.png
│   ├── accidents_by_day.png
│   ├── accidents_by_season.png
│   ├── accidents_by_timeofday.png
│   ├── severity_distribution.png
│   ├── top_10_states.png
│   ├── top_10_cities.png
│   ├── top_weather_conditions.png
│   └── rushhour_vs_normal.png
└── README.md
```

---

## How to Run

### Prerequisites
- Apache Hadoop 3.5.0
- Apache Spark 4.1.1
- Docker Desktop
- Python 3.11+
- Jupyter Lab

### Step 1 — Start Infrastructure
```bash
start-dfs.sh
start-master.sh
start-worker.sh spark://localhost:7077
```

### Step 2 — Upload Data to HDFS
```bash
hdfs dfs -mkdir -p /user/accidents/raw
hdfs dfs -put US_Accidents_March23.csv /user/accidents/raw/
```

### Step 3 — Run Jupyter Notebook
```bash
jupyter notebook
```
Open `notebooks/Main.ipynb` and run all cells.

### Step 4 — Start Airflow Pipeline
```bash
cd airflow-docker
docker compose up -d
```
Open `http://localhost:8085` — login: `airflow` / `airflow`

### Step 5 — Run Live Demo
```bash
cd demo
pip3 install flask
python3 app.py
```
Open `http://localhost:5000`

---

## Live Demo

The Flask app allows real-time predictions using all 3 ML models.

**Input:** State, City, Hour, Day, Weather, Temperature, Humidity, Visibility, Wind Speed, Road Features

**Output:**
- Severity Level (1–4) with confidence
- Accident Duration (minutes)
- Rush Hour prediction (Yes/No) with probability

**Example predictions:**

| Scenario | Severity | Duration | Rush Hour |
|----------|----------|----------|-----------|
| CA, Friday 7AM, Light Rain | Level 3 | ~95 min | YES 87.1% |
| MN, Sunday 3AM, Heavy Snow | Level 4 | ~180 min | NO |
| FL, Saturday 2PM, Fair | Level 2 | ~45 min | NO |

---

## Dashboards

Two interactive HTML dashboards with live filters:

**Dashboard 1 — Temporal Analysis**
- Filters: Season, Severity Level, Time of Day
- Charts: Accidents by year, hour, season, day of week, month, time of day

**Dashboard 2 — Geographic & Severity**
- Filters: Weather condition, Region, Severity Level
- Charts: Top states, top cities, severity distribution, weather conditions, ML results

---

## Results Summary

| Metric | Value |
|--------|-------|
| Total records processed | 7,493,637 |
| Data retained after cleaning | 97% |
| Storage compression | 78% (3GB → 672MB) |
| ML model accuracy (best) | 80.17% |
| Pipeline tasks | 7 |
| EDA outputs | 15 CSV files |
| Interactive dashboards | 2 |
| States covered | 49 |

---

## References

- Moosavi, S., Samavatian, M. H., Parthasarathy, S., & Ramnath, R. (2019). A countrywide traffic accident dataset. arXiv preprint arXiv:1906.05409
- Dataset: https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents
- Apache Spark MLlib: https://spark.apache.org/mllib/
- Apache Airflow: https://airflow.apache.org/
- Apache Hadoop: https://hadoop.apache.org/
