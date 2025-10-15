import React from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider } from './context/AuthContext';
import { DataProvider } from './context/DataContext';
import Dashboard from './components/Dashboard/Dashboard';
import './App.css';

function App() {
  return (
    <ThemeProvider>
        <AuthProvider>
          <DataProvider>
            <div className="App">
              <Dashboard />
            </div>
          </DataProvider>
        </AuthProvider>
    </ThemeProvider>
  );
}

export default App;