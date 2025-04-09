import sqlite3
import os

def init_db():
    # Create the database file if it doesn't exist
    if not os.path.exists('finance.db'):
        print("Creating new database file...")
    
    # Connect to the database
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    # Create the transactions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            notes TEXT
        )
    ''')
    
    # Check if the table is empty
    c.execute('SELECT COUNT(*) FROM transactions')
    count = c.fetchone()[0]
    
    if count == 0:
        print("Adding sample data...")
        # Add some sample transactions for the last 3 months
        sample_data = [
            # Last month
            ('2024-03-01', 'expense', 'food', 150.00, 'Grocery shopping'),
            ('2024-03-05', 'expense', 'rent', 1200.00, 'Monthly rent'),
            ('2024-03-10', 'expense', 'food', 80.00, 'Restaurant'),
            ('2024-03-15', 'expense', 'utilities', 100.00, 'Electricity bill'),
            ('2024-03-20', 'expense', 'food', 120.00, 'Grocery shopping'),
            ('2024-03-25', 'income', 'salary', 3000.00, 'Monthly salary'),
            
            # Two months ago
            ('2024-02-01', 'expense', 'food', 140.00, 'Grocery shopping'),
            ('2024-02-05', 'expense', 'rent', 1200.00, 'Monthly rent'),
            ('2024-02-12', 'expense', 'food', 90.00, 'Restaurant'),
            ('2024-02-15', 'expense', 'utilities', 95.00, 'Electricity bill'),
            ('2024-02-18', 'expense', 'food', 130.00, 'Grocery shopping'),
            ('2024-02-25', 'income', 'salary', 3000.00, 'Monthly salary'),
            
            # Three months ago
            ('2024-01-01', 'expense', 'food', 145.00, 'Grocery shopping'),
            ('2024-01-05', 'expense', 'rent', 1200.00, 'Monthly rent'),
            ('2024-01-10', 'expense', 'food', 75.00, 'Restaurant'),
            ('2024-01-15', 'expense', 'utilities', 98.00, 'Electricity bill'),
            ('2024-01-22', 'expense', 'food', 110.00, 'Grocery shopping'),
            ('2024-01-25', 'income', 'salary', 3000.00, 'Monthly salary'),
        ]
        
        c.executemany('''
            INSERT INTO transactions (date, type, category, amount, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_data)
        
        print(f"Added {len(sample_data)} sample transactions.")
    else:
        print(f"Database already contains {count} transactions.")
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    print("Database initialization complete.")

if __name__ == "__main__":
    init_db() 