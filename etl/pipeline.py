import logging
import time
from collections import defaultdict

import psycopg2
import requests
from pydantic import ValidationError

from models import MarketData

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

API_URL = "http://api:8000/v1/market-data"

DB_CONFIG = {
    "host": "postgres",
    "dbname": "marketdb",
    "user": "postgres",
    "password": "alphapluscapital",
    "port": 5432
}


def fetch_market_data():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        return []


def validate_records(records):
    valid_records = []
    dropped = 0

    for record in records:
        try:
            validated = MarketData(**record)
            valid_records.append(validated)

        except ValidationError as e:
            dropped += 1
            logger.warning(f"Validation failed: {e}")

    return valid_records, dropped


def calculate_vwap(records):
    grouped = defaultdict(list)

    for record in records:
        grouped[record.instrument_id].append(record)

    vwap_map = {}

    for instrument, values in grouped.items():
        total_price_volume = sum(v.price * v.volume for v in values)
        total_volume = sum(v.volume for v in values)

        vwap = total_price_volume / total_volume
        vwap_map[instrument] = vwap

    return vwap_map


def detect_outliers(records):
    grouped = defaultdict(list)

    for record in records:
        grouped[record.instrument_id].append(record)

    outlier_map = {}

    for instrument, values in grouped.items():
        avg_price = sum(v.price for v in values) / len(values)

        for value in values:
            deviation = abs(value.price - avg_price) / avg_price
            outlier_map[
                (value.instrument_id, value.timestamp)
            ] = deviation > 0.15

    return outlier_map


def insert_records(records, vwap_map, outlier_map):
    connection = psycopg2.connect(**DB_CONFIG)

    cursor = connection.cursor()

    query = """
    INSERT INTO market_data (
        instrument_id,
        price,
        volume,
        timestamp,
        vwap,
        is_outlier
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (instrument_id, timestamp)
    DO NOTHING;
    """

    for record in records:
        cursor.execute(
            query,
            (
                record.instrument_id,
                record.price,
                record.volume,
                record.timestamp,
                vwap_map[record.instrument_id],
                outlier_map[
                    (record.instrument_id, record.timestamp)
                ]
            )
        )

    connection.commit()

    cursor.close()
    connection.close()


def run_pipeline():
    start_time = time.time()

    raw_records = fetch_market_data()

    valid_records, dropped = validate_records(raw_records)

    if not valid_records:
        logger.warning("No valid records found")
        return

    vwap_map = calculate_vwap(valid_records)

    outlier_map = detect_outliers(valid_records)

    insert_records(valid_records, vwap_map, outlier_map)

    execution_time = round(time.time() - start_time, 2)

    logger.info(
        f"processed={len(valid_records)} "
        f"dropped={dropped} "
        f"execution_time={execution_time}s"
    )


if __name__ == "__main__":

    print("Waiting for PostgreSQL to start...")
    time.sleep(20)

    while True:
        try:
            run_pipeline()
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")

        time.sleep(10)