import sqlite3
from datetime import datetime

def get_transactions():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    
    # Query to get expenses grouped by category and month
    query = """
    SELECT 
        category,
        strftime('%Y-%m', date) as month,
        COUNT(*) as transaction_count,
        SUM(amount) as total_amount
    FROM transactions 
    WHERE type = 'expense'
    GROUP BY category, month
    ORDER BY month DESC, total_amount DESC;
    """
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            print("No expense transactions found in the database.")
            return
        
        current_month = None
        for row in results:
            category, month, count, total = row
            
            # Print month header when month changes
            if month != current_month:
                print(f"\n=== {month} ===")
                current_month = month
            
            # Print category details
            print(f"Category: {category}")
            print(f"Number of transactions: {count}")
            print(f"Total amount: ${total:.2f}")
            print("-" * 30)
            
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        if "no such table" in str(e):
            print("The transactions table doesn't exist. Please run db_init.py first.")
    finally:
        conn.close()

if __name__ == "__main__":
    get_transactions() 