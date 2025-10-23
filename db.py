# db.py
import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            chat_id INTEGER
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username, chat_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?)", (user_id, username, chat_id))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT chat_id FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
