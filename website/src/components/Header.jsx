import { useState, useRef, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { AvatarGenerator } from 'random-avatar-generator';
import { useLocation } from 'react-router-dom';

const generator = new AvatarGenerator();

export default function Header({ onLogout }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef(null);
  const { user, logout } = useAuth();
  const [avatarUrl, setAvatarUrl] = useState('');
  const location = useLocation();

  // Déterminer le titre en fonction de la route
  const title = location.pathname === '/home' ? 'Can Frame' : 'Utilisateurs';

  useEffect(() => {
    const avatar = generator.generateRandomAvatar();
    setAvatarUrl(avatar);
  }, []);

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <header className="header">
      <h1>{title}</h1>
      <div className="profile-container" ref={menuRef}>
        <button
          className="profile-icon"
          onClick={() => setMenuOpen(open => !open)}
          aria-label="Profile menu"
          style={{ padding: 0, border: 'none', background: 'none' }}
        >
          {avatarUrl ? (
            <img
              src={avatarUrl}
              alt="Profile"
              style={{ width: 32, height: 32, borderRadius: '50%' }}
            />
          ) : (
            <span>👤</span>
          )}
        </button>
        {menuOpen && (
          <div className="profile-menu">
            <button onClick={logout} aria-label="Logout">Logout</button>
          </div>
        )}
      </div>
    </header>
  );
}
