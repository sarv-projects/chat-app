import sqlite3

DB_NAME = "chat.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room TEXT,
            username TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_message(room, username, content):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO messages (room, username, content) VALUES (?, ?, ?)", (room, username, content))
    conn.commit()
    conn.close()

def get_recent_messages(room):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT username, content, timestamp
        FROM messages
        WHERE room = ?
          AND timestamp >= datetime('now', '-7 days')
        ORDER BY timestamp ASC
    """, (room,))
    rows = c.fetchall()
    conn.close()
    return rows
