import { FaUserCircle } from 'react-icons/fa';
import { useState, useRef, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

export default function Header({ title = "Dashboard", onLogout }) {
    const [menuOpen, setMenuOpen] = useState(false);
    const menuRef = useRef(null);
    const { logout } = useAuth();

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
                    onClick={() => setMenuOpen((open) => !open)}
                    aria-label="Profile menu"
                >
                    <FaUserCircle size={24} />
                </button>
                {menuOpen && (
                    <div className="profile-menu">
                        <button onClick={logout} aria-label="Logout">
                            Logout
                        </button>
                    </div>
                )}
            </div>
        </header>
    );
}
