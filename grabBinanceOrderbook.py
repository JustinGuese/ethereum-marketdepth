from os import environ, path

import pandas as pd
import requests
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://" + environ["PSQL_URI"])


def oneLoop(symbol: str = "ETHTUSD"):
    r = requests.get("https://api.binance.com/api/v3/depth", params=dict(symbol=symbol))
    results = r.json()
    price_summary = {
        side: pd.DataFrame(
            data=results[side], columns=["price", "quantity"], dtype=float
        )
        for side in ["bids", "asks"]
    }

    # Concatenate DataFrames directly
    price_summary = pd.concat(
        [price_summary[side].assign(side=side) for side in price_summary],
        axis="index",
        ignore_index=True,
        sort=True,
    )

    # Calculate spread and spread percentage while aggregating
    price_summary = (
        price_summary.groupby("side")
        .agg(
            {
                "price": ["min", "max", "mean", "median"],
                "quantity": ["count", "sum", "min", "max", "mean", "median"],
            }
        )
        .reset_index()
    )
    price_summary.columns = [
        "side",
        "min",
        "max",
        "mean",
        "median",
        "quantity_count",
        "quantity_sum",
        "quantity_min",
        "quantity_max",
        "quantity_mean",
        "quantity_median",
    ]
    price_summary["timestamp"] = pd.Timestamp.now()
    price_summary["symbol"] = symbol
    price_summary["month"] = price_summary["timestamp"].dt.month
    price_summary["year"] = price_summary["timestamp"].dt.year
    price_summary = price_summary.set_index("timestamp")
    return price_summary


if __name__ == "__main__":
    symbol = environ.get("SYMBOL", "ETHTUSD")
    logevery = int(environ.get("LOGEVERY", 100))
    loopcnt = 0
    startTime = pd.Timestamp.now()
    while True:
        try:
            price_summary = oneLoop(symbol)
            price_summary.to_sql("binance_orderbook", engine, if_exists="append")

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            break
