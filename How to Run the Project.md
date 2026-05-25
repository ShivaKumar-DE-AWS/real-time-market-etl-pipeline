# How to Run the Project

## 1. Clone Repository

```bash
git clone https://github.com/ShivaKumar-DE-AWS/real-time-market-etl-pipeline.git
```

---

## 2. Move Into Project Directory

```bash
cd real-time-market-etl-pipeline
```

---

## 3. Create Environment File

Create a `.env` file in the project root.

Add:

```env
POSTGRES_DB=marketdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

---

## 4. Build and Start Containers

```bash
docker compose up --build
```

---

# Verify Services

## API Endpoint

Open browser:

```text
http://localhost:8000/v1/market-data
```

---

## Health Check

```text
http://localhost:8000/health
```

---

# Verify ETL Logs

```bash
docker compose logs etl
```

Expected logs:

```text
processed=5 dropped=0 execution_time=0.04s
```

---

# Verify Database Inserts

Open PostgreSQL container:

```bash
docker exec -it market_postgres psql -U postgres -d marketdb
```

Run SQL:

```sql
SELECT COUNT(*) FROM market_data;
```

---

# Stop Containers

```bash
docker compose down
```
