"""
binance_data.py
Download data at 4-hour intervals from Binance for any symbol (e.g. BTCUSDT, ETHUSDT).
Stores in 'crypto_ohlc' with symbol + date as primary key.

FIX: We pass symbol=symbol_pair to get_missing_date_ranges to ensure
     symbol-based coverage check is used.
"""

import requests
import logging
import time
from datetime import datetime
from cache_manager import get_missing_date_ranges, insert_ohlc_data
from database_manager import init_db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BINANCE_API_URL = "https://api.binance.com/api/v3/klines"
INTERVAL = "4h"  # or "1d"

def date_to_millis(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return int(dt.timestamp() * 1000)

def download_binance_klines(symbol_pair, interval, start_ts, end_ts):
    """
    Download klines from Binance in the given TS range. Returns raw klines array.
    """
    all_klines = []
    limit = 1000
    cur_ts = start_ts
    while cur_ts < end_ts:
        params = {
            "symbol": symbol_pair,
            "interval": interval,
            "startTime": cur_ts,
            "endTime": end_ts,
            "limit": limit
        }
        try:
            resp = requests.get(BINANCE_API_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
            if not data:
                break
            all_klines.extend(data)
            last_close_time = data[-1][6]
            cur_ts = last_close_time + 1
            time.sleep(0.4)  # rate limit
        except Exception as e:
            logger.error(f"Error fetching Binance klines for {symbol_pair}: {e}", exc_info=True)
            time.sleep(2)
    return all_klines

def binance_klines_to_ohlc(klines, symbol_pair):
    """
    Convert raw klines to a list of { symbol, date, open, high, low, close }
    each row is a 4h candle.
    """
    from datetime import datetime
    results = []
    for k in klines:
        open_time_ms = k[0]
        open_price   = float(k[1])
        high_price   = float(k[2])
        low_price    = float(k[3])
        close_price  = float(k[4])

        dt_str = datetime.utcfromtimestamp(open_time_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")

        results.append({
            'symbol': symbol_pair,
            'date': dt_str,
            'open': open_price,
            'high': high_price,
            'low':  low_price,
            'close':close_price
        })
    return results

def download_binance_data(symbol_pair, start_date, end_date):
    """
    Ensure 'symbol_pair' data is cached from [start_date, end_date].
    We'll do a symbol-based coverage check so that if there's no data for BTCUSDT,
    it triggers a full download even if some other symbol is present.
    """
    logger.info(f"=== Downloading {symbol_pair} data for {start_date} to {end_date} ===")
    init_db()

    try:
        # Pass the symbol param so it's symbol-based coverage
        missing_ranges = get_missing_date_ranges("crypto_ohlc", start_date, end_date, symbol=symbol_pair)
    except ValueError as e:
        logger.error(f"Error checking missing range for {symbol_pair}: {e}", exc_info=True)
        # We can fallback to a full range if desired
        logger.info(f"Symbol param error => forcing a full download for {symbol_pair}.")
        missing_ranges = [(start_date, end_date)]

    if not missing_ranges:
        logger.info(f"{symbol_pair} data fully cached for that range. No download needed.")
        return

    for (m_start, m_end) in missing_ranges:
        logger.info(f"Downloading missing range: {m_start} to {m_end} for {symbol_pair}")
        start_ts = date_to_millis(m_start)
        end_ts   = date_to_millis(m_end)
        klines   = download_binance_klines(symbol_pair, INTERVAL, start_ts, end_ts)
        if klines:
            ohlc     = binance_klines_to_ohlc(klines, symbol_pair)
            insert_ohlc_data("crypto_ohlc", ohlc)
        else:
            logger.warning(f"No klines fetched from Binance for {symbol_pair} in range {m_start}..{m_end}")
    logger.info(f"=== Finished {symbol_pair} data updates ===")
