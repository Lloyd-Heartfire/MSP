import React from 'react';
import { useData } from '../../context/DataContext';
import './MetricChangeButton.css';

const MetricChangeToggle = () => {
  const { filters, updateFilters } = useData();

  // Toggle de la normalisation "1 per 100 000"
  const handleToggle = () => {
    updateFilters({ change_metric: !filters.change_metric });
  };

  return (
    <div className="metric-change-toggle">
      <label className="toggle-label">
        <input
          type="checkbox"
          checked={filters.change_metric}
          onChange={handleToggle}
        />
        <span className="toggle-text">1 per 100 000</span>
      </label>
    </div>
  );
};

export default MetricChangeToggle;