import React, { useEffect, useState, useRef } from 'react';
import { fetchCanFrames } from '../services/apiService';
import { Link } from 'react-router-dom';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from 'recharts';
import { FaUserCircle } from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';

function groupDataByMonthYear(data, dateField = 'date') {
  const grouped = data.reduce((acc, item) => {
    if (!item[dateField]) return acc;
    const d = new Date(item[dateField]);
    if (isNaN(d)) return acc;

    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
    if (!acc[key]) acc[key] = 0;
    acc[key]++;
    return acc;
  }, {});

  return Object.entries(grouped)
    .map(([month, count]) => ({
      month,
      count,
      label: new Date(month + '-01').toLocaleDateString('fr-FR', { year: 'numeric', month: 'short' })
    }))
    .sort((a, b) => new Date(a.month + '-01') - new Date(b.month + '-01'));
}

export default function TrackingPage({ theme, toggleTheme }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef(null);
  const { logout } = useAuth();

  useEffect(() => {
    fetchCanFrames()
      .then(rawData => {
        const grouped = groupDataByMonthYear(rawData, 'date');
        setData(grouped);
        setLoading(false);
      })
      .catch(() => {
        setError('Erreur lors du chargement des données');
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (loading) return <p>Chargement des données...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className={`app-container ${theme}`} style={{ display: 'flex', height: '100vh' }}>
      {/* Sidebar */}
      <aside className="sidebar" style={{ width: 240 }}>
        <h3>Menu</h3>
        {/* Toggle theme switch */}
        <div className="theme-switch-container">
          <label className="switch" aria-label="Toggle theme">
            <input
              type="checkbox"
              checked={theme === 'dark'}
              onChange={toggleTheme}
            />
            <span className="slider"></span>
            <span className="icon">{theme === 'light' ? '🌞' : '🌙'}</span>
          </label>
        </div>
        <nav className="sidebar-nav">
          <Link to="/home" className="sidebar-link">Homepage</Link>
          <Link to="/tracking" className="sidebar-link">TrackingPage</Link>
        </nav>
      </aside>

      {/* Main content */}
      <main className="main">
        <header className="header">
          <h1>Tracking Dashboard</h1>
          <div className="profile-container" ref={menuRef}>
            <button
              className="profile-icon"
              onClick={() => setMenuOpen(open => !open)}
              aria-haspopup="true"
              aria-expanded={menuOpen}
              aria-label="Profile menu"
            >
              <FaUserCircle size={24} />
            </button>
            {menuOpen && (
              <div className="profile-dropdown" role="menu" aria-label="User profile menu">
                <button onClick={logout} role="menuitem" aria-label="Logout">
                  Logout
                </button>
              </div>
            )}
          </div>
        </header>

        <section className="content-box">
          <h2>Suivi mensuel des données</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="label" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Line type="monotone" dataKey="count" stroke="#8884d8" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </section>
      </main>
    </div>
  );
}
