import './App.css'
import ExportButton from './components/ExportButton/ExportButton'

function App() {
  return (
    <div className="app-container">
      <div className="content">
        <h1 className="main-title">Analyse of the pandemics in the world</h1>
        <div className="export-section">
          <ExportButton />
        </div>
      </div>
    </div>
  )
}

export default App
