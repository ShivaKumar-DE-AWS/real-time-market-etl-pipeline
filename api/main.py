from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone
import random

app = FastAPI()

INSTRUMENTS = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "BTC-USD",
    "ETH-USD"
]

@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/v1/market-data")
def get_market_data():
    fault_chance = random.random()

    if fault_chance < 0.05:
        raise HTTPException(status_code=500, detail="Injected server error")

    data = []

    for instrument in INSTRUMENTS:
        record = {
            "instrument_id": instrument,
            "price": round(random.uniform(100, 1000), 2),
            "volume": round(random.uniform(10, 10000), 2),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        data.append(record)

    if 0.05 <= fault_chance < 0.10:
        data[0]["price"] = "INVALID_PRICE"

    return data