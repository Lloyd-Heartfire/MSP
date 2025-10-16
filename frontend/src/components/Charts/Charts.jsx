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
  const { data, isValidated } = useData();
  const { theme } = useTheme();

  if (!isValidated || !data || !data.charts) {
    return null;
  }

  const { horizontalBar, lineChart, groupedBar } = data.charts;

  return (
    <div className="charts-container">
      {/* Graphique à barres horizontales */}
      <div className="chart-wrapper chart-horizontal-bar">
        <h3 className="chart-title">Cases by Region</h3>
        <HorizontalBarChart data={horizontalBar} theme={theme} />
      </div>

      {/* Graphique en courbe */}
      <div className="chart-wrapper chart-line">
        <h3 className="chart-title">Cases Over Time</h3>
        <LineChartComponent data={lineChart} theme={theme} />
      </div>

      {/* Graphique à barres groupées */}
      <div className="chart-wrapper chart-grouped-bar">
        <h3 className="chart-title">Cases by Demographics</h3>
        <GroupedBarChart data={groupedBar} theme={theme} />
      </div>
    </div>
  );
};

// Graphique à barres horizontales
const HorizontalBarChart = ({ data, theme }) => {
  if (!data || data.length === 0) {
    return <div className="chart-no-data">No data available</div>;
  }

  const chartData = {
    labels: data.map(item => item.label) || [],
    datasets: [
      {
        label: 'Total Cases',
        data: data.map(item => item.total) || [],
        backgroundColor: theme === 'dark' ? '#019DD6' : '#017AB1',
        borderRadius: 4,
      },
      {
        label: 'Deaths',
        data: data.map(item => item.alcoholInvolved) || [],
        backgroundColor: theme === 'dark' ? '#BC0707' : '#BC0707',
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
      },
    },
    scales: {
      x: {
        grid: { color: theme === 'dark' ? '#003838' : '#E8E8E8' },
        ticks: { 
          color: theme === 'dark' ? '#B0B0B0' : '#666666',
          font: { family: 'Fira Sans' }
        },
      },
      y: {
        grid: { color: theme === 'dark' ? '#003838' : '#E8E8E8' },
        ticks: { 
          color: theme === 'dark' ? '#B0B0B0' : '#666666',
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

// Graphique en courbe
const LineChartComponent = ({ data, theme }) => {
  if (!data || data.length === 0) {
    return <div className="chart-no-data">No data available</div>;
  }

  const chartData = {
    labels: data.map(item => item.month) || [],
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
          font: { family: 'Fira Sans', size: 12 },
        },
      },
      tooltip: {
        backgroundColor: theme === 'dark' ? '#002020' : '#FFFFFF',
        titleColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        bodyColor: theme === 'dark' ? '#FFFFFF' : '#000000',
        borderColor: '#BC0707',
        borderWidth: 2,
        padding: 12,
      },
    },
    scales: {
      x: {
        grid: { color: theme === 'dark' ? '#003838' : '#E8E8E8' },
        ticks: { 
          color: theme === 'dark' ? '#B0B0B0' : '#666666',
          font: { family: 'Fira Sans' }
        },
      },
      y: {
        grid: { color: theme === 'dark' ? '#003838' : '#E8E8E8' },
        ticks: { 
          color: theme === 'dark' ? '#B0B0B0' : '#666666',
          font: { family: 'Fira Sans' }
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
  if (!data || data.length === 0) {
    return <div className="chart-no-data">No data available</div>;
  }

  const chartData = {
    labels: data.map(item => item.category) || [],
    datasets: [
      {
        label: 'Male',
        data: data.map(item => item.male) || [],
        backgroundColor: theme === 'dark' ? '#019DD6' : '#017AB1',
        borderRadius: 4,
      },
      {
        label: 'Female',
        data: data.map(item => item.female) || [],
        backgroundColor: '#066C06',
        borderRadius: 4,
      },
      {
        label: 'Total',
        data: data.map(item => item.total) || [],
        backgroundColor: '#C98912',
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
      },
    },
    scales: {
      x: {
        grid: { color: theme === 'dark' ? '#003838' : '#E8E8E8' },
        ticks: { 
          color: theme === 'dark' ? '#B0B0B0' : '#666666',
          font: { family: 'Fira Sans' }
        },
      },
      y: {
        grid: { color: theme === 'dark' ? '#003838' : '#E8E8E8' },
        ticks: { 
          color: theme === 'dark' ? '#B0B0B0' : '#666666',
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

export default Charts;