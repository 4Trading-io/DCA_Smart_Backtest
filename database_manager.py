# database_manager.py
"""
database_manager.py
Handles PostgreSQL database connections and schema creation.
"""

import os
import logging
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from credentials import postgres_user, postgres_pass, postgress_table
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Environment variables for best practice in production
POSTGRES_HOST =  "localhost"
POSTGRES_PORT =  "5432"
POSTGRES_DB   = postgress_table
POSTGRES_USER = postgres_user
POSTGRES_PASS = postgres_pass

# Initialize a connection pool (tune minconn/maxconn as needed)
MINCONN = 1
MAXCONN = 10
pool = SimpleConnectionPool(
    MINCONN, MAXCONN,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASS
)

def get_connection():
    """
    Obtain a connection from the pool.
    You MUST call `put_connection(conn)` when done to return it.
    """
    return pool.getconn()

def put_connection(conn):
    """
    Return a connection to the pool.
    """
    pool.putconn(conn)

def init_db():
    """
    Create all needed tables if they don't exist yet.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Create the crypto_ohlc table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS crypto_ohlc (
                symbol TEXT NOT NULL,
                date TEXT NOT NULL,
                open DOUBLE PRECISION,
                high DOUBLE PRECISION,
                low DOUBLE PRECISION,
                close DOUBLE PRECISION,
                PRIMARY KEY (symbol, date)
            );
        ''')

        # For USD/IRR
        cur.execute('''
            CREATE TABLE IF NOT EXISTS usd_ohlc (
                date TEXT PRIMARY KEY,
                open DOUBLE PRECISION,
                high DOUBLE PRECISION,
                low  DOUBLE PRECISION,
                close DOUBLE PRECISION
            );
        ''')

        # For Gold IRR or Gold USD
        cur.execute('''
            CREATE TABLE IF NOT EXISTS gold_ohlc (
                date TEXT PRIMARY KEY,
                open DOUBLE PRECISION,
                high DOUBLE PRECISION,
                low  DOUBLE PRECISION,
                close DOUBLE PRECISION
            );
        ''')

        # For user sessions (moved from sessions.db to Postgres)
        cur.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                chat_id TEXT PRIMARY KEY,
                state TEXT,
                inputs TEXT,
                last_updated DOUBLE PRECISION
            );
        ''')

        conn.commit()
        cur.close()
        put_connection(conn)
        logger.info("Database tables initialized (or already exist).")

    except Exception as e:
        logger.error(f"Error initializing DB: {e}", exc_info=True)
        raise
