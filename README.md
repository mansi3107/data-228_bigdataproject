# 🚗 US Accidents Big Data Analysis

## 📌 Project Overview
This project analyzes a large-scale US traffic accident dataset containing over 7.7 million records. Due to the size of the data, Big Data technologies are used to efficiently store, process, and analyze the dataset.

The goal of this project is to identify patterns and trends in road accidents based on factors like time, location, and severity.

## 🛠️ Technologies Used
- Docker (for cluster setup)
- Hadoop HDFS (distributed storage)
- Apache Spark (data processing)
- Jupyter Notebook (analysis & visualization)
- Python

## 📂 Dataset
- Source: US Accidents Dataset
- Size: ~7.7 million records
- Features include:
  - Time & Date
  - Location (State, City)
  - Weather conditions
  - Accident severity

## ⚙️ Project Workflow

### 1. Data Ingestion
- Uploaded dataset to HDFS
- Data split into multiple blocks and stored across nodes

### 2. Data Preprocessing
- Removed unnecessary columns
- Handled missing values
- Filtered invalid records

### 3. Feature Engineering
- Created new features:
  - Hour of accident
  - Day of week
  - Month
  - Rush hour indicator
  - Weekend indicator

### 4. Exploratory Data Analysis (EDA)
- Analyzed accident severity
- Identified top states with highest accidents
- Studied accident patterns by time

### 5. Data Storage
- Saved cleaned data in Parquet format

### 6. Visualization
- Bar chart for accident severity
- Bar chart for top states
- Line chart for accidents by hour

## 📊 Key Insights
- Most accidents are Severity 2
- California has the highest number of accidents
- Accidents peak during morning and evening rush hours
- Around 40% of accidents occur during rush hours

## 🚀 How to Run
1. Start Docker containers
2. Upload dataset to HDFS
3. Run Spark processing scripts
4. Use Jupyter Notebook for analysis and visualization

## 🎯 Conclusion
This project demonstrates how Hadoop and Spark can be used to process large datasets and extract meaningful insights about traffic accidents.

## 👥 Team Members
- Mansi
- Sharan
- Sanjay
- Faiq
