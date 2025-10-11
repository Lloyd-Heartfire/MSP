import './ExportButton.css' 

function ExportButton() {
  const handleExport = () => {
    // Add your export functionality here
    // For example: export data to CSV, PDF, etc.
    console.log('Export button clicked - implementing export functionality...');
    
    // Example: You can implement different export formats
    // exportToCSV() or exportToPDF() or exportToExcel()
  }

  return (
    <button className="export-button" onClick={handleExport}>
      <img src="./src/assets/export.png" width="20" alt="icon" /> Export
    </button>
  )
}

export default ExportButton;
