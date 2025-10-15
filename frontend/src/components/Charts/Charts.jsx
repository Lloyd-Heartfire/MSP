import React, { useEffect, useRef } from 'react';
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

// Enregistrement des composants Chart.js
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
  const { data, isValidated } = useData();
  const { theme } = useTheme();

  // Ne rien afficher si les données n'ont pas été validées
  // if (!isValidated) {
  //   return null;
  // }

  return (
    <div className="charts-container">
      {/* Graphique à barres horizontales */}
      <div className="chart-wrapper chart-horizontal-bar">
        <HorizontalBarChart data={data.charts.horizontalBar} theme={theme} />
      </div>

      {/* Graphique en courbe */}
      <div className="chart-wrapper chart-line">
        <LineChartComponent data={data.charts.lineChart} theme={theme} />
      </div>

      {/* Graphique à barres groupées */}
      <div className="chart-wrapper chart-grouped-bar">
        <GroupedBarChart data={data.charts.groupedBar} theme={theme} />
      </div>
    </div>
  );
};

// Graphique à barres horizontales
const HorizontalBarChart = ({ data, theme }) => {
  const chartData = {
    labels: data.map(item => item.name) || [],
    datasets: [
      {
        label: 'Total',
        data: data.map(item => item.total) || [],
        backgroundColor: theme === 'dark' ? '#019DD6' : '#017AB1',
        borderColor: '#017AB1',
        borderWidth: 2,
      },
      {
        label: 'Test Involved',
        data: data.map(item => item.testInvolved) || [],
        backgroundColor: theme === 'dark' ? '#D4F5F0' : '#ABFAF0',
        borderColor: '#ABFAF0',
        borderWidth: 2,
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
          font: {
            family: 'Fira Sans',
            size: 12,
          },
        },
      },
      tooltip: {
        backgroundColor: theme === 'dark' ? '#002020' : '#FFFFFF',
        titleColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        bodyColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        borderColor: '#017AB1',
        borderWidth: 2,
        padding: 12,
        bodyFont: {
          family: 'Fira Sans',
        },
        titleFont: {
          family: 'Fira Sans',
          weight: 'bold',
        },
      },
    },
    scales: {
      x: {
        grid: {
          color: theme === 'dark' ? '#003838' : '#E8E8E8',
        },
        ticks: {
          color: theme === 'dark' ? '#B0B0B0' : '#666666',
          font: {
            family: 'Fira Sans',
          },
        },
      },
      y: {
        grid: {
          color: theme === 'dark' ? '#003838' : '#E8E8E8',
        },
        ticks: {
          color: theme === 'dark' ? '#B0B0B0' : '#666666',
          font: {
            family: 'Fira Sans',
          },
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

// Graphique en courbe
const LineChartComponent = ({ data, theme }) => {
  const chartData = {
    labels: data.map(item => item.date) || [],
    datasets: [
      {
        label: 'Cases',
        data: data.map(item => item.cases) || [],
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
          font: {
            family: 'Fira Sans',
            size: 12,
          },
        },
      },
      tooltip: {
        backgroundColor: theme === 'dark' ? '#002020' : '#FFFFFF',
        titleColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        bodyColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        borderColor: '#BC0707',
        borderWidth: 2,
        padding: 12,
        bodyFont: {
          family: 'Fira Sans',
        },
        titleFont: {
          family: 'Fira Sans',
          weight: 'bold',
        },
      },
    },
    scales: {
      x: {
        grid: {
          color: theme === 'dark' ? '#003838' : '#E8E8E8',
        },
        ticks: {
          color: theme === 'dark' ? '#B0B0B0' : '#666666',
          font: {
            family: 'Fira Sans',
          },
        },
      },
      y: {
        grid: {
          color: theme === 'dark' ? '#003838' : '#E8E8E8',
        },
        ticks: {
          color: theme === 'dark' ? '#B0B0B0' : '#666666',
          font: {
            family: 'Fira Sans',
          },
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

// Graphique à barres groupées
const GroupedBarChart = ({ data, theme }) => {
  const chartData = {
    labels: data.map(item => item.category) || [],
    datasets: [
      {
        label: 'Group 1',
        data: data.map(item => item.group1) || [],
        backgroundColor: theme === 'dark' ? '#019DD6' : '#017AB1',
        borderColor: '#017AB1',
        borderWidth: 2,
      },
      {
        label: 'Group 2',
        data: data.map(item => item.group2) || [],
        backgroundColor: '#066C06',
        borderColor: '#066C06',
        borderWidth: 2,
      },
      {
        label: 'Group 3',
        data: data.map(item => item.group3) || [],
        backgroundColor: '#C98912',
        borderColor: '#C98912',
        borderWidth: 2,
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
          font: {
            family: 'Fira Sans',
            size: 12,
          },
        },
      },
      tooltip: {
        backgroundColor: theme === 'dark' ? '#002020' : '#FFFFFF',
        titleColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        bodyColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        borderColor: '#017AB1',
        borderWidth: 2,
        padding: 12,
        bodyFont: {
          family: 'Fira Sans',
        },
        titleFont: {
          family: 'Fira Sans',
          weight: 'bold',
        },
      },
    },
    scales: {
      x: {
        grid: {
          color: theme === 'dark' ? '#003838' : '#E8E8E8',
        },
        ticks: {
          color: theme === 'dark' ? '#B0B0B0' : '#666666',
          font: {
            family: 'Fira Sans',
          },
        },
      },
      y: {
        grid: {
          color: theme === 'dark' ? '#003838' : '#E8E8E8',
        },
        ticks: {
          color: theme === 'dark' ? '#B0B0B0' : '#666666',
          font: {
            family: 'Fira Sans',
          },
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