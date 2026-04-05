import sqlite3
import os

DB_PATH = "data/users.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create User Profiles Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            phone_number TEXT PRIMARY KEY,
            name TEXT,
            state TEXT,
            district TEXT,
            land_size REAL,
            caste TEXT,
            primary_crop TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def add_or_update_user(phone_number, name, state, district, land_size, caste, primary_crop):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (phone_number, name, state, district, land_size, caste, primary_crop)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(phone_number) 
        DO UPDATE SET 
            name=excluded.name,
            state=excluded.state,
            district=excluded.district,
            land_size=excluded.land_size,
            caste=excluded.caste,
            primary_crop=excluded.primary_crop
    ''', (phone_number, name, state, district, land_size, caste, primary_crop))
    
    conn.commit()
    conn.close()

def get_user(phone_number):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE phone_number = ?', (phone_number,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            "phone_number": user[0],
            "name": user[1],
            "state": user[2],
            "district": user[3],
            "land_size": user[4],
            "caste": user[5],
            "primary_crop": user[6]
        }
    return None

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    
    return [
        {
            "phone_number": u[0],
            "name": u[1],
            "state": u[2],
            "district": u[3],
            "land_size": u[4],
            "caste": u[5],
            "primary_crop": u[6]
        } for u in users
    ]

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
