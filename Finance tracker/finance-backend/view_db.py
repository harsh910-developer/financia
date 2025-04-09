import sqlite3

def view_database():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    # View users table
    print("\n=== Users Table ===")
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    for user in users:
        print(f"ID: {user[0]}, Email: {user[1]}, Created At: {user[3]}")
    
    # View transactions table
    print("\n=== Transactions Table ===")
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()
    for trans in transactions:
        print(f"ID: {trans[0]}, Date: {trans[1]}, Type: {trans[2]}, Category: {trans[3]}, Amount: ${trans[4]}, Notes: {trans[5]}, User ID: {trans[6]}")
    
    conn.close()

if __name__ == "__main__":
    view_database() 