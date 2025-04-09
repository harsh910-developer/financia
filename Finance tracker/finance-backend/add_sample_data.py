import sqlite3
from datetime import datetime, timedelta
import random

def add_sample_transactions():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    # Get the user ID
    c.execute("SELECT id FROM users WHERE email = ?", ('hindustaniboy89@gmail.com',))
    user_id = c.fetchone()[0]
    
    # Categories and their typical ranges
    categories = {
        'food': (20, 100),
        'rent': (800, 1200),
        'utilities': (50, 200),
        'entertainment': (20, 150),
        'transportation': (10, 50)
    }
    
    # Generate transactions for the last 3 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    current_date = start_date
    
    transactions = []
    while current_date <= end_date:
        # 2-3 transactions per day
        for _ in range(random.randint(2, 3)):
            category = random.choice(list(categories.keys()))
            min_amount, max_amount = categories[category]
            amount = round(random.uniform(min_amount, max_amount), 2)
            
            transactions.append((
                current_date.strftime('%Y-%m-%d'),
                'expense',
                category,
                amount,
                f'Sample {category} expense',
                user_id
            ))
        
        current_date += timedelta(days=1)
    
    # Insert transactions
    c.executemany('''
        INSERT INTO transactions (date, type, category, amount, notes, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', transactions)
    
    conn.commit()
    print(f"Added {len(transactions)} sample transactions")
    conn.close()

if __name__ == "__main__":
    add_sample_transactions() 