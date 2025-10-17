import React from 'react';
import { useData } from '../../context/DataContext';
import Header from '../Header/Header';
import Footer from '../Footer/Footer';
import PandemicSelector from '../PandemicSelector/PandemicSelector';
import FilterPanel from '../FilterPanel/FilterPanel';
import DatePicker from '../DatePicker/DatePicker';
import ExportButton from '../ExportButton/ExportButton';
import MetricChangeButton from '../MetricChangeButton/MetricChangeButton';
import ValidateButton from '../ValidateButton/ValidateButton';
import StatsCards from '../StatsCards/StatsCards';
import Charts from '../Charts/Charts';
import './Dashboard.css';

const Dashboard = () => {
  const { data, loading, error, isValidated } = useData();

  return (
    <div className="dashboard">
      {/* Header avec logo, thème, user */}
      <Header />

      {/* Contenu principal */}
      <main className="dashboard-main">
        <div className="dashboard-container">
          {/* Titre principal */}
          <h1 className="dashboard-title">
            Analysis of the pandemics in the world
          </h1>

          {/* Ligne 1 : Pandemic, Import, Export, Toggle, Validate */}
          <section className="dashboard-section actions-section">
            <div className="actions-row">
              <PandemicSelector />
              <ExportButton />
              <MetricChangeButton />
              <ValidateButton />
            </div>
          </section>

          {/* Ligne 2 : Filtres géographiques */}
          <section className="dashboard-section filters-section">
            <div className="filters-row">
              <FilterPanel />
            </div>
          </section>

          {/* Section du sélecteur de dates */}
          <section className="dashboard-section">
            <DatePicker />
          </section>

          {loading && (
            <section className="dashboard-section">
              <div className="loading-state">
                <p>Loading data...</p>
              </div>
            </section>
          )}

          {error && !loading && (
            <section className="dashboard-section">
              <div className="error-state">
                <p>Error: {error}</p>
                <p>Please check your filters and try again.</p>
              </div>
            </section>
          )}

          {!isValidated && !loading && !error && (
            <section className="dashboard-section">
              <div className="empty-state">
                <p>Please select your filters and click "Validate" to display the data</p>
              </div>
            </section>
          )}

          {/* Section des statistiques et graphiques (visible après validation) */}
          {isValidated && data && !loading && (
            <section className="dashboard-section results-section">
              <StatsCards stats={data.stats} />
              <Charts data={data.charts} />
            </section>
          )}
        </div>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Dashboard;