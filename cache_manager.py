# cache_manager.py
"""
cache_manager.py
Contains utility functions for:
  - Determining missing date ranges (symbol-based for crypto_ohlc)
  - Inserting OHLC data (using PostgreSQL ON CONFLICT)
  - Fetching cached data
"""

import logging
import datetime
from database_manager import get_connection, put_connection, init_db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def insert_ohlc_data(table_name, ohlc_data):
    """
    Insert or upsert multiple rows into:
      - crypto_ohlc (symbol, date, open, high, low, close)
      - gold_ohlc   (date, open, high, low, close)
      - usd_ohlc    (date, open, high, low, close)

    Using PostgreSQL "ON CONFLICT DO UPDATE" to mimic "INSERT OR REPLACE".
    """
    try:
        if not ohlc_data:
            logger.warning(f"No data to insert into {table_name}. Skipping.")
            return

        conn = get_connection()
        cur = conn.cursor()

        if table_name == "crypto_ohlc":
            # Upsert by (symbol,date)
            sql = f"""
            INSERT INTO {table_name} (symbol, date, open, high, low, close)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol, date)
            DO UPDATE SET
                open  = EXCLUDED.open,
                high  = EXCLUDED.high,
                low   = EXCLUDED.low,
                close = EXCLUDED.close
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
            cur.executemany(sql, rows_to_insert)
            logger.info(f"Upserted {len(rows_to_insert)} records into {table_name}.")

        else:
            # gold_ohlc or usd_ohlc, upsert by (date)
            sql = f"""
            INSERT INTO {table_name} (date, open, high, low, close)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (date)
            DO UPDATE SET
                open  = EXCLUDED.open,
                high  = EXCLUDED.high,
                low   = EXCLUDED.low,
                close = EXCLUDED.close
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
            cur.executemany(sql, rows_to_insert)
            logger.info(f"Upserted {len(rows_to_insert)} records into {table_name}.")

        conn.commit()
        cur.close()
        put_connection(conn)

    except Exception as e:
        logger.error(f"Error inserting data into {table_name}: {e}", exc_info=True)
        raise

def get_cached_dates_for_crypto(symbol):
    """
    Returns a set of all 'date' values stored in crypto_ohlc for the given symbol.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT date FROM crypto_ohlc
            WHERE symbol=%s
        """, (symbol,))
        rows = cur.fetchall()
        cur.close()
        put_connection(conn)
        return set(r[0] for r in rows)

    except Exception as e:
        logger.error(f"Error getting cached dates for {symbol} in crypto_ohlc: {e}", exc_info=True)
        return set()

def get_cached_dates(table_name):
    """
    For gold_ohlc or usd_ohlc, we just return all date strings in that table.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT date FROM {table_name}")
        rows = cur.fetchall()
        cur.close()
        put_connection(conn)
        return set(r[0] for r in rows)
    except Exception as e:
        logger.error(f"Error getting cached dates for {table_name}: {e}", exc_info=True)
        return set()

def get_missing_date_ranges(table_name, start_date, end_date, symbol=None):
    """
    Determine which portions of [start_date, end_date] are not cached.
    If table_name == "crypto_ohlc", we do symbol-based coverage. (Need symbol param)
    If table_name in ("gold_ohlc","usd_ohlc"), we do coverage ignoring symbol.

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
            cached_dates = get_cached_dates_for_crypto(symbol)
        else:
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
        cur = conn.cursor()
        cur.execute(f'''
          SELECT date, open, high, low, close
          FROM {table_name}
          WHERE date >= %s AND date <= %s
          ORDER BY date ASC
        ''', (start_date, end_date))
        rows = cur.fetchall()
        cur.close()
        put_connection(conn)

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
