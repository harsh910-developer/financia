from flask import Flask, request, jsonify, send_file, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
import jwt
import os
from functools import wraps

app = Flask(__name__)
# Update CORS to allow all localhost ports
CORS(app, origins=["http://localhost:*"], supports_credentials=True)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Replace with a secure secret key

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

# Root endpoint
@app.route('/')
def home():
    return jsonify({"message": "Finance Tracker API", "status": "running"})

# Authentication middleware
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorated

# Authentication routes
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400
    
    try:
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        
        # Check if user exists
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        if c.fetchone():
            return jsonify({'message': 'Email already registered'}), 409
        
        # Create new user
        password_hash = generate_password_hash(password)
        c.execute('INSERT INTO users (email, password_hash) VALUES (?, ?)',
                 (email, password_hash))
        conn.commit()
        
        # Get the new user's ID
        c.execute('SELECT id FROM users WHERE email = ?', (email,))
        user_id = c.fetchone()[0]
        
        # Generate token
        token = jwt.encode(
            {'user_id': user_id, 'email': email},
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user': {'id': user_id, 'email': email}
        }), 201
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400
    
    try:
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        
        # Get user
        c.execute('SELECT id, email, password_hash FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        
        if not user or not check_password_hash(user[2], password):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        # Generate token
        token = jwt.encode(
            {'user_id': user[0], 'email': user[1]},
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        
        return jsonify({
            'token': token,
            'user': {'id': user[0], 'email': user[1]}
        })
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

# Protected routes
@app.route('/api/transactions', methods=['GET'])
@token_required
def get_transactions(current_user_id):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC', (current_user_id,))
    transactions = []
    for row in c.fetchall():
        transactions.append({
            'id': row[0],
            'date': row[1],
            'type': row[2],
            'category': row[3],
            'amount': row[4],
            'notes': row[5],
            'user_id': row[6]
        })
    conn.close()
    return jsonify(transactions)

@app.route('/api/transactions', methods=['POST'])
@token_required
def add_transaction(current_user_id):
    data = request.json
    
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT INTO transactions (type, amount, category, date, notes, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['type'], data['amount'], data['category'], 
              data['date'], data.get('notes', ''), current_user_id))
        
        conn.commit()
        transaction_id = c.lastrowid
        
        # Fetch the newly created transaction
        c.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
        row = c.fetchone()
        transaction = {
            'id': row[0],
            'date': row[1],
            'type': row[2],
            'category': row[3],
            'amount': row[4],
            'notes': row[5],
            'user_id': row[6]
        }
        
        return jsonify(transaction), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/predict/<category>', methods=['GET'])
@token_required
def predict_spending(current_user_id, category):
    """
    Endpoint for predicting spending for a specific category
    """
    try:
        # Get current month and year
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        
        # Get current month's spending so far
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        # Query for current month's spending
        cursor.execute('''
            SELECT SUM(amount)
            FROM transactions
            WHERE type = 'expense'
            AND category = ?
            AND strftime('%m', date) = ?
            AND strftime('%Y', date) = ?
        ''', (category, f"{current_month:02d}", str(current_year)))
        
        current_spending = cursor.fetchone()[0] or 0.0
        
        # Get historical monthly totals for the last 3 months
        cursor.execute('''
            SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
            FROM transactions
            WHERE type = 'expense'
            AND category = ?
            GROUP BY month
            ORDER BY month DESC
            LIMIT 3
        ''', (category,))
        
        historical_totals = [row[1] or 0.0 for row in cursor.fetchall()]
        
        # Calculate average monthly spending
        avg_monthly = sum(historical_totals) / len(historical_totals) if historical_totals else 0.0
        
        # Calculate month progress (as a percentage)
        days_in_month = 30  # Approximation
        day_of_month = now.day
        month_progress = (day_of_month / days_in_month) * 100
        
        # Calculate remaining predicted spending
        predicted_remaining = max(0, avg_monthly - current_spending)
        
        # Calculate projected total (current + remaining)
        projected_total = current_spending + predicted_remaining
        
        # Determine if spending is on track
        elapsed_portion = day_of_month / days_in_month
        expected_spending_so_far = avg_monthly * elapsed_portion
        warning = current_spending > expected_spending_so_far
        
        conn.close()
        
        # Convert all values to JSON-serializable types
        return jsonify({
            "category": category,
            "predicted_monthly": float(round(avg_monthly, 2)),
            "current_spending": float(round(current_spending, 2)),
            "predicted_remaining": float(round(predicted_remaining, 2)),
            "projected_total": float(round(projected_total, 2)),
            "month_progress": float(round(month_progress, 2)),
            "warning": bool(warning),
            "historical_monthly_totals": [float(round(total, 2)) for total in historical_totals]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export', methods=['GET'])
@token_required
def export_transactions(current_user_id):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC', (current_user_id,))
    transactions = []
    for row in c.fetchall():
        transactions.append({
            'id': row[0],
            'date': row[1],
            'type': row[2],
            'category': row[3],
            'amount': row[4],
            'notes': row[5],
            'user_id': row[6]
        })
    conn.close()
    
    # Export to CSV
    csv_file = 'transactions_export.csv'
    with open(csv_file, 'w') as f:
        for transaction in transactions:
            f.write(f"{transaction['date']},{transaction['type']},{transaction['category']},{transaction['amount']},{transaction['notes']},{transaction['user_id']}\n")
    
    return send_file(csv_file,
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name=f'transactions_{datetime.now().strftime("%Y%m%d")}.csv')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 