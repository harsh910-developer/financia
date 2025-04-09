import sqlite3
from datetime import datetime, timedelta
import random

# Connect to the database
conn = sqlite3.connect('finance.db')
c = conn.cursor()

# Clear existing data (optional)
c.execute('DELETE FROM transactions')
conn.commit()

# Sample categories
categories = ['food', 'rent', 'entertainment', 'utilities', 'transportation', 'other']

# Generate sample data for the past 3 months
today = datetime.now()
start_date = today - timedelta(days=90)  # 3 months ago

# Sample data for each category
sample_data = {
    'food': {'min': 50, 'max': 200, 'frequency': 15},  # 15 transactions per month
    'rent': {'min': 800, 'max': 1000, 'frequency': 1},  # 1 transaction per month
    'entertainment': {'min': 20, 'max': 100, 'frequency': 5},  # 5 transactions per month
    'utilities': {'min': 50, 'max': 150, 'frequency': 3},  # 3 transactions per month
    'transportation': {'min': 30, 'max': 80, 'frequency': 8},  # 8 transactions per month
    'other': {'min': 10, 'max': 50, 'frequency': 10}  # 10 transactions per month
}

# Generate transactions
for category, params in sample_data.items():
    # Calculate how many transactions to create
    num_transactions = params['frequency'] * 3  # 3 months worth
    
    for _ in range(num_transactions):
        # Generate a random date within the past 3 months
        days_ago = random.randint(0, 90)
        transaction_date = (start_date + timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Generate a random amount
        amount = round(random.uniform(params['min'], params['max']), 2)
        
        # Insert the transaction
        c.execute('''
            INSERT INTO transactions (date, type, category, amount, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (transaction_date, 'expense', category, amount, f'Sample {category} transaction'))
        
        # Add some income transactions too
        if random.random() < 0.2:  # 20% chance of income
            income_amount = round(random.uniform(500, 2000), 2)
            c.execute('''
                INSERT INTO transactions (date, type, category, amount, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (transaction_date, 'income', 'salary', income_amount, 'Sample income'))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Sample data added successfully!") 