import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PredictionDisplay from './PredictionDisplay';
import './PredictionsDashboard.css';

const PredictionsDashboard = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        // First, get all transactions to extract unique categories
        const response = await axios.get('http://localhost:5000/api/transactions');
        const transactions = response.data;
        
        // Extract unique expense categories
        const uniqueCategories = [...new Set(
          transactions
            .filter(t => t.type === 'expense')
            .map(t => t.category)
        )];
        
        setCategories(uniqueCategories);
        setError(null);
      } catch (err) {
        setError('Failed to fetch categories');
        console.error('Error fetching categories:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  if (loading) {
    return (
      <div className="predictions-dashboard loading">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p>Loading prediction dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="predictions-dashboard error">
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      </div>
    );
  }

  if (categories.length === 0) {
    return (
      <div className="predictions-dashboard empty">
        <div className="alert alert-info" role="alert">
          No expense categories found. Add some transactions first!
        </div>
      </div>
    );
  }

  return (
    <div className="predictions-dashboard">
      <h2 className="dashboard-title">Spending Predictions</h2>
      <p className="dashboard-description">
        View predictions for your spending categories based on your transaction history.
      </p>
      
      <div className="predictions-grid">
        {categories.map(category => (
          <PredictionDisplay key={category} category={category} />
        ))}
      </div>
    </div>
  );
};

export default PredictionsDashboard; 