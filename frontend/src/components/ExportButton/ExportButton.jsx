import './ExportButton.css'
import ExportIcon from '../../assets/export.png'

// Minimal CSV exporter button
// Props:
// - data: array of objects (required)
// - filename: string (optional, default 'export.csv')
function ExportButton({ data = [], filename = 'export.csv' }) {
  const escapeCsv = (value) => {
    if (value === null || value === undefined) return '';
    const str = String(value);
    // If field contains comma, quote or newline, wrap in quotes and escape quotes
    if (/[",\n]/.test(str)) {
      return '"' + str.replaceAll('"', '""') + '"';
    }
    return str;
  };

  const toCsv = (rows) => {
    if (!Array.isArray(rows) || rows.length === 0) return '';
    // Use keys from first row as headers (minimalist)
    const headers = Object.keys(rows[0]);
    const headerLine = headers.map(escapeCsv).join(',');
    const lines = rows.map((row) => headers.map((h) => escapeCsv(row[h])).join(','));
    return [headerLine, ...lines].join('\n');
  };

  const handleExport = () => {
    if (!data || data.length === 0) {
      // Minimal feedback; no UI framework here
      console.warn('Export: aucun data à exporter');
      return;
    }
    const csv = toCsv(data);
    // Add UTF-8 BOM for Excel compatibility
    const blob = new Blob(["\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <button className="export-button" onClick={handleExport}>
      <img src={ExportIcon} width="20" alt="export icon" /> Export
    </button>
  )
}

export default ExportButton;
