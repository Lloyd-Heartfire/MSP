import './Home.css'
import ExportButton from '../ExportButton/ExportButton'
import Header from '../Header/Header'
import Footer from '../Footer/Footer'

function Home() {
  // Exemple minimal de données de tableau à exporter
  const tableauData = [
    { Pays: 'France', Cas: 1200, Deces: 30 },
    { Pays: 'Germany', Cas: 950, Deces: 18 },
    { Pays: 'Spain', Cas: 1100, Deces: 22 },
  ]
  return (
    <div className="app-container">
      <Header />
      <div className="content">
        <h1 className="main-title">Analyse of the pandemics in the world</h1>
        <div className="export-section">
          <ExportButton data={tableauData} filename="tableau_data.csv" />
        </div>
      </div>
      <Footer />
    </div>
  )
}

export default Home