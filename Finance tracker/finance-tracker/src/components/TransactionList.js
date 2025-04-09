import React from 'react';
import './TransactionList.css';

const API_BASE_URL = 'http://localhost:5000';

const TransactionList = ({ transactions, loading, error }) => {
  // Group transactions by date
  const groupedTransactions = transactions.reduce((groups, transaction) => {
    const date = transaction.date;
    if (!groups[date]) {
      groups[date] = [];
    }
    groups[date].push(transaction);
    return groups;
  }, {});

  // Sort dates in descending order
  const sortedDates = Object.keys(groupedTransactions).sort((a, b) => new Date(b) - new Date(a));

  // Format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  // Format date
  const formatDate = (dateString) => {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  };

  // Handle export to CSV
  const handleExport = async () => {
    try {
      window.location.href = `${API_BASE_URL}/api/export`;
    } catch (err) {
      console.error('Error exporting transactions:', err);
    }
  };

  return (
    <div className="transaction-list card">
      <div className="card-header d-flex flex-column flex-sm-row justify-content-between align-items-center gap-2">
        <h2 className="h5 mb-0">Transaction History</h2>
        <button 
          className="btn btn-success btn-sm w-100 w-sm-auto"
          onClick={handleExport}
          disabled={sortedDates.length === 0 || loading}
        >
          <i className="bi bi-download me-1"></i>
          Export to CSV
        </button>
      </div>
      
      <div className="card-body p-0">
        {loading ? (
          <div className="p-4 text-center">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="mt-2 text-muted">Loading transactions...</p>
          </div>
        ) : error ? (
          <div className="alert alert-danger m-3" role="alert">
            <i className="bi bi-exclamation-triangle me-2"></i>
            {error}
          </div>
        ) : sortedDates.length === 0 ? (
          <div className="empty-state p-4 text-center">
            <p className="text-muted mb-0">No transactions yet. Add your first transaction to get started!</p>
          </div>
        ) : (
          <div className="list-group list-group-flush">
            {sortedDates.map(date => (
              <div key={date} className="transaction-group">
                <div className="list-group-item bg-light">
                  <h3 className="h6 mb-0 text-muted">{formatDate(date)}</h3>
                </div>
                <div className="transactions">
                  {groupedTransactions[date].map(transaction => (
                    <div 
                      key={transaction.id} 
                      className={`list-group-item list-group-item-action ${transaction.type}`}
                    >
                      <div className="d-flex flex-column flex-sm-row justify-content-between align-items-start align-items-sm-center gap-2">
                        <div className="transaction-info">
                          <div className="transaction-category">
                            <span className="fw-medium">{transaction.category}</span>
                            {transaction.notes && (
                              <small className="text-muted d-block d-sm-inline mt-1 mt-sm-0 ms-sm-2">
                                {transaction.notes}
                              </small>
                            )}
                          </div>
                        </div>
                        <div className="transaction-amount">
                          <span className={`badge ${transaction.type === 'income' ? 'bg-success' : 'bg-danger'}`}>
                            {formatCurrency(transaction.amount)}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TransactionList; 