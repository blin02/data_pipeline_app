# 📄 Donation Data Pipeline: Design Document

## 📋 Overview

This document outlines the architecture, design choices, and implementation details for a donation data pipeline created for a take-home assignment. The pipeline ingests, validates, transforms, and aggregates donation data in a modular, scalable, and testable way.

---

## 🎯 Goals

* Ingest raw donation data in multiple formats (JSON, CSV, Parquet)
* Validate schema and enforce data quality
* Transform raw data with enriched features
* Produce aggregated metrics for reporting
* Structure the pipeline to support scaling and production-readiness
* Provide automated tests for key logic

---

## 🧱 Architecture

### 📂 Components

* **Ingestion Layer**: Loads files from disk and validates schema.
* **Transformation Layer**: Adds derived columns and computes aggregations.
* **Storage Layer**: Writes outputs in Parquet format to staged and final directories.
* **Testing Layer**: Validates correctness of ingestion and transformation logic.

### 🧩 Technologies

* Python 3.8+
* Pandas
* Pandera (schema validation)
* Pytest (unit testing)

### 📁 Directory Structure

```
project_root/
├── service/
│   ├── base_service.py
│   ├── donation_ingestion_service.py
│   └── donation_transformation_service.py
├── constant/
│   ├── data.py
│   └── schema.py
├── tests/
│   ├── test_ingestion.py
│   ├── test_transformation.py
│   └── README.md
├── temp/data/
│   ├── stage/
│   └── final/
└── resources/
    └── donations_1.json
```

---

## 🔄 Pipeline Flow

### 1. **Ingestion & Validation**

* Input files are read based on file type (`DataFormat` enum).
* A schema is defined using `pandera`, and invalid rows are captured separately.

### 2. **Transformation**

* A `donation_date` column is extracted from the timestamp.
* Two types of aggregations are performed:

  * Donations per campaign per day
  * Donations per day
* Future enrichments can include features like donor tiering and recurrence.

### 3. **Storage**

* Outputs are saved as Parquet files to the `/stage` and `/final` directories.
* Partitioning is designed but not implemented in the prototype.

### 4. **Testing**

* Unit tests cover valid and invalid data cases.
* Transformations are verified through grouped aggregations.

---

## ⚖️ Design Considerations

### ✅ Tradeoffs Made

* **Used Pandas instead of Spark**: Simpler for small-scale demo, with a note that Spark would be used for production-scale data.
* **Schema validation with Pandera**: Lightweight and Python-native, ideal for prototyping.
* **File-based staging**: Easier to test and inspect vs. DB-based staging.

### 🧠 Future Improvements

* Add support for incremental loads (merge new data with historical roll-ups).
* Integrate into orchestration tools like Airflow or Dagster.
* Use dbt for SQL-based transformations.
* Stream ingestion via Kafka or AWS Kinesis.
* Add data quality alerts and lineage tracking.

---

## 📦 Output Summary

| File                                               | Description                           |
| -------------------------------------------------- | ------------------------------------- |
| `donation_1_output.parquet`                        | Validated donation data               |
| `donation_1_raw.parquet`                           | Enriched raw donation records         |
| `donation_1_donation_per_day.parquet`              | Aggregated donations per day          |
| `donation_1_donation_per_campaign_per_day.parquet` | Aggregated donations per campaign/day |

---

## ✅ Conclusion

This pipeline demonstrates clean modular design, schema-driven validation, and practical transformation logic — with room to scale toward production. It’s structured for maintainability, testability, and future growth.

---

*Authored by: \[Your Name]*
