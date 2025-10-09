import React, { useState } from 'react';
import './Footer.css';

const Footer = () => {

  return (
      <footer className="login-footer">
        <div className="footer-logo">
          <img width="30" height="30" src='/src/assets/logos/who.png' />          
        </div>
        <span className="footer-text">Property of World Health Organization</span>
        <div className="footer-logo-right">
          <img width="30" height="30" src='/src/assets/logos/who.png' />  
        </div>
      </footer>
  );
};

export default Footer;