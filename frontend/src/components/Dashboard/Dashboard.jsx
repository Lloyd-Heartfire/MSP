import React from 'react';
import Header from '../Header/Header';
import Footer from '../Footer/Footer';
import FilterPanel from '../FilterPanel/FilterPanel';
import DatePicker from '../DatePicker/DatePicker';
import ExportButton from '../ExportButton/ExportButton';
import MetricChangeButton from '../MetricChangeButton/MetricChangeButton';
import ValidateButton from '../ValidateButton/ValidateButton';
import StatsCards from '../StatsCards/StatsCards';
import Charts from '../Charts/Charts';
import './Dashboard.css';

const Dashboard = () => {
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

          {/* Section des filtres */}
          <section className="dashboard-section filters-section">
            <div className="filters-row">
              <FilterPanel />
            </div>
          </section>

          {/* Section des actions (Export, Toggle, Validate) */}
          <section className="dashboard-section actions-section">
            <div className="actions-row">
              <ExportButton />
              <MetricChangeButton />
              <ValidateButton />
            </div>
          </section>

          {/* Section du sélecteur de dates */}
          <section className="dashboard-section">
            <DatePicker />
          </section>

          {/* Section des statistiques et graphiques (visible après validation) */}
          <section className="dashboard-section results-section">
            <StatsCards />
            <Charts />
          </section>
        </div>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Dashboard;