"""
navasan_data.py
We add a forward-fill step for USD data so that every day has a valid price.
"""

import requests
import jdatetime
import logging
import time
import os
import pandas as pd
from datetime import datetime
from cache_manager import insert_ohlc_data, fetch_cached_data
from database_manager import init_db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

API_KEY = "freeYM34bO6B5FJWe7sZ6q8UDrktMjuy"
BASE_URL = "http://api.navasan.tech/ohlcSearch/"

def persian_to_gregorian(persian_date_str):
    y, m, d = map(int, persian_date_str.split('-'))
    import jdatetime
    gdate = jdatetime.date(y, m, d).togregorian()
    return gdate.strftime("%Y-%m-%d")

def fetch_navasan_data(item, start_shamsi, end_shamsi):
    params = {
        "api_key": API_KEY,
        "item": item,
        "start": start_shamsi,
        "end": end_shamsi
    }
    try:
        logger.info(f"Requesting {item} from Navasan: {start_shamsi} -> {end_shamsi}")
        resp = requests.get(BASE_URL, params=params)
        resp.raise_for_status()
        raw = resp.json()
        cleaned = []
        for row in raw:
            gdate = persian_to_gregorian(row['date'])
            cleaned.append({
                'date': gdate,
                'open': float(row.get('open', 0.0)),
                'high': float(row.get('high', 0.0)),
                'low':  float(row.get('low',  0.0)),
                'close':float(row.get('close',0.0)),
            })
        logger.info(f"Fetched {len(cleaned)} records for {item}.")
        return cleaned
    except Exception as e:
        logger.error(f"Error fetching {item} from Navasan: {e}", exc_info=True)
        return []

def download_usd_data(start_shamsi, end_shamsi):
    init_db()
    data = fetch_navasan_data("usd_sell", start_shamsi, end_shamsi)
    insert_ohlc_data("usd_ohlc", data)

def download_gold_data(start_shamsi, end_shamsi):
    init_db()
    data = fetch_navasan_data("18ayar", start_shamsi, end_shamsi)
    insert_ohlc_data("gold_ohlc", data)

def forward_fill_usd_data():
    """
    1. Load all USD data from the DB.
    2. Convert to a DataFrame, parse dates, sort.
    3. Reindex to a daily range with forward-fill so that *every day* has a valid close.
    4. Re-insert into the DB with the newly filled rows.
       (Optional, or we can keep the forward-filled DataFrame in memory for the next step.)
    """
    logger.info("Starting forward-fill for USD data to handle missing days.")
    usd_all = fetch_cached_data("usd_ohlc", "0000-01-01", "9999-12-31")
    if not usd_all:
        logger.warning("No USD data found, cannot forward-fill.")
        return

    df = pd.DataFrame(usd_all)
    df['Date'] = pd.to_datetime(df['date'], format="%Y-%m-%d", errors='coerce')
    df.drop(columns=['date'], inplace=True, errors='ignore')
    df.sort_values('Date', inplace=True)
    df.set_index('Date', inplace=True)

    # We reindex daily from min to max
    all_days = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    df = df.reindex(all_days)
    df[['open','high','low','close']] = df[['open','high','low','close']].ffill()

    # Now df has no missing days, each day is forward-filled.
    # We can re-insert into DB if we want the DB to store all these new rows:
    fill_data = []
    for idx, row in df.iterrows():
        fill_data.append({
            'date': idx.strftime("%Y-%m-%d"),
            'open': row['open'] if not pd.isnull(row['open']) else 0.0,
            'high': row['high'] if not pd.isnull(row['high']) else 0.0,
            'low':  row['low']  if not pd.isnull(row['low'])  else 0.0,
            'close':row['close']if not pd.isnull(row['close'])else 0.0
        })
    insert_ohlc_data("usd_ohlc", fill_data)
    logger.info("USD forward-fill completed and reinserted into DB.")

def convert_gold_to_usd():
    """
    Convert gold_ohlc from IRR to USD using matching or forward-filled USD close.
    We'll do a simple approach:
      1) forward_fill_usd_data() so the DB has a valid close for every day
      2) fetch the gold_ohlc and usd_ohlc again
      3) do the IRR->USD division day by day
      4) re-insert updated gold data
    """
    forward_fill_usd_data()  # ensure USD is fully daily and filled

    gold_all = fetch_cached_data("gold_ohlc", "0000-01-01", "9999-12-31")
    if not gold_all:
        logger.warning("No gold data to convert.")
        return

    usd_all  = fetch_cached_data("usd_ohlc",  "0000-01-01", "9999-12-31")
    usd_map  = {u['date']: u for u in usd_all if u['close'] != 0}

    updated = []
    for g in gold_all:
        date_str = g['date']
        usd = usd_map.get(date_str, None)
        if usd:
            factor = float(usd['close'])
            if factor > 0:
                g['open']  = round(g['open'] / factor, 4)
                g['high']  = round(g['high'] / factor, 4)
                g['low']   = round(g['low']  / factor, 4)
                g['close'] = round(g['close']/ factor, 4)
        updated.append(g)

    logger.info(f"Converted {len(updated)} gold records from IRR to USD using forward-filled USD.")
    insert_ohlc_data("gold_ohlc", updated)

def main_download_and_convert_gold(start_shamsi, end_shamsi):
    logger.info(f"=== Downloading USD & Gold from Navasan in range {start_shamsi}-{end_shamsi} ===")
    download_usd_data(start_shamsi, end_shamsi)
    download_gold_data(start_shamsi, end_shamsi)
    # Now convert IRR -> USD with forward fill
    convert_gold_to_usd()
    logger.info("Finished Gold & USD updates (with forward fill).")
