"""
database_manager.py
Handles SQLite database connections for caching market data.
We store:
  - crypto_ohlc (symbol TEXT, date TEXT, open REAL, high REAL, low REAL, close REAL)
  - usd_ohlc
  - gold_ohlc
"""

import sqlite3
import logging
import os

DB_FILE = "market_data.db"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.makedirs('logs', exist_ok=True)

def init_db():
    """Initialize the database (create tables if not exist)."""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # For general crypto pairs on Binance
        c.execute('''
            CREATE TABLE IF NOT EXISTS crypto_ohlc (
                symbol TEXT,
                date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                PRIMARY KEY (symbol, date)
            )
        ''')

        # For USD/IRR
        c.execute('''
            CREATE TABLE IF NOT EXISTS usd_ohlc (
                date TEXT PRIMARY KEY,
                open REAL,
                high REAL,
                low REAL,
                close REAL
            )
        ''')

        # For Gold IRR or Gold USD
        c.execute('''
            CREATE TABLE IF NOT EXISTS gold_ohlc (
                date TEXT PRIMARY KEY,
                open REAL,
                high REAL,
                low REAL,
                close REAL
            )
        ''')

        conn.commit()
        conn.close()
        logger.info("Database tables initialized or already exist.")
    except Exception as e:
        logger.error(f"Error initializing DB: {e}", exc_info=True)
        raise

def get_connection():
    """Return a sqlite3 connection object."""
    init_db()
    return sqlite3.connect(DB_FILE)
