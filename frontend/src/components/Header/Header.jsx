import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Header.css';
import ThemeToggle from '../ThemeToggle/ThemeToggle';

const Header = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);

  // Gestion du clic sur le logo WHO pour retourner à l'accueil
  const handleLogoClick = () => {
    navigate('/');
  };

  // Gestion du clic sur l'icône utilisateur
  const handleUserIconClick = () => {
    if (isAuthenticated) {
      // Si connecté, toggle le menu
      setShowUserMenu(!showUserMenu);
    } else {
      // Si non connecté, rediriger vers login
      navigate('/login');
    }
  };

  // Gestion de la déconnexion
  const handleLogout = () => {
    logout();
    setShowUserMenu(false);
    navigate('/');
  };

  // Fermer le menu si on clique ailleurs
  React.useEffect(() => {
    const handleClickOutside = () => setShowUserMenu(false);
    if (showUserMenu) {
      document.addEventListener('click', handleClickOutside);
    }
    return () => document.removeEventListener('click', handleClickOutside);
  }, [showUserMenu]);

  return (
      <header className="header-container">
        <div className="logo-container" onClick={handleLogoClick}>
          <div className="who-logo">
            <img width="50" height="50" src='/src/assets/logos/who.png' alt="WHO Logo" />  
          </div>
          <div className="org-text">
            <span className="who-title">World Health</span>
            <span className="who-subtitle">Organization</span>
          </div>
        </div>
        <div className="header-controls">

        {/* Icône utilisateur avec menu */}
        <div className="user-icon-wrapper">
          <button 
            className="user-icon"
            onClick={handleUserIconClick}
            aria-label="User menu"
          >
            <img width="32" height="32" src='/src/assets/logos/logo-user.jpeg' alt="User" />  
          </button>

          {/* Menu déroulant si connecté */}
          {isAuthenticated && showUserMenu && (
            <div className="user-dropdown" onClick={(e) => e.stopPropagation()}>
              <div className="user-info">
                <p className="user-name">{user?.name || user?.email || 'User'}</p>
                <p className="user-email">{user?.email}</p>
              </div>
              <hr className="dropdown-divider" />
              <button className="dropdown-item" onClick={handleLogout}>
                <svg viewBox="0 0 24 24" width="16" height="16">
                  <path d="M16 17l5-5-5-5M21 12H9M9 3H5a2 2 0 00-2 2v14a2 2 0 002 2h4" 
                        stroke="currentColor" 
                        strokeWidth="2" 
                        fill="none" 
                  />
                </svg>
                Logout
              </button>
            </div>
          )}
        </div>
          
          {/* Groupe toggle avec soleil et lune */}
          <div className="theme-group">
            <img className="theme-icon sun-icon" width="20" height="20" src="/src/assets/logos/sun.png" alt="Mode clair" />
            <ThemeToggle />
            <img className="theme-icon moon-icon" width="20" height="20" src="/src/assets/logos/moon.png" alt="Mode sombre" />
          </div>
          
          {/* <div className="language">
            <span className="flag">
              <img width="24" height="24"  src="/src/assets/flags/en.png" alt="EN" />
            </span>
            <span>EN</span>
          </div> */}
        </div>
      </header>
  );
};

export default Header;