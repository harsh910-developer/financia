import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
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

    # Create transactions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            notes TEXT,
            user_id INTEGER REFERENCES users(id)
        )
    ''')

    # Create a test user if it doesn't exist
    test_email = 'hindustaniboy89@gmail.com'
    test_password = 'enqueand'
    
    c.execute('SELECT * FROM users WHERE email = ?', (test_email,))
    if not c.fetchone():
        password_hash = generate_password_hash(test_password)
        c.execute('INSERT INTO users (email, password_hash) VALUES (?, ?)',
                 (test_email, password_hash))
        print(f"Created test user: {test_email}")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!") 