# Real-Time Market Data ETL Pipeline

This project is an end-to-end Dockerized data engineering pipeline that simulates real-time market data ingestion, validates incoming records, performs transformations, and stores processed data into PostgreSQL.

The project was built using FastAPI, Python, PostgreSQL, Docker, and Pydantic validation.

---

# Architecture

FastAPI API → ETL Pipeline → PostgreSQL

**Key Stages of Project**

--API Endpoint--
 - Market Data API
 - GET /v1/market-data

--Fault Injection--
- To test ETL resiliency:
 - 5% of requests return HTTP 500 errors
 - 5% of responses return malformed data
 - This helps validate error handling and schema validation logic.

--ETL Workflow--

** Extraction
- Polls FastAPI endpoint periodically
- Handles API failures and malformed responses

** Validation
- Uses Pydantic schema validation
- Invalid records are dropped safely

** Transformation
- Calculates VWAP for each instrument
- Detects outlier prices

** Loading
- Stores validated records into PostgreSQL
- Prevents duplicate records using unique constraints

** VWAP Formula
 - VWAP = Σ(Price × Volume) / Σ(Volume)

** Outlier Detection
- A record is flagged as an outlier when:
  - abs(price - avg_price) / avg_price > 0.15

** Idempotency
- The pipeline prevents duplicate records using:
 - UNIQUE(instrument_id, timestamp)
and:
- ON CONFLICT DO NOTHING
 - This ensures retries do not create duplicate data.

** Logging
- The ETL logs:
 - Processed records
 - Dropped records
 - Validation failures
 - Execution time
