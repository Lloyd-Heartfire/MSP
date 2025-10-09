import React, { useState, useEffect } from 'react';
import './ThemeToggle.css';

const ThemeToggle = () => {
  const [isDark, setIsDark] = useState(false);

  // Initialiser le thème au chargement
  useEffect(() => {

    // Vérifier le thème sauvegardé ou la préférence du système
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light');
    setIsDark(initialTheme === 'dark');
    document.body.setAttribute('data-theme', initialTheme);
  }, []);

  const handleThemeChange = () => {
    const newTheme = isDark ? 'light' : 'dark';
    setIsDark(!isDark);
    document.body.setAttribute('data-theme', newTheme);

    // Sauvegarder la préférence
    localStorage.setItem('theme', newTheme);
  };

  return (
    <label className="theme-toggle-label" >
      <div className="theme-toggle-switch">
        <input
          type="checkbox"
          checked={isDark}
          onChange={handleThemeChange}
          className="theme-toggle-checkbox"
        />
        <div className="theme-toggle-track">
          <div className="theme-toggle-dot"></div>
        </div>
      </div>
    </label>
  );
};

export default ThemeToggle;