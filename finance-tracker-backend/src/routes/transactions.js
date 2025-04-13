const express = require('express');
const router = express.Router();
const db = require('../config/database');
const auth = require('../middleware/auth');

// Get all transactions for user
router.get('/', auth, (req, res) => {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const offset = (page - 1) * limit;

    db.all(
        `SELECT * FROM transactions 
         WHERE user_id = ? 
         ORDER BY date DESC 
         LIMIT ? OFFSET ?`,
        [req.user.id, limit, offset],
        (err, transactions) => {
            if (err) {
                return res.status(500).json({ error: 'Database error' });
            }

            // Get total count
            db.get(
                'SELECT COUNT(*) as count FROM transactions WHERE user_id = ?',
                [req.user.id],
                (err, result) => {
                    if (err) {
                        return res.status(500).json({ error: 'Database error' });
                    }

                    res.json({
                        transactions,
                        total: result.count,
                        page,
                        pages: Math.ceil(result.count / limit)
                    });
                }
            );
        }
    );
});

// Create new transaction
router.post('/', auth, (req, res) => {
    const { date, type, category, amount, notes } = req.body;

    // Validate input
    if (!date || !type || !category || !amount) {
        return res.status(400).json({ error: 'Please enter all required fields' });
    }

    if (type !== 'income' && type !== 'expense') {
        return res.status(400).json({ error: 'Invalid transaction type' });
    }

    if (amount <= 0) {
        return res.status(400).json({ error: 'Amount must be greater than 0' });
    }

    db.run(
        `INSERT INTO transactions (user_id, date, type, category, amount, notes)
         VALUES (?, ?, ?, ?, ?, ?)`,
        [req.user.id, date, type, category, amount, notes || ''],
        function(err) {
            if (err) {
                return res.status(500).json({ error: 'Error creating transaction' });
            }

            db.get(
                'SELECT * FROM transactions WHERE id = ?',
                [this.lastID],
                (err, transaction) => {
                    if (err) {
                        return res.status(500).json({ error: 'Database error' });
                    }
                    res.status(201).json(transaction);
                }
            );
        }
    );
});

// Get transaction by ID
router.get('/:id', auth, (req, res) => {
    db.get(
        'SELECT * FROM transactions WHERE id = ? AND user_id = ?',
        [req.params.id, req.user.id],
        (err, transaction) => {
            if (err) {
                return res.status(500).json({ error: 'Database error' });
            }
            if (!transaction) {
                return res.status(404).json({ error: 'Transaction not found' });
            }
            res.json(transaction);
        }
    );
});

// Get transaction statistics
router.get('/stats/summary', auth, (req, res) => {
    const currentDate = new Date();
    const firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1)
        .toISOString()
        .split('T')[0];

    // Get monthly totals
    db.all(
        `SELECT type, SUM(amount) as total
         FROM transactions
         WHERE user_id = ? AND date >= ?
         GROUP BY type`,
        [req.user.id, firstDayOfMonth],
        (err, results) => {
            if (err) {
                return res.status(500).json({ error: 'Database error' });
            }

            const income = results.find(r => r.type === 'income')?.total || 0;
            const expenses = results.find(r => r.type === 'expense')?.total || 0;
            const savings = income - expenses;
            const savingsRate = income > 0 ? (savings / income) * 100 : 0;

            // Get category breakdown
            db.all(
                `SELECT category, SUM(amount) as total
                 FROM transactions
                 WHERE user_id = ? AND date >= ? AND type = 'expense'
                 GROUP BY category`,
                [req.user.id, firstDayOfMonth],
                (err, categories) => {
                    if (err) {
                        return res.status(500).json({ error: 'Database error' });
                    }

                    res.json({
                        monthly_income: income,
                        monthly_expenses: expenses,
                        savings_rate: Math.round(savingsRate * 100) / 100,
                        category_breakdown: categories
                    });
                }
            );
        }
    );
});

module.exports = router; 