import sqlite3
from db_init import DB_FILE

def test_add_transaction():
    """Add a test transaction and verify it's saved correctly."""
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Add a test transaction
        test_transaction = {
            'type': 'expense',
            'amount': 50.00,
            'category': 'food',
            'date': '2025-04-09'
        }
        
        cursor.execute(
            'INSERT INTO transactions (type, amount, category, date) VALUES (?, ?, ?, ?)',
            (test_transaction['type'], test_transaction['amount'], 
             test_transaction['category'], test_transaction['date'])
        )
        conn.commit()
        
        # Get the ID of the inserted transaction
        transaction_id = cursor.lastrowid
        
        # Verify the transaction was saved correctly
        cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
        saved_transaction = cursor.fetchone()
        
        # Close the connection
        conn.close()
        
        # Check if the saved transaction matches what we inserted
        if saved_transaction:
            print("Test transaction added successfully!")
            print(f"ID: {saved_transaction[0]}")
            print(f"Type: {saved_transaction[1]}")
            print(f"Amount: ${saved_transaction[2]:.2f}")
            print(f"Category: {saved_transaction[3]}")
            print(f"Date: {saved_transaction[4]}")
            return True
        else:
            print("Error: Transaction was not saved correctly.")
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_add_transaction() 