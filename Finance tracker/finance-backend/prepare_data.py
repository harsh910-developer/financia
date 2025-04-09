import sqlite3
import pandas as pd
from datetime import datetime

def prepare_data():
    """
    Prepare transaction data by:
    1. Converting dates to month numbers
    2. Calculating total spending per category per month
    """
    try:
        # Connect to the database
        conn = sqlite3.connect('transactions.db')
        
        # Query to get all transactions
        query = """
        SELECT 
            id,
            type,
            amount,
            category,
            date
        FROM transactions
        ORDER BY date DESC
        """
        
        # Load data into a pandas DataFrame
        df = pd.read_sql_query(query, conn)
        
        if df.empty:
            print("No transactions found in the database.")
            return
        
        # Convert date strings to datetime objects
        df['date'] = pd.to_datetime(df['date'])
        
        # Extract month and year
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        df['month_name'] = df['date'].dt.strftime('%B')
        df['month_year'] = df['date'].dt.strftime('%B %Y')
        
        # Filter for expenses only
        expenses_df = df[df['type'] == 'expense'].copy()
        
        if expenses_df.empty:
            print("No expense transactions found.")
            return
        
        # Calculate total spending per category per month
        spending_by_category_month = expenses_df.groupby(['category', 'month_year', 'month', 'year'])['amount'].sum().reset_index()
        spending_by_category_month = spending_by_category_month.sort_values(['year', 'month', 'amount'], ascending=[False, False, False])
        
        # Print results
        print("\n=== SPENDING BY CATEGORY AND MONTH ===")
        print(f"Total number of transactions: {len(df)}")
        print(f"Total number of expense transactions: {len(expenses_df)}")
        
        current_month = None
        for _, row in spending_by_category_month.iterrows():
            if row['month_year'] != current_month:
                print(f"\n=== {row['month_year']} (Month: {row['month']}) ===")
                current_month = row['month_year']
            
            print(f"Category: {row['category']}")
            print(f"Total amount: ${row['amount']:.2f}")
            print("-" * 30)
        
        # Calculate total spending per month
        spending_by_month = expenses_df.groupby('month_year')['amount'].sum().reset_index()
        spending_by_month = spending_by_month.sort_values('amount', ascending=False)
        
        print("\n=== TOTAL SPENDING BY MONTH ===")
        for _, row in spending_by_month.iterrows():
            print(f"{row['month_year']}: ${row['amount']:.2f}")
        
        # Save processed data to CSV for further analysis
        expenses_df.to_csv('processed_expenses.csv', index=False)
        print("\nProcessed data saved to 'processed_expenses.csv'")
        
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        if "no such table" in str(e):
            print("The transactions table does not exist. Please run db_init.py first.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    prepare_data() 