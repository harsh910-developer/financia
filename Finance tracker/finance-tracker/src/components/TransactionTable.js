import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const TransactionTable = ({ transactions }) => {
  // Format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  // Format date
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  return (
    <div className="card mb-4">
      <div className="card-header bg-primary text-white">
        <h4 className="mb-0">Transactions</h4>
      </div>
      <div className="card-body">
        {transactions.length === 0 ? (
          <p className="text-center">No transactions found. Add your first transaction above!</p>
        ) : (
          <div className="table-responsive">
            <table className="table table-striped table-hover">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Type</th>
                  <th>Category</th>
                  <th>Amount</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((transaction, index) => (
                  <tr key={index}>
                    <td>{formatDate(transaction.date)}</td>
                    <td>
                      <span className={`badge ${transaction.type === 'income' ? 'bg-success' : 'bg-danger'}`}>
                        {transaction.type.charAt(0).toUpperCase() + transaction.type.slice(1)}
                      </span>
                    </td>
                    <td>{transaction.category.charAt(0).toUpperCase() + transaction.category.slice(1)}</td>
                    <td className={transaction.type === 'income' ? 'text-success' : 'text-danger'}>
                      {transaction.type === 'income' ? '+' : '-'} {formatCurrency(transaction.amount)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default TransactionTable; 