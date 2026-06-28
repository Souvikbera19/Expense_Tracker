import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(os.path.dirname(BASE_DIR), "database.db")
def get_conn():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn
    
def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(50) NOT NULL,
            full_name VARCHAR(50) NOT NULL,
            hashed_password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            created_at TEXT,
            user_id INTEGER REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()

    
if __name__ == "__main__":
    init_db()
    
        
    