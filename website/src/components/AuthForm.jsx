import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, register } from '../services/apiService';
import { useAuth } from '../context/AuthContext';

export default function AuthForm() {
  const [mode, setMode] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const { login: authLogin } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (mode === 'register' && password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    setLoading(true);
    try {
      if (mode === 'login') {
        await login(email, password); // Llama al servicio real
        authLogin();
      } else if (mode === 'register') {
        await register(email, password); // Llama al servicio real
        alert('Registration successful');
        setMode('login');
      } else {
        alert('Forgot password feature coming soon');
      }
    } catch (error) {
      alert(error.message || 'An error occurred');
    }
    setLoading(false);
  };

  const renderPasswordInput = (value, onChange, placeholder) => (
    <div style={{ position: 'relative' }}>
      <input
        type={showPassword ? 'text' : 'password'}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required
        style={{ width: '100%' }}
      />
      <button
        type="button"
        onClick={() => setShowPassword(!showPassword)}
        style={{
          position: 'absolute',
          right: '0.75rem',
          top: '50%',
          transform: 'translateY(-50%)',
          background: 'none',
          border: 'none',
          color: 'var(--text-200)',
          cursor: 'pointer',
          fontSize: '1rem',
        }}
      >
        {showPassword ? '🙈' : '👁️'}
      </button>
    </div>
  );

  return (
    <div className="auth-form-wrapper">
      <h2>
        {mode === 'login'
          ? 'Sign in'
          : mode === 'register'
            ? 'Create an account'
            : 'Password recovery'}
      </h2>

      <form onSubmit={handleSubmit}>
        {(mode === 'login' || mode === 'register') && (
          <>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            {renderPasswordInput(password, (e) => setPassword(e.target.value), 'Password')}
          </>
        )}

        {mode === 'register' &&
          renderPasswordInput(confirmPassword, (e) => setConfirmPassword(e.target.value), 'Confirm password')}

        {mode === 'forgot' && (
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        )}

        <button type="submit" disabled={loading}>
          {loading
            ? 'Processing...'
            : mode === 'login'
              ? 'Sign in'
              : mode === 'register'
                ? 'Register'
                : 'Send reset link'}
        </button>
      </form>

      <div className="auth-footer">
        {mode === 'login' && (
          <>
            <button type="button" onClick={() => setMode('register')}>
              Don't have an account? Register
            </button>
            <button type="button" onClick={() => setMode('forgot')}>
              Forgot your password?
            </button>
          </>
        )}
        {mode === 'register' && (
          <button type="button" onClick={() => setMode('login')}>
            Already have an account? Sign in
          </button>
        )}
        {mode === 'forgot' && (
          <button type="button" onClick={() => setMode('login')}>
            Back to login
          </button>
        )}
      </div>
    </div>
  );
}
