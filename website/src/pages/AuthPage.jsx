import React from 'react';
import AuthForm from '../components/AuthForm';

export default function AuthPage({ theme, toggleTheme }) {
  return (
    <div className="auth-page">
      <div className="theme-button-container">
        <label className="switch">
          <input 
            type="checkbox" 
            checked={theme === 'dark'} 
            onChange={toggleTheme} 
            aria-label="Toggle theme"
          />
          <span className="slider"></span>
          <span className="icon">{theme === 'light' ? '🌞' : '🌙'}</span>
        </label>
      </div>
      <AuthForm />
    </div>
  );
}


