import React, { useState } from 'react';
import { useData } from '../../context/DataContext';
import './ExportButton.css';
import ExportIcon from '../../assets/export.png';

/* Export button with API integration */
function ExportButton() {
  const { exportData, isValidated } = useData();
  const [showFormatMenu, setShowFormatMenu] = useState(false);
  const [isExporting, setIsExporting] = useState(false);

  // Handle export for a specific format
  const handleExport = async (format) => {
    setShowFormatMenu(false);
    setIsExporting(true);

    // Call the export API from DataContext
    const result = await exportData(format);

    if (result.success) {
      console.log(`Export ${format.toUpperCase()} réussi`);
      // Optional: Show success notification here
    } else {
      console.error(`Erreur d'export ${format.toUpperCase()}:`, result.error);
      // Optional: Show error notification here
      alert(`Erreur lors de l'export: ${result.error}`);
    }

    setIsExporting(false);
  };

  // Toggle format menu
  const toggleMenu = () => {
    if (!isValidated) {
      alert('Veuillez d\'abord valider vos filtres pour exporter les données.');
      return;
    }
    setShowFormatMenu(!showFormatMenu);
  };

  return (
    <div className="export-button-wrapper">
      <button 
        className="export-button" 
        onClick={toggleMenu}
        disabled={isExporting}
      >
        <img src={ExportIcon} width="20" alt="export icon" />
        {isExporting ? 'Export en cours...' : ('Export')}
      </button>

      {/* Format selection menu */}
      {showFormatMenu && (
        <div className="export-format-menu">
          <button 
            className="export-format-item"
            onClick={() => handleExport('csv')}
          >
            CSV
          </button>
        </div>
      )}
    </div>
  );
}

export default ExportButton;