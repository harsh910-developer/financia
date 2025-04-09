import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import './SpendingInsights.css';

const SpendingInsights = () => {
    const [insights, setInsights] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Use useMemo to memoize the categories array
    const categories = useMemo(() => ['food', 'rent', 'utilities', 'entertainment', 'transportation'], []);

    useEffect(() => {
        const fetchInsights = async () => {
            try {
                setLoading(true);
                const results = await Promise.all(
                    categories.map(category =>
                        axios.get(`http://localhost:5000/api/predict/${category}`)
                    )
                );
                
                const insightsData = {};
                results.forEach((result, index) => {
                    insightsData[categories[index]] = result.data;
                });
                
                setInsights(insightsData);
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch spending insights');
                setLoading(false);
            }
        };

        fetchInsights();
        // Refresh data every 5 minutes
        const interval = setInterval(fetchInsights, 300000);
        return () => clearInterval(interval);
    }, [categories]); // Now categories is memoized and won't cause unnecessary re-renders

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    };

    if (loading) {
        return (
            <div className="container-fluid py-4">
                <h2 className="mb-4 h3">Spending Insights</h2>
                <div className="d-flex justify-content-center">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="container-fluid py-4">
                <h2 className="mb-4 h3">Spending Insights</h2>
                <div className="alert alert-danger" role="alert">
                    {error}
                </div>
            </div>
        );
    }

    return (
        <div className="container-fluid py-3">
            <h2 className="mb-3 h3 px-2">Spending Insights</h2>
            <div className="row g-3">
                {categories.map(category => {
                    const data = insights[category];
                    if (!data) return null;

                    const progressPercentage = (data.current_spending / data.predicted_monthly) * 100;
                    const isOverBudget = data.warning;
                    const isNearBudget = progressPercentage >= 80;

                    return (
                        <div key={category} className="col-12 col-md-6 col-xl-4 px-2">
                            <div className={`card h-100 shadow-sm ${isOverBudget ? 'border-danger' : isNearBudget ? 'border-warning' : 'border-primary'}`}>
                                <div className={`card-header py-3 ${isOverBudget ? 'bg-danger text-white' : isNearBudget ? 'bg-warning' : 'bg-primary text-white'}`}>
                                    <h5 className="card-title mb-0 d-flex align-items-center">
                                        <i className={`bi bi-${getCategoryIcon(category)} me-2 fs-4`}></i>
                                        {category.charAt(0).toUpperCase() + category.slice(1)}
                                    </h5>
                                </div>
                                <div className="card-body p-3">
                                    <div className="mb-4">
                                        <div className="d-flex justify-content-between align-items-center mb-3">
                                            <span className="text-muted fs-6">Current Spending:</span>
                                            <strong className="fs-5">{formatCurrency(data.current_spending)}</strong>
                                        </div>
                                        <div className="d-flex justify-content-between align-items-center mb-3">
                                            <span className="text-muted fs-6">Predicted Monthly:</span>
                                            <strong className="fs-5">{formatCurrency(data.predicted_monthly)}</strong>
                                        </div>
                                        <div className="d-flex justify-content-between align-items-center">
                                            <span className="text-muted fs-6">Remaining:</span>
                                            <strong className={`fs-5 ${data.predicted_remaining < 0 ? 'text-danger' : 'text-success'}`}>
                                                {formatCurrency(data.predicted_remaining)}
                                            </strong>
                                        </div>
                                    </div>
                                    
                                    <div className="progress mb-3" style={{ height: '12px' }}>
                                        <div 
                                            className={`progress-bar ${isOverBudget ? 'bg-danger' : isNearBudget ? 'bg-warning' : 'bg-primary'}`}
                                            role="progressbar"
                                            style={{ width: `${Math.min(progressPercentage, 100)}%` }}
                                            aria-valuenow={Math.min(progressPercentage, 100)}
                                            aria-valuemin="0"
                                            aria-valuemax="100"
                                        />
                                    </div>

                                    {isOverBudget && (
                                        <div className="alert alert-danger d-flex align-items-center py-2 mb-0" role="alert">
                                            <i className="bi bi-exclamation-triangle-fill me-2 fs-5"></i>
                                            <span className="fs-6">Over predicted spending!</span>
                                        </div>
                                    )}
                                    {!isOverBudget && isNearBudget && (
                                        <div className="alert alert-warning d-flex align-items-center py-2 mb-0" role="alert">
                                            <i className="bi bi-exclamation-triangle-fill me-2 fs-5"></i>
                                            <span className="fs-6">Nearing predicted limit!</span>
                                        </div>
                                    )}
                                </div>
                                <div className="card-footer text-muted py-2">
                                    <div className="d-flex align-items-center">
                                        <i className="bi bi-calendar-event me-2 fs-5"></i>
                                        <span className="fs-6">Month Progress: {Math.round(data.month_progress)}%</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

// Helper function to get category icons
const getCategoryIcon = (category) => {
    const icons = {
        food: 'cart',
        rent: 'house',
        utilities: 'lightning',
        entertainment: 'film',
        transportation: 'car-front'
    };
    return icons[category] || 'tag';
};

export default SpendingInsights; 