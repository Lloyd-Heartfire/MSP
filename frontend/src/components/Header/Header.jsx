import React, { useState } from 'react';
import './Header.css';
import ThemeToggle from '../ThemeToggle/ThemeToggle';

const Header = () => {
  return (
      <header className="header-container">
        <div className="logo-container">
          <div className="who-logo">
            <img width="50" height="50" src='/src/assets/logos/who.png' />  
          </div>
          <div className="org-text">
            <span className="who-title">World Health</span>
            <span className="who-subtitle">Organization</span>
          </div>
        </div>
        <div className="header-controls">
          <div className="user-icon">
            <img width="32" height="32" src='/src/assets/logos/logo-user.jpeg' />  
          </div>
          
          {/* Groupe toggle avec soleil et lune */}
          <div className="theme-group">
            <img className="theme-icon sun-icon" width="20" height="20" src="/src/assets/logos/sun.png" alt="Mode clair" />
            <ThemeToggle />
            <img className="theme-icon moon-icon" width="20" height="20" src="/src/assets/logos/moon.png" alt="Mode sombre" />
          </div>
          
          <div className="language">
            <span className="flag">
              <img width="24" height="24"  src="/src/assets/flags/en.png" alt="EN" />
            </span>
            <span>EN</span>
          </div>
        </div>
      </header>
  );
};

export default Header;