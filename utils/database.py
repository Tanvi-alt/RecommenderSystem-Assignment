import sqlite3
import os

# ==========================================
# DATABASE PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

db_path = os.path.join(
    BASE_DIR,
    "database",
    "users.db"
)

# ==========================================
# DATABASE CONNECTION
# ==========================================

conn = sqlite3.connect(
    db_path,
    check_same_thread=False
)

cursor = conn.cursor()

# ==========================================
# CREATE USERS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# ==========================================
# CREATE HISTORY TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    movie TEXT
)
""")

conn.commit()

# ==========================================
# SAVE HISTORY
# ==========================================

def save_history(username, movie):
    cursor.execute(
        "INSERT INTO history(username, movie) VALUES (?, ?)",
        (username, movie)
    )
    conn.commit()

# ==========================================
# GET HISTORY
# ==========================================

def get_history(username):
    cursor.execute(
        "SELECT movie FROM history WHERE username=?",
        (username,)
    )
    data = cursor.fetchall()
    return [i[0] for i in data]

# ==========================================
# REMOVE HISTORY (NEW)
# ==========================================

def remove_history(username, movie):
    """
    Deletes a specific movie from the user's watch history.
    """
    cursor.execute(
        "DELETE FROM history WHERE username=? AND movie=?",
        (username, movie)
    )
    conn.commit()