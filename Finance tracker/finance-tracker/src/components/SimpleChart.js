import React from 'react';
import './SimpleChart.css';

const SimpleChart = ({ pieData }) => {
  // Calculate total for percentages
  const total = pieData.reduce((sum, item) => sum + item.value, 0);
  
  // Colors for the chart
  const colors = ['#0066cc', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];
  
  return (
    <div className="simple-chart card">
      <div className="chart-title">
        Spending Distribution
      </div>
      <div className="chart-container">
        {pieData.map((item, index) => {
          const percentage = (item.value / total) * 100;
          return (
            <div 
              key={index} 
              className="chart-segment"
              style={{
                width: `${percentage}%`,
                backgroundColor: colors[index % colors.length],
                height: '100%',
                display: 'inline-block',
                transition: 'width 0.5s ease-in-out'
              }}
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              title={`${item.name}: $${item.value.toFixed(2)} (${percentage.toFixed(1)}%)`}
            />
          );
        })}
      </div>
      <div className="chart-legend">
        {pieData.map((item, index) => (
          <div key={index} className="legend-item">
            <div 
              className="legend-color" 
              style={{ backgroundColor: colors[index % colors.length] }}
            />
            <span className="legend-label">{item.name}</span>
            <span className="legend-value">${item.value.toFixed(2)}</span>
          </div>
        ))}
      </div>
      <div className="chart-total">
        Total: ${total.toFixed(2)}
      </div>
    </div>
  );
};

export default SimpleChart; 