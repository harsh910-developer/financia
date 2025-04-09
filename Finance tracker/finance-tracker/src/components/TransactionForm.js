import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

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
    // Clear error when user starts typing
    if (error) setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    
    try {
      const response = await axios.post('http://localhost:5000/api/transactions', formData);
      console.log('Transaction added:', response.data);
      
      // Call the callback to update the parent component
      onTransactionAdded(response.data);
      
      // Reset the form
      setFormData({
        type: 'expense',
        amount: '',
        category: 'food',
        date: new Date().toISOString().split('T')[0],
        notes: ''
      });

      // Show success message
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
      <div className="card-header bg-primary text-white py-3">
        <h4 className="h5 mb-0 d-flex align-items-center">
          <i className="bi bi-plus-circle me-2 fs-4"></i>
          Add New Transaction
        </h4>
      </div>
      <div className="card-body p-3 p-sm-4">
        <form onSubmit={handleSubmit}>
          {error && (
            <div className="alert alert-danger d-flex align-items-center mb-4" role="alert">
              <i className="bi bi-exclamation-triangle-fill me-2 fs-5"></i>
              <span>{error}</span>
            </div>
          )}
          
          <div className="row g-3">
            <div className="col-12 col-sm-6 col-lg-3">
              <label className="form-label fs-6">Type</label>
              <select 
                className="form-select form-select-lg"
                name="type" 
                value={formData.type} 
                onChange={handleChange}
                required
              >
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
            </div>
            
            <div className="col-12 col-sm-6 col-lg-3">
              <label className="form-label fs-6">Amount</label>
              <div className="input-group input-group-lg">
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
            
            <div className="col-12 col-sm-6 col-lg-3">
              <label className="form-label fs-6">Category</label>
              <select 
                className="form-select form-select-lg" 
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
            
            <div className="col-12 col-sm-6 col-lg-3">
              <label className="form-label fs-6">Date</label>
              <input 
                type="date" 
                className="form-control form-control-lg" 
                name="date" 
                value={formData.date} 
                onChange={handleChange}
                required
              />
            </div>

            <div className="col-12">
              <label className="form-label fs-6">Notes (Optional)</label>
              <input 
                type="text" 
                className="form-control form-control-lg" 
                name="notes" 
                value={formData.notes} 
                onChange={handleChange}
                placeholder="Add any additional notes..."
              />
            </div>
          </div>
          
          <div className="mt-4">
            <button 
              type="submit" 
              className="btn btn-primary btn-lg w-100 w-sm-auto px-5"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Adding...
                </>
              ) : (
                <>
                  <i className="bi bi-plus-circle me-2"></i>
                  Add Transaction
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TransactionForm; 