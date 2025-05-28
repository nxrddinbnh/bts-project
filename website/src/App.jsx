import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AuthPage from './pages/AuthPage';
import MainPage from './pages/MainPage';
import PrivateRoute from './services/PrivateRoute';

function App() {
  return (
    <Routes>
      <Route path="/" element={<AuthPage />} />
      <Route path="/home" element={
        <PrivateRoute>
          <MainPage />
        </PrivateRoute>
      } />
    </Routes>
  );
}

export default App;