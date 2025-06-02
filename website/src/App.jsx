import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AuthPage from './pages/AuthPage';
import MainPage from './pages/MainPage';
import UserList from './pages/UserList';
import PrivateRoute from './services/PrivateRoute';

function App() {
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) return savedTheme;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  });

  const toggleTheme = () => {
    setTheme((curr) => (curr === 'dark' ? 'light' : 'dark'));
  };

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  return (
    <Routes>
      <Route path="/" element={<AuthPage theme={theme} toggleTheme={toggleTheme} />} />
      
      <Route
        path="/home"
        element={
          <PrivateRoute>
            <MainPage theme={theme} toggleTheme={toggleTheme} />
          </PrivateRoute>
        }
      />

      <Route
        path="/users"
        element={
          <PrivateRoute>
            <UserList theme={theme} toggleTheme={toggleTheme}/>
          </PrivateRoute>
        }
      />
    </Routes>
  );
}

export default App;
