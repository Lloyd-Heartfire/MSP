import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Login.css';
import Header from '../Header/Header.jsx';
import Footer from '../Footer/Footer.jsx';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (submitEvent) => {
    submitEvent.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(email, password);
    
    if (result.success) {
      navigate('/');
    } else {
      setError(result.error || 'Invalid credentials');
    }
    
    setLoading(false);
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
                disabled={loading}
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
                disabled={loading}
              />
            </div>
            
            {error && <p className="error-message">{error}</p>}
            
            <button type="submit" className="sign-in-btn" disabled={loading}>
              {loading ? 'Signing in...' : 'Sign in'}
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