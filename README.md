# Crop Yield Prediction Pipeline (Work in Progress)

## 📌 Project Overview

The goal of this project is to build an **end-to-end data pipeline** that will ultimately support a **machine learning model to predict crop yield across the United States**.

This repository focuses on building a **solid data engineering foundation**, including:
- ingesting data from web-based APIs,
- performing light transformations and data quality checks,
- storing raw data in a transactional database (PostgreSQL),
- and preparing the data to be later processed in a data warehouse / lakehouse environment.

This is a **learning and portfolio project**, designed to reflect real-world data workflows rather than a one-off analysis.

---

## 🧱 High-Level Architecture

### Planned workflow

1. **Data Sources (Web APIs)**
   - NASA POWER API (weather data)
   - USDA NASS QuickStats API (crop yield data)

2. **Ingestion Layer (Python)**
   - API calls return JSON
   - Parsed into Pandas DataFrames
   - Minimal validation and light transformations

3. **OLTP Storage (PostgreSQL)**
   - Raw tables (`raw` schema)
   - Idempotent loads (truncate + reload)
   - Preserves raw structure for traceability

4. **Analytics / Lakehouse Layer (Planned)**
   - Databricks (Silver layer: heavy transformations)
   - Gold layer: aggregated datasets for ML and dashboards

5. **Machine Learning (Planned)**
   - Feature engineering
   - Crop yield prediction models

---

## 📊 Data Sources

### NASA POWER API — Weather Data

- Monthly weather observations
- Variables currently ingested:
  - Average temperature (°C)
  - Precipitation (mm)
  - Solar radiation
- **Current scope:**  
  Weather data is ingested **one location (latitude/longitude) at a time**
- **Planned scope:**  
  Extend ingestion to cover **all U.S. states**, using state-level centroids or equivalent geographic mapping

This staged approach keeps the pipeline simple initially while allowing future scalability.

---

### USDA NASS QuickStats API — Crop Yield Data

- Annual crop yield data
- State-level aggregation
- Focus on U.S. crops (e.g., corn)
- Returned in JSON format and ingested into Pandas DataFrames

---

## ⚙️ Current Implementation Status

### ✅ Completed

- API connections to NASA POWER and USDA NASS
- JSON → Pandas DataFrame ingestion using `requests` and `pandas`
- Initial transformations:
  - year and month extraction
  - basic filtering and data quality checks
- PostgreSQL setup:
  - database, schema, and raw tables
- End-to-end ETL pipeline for weather data:
  - Extract → Transform → Load
  - Idempotent loads using `TRUNCATE TABLE … RESTART IDENTITY`
- Secure credential handling using `.env` and `.gitignore`
- Reusable SQLAlchemy engine function for database connections

### 🚧 In Progress

- ETL pipeline for USDA crop yield data
- Weather ingestion across all U.S. states (looping over locations)

### 🔜 Planned

- Load curated data into Databricks
- Heavy data cleaning and feature engineering (Silver layer)
- Aggregation tables for analytics and dashboards (Gold layer)
- Machine learning models for crop yield prediction

---

## 🛠️ Tech Stack

### Languages & Libraries
- **Python**
  - pandas
  - requests
  - SQLAlchemy
  - python-dotenv

### Databases
- **PostgreSQL**
  - OLTP / raw ingestion layer

### Data Engineering Concepts
- ETL pipelines
- Idempotent data loads
- Environment-based configuration
- Schema alignment between DataFrames and database tables

### Planned
- Databricks
- Machine learning (scikit-learn or similar)

---


## 🚀 How to Run
```bash
python main.py
```

## 📁 Project Structure

```
crop_yield/
│
├── src/
│   ├── api/
│   │   ├── nasa_weather.py
│   │   └── usda_yield.py
│   ├── etl/
│   │   ├── etl_weather.py
│   │   └── etl_yield.py
│
├── db/
│   └── engine_call.py
│
├── notebooks/
│   ├── api_weather_test.ipynb
│   └── api_yield_test.ipynb
│   ├── etl_weather_test.ipynb
│   └── etl_yield_test.ipynb
│
├── data/
│   └── soil_properties.csv
│   └── state_loc.csv
│
├── .env
├── requirements.txt
├── .gitignore
├── README.md
└── main.py
```

## 📌 Notes

This project prioritizes correct architecture and data flow over premature optimization.

Heavy transformations and machine learning are intentionally deferred until a reliable ingestion and storage layer is fully established.

## 🔗 API Documentation Links
- NASA POWER API (weather conditions): https://power.larc.nasa.gov/docs/services/api/temporal/

- USDA NASS API (agriculture data): https://quickstats.nass.usda.gov/api#param_define

