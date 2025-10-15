import React, { useState, useEffect } from 'react';
import { useData } from '../../context/DataContext';
import './DatePicker.css';

const DatePicker = () => {
  const { filters, updateFilters } = useData();

  // Dates min et max disponibles
  const minDate = new Date('2020-03-01');
  const maxDate = new Date('2022-03-01');

  // Conversion date <-> timestamp
  const dateToTimestamp = (date) => new Date(date).getTime();
  const timestampToDate = (timestamp) => {
    const date = new Date(timestamp);
    return date.toISOString().split('T')[0];
  };

  // États locaux pour le slider
  const [startTimestamp, setStartTimestamp] = useState(dateToTimestamp(filters.startDate));
  const [endTimestamp, setEndTimestamp] = useState(dateToTimestamp(filters.endDate));

  // Mise à jour des timestamps quand les filtres changent
  useEffect(() => {
    setStartTimestamp(dateToTimestamp(filters.startDate));
    setEndTimestamp(dateToTimestamp(filters.endDate));
  }, [filters.startDate, filters.endDate]);

  // Gestion du changement de date de début
  const handleStartChange = (e) => {
    const newTimestamp = parseInt(e.target.value);
    setStartTimestamp(newTimestamp);
    updateFilters({ startDate: timestampToDate(newTimestamp) });
  };

  // Gestion du changement de date de fin
  const handleEndChange = (e) => {
    const newTimestamp = parseInt(e.target.value);
    setEndTimestamp(newTimestamp);
    updateFilters({ endDate: timestampToDate(newTimestamp) });
  };

  // Gestion de l'input texte pour la date de début
  const handleStartInputChange = (e) => {
    const newDate = e.target.value;
    if (newDate) {
      updateFilters({ startDate: newDate });
    }
  };

  // Gestion de l'input texte pour la date de fin
  const handleEndInputChange = (e) => {
    const newDate = e.target.value;
    if (newDate) {
      updateFilters({ endDate: newDate });
    }
  };

  // Calcul du pourcentage pour le style du slider
  const minTimestamp = dateToTimestamp(minDate);
  const maxTimestamp = dateToTimestamp(maxDate);
  
  const startPercent = ((startTimestamp - minTimestamp) / (maxTimestamp - minTimestamp)) * 100;
  const endPercent = ((endTimestamp - minTimestamp) / (maxTimestamp - minTimestamp)) * 100;

  return (
    <div className="date-range-slider-container">
      <h3 className="date-picker-title">{'Date picker'}</h3>
      
      {/* Inputs de dates */}
      <div className="date-inputs">
        <div className="date-input-group">
          <input
            type="date"
            value={filters.startDate}
            onChange={handleStartInputChange}
            min={minDate.toISOString().split('T')[0]}
            max={filters.endDate}
            className="date-input"
          />
        </div>
        
        <span className="date-separator">to</span>
        
        <div className="date-input-group">
          <input
            type="date"
            value={filters.endDate}
            onChange={handleEndInputChange}
            min={filters.startDate}
            max={maxDate.toISOString().split('S')[0]}
            className="date-input"
          />
        </div>
      </div>

      {/* Slider double */}
      <div className="slider-container">
        {/* Labels de dates aux extrémités */}
        <div className="slider-labels">
          <span className="slider-label-start">{filters.startDate}</span>
          <span className="slider-label-end">{filters.endDate}</span>
        </div>

        {/* Track du slider */}
        <div className="slider-track">
          {/* Zone sélectionnée */}
          <div 
            className="slider-range"
            style={{
              left: `${startPercent}%`,
              right: `${100 - endPercent}%`,
            }}
          />
          
          {/* Input pour la date de début */}
          <input
            type="range"
            min={minTimestamp}
            max={maxTimestamp}
            value={startTimestamp}
            onChange={handleStartChange}
            className="slider-input slider-input-start"
            style={{ zIndex: startTimestamp > endTimestamp - (maxTimestamp - minTimestamp) * 0.05 ? 5 : 3 }}
          />
          
          {/* Input pour la date de fin */}
          <input
            type="range"
            min={minTimestamp}
            max={maxTimestamp}
            value={endTimestamp}
            onChange={handleEndChange}
            className="slider-input slider-input-end"
          />
        </div>

        {/* Marqueurs de dates */}
        <div className="slider-ticks">
          <span className="tick-label">{minDate.getFullYear()}</span>
          <span className="tick-label">{maxDate.getFullYear()}</span>
        </div>
      </div>
    </div>
  );
};

export default DatePicker;