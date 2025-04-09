import sqlite3
import os

# Database file path
DB_FILE = 'transactions.db'

def init_db():
    """Initialize the database and create tables if they don't exist."""
    # Check if database file exists
    db_exists = os.path.exists(DB_FILE)
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create transactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL
    )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    # Return whether this was a new database
    return not db_exists

if __name__ == "__main__":
    # Run this script directly to initialize the database
    is_new = init_db()
    if is_new:
        print(f"Created new database at {DB_FILE}")
    else:
        print(f"Database already exists at {DB_FILE}") 