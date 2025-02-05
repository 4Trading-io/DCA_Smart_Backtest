"""
cache_manager.py
Contains utility functions for:
  - Determining missing date ranges (symbol-based for crypto_ohlc)
  - Inserting OHLC data
  - Fetching cached data
"""

import logging
import datetime
from database_manager import get_connection

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def insert_ohlc_data(table_name, ohlc_data):
    """
    Insert or replace multiple rows into:
      - crypto_ohlc (symbol, date, open, high, low, close)
      - gold_ohlc   (date, open, high, low, close)
      - usd_ohlc    (date, open, high, low, close)
    """
    try:
        if not ohlc_data:
            logger.warning(f"No data to insert into {table_name}. Skipping.")
            return
        conn = get_connection()
        c = conn.cursor()

        if table_name == "crypto_ohlc":
            sql = f"""
            INSERT OR REPLACE INTO {table_name}
            (symbol, date, open, high, low, close)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            rows_to_insert = []
            for row in ohlc_data:
                rows_to_insert.append((
                    row.get('symbol', ''),
                    row.get('date', ''),
                    row.get('open', 0.0),
                    row.get('high', 0.0),
                    row.get('low',  0.0),
                    row.get('close',0.0)
                ))
            c.executemany(sql, rows_to_insert)
            logger.info(f"Inserted/updated {len(rows_to_insert)} records into {table_name}.")
        else:
            # gold_ohlc, usd_ohlc
            sql = f"""
            INSERT OR REPLACE INTO {table_name} (date, open, high, low, close)
            VALUES (?, ?, ?, ?, ?)
            """
            rows_to_insert = []
            for row in ohlc_data:
                rows_to_insert.append((
                    row.get('date', ''),
                    row.get('open', 0.0),
                    row.get('high', 0.0),
                    row.get('low',  0.0),
                    row.get('close',0.0)
                ))
            c.executemany(sql, rows_to_insert)
            logger.info(f"Inserted/updated {len(rows_to_insert)} records into {table_name}.")

        conn.commit()
        conn.close()

    except Exception as e:
        logger.error(f"Error inserting data into {table_name}: {e}", exc_info=True)
        raise

def get_cached_dates_for_crypto(symbol):
    """
    Returns a set of all 'date' values stored in crypto_ohlc for the given symbol.
    """
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT date FROM crypto_ohlc
            WHERE symbol=?
        """, (symbol,))
        rows = c.fetchall()
        conn.close()
        return set(r[0] for r in rows)
    except Exception as e:
        logger.error(f"Error getting cached dates for {symbol} in crypto_ohlc: {e}", exc_info=True)
        return set()

def get_cached_dates(table_name):
    """
    For gold_ohlc or usd_ohlc, we just return all date strings in that table.
    (Used if you want to do daily coverage logic.)
    """
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(f"SELECT date FROM {table_name}")
        rows = c.fetchall()
        conn.close()
        return set(r[0] for r in rows)
    except Exception as e:
        logger.error(f"Error getting cached dates for {table_name}: {e}", exc_info=True)
        return set()

def get_missing_date_ranges(table_name, start_date, end_date, symbol=None):
    """
    Determine which portions of [start_date, end_date] are not cached.
    If table_name == "crypto_ohlc", we do symbol-based coverage. (Need symbol param)
    If table_name in ("gold_ohlc","usd_ohlc"), we do old coverage ignoring symbol.

    Returns a list of (start, end) tuples for missing daily coverage.
    Currently returns at most one chunk if partially missing.
    """
    try:
        start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_dt   = datetime.datetime.strptime(end_date,   "%Y-%m-%d")

        all_required = []
        delta_days = (end_dt - start_dt).days
        for i in range(delta_days+1):
            day = (start_dt + datetime.timedelta(days=i))
            all_required.append(day)

        if table_name == "crypto_ohlc":
            if not symbol:
                raise ValueError("Must provide 'symbol' for crypto coverage check.")

            # get cached dates *for that symbol*
            cached_dates = get_cached_dates_for_crypto(symbol)
        else:
            # gold_ohlc or usd_ohlc
            cached_dates = get_cached_dates(table_name)

        # Convert cached to daily datetimes by substring
        cached_datetimes = set()
        for d_str in cached_dates:
            day_str = d_str[:10]  # "YYYY-MM-DD"
            try:
                c_dt = datetime.datetime.strptime(day_str, "%Y-%m-%d")
                cached_datetimes.add(c_dt)
            except:
                pass

        missing = sorted(d for d in all_required if d not in cached_datetimes)
        if not missing:
            logger.info(f"No missing dates in {table_name} for {symbol or ''} from {start_date} to {end_date}.")
            return []

        return [(missing[0].strftime("%Y-%m-%d"), missing[-1].strftime("%Y-%m-%d"))]

    except Exception as e:
        logger.error(f"Error getting missing date ranges for {table_name}: {e}", exc_info=True)
        return []

def fetch_cached_data(table_name, start_date, end_date):
    """
    Retrieve data from table_name for [start_date, end_date], ignoring symbol.
    Typically used for gold_ohlc or usd_ohlc.
    For crypto_ohlc by symbol, you'd do a separate custom query.
    """
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(f'''
          SELECT date, open, high, low, close
          FROM {table_name}
          WHERE date >= ? AND date <= ?
          ORDER BY date ASC
        ''', (start_date, end_date))
        rows = c.fetchall()
        conn.close()

        data = []
        for r in rows:
            data.append({
                'date': r[0],
                'open': r[1],
                'high': r[2],
                'low':  r[3],
                'close':r[4],
            })
        logger.debug(f"Fetched {len(data)} rows from {table_name} in range [{start_date}, {end_date}].")
        return data
    except Exception as e:
        logger.error(f"Error fetching data from {table_name}: {e}", exc_info=True)
        return []
