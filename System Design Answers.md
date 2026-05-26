**System Design Answers**
1. Scaling :

if the data volume increased to 1 billion events per day, the architecture can be scaled using:

Kafka or Amazon Kinesis for streaming ingestion
AWS Glue or Spark for distributed ETL processing
Amazon S3 for scalable storage
Redshift or Snowflake for analytics
Airflow or Step Functions for orchestration

This improves scalability and fault tolerance for large-scale data processing.

2. Monitoring :

Health checks can be implemented using:

API /health endpoint
Structured logging
CloudWatch or Prometheus/Grafana monitoring
Alerts for ETL failures and high latency
Database connectivity checks

This helps monitor pipeline health and detect failures quickly.

3. Recovery & Idempotency :

The pipeline ensures idempotent processing using:

Composite unique constraints
ON CONFLICT DO NOTHING
Validation before inserts
Retry-safe ETL execution

This prevents duplicate or partial data during retries or failures.

---Future AWS Extension---

This local Dockerized architecture can be extended into AWS-native services:

**Local Component to	AWS Equivalent**
FastAPI	ECS / API Gateway
PostgreSQL /	Amazon RDS
ETL Service	AWS Glue / Lambda
Logging /	CloudWatch
Streaming /	Kinesis
Storage	 / Amazon S3
