# user_sessions.py

import json
import time
import logging
from database_manager import get_connection, put_connection, init_db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def init_sessions_table():
    # Ensure the sessions table exists (already done in init_db, but you can call again if needed)
    init_db()

def get_session(chat_id):
    init_sessions_table()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT state, inputs FROM sessions WHERE chat_id=%s", (str(chat_id),))
    row = cur.fetchone()
    cur.close()
    put_connection(conn)
    if row:
        state, inputs_json = row
        inputs = json.loads(inputs_json) if inputs_json else {}
        return {"state": state, "inputs": inputs}
    else:
        return None

def update_session(chat_id, state, inputs):
    init_sessions_table()
    conn = get_connection()
    cur = conn.cursor()
    inputs_json = json.dumps(inputs)
    timestamp = time.time()
    # Use ON CONFLICT to update or insert
    cur.execute("""
        INSERT INTO sessions (chat_id, state, inputs, last_updated)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (chat_id)
        DO UPDATE SET
            state = EXCLUDED.state,
            inputs = EXCLUDED.inputs,
            last_updated = EXCLUDED.last_updated
    """, (str(chat_id), state, inputs_json, timestamp))
    conn.commit()
    cur.close()
    put_connection(conn)
    logger.debug(f"Updated session for chat_id={chat_id}, state={state}.")

def delete_session(chat_id):
    init_sessions_table()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM sessions WHERE chat_id=%s", (str(chat_id),))
    conn.commit()
    cur.close()
    put_connection(conn)
    logger.debug(f"Deleted session for chat_id={chat_id}.")
