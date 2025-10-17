import React, { useState, useEffect } from 'react';
import { useData } from '../../context/DataContext';
import './DatePicker.css';

const DatePicker = () => {
  const { filters, updateFilters } = useData();

  // Dates min et max disponibles
  const minDate = new Date('2020-03-01');
  const maxDate = new Date('2022-03-01');

  // Calcul du nombre de mois entre deux dates
  const getMonthsBetween = (date1, date2) => {
    const d1 = new Date(date1);
    const d2 = new Date(date2);
    return (d2.getFullYear() - d1.getFullYear()) * 12 + (d2.getMonth() - d1.getMonth());
  };

  // Conversion mois -> date
  const monthsToDate = (months) => {
    const date = new Date(minDate);
    date.setMonth(date.getMonth() + months);
    return date.toISOString().split('T')[0];
  };

  // Conversion date -> mois
  const dateToMonths = (dateStr) => {
    return getMonthsBetween(minDate, new Date(dateStr));
  };

  // Nombre total de mois disponibles
  const totalMonths = getMonthsBetween(minDate, maxDate);

  // États locaux pour le slider (en mois)
  const [startMonth, setStartMonth] = useState(dateToMonths(filters.startDate));
  const [endMonth, setEndMonth] = useState(dateToMonths(filters.endDate));

  // Mise à jour des mois quand les filtres changent
  useEffect(() => {
    setStartMonth(dateToMonths(filters.startDate));
    setEndMonth(dateToMonths(filters.endDate));
  }, [filters.startDate, filters.endDate]);

  // Gestion du changement de date de début (slider)
  const handleStartChange = (e) => {
    const newMonth = parseInt(e.target.value);
    
    // Empêcher de dépasser la date de fin
    if (newMonth <= endMonth) {
      setStartMonth(newMonth);
      updateFilters({ startDate: monthsToDate(newMonth) });
    }
  };

  // Gestion du changement de date de fin (slider)
  const handleEndChange = (e) => {
    const newMonth = parseInt(e.target.value);
    
    // Empêcher d'être avant la date de début
    if (newMonth >= startMonth) {
      setEndMonth(newMonth);
      updateFilters({ endDate: monthsToDate(newMonth) });
    }
  };

  // Gestion de l'input texte pour la date de début
  const handleStartInputChange = (e) => {
    const newDate = e.target.value;
    if (newDate) {
      const newDateObj = new Date(newDate);
      const endDateObj = new Date(filters.endDate);
      
      // Vérifier que la date de début <= date de fin
      if (newDateObj <= endDateObj && newDateObj >= minDate && newDateObj <= maxDate) {
        updateFilters({ startDate: newDate });
      } else if (newDateObj > endDateObj) {
        // Si date de début > date de fin, mettre la date de fin = date de début
        updateFilters({ 
          startDate: newDate,
          endDate: newDate
        });
      }
    }
  };

  // Gestion de l'input texte pour la date de fin
  const handleEndInputChange = (e) => {
    const newDate = e.target.value;
    if (newDate) {
      const newDateObj = new Date(newDate);
      const startDateObj = new Date(filters.startDate);
      
      // Vérifier que la date de fin >= date de début
      if (newDateObj >= startDateObj && newDateObj >= minDate && newDateObj <= maxDate) {
        updateFilters({ endDate: newDate });
      } else if (newDateObj < startDateObj) {
        // Si date de fin < date de début, mettre la date de début = date de fin
        updateFilters({ 
          startDate: newDate,
          endDate: newDate
        });
      }
    }
  };

  // Calcul du pourcentage pour le style du slider
  const startPercent = (startMonth / totalMonths) * 100;
  const endPercent = (endMonth / totalMonths) * 100;

  return (
    <div className="date-range-slider-container">
      <h3 className="date-picker-title">Date picker</h3>
      
      {/* Inputs de dates */}
      <div className="date-inputs">
        <div className="date-input-group">
          <input
            type="date"
            value={filters.startDate}
            onChange={handleStartInputChange}
            min={minDate.toISOString().split('T')[0]}
            max={maxDate.toISOString().split('T')[0]}
            className="date-input"
          />
        </div>
        
        <span className="date-separator">to</span>
        
        <div className="date-input-group">
          <input
            type="date"
            value={filters.endDate}
            onChange={handleEndInputChange}
            min={minDate.toISOString().split('T')[0]}
            max={maxDate.toISOString().split('T')[0]}
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
          {/* Barres de graduation (25 barres pour 24 mois) */}
          <div className="slider-graduations">
            {Array.from({ length: 25 }).map((_, index) => (
              <div key={index} className="graduation-mark" />
            ))}
          </div>

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
            min={0}
            max={totalMonths}
            step={1}
            value={startMonth}
            onChange={handleStartChange}
            className="slider-input slider-input-start"
            style={{ zIndex: startMonth > endMonth - 1 ? 5 : 3 }}
          />
          
          {/* Input pour la date de fin */}
          <input
            type="range"
            min={0}
            max={totalMonths}
            step={1}
            value={endMonth}
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