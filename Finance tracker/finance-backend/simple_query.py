import sqlite3

def main():
    try:
        # Connect to the database
        conn = sqlite3.connect('transactions.db')
        cursor = conn.cursor()
        
        # Get total number of transactions
        cursor.execute('SELECT COUNT(*) FROM transactions')
        total = cursor.fetchone()[0]
        print(f"\nTotal number of transactions: {total}")
        
        # Get expenses by category and month
        cursor.execute('''
            SELECT 
                category,
                strftime('%Y-%m', date) as month,
                COUNT(*) as count,
                SUM(amount) as total
            FROM transactions 
            WHERE type = 'expense'
            GROUP BY category, month
            ORDER BY month DESC, total DESC
        ''')
        
        results = cursor.fetchall()
        if not results:
            print("\nNo expense transactions found.")
        else:
            current_month = None
            for category, month, count, total in results:
                if month != current_month:
                    print(f"\n=== {month} ===")
                    current_month = month
                
                print(f"Category: {category}")
                print(f"Number of transactions: {count}")
                print(f"Total amount: ${total:.2f}")
                print("-" * 30)
    
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        if "no such table" in str(e):
            print("The transactions table does not exist. Please run db_init.py first.")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    main() 