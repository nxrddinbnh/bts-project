import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export default function Sidebar({ theme, toggleTheme }) {
  const location = useLocation();

  return (
    <div className="sidebar">
      <h3>Menu</h3>

      {/* Switch thème sombre/clair */}
      <div
        style={{
          marginBottom: '2rem',
          position: 'sticky',
          top: 0,
          backgroundColor: 'var(--bg-200)',
          paddingBottom: '1rem',
          zIndex: 10,
        }}
      >
        <label
          className="switch"
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        >
          <input
            type="checkbox"
            checked={theme === 'dark'}
            onChange={toggleTheme}
            aria-label="Toggle theme"
          />
          <span className="slider"></span>
          <span className="icon" style={{ fontSize: '.8rem' }}>
            {theme === 'light' ? '🌞' : '🌙'}
          </span>
        </label>
      </div>

      {/* Liens de navigation */}
      <nav>
        <Link to="/home" className="sidebar-link">
          🏠 Can Frame
        </Link>
        <Link to="/users" className="sidebar-link">
          👥 Utilisateurs
        </Link>
      </nav>
    </div>
  );
}
