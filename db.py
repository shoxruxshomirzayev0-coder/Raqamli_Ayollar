import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

# Jadval yaratish
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    title TEXT,
    url TEXT,
    thumbnail TEXT
)
""")

conn.commit()

def add_category(name):
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()

def get_categories():
    return cursor.execute("SELECT * FROM categories").fetchall()

def add_video(cat_id, title, url, thumb):
    cursor.execute("INSERT INTO videos (category_id, title, url, thumbnail) VALUES (?, ?, ?, ?)",
                   (cat_id, title, url, thumb))
    conn.commit()

def get_videos(cat_id):
    return cursor.execute("SELECT * FROM videos WHERE category_id=?", (cat_id,)).fetchall()