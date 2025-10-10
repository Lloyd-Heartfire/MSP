import React, { useState } from 'react';
import './Login.css';
import Header from './Header/Header.jsx';
import Footer from './Footer/Footer.jsx';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const handleSubmit = (submitEvent) => {
    submitEvent.preventDefault();
    console.log('Login attempt:', { email, password });
  };

  return (
    <div className="login-page">

      <Header />

      <main className="login-main">
        <div className="login-card">
          <h1>Sign in</h1>
          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(inputEvent) => setEmail(inputEvent.target.value)}
                required
                className="form-input"
              />
            </div>
            <div className="form-group">
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(inputEvent) => setPassword(inputEvent.target.value)}
                required
                className="form-input"
              />
            </div>
            <button type="submit" className="sign-in-btn">
              Sign in
            </button>
          </form>
          <div className="signup-link">
            Don't have an account? <a href="#">Ask an admin</a>
          </div>
        </div>
      </main>

      <Footer />
      
    </div>
  );
};
export default Login;