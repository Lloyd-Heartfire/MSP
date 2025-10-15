import React from 'react';
import './PandemicSelector.css';

const PandemicSelector = () => {
  return (
    <div className="pandemic-selector">
      <div className="dropdown-button">
        <span className="pandemic-label">COVID-19</span>
        <button className="pandemic-dropdown-btn">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="white">
            <path d="M7 10l5 5 5-5z"/>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default PandemicSelector;