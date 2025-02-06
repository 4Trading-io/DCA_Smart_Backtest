# data_preprocessing.py
"""
data_preprocessing.py
Fetches OHLC from DB for either:
 - crypto_ohlc (4h or daily), filtered by user-chosen symbol
 - gold_ohlc (daily)
Then we parse them accordingly, keep full timestamps, and compute returns.
"""

import logging
import pandas as pd
from datetime import datetime
from cache_manager import fetch_cached_data
from database_manager import get_connection, put_connection, init_db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_crypto_data(symbol_pair, start_date="2020-01-01", end_date="2030-01-01"):
    """
    Pull from crypto_ohlc for the given `symbol_pair`.
    Return a DataFrame [Date, Open, High, Low, Close, Return].
    Possibly multiple rows per day (4h).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT date, open, high, low, close
        FROM crypto_ohlc
        WHERE symbol=%s 
          AND date >= %s
          AND date <= %s
        ORDER BY date ASC
    ''', (symbol_pair, start_date, end_date))
    rows = cur.fetchall()
    cur.close()
    put_connection(conn)

    df = pd.DataFrame(rows, columns=['date','Open','High','Low','Close'])
    if df.empty:
        logger.warning(f"No data returned for {symbol_pair} in range {start_date}..{end_date}.")
        return df

    df['Date'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S", errors='coerce')
    df['Date'] = df['Date'].fillna(pd.to_datetime(df['date'], format="%Y-%m-%d", errors='coerce'))
    df.drop(columns=['date'], inplace=True)
    df.sort_values(by='Date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    df['Return'] = df['Close'].pct_change()
    logger.debug(f"get_crypto_data({symbol_pair}): {len(df)} rows. Head:\n{df.head(5)}")
    return df

def get_gold_data(start_date="2020-01-01", end_date="2030-01-01"):
    """
    Pull from gold_ohlc. 
    Returns a daily DF [Date, Open, High, Low, Close, Return].
    """
    rows = fetch_cached_data("gold_ohlc", start_date, end_date)
    df = pd.DataFrame(rows)
    if df.empty:
        logger.warning(f"No gold data in range {start_date}..{end_date}.")
        return df

    df.rename(columns={'open':'Open','high':'High','low':'Low','close':'Close'}, inplace=True)
    df['Date'] = pd.to_datetime(df['date'], format="%Y-%m-%d", errors='coerce')
    df.drop(columns=['date'], inplace=True)
    df.sort_values(by='Date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['Return'] = df['Close'].pct_change()
    logger.debug(f"get_gold_data: {len(df)} rows. Head:\n{df.head(5)}")
    return df
