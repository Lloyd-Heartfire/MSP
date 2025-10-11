import './Home.css'
import ExportButton from '../ExportButton/ExportButton'
import Header from '../Header/Header'
import Footer from '../Footer/Footer'

function Home() {
  return (
    <div className="app-container">
      <Header />
      <div className="content">
        <h1 className="main-title">Analyse of the pandemics in the world</h1>
        <div className="export-section">
          <ExportButton />
        </div>
      </div>
      <Footer />
    </div>
  )
}

export default Home