import sqlite3

DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            chat_id INTEGER PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()


def add_user(chat_id: int):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users(chat_id) VALUES(?)",
        (chat_id,)
    )

    conn.commit()
    conn.close()


def get_users():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT chat_id FROM users")

    users = [row[0] for row in cur.fetchall()]

    conn.close()

    return users


def remove_user(chat_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM users WHERE chat_id=?",
        (chat_id,)
    )

    conn.commit()
    conn.close()
