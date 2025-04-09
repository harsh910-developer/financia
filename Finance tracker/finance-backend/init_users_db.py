import sqlite3
from werkzeug.security import generate_password_hash

def init_users_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Add foreign key to transactions table
    c.execute('''
        ALTER TABLE transactions 
        ADD COLUMN user_id INTEGER REFERENCES users(id)
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_users_db()
    print("Users database initialized successfully!") 