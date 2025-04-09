import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PredictionDisplay.css';

const PredictionDisplay = ({ category }) => {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`http://localhost:5000/api/predict/${category}`);
        setPrediction(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch prediction data');
        console.error('Error fetching prediction:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPrediction();
  }, [category]);

  if (loading) {
    return (
      <div className="prediction-card loading">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p>Loading prediction data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="prediction-card error">
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      </div>
    );
  }

  if (!prediction) {
    return null;
  }

  // Calculate progress percentage for the progress bar
  const progressPercentage = Math.min(100, (prediction.current_spending / prediction.predicted_monthly) * 100);
  
  // Determine the color class based on the warning status
  const progressColorClass = prediction.warning ? 'bg-danger' : 'bg-success';

  return (
    <div className="prediction-card">
      <h3 className="prediction-title">Spending Prediction: {category}</h3>
      
      <div className="prediction-details">
        <div className="prediction-item">
          <span className="label">Predicted Monthly:</span>
          <span className="value">${prediction.predicted_monthly.toFixed(2)}</span>
        </div>
        
        <div className="prediction-item">
          <span className="label">Current Spending:</span>
          <span className="value">${prediction.current_spending.toFixed(2)}</span>
        </div>
        
        <div className="prediction-item">
          <span className="label">Predicted Remaining:</span>
          <span className={`value ${prediction.predicted_remaining < 0 ? 'text-danger' : ''}`}>
            ${prediction.predicted_remaining.toFixed(2)}
          </span>
        </div>
        
        <div className="prediction-item">
          <span className="label">Projected Total:</span>
          <span className="value">${prediction.projected_total.toFixed(2)}</span>
        </div>
      </div>
      
      <div className="progress-container">
        <div className="progress-label">
          <span>Month Progress: {prediction.month_progress}%</span>
          <span>{prediction.warning ? 'Warning: Approaching Limit' : 'On Track'}</span>
        </div>
        <div className="progress">
          <div 
            className={`progress-bar ${progressColorClass}`} 
            role="progressbar" 
            style={{ width: `${progressPercentage}%` }}
            aria-valuenow={progressPercentage} 
            aria-valuemin="0" 
            aria-valuemax="100"
          >
            {Math.round(progressPercentage)}%
          </div>
        </div>
      </div>
      
      {prediction.warning && (
        <div className="alert alert-warning mt-3" role="alert">
          <i className="bi bi-exclamation-triangle-fill me-2"></i>
          You're approaching your predicted spending limit for this category.
        </div>
      )}
    </div>
  );
};

export default PredictionDisplay; 