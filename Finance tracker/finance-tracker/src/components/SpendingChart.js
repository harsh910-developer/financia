import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js';
import { Pie } from 'react-chartjs-2';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'chart.js/auto';

// Register ChartJS components
ChartJS.register(ArcElement, Tooltip, Legend);

const SpendingChart = ({ transactions }) => {
  const [chartHeight, setChartHeight] = useState(300);

  useEffect(() => {
    const handleResize = () => {
      setChartHeight(window.innerWidth < 768 ? 250 : 300);
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Process transactions to get spending by category
  const getSpendingByCategory = () => {
    if (!transactions || transactions.length === 0) return {};
    
    const categoryTotals = {};
    transactions.forEach(transaction => {
      if (transaction.type === 'expense') {
        const category = transaction.category || 'other';
        categoryTotals[category] = (categoryTotals[category] || 0) + Number(transaction.amount);
      }
    });
    return categoryTotals;
  };

  const chartData = {
    labels: Object.keys(getSpendingByCategory()).map(category => 
      category.charAt(0).toUpperCase() + category.slice(1)
    ),
    datasets: [{
      data: Object.values(getSpendingByCategory()),
      backgroundColor: [
        'rgba(255, 99, 132, 0.8)',
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 206, 86, 0.8)',
        'rgba(75, 192, 192, 0.8)',
        'rgba(153, 102, 255, 0.8)',
        'rgba(255, 159, 64, 0.8)'
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
      borderWidth: 2,
    }]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: window.innerWidth < 768 ? 'bottom' : 'right',
        labels: {
          boxWidth: window.innerWidth < 768 ? 15 : 20,
          padding: window.innerWidth < 768 ? 15 : 20,
          font: {
            size: window.innerWidth < 768 ? 12 : 14
          }
        }
      },
      tooltip: {
        bodyFont: {
          size: 14
        },
        padding: 12,
        callbacks: {
          label: function(context) {
            const value = context.raw || 0;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
            return ` $${value.toFixed(2)} (${percentage}%)`;
          }
        }
      }
    }
  };

  if (!transactions || transactions.length === 0) {
    return (
      <div className="card mb-4 shadow-sm">
        <div className="card-header bg-primary text-white py-3">
          <h4 className="h5 mb-0 d-flex align-items-center">
            <i className="bi bi-pie-chart-fill me-2 fs-4"></i>
            Spending by Category
          </h4>
        </div>
        <div className="card-body p-4 text-center">
          <p className="text-muted mb-0">No transactions found. Add some expenses to see the chart!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card mb-4 shadow-sm">
      <div className="card-header bg-primary text-white py-3">
        <h4 className="h5 mb-0 d-flex align-items-center">
          <i className="bi bi-pie-chart-fill me-2 fs-4"></i>
          Spending by Category
        </h4>
      </div>
      <div className="card-body p-3 p-sm-4">
        <div style={{ 
          height: chartHeight,
          position: 'relative',
          margin: window.innerWidth < 768 ? '0.5rem 0 1.5rem' : '1rem 0'
        }}>
          <Pie data={chartData} options={options} />
        </div>
      </div>
    </div>
  );
};

export default SpendingChart; 