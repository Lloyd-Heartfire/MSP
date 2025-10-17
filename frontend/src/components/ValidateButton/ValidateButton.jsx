import React from 'react';
import { useData } from '../../context/DataContext';
import './ValidateButton.css';

const ValidateButton = () => {
  const { fetchData, loading } = useData();

  // Validation des filtres et chargement des données
  const handleValidate = async () => {
    await fetchData();
  };

  return (
    <button 
      className="btn btn-primary validate-button"
      onClick={handleValidate}
      disabled={loading}
    >
      {loading ? (
        <>
          <div className="spinner"></div>
          <span>Loading...</span>
        </>
      ) : (
        <>
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path d="M20 6L9 17l-5-5" 
                  stroke="currentColor" 
                  strokeWidth="2" 
                  fill="none" 
            />
          </svg>
          <span>Validate</span>
        </>
      )}
    </button>
  );
};

export default ValidateButton;