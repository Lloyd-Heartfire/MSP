import React from 'react';
import { useData } from '../../context/DataContext';
import { useTheme } from '../../context/ThemeContext';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';
import './Charts.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

const Charts = () => {
  const { data, isValidated, perCapita } = useData();
  const { theme } = useTheme();

  if (!isValidated || !data || !data.charts) {
    return null;
  }

  const { horizontalBar, lineChart, groupedBar } = data.charts;

  return (
    <div className="charts-container">
      {/* Graphique 1 : Barres horizontales - Total Cases vs Total Deaths */}
      <div className="chart-wrapper chart-horizontal-bar">
        <h3 className="chart-title">
          Total Cases vs Total Deaths by Region {perCapita && '(per 100k)'}
        </h3>
        <HorizontalBarChart data={horizontalBar} theme={theme} perCapita={perCapita} />
      </div>

      {/* Graphique 2 : Ligne - New Cases and New Deaths over time */}
      <div className="chart-wrapper chart-line">
        <h3 className="chart-title">New Cases and New Deaths Over Time</h3>
        <LineChartComponent data={lineChart} theme={theme} />
      </div>

      {/* Graphique 3 : Barres verticales - Active Cases vs Recovered */}
      <div className="chart-wrapper chart-grouped-bar">
        <h3 className="chart-title">
          Active Cases vs Recovered {perCapita && '(per 100k)'}
        </h3>
        <GroupedBarChart data={groupedBar} theme={theme} perCapita={perCapita} />
      </div>
    </div>
  );
};

// Graphique 1 : Barres horizontales - Total Cases vs Total Deaths
const HorizontalBarChart = ({ data, theme, perCapita }) => {
  if (!data || data.length === 0) {
    return <div className="chart-no-data">No data available</div>;
  }

  // Calculer les données selon le mode per capita
  const processedData = data.map(item => {
    if (perCapita && item.population > 0) {
      return {
        ...item,
        totalCases: (item.totalCases / item.population) * 100000,
        totalDeaths: (item.totalDeaths / item.population) * 100000
      };
    }
    return item;
  });

  const chartData = {
    labels: processedData.map(item => item.label) || [],
    datasets: [
      {
        label: `Total Cases${perCapita ? ' (per 100k)' : ''}`,
        data: processedData.map(item => item.totalCases) || [],
        backgroundColor: theme === 'dark' ? '#019DD6' : '#017AB1',
        borderRadius: 4,
      },
      {
        label: `Total Deaths${perCapita ? ' (per 100k)' : ''}`,
        data: processedData.map(item => item.totalDeaths) || [],
        backgroundColor: '#BC0707',
        borderRadius: 4,
      },
    ],
  };

  const options = {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: theme === 'dark' ? '#FFFFFF' : '#000000',
          font: { family: 'Fira Sans', size: 12 },
        },
      },
      tooltip: {
        backgroundColor: theme === 'dark' ? '#002020' : '#FFFFFF',
        titleColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        bodyColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        borderColor: '#017AB1',
        borderWidth: 2,
        padding: 12,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (perCapita) {
              label += context.parsed.x.toFixed(2);
            } else {
              label += new Intl.NumberFormat('en-US').format(context.parsed.x);
            }
            return label;
          }
        }
      },
    },
    scales: {
      x: {
        grid: { color: theme === 'dark' ? '#003838' : '#E8E8E8' },
        ticks: { 
          color: theme === 'dark' ? '#FFFFFF' : '#000000',
          font: { family: 'Fira Sans' },
          callback: function(value) {
            if (perCapita) {
              return value.toFixed(0);
            }
            return new Intl.NumberFormat('en-US', { notation: 'compact' }).format(value);
          }
        },
      },
      y: {
        grid: { color: theme === 'dark' ? '#003838' : '#E8E8E8' },
        ticks: { 
          color: theme === 'dark' ? '#FFFFFF' : '#000000',
          font: { family: 'Fira Sans' }
        },
      },
    },
  };

  return (
    <div className="chart-content">
      <Bar data={chartData} options={options} />
    </div>
  );
};

// Graphique 2 : Ligne - New Cases and New Deaths
const LineChartComponent = ({ data, theme }) => {
  if (!data || !data.periods || data.periods.length === 0) {
    return <div className="chart-no-data">No data available</div>;
  }

  const chartData = {
    labels: data.periods || [],
    datasets: [
      {
        label: 'New Cases',
        data: data.newCases || [],
        borderColor: '#017AB1',
        backgroundColor: 'rgba(1, 122, 177, 0.1)',
        borderWidth: 3,
        pointRadius: 5,
        pointBackgroundColor: '#017AB1',
        pointBorderColor: '#FFFFFF',
        pointBorderWidth: 2,
        tension: 0.4,
        fill: true,
      },
      {
        label: 'New Deaths',
        data: data.newDeaths || [],
        borderColor: '#BC0707',
        backgroundColor: 'rgba(188, 7, 7, 0.1)',
        borderWidth: 3,
        pointRadius: 5,
        pointBackgroundColor: '#BC0707',
        pointBorderColor: '#FFFFFF',
        pointBorderWidth: 2,
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: theme === 'dark' ? '#FFFFFF' : '#000000',
          font: { family: 'Fira Sans', size: 12 },
        },
      },
      tooltip: {
        backgroundColor: theme === 'dark' ? '#002020' : '#FFFFFF',
        titleColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        bodyColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        borderColor: '#017AB1',
        borderWidth: 2,
        padding: 12,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            label += new Intl.NumberFormat('en-US').format(context.parsed.y);
            return label;
          }
        }
      },
    },
    scales: {
      x: {
        grid: { color: theme === 'dark' ? '#003838' : '#E8E8E8' },
        ticks: { 
          color: theme === 'dark' ? '#FFFFFF' : '#000000',
          font: { family: 'Fira Sans' }
        },
      },
      y: {
        grid: { color: theme === 'dark' ? '#003838' : '#E8E8E8' },
        ticks: { 
          color: theme === 'dark' ? '#FFFFFF' : '#000000',
          font: { family: 'Fira Sans' },
          callback: function(value) {
            return new Intl.NumberFormat('en-US', { notation: 'compact' }).format(value);
          }
        },
      },
    },
  };

  return (
    <div className="chart-content">
      <Line data={chartData} options={options} />
    </div>
  );
};

// Graphique 3 : Barres verticales - Active Cases vs Recovered
const GroupedBarChart = ({ data, theme, perCapita }) => {
  if (!data || data.length === 0) {
    return <div className="chart-no-data">No data available</div>;
  }

  // Calculer les données selon le mode per capita
  const processedData = data.map(item => {
    if (perCapita && item.population > 0) {
      return {
        ...item,
        activeCases: (item.activeCases / item.population) * 100000,
        totalRecovered: (item.totalRecovered / item.population) * 100000
      };
    }
    return item;
  });

  const chartData = {
    labels: processedData.map(item => item.category) || [],
    datasets: [
      {
        label: `Active Cases${perCapita ? ' (per 100k)' : ''}`,
        data: processedData.map(item => item.activeCases) || [],
        backgroundColor: '#C98912',
        borderRadius: 4,
      },
      {
        label: `Total Recovered${perCapita ? ' (per 100k)' : ''}`,
        data: processedData.map(item => item.totalRecovered) || [],
        backgroundColor: '#066C06',
        borderRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: theme === 'dark' ? '#FFFFFF' : '#000000',
          font: { family: 'Fira Sans', size: 12 },
        },
      },
      tooltip: {
        backgroundColor: theme === 'dark' ? '#002020' : '#FFFFFF',
        titleColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        bodyColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        borderColor: '#017AB1',
        borderWidth: 2,
        padding: 12,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (perCapita) {
              label += context.parsed.y.toFixed(2);
            } else {
              label += new Intl.NumberFormat('en-US').format(context.parsed.y);
            }
            return label;
          }
        }
      },
    },
    scales: {
      x: {
        grid: { color: theme === 'dark' ? '#003838' : '#E8E8E8' },
        ticks: { 
          color: theme === 'dark' ? '#FFFFFF' : '#000000',
          font: { family: 'Fira Sans' },
          maxRotation: 45,
          minRotation: 45
        },
      },
      y: {
        grid: { color: theme === 'dark' ? '#003838' : '#E8E8E8' },
        ticks: { 
          color: theme === 'dark' ? '#FFFFFF' : '#000000',
          font: { family: 'Fira Sans' },
          callback: function(value) {
            if (perCapita) {
              return value.toFixed(0);
            }
            return new Intl.NumberFormat('en-US', { notation: 'compact' }).format(value);
          }
        },
      },
    },
  };

  return (
    <div className="chart-content">
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default Charts;