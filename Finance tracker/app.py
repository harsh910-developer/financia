from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import calendar
import csv
import io

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
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
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions ORDER BY date DESC')
    transactions = [
        {
            'id': row[0],
            'date': row[1],
            'type': row[2],
            'category': row[3],
            'amount': row[4],
            'notes': row[5]
        }
        for row in c.fetchall()
    ]
    conn.close()
    return jsonify(transactions)

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    if not all(k in data for k in ('date', 'type', 'category', 'amount')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO transactions (date, type, category, amount, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['date'],
        data['type'],
        data['category'],
        data['amount'],
        data.get('notes', '')
    ))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    
    return jsonify({
        'id': new_id,
        'date': data['date'],
        'type': data['type'],
        'category': data['category'],
        'amount': data['amount'],
        'notes': data.get('notes', '')
    }), 201

@app.route('/api/predict/<category>', methods=['GET'])
def predict_spending(category):
    """
    Predict spending for a specific category based on historical data.
    Uses a simple average of the last 3 months' spending as the prediction.
    """
    try:
        # Get current date info
        today = datetime.now()
        current_month = today.month
        current_year = today.year
        days_in_month = calendar.monthrange(current_year, current_month)[1]
        day_of_month = today.day
        
        # Calculate the fraction of the month that has passed
        month_progress = day_of_month / days_in_month
        
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        
        # Get current month's spending
        c.execute('''
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions 
            WHERE category = ? 
            AND type = 'expense'
            AND strftime('%Y-%m', date) = ?
        ''', (category, f"{current_year}-{current_month:02d}"))
        current_spending = c.fetchone()[0]
        
        # Get average monthly spending for the last 3 months (excluding current month)
        three_months_ago = datetime.now() - timedelta(days=90)
        c.execute('''
            SELECT strftime('%Y-%m', date) as month,
                   SUM(amount) as monthly_total
            FROM transactions
            WHERE category = ?
            AND type = 'expense'
            AND date >= ?
            AND strftime('%Y-%m', date) != ?
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month DESC
            LIMIT 3
        ''', (category, three_months_ago.strftime('%Y-%m-%d'), 
              f"{current_year}-{current_month:02d}"))
        
        monthly_totals = [row[1] for row in c.fetchall()]
        conn.close()
        
        # Calculate prediction based on average
        if monthly_totals:
            predicted_amount = sum(monthly_totals) / len(monthly_totals)
        else:
            # If no historical data, use current month's spending as prediction
            predicted_amount = current_spending if current_spending > 0 else 0
        
        # Calculate remaining budget and projected total
        predicted_remaining = predicted_amount - current_spending
        projected_total = (current_spending / month_progress) if month_progress > 0 else current_spending
        
        # Determine if we're approaching the predicted limit (>80% of prediction)
        warning = current_spending > (predicted_amount * 0.8) if predicted_amount > 0 else False
        
        return jsonify({
            'category': category,
            'predicted_monthly': round(predicted_amount, 2),
            'current_spending': round(current_spending, 2),
            'predicted_remaining': round(predicted_remaining, 2),
            'projected_total': round(projected_total, 2),
            'month_progress': round(month_progress * 100, 1),
            'warning': warning,
            'historical_monthly_totals': [round(x, 2) for x in monthly_totals]
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error calculating prediction: {str(e)}'
        }), 500

@app.route('/api/export', methods=['GET'])
def export_transactions():
    """
    Export all transactions as a CSV file.
    """
    try:
        # Create a StringIO object to write CSV data
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header row
        writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Notes'])
        
        # Fetch all transactions from database
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        c.execute('SELECT date, type, category, amount, notes FROM transactions ORDER BY date DESC')
        
        # Write transaction rows
        for row in c.fetchall():
            writer.writerow(row)
        
        conn.close()
        
        # Prepare the output
        output.seek(0)
        
        # Generate filename with current timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'transactions_export_{timestamp}.csv'
        
        # Return the CSV file
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            'error': f'Error exporting transactions: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 