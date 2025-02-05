"""
user_sessions.py
Manages user conversation states in sessions.db
"""

import sqlite3
import json
import time
import os
import logging

DB_FILE = "sessions.db"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            chat_id TEXT PRIMARY KEY,
            state TEXT,
            inputs TEXT,
            last_updated REAL
        )
    ''')
    conn.commit()
    conn.close()
    logger.debug("Initialized sessions table for user sessions.")

def get_session(chat_id):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT state, inputs FROM sessions WHERE chat_id=?", (str(chat_id),))
    row = c.fetchone()
    conn.close()
    if row:
        state, inputs_json = row
        inputs = json.loads(inputs_json) if inputs_json else {}
        return {"state": state, "inputs": inputs}
    else:
        return None

def update_session(chat_id, state, inputs):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    inputs_json = json.dumps(inputs)
    timestamp = time.time()
    c.execute("REPLACE INTO sessions (chat_id, state, inputs, last_updated) VALUES (?, ?, ?, ?)",
              (str(chat_id), state, inputs_json, timestamp))
    conn.commit()
    conn.close()
    logger.debug(f"Updated session for chat_id={chat_id}, state={state}.")

def delete_session(chat_id):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM sessions WHERE chat_id=?", (str(chat_id),))
    conn.commit()
    conn.close()
    logger.debug(f"Deleted session for chat_id={chat_id}.")
