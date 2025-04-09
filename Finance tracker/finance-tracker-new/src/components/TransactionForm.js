import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const TransactionForm = ({ onTransactionAdded }) => {
  const [formData, setFormData] = useState({
    type: 'expense',
    amount: '',
    category: 'food',
    date: new Date().toISOString().split('T')[0],
    notes: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const categories = ['food', 'rent', 'entertainment', 'utilities', 'transportation', 'other'];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
    if (error) setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    
    try {
      const response = await axios.post('http://localhost:5000/api/transactions', formData);
      console.log('Transaction added:', response.data);
      
      if (onTransactionAdded) {
        onTransactionAdded(response.data);
      }
      
      setFormData({
        type: 'expense',
        amount: '',
        category: 'food',
        date: new Date().toISOString().split('T')[0],
        notes: ''
      });

      alert('Transaction added successfully!');
    } catch (error) {
      console.error('Error adding transaction:', error);
      setError('Failed to add transaction. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="card mb-4 shadow-sm">
      <div className="card-header bg-primary text-white">
        <h4 className="h5 mb-0">Add New Transaction</h4>
      </div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          {error && (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          )}
          
          <div className="row g-3">
            <div className="col-12 col-sm-6 col-md-3">
              <label className="form-label">Type</label>
              <select 
                className="form-select" 
                name="type" 
                value={formData.type} 
                onChange={handleChange}
                required
              >
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
            </div>
            
            <div className="col-12 col-sm-6 col-md-3">
              <label className="form-label">Amount</label>
              <div className="input-group">
                <span className="input-group-text">$</span>
                <input 
                  type="number" 
                  className="form-control" 
                  name="amount" 
                  value={formData.amount} 
                  onChange={handleChange}
                  placeholder="0.00"
                  step="0.01"
                  min="0"
                  required
                />
              </div>
            </div>
            
            <div className="col-12 col-sm-6 col-md-3">
              <label className="form-label">Category</label>
              <select 
                className="form-select" 
                name="category" 
                value={formData.category} 
                onChange={handleChange}
                required
              >
                {categories.map(category => (
                  <option key={category} value={category}>
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="col-12 col-sm-6 col-md-3">
              <label className="form-label">Date</label>
              <input 
                type="date" 
                className="form-control" 
                name="date" 
                value={formData.date} 
                onChange={handleChange}
                required
              />
            </div>

            <div className="col-12">
              <label className="form-label">Notes (Optional)</label>
              <input 
                type="text" 
                className="form-control" 
                name="notes" 
                value={formData.notes} 
                onChange={handleChange}
                placeholder="Add any additional notes..."
              />
            </div>
          </div>
          
          <div className="mt-3">
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Adding...
                </>
              ) : (
                'Add Transaction'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TransactionForm; 