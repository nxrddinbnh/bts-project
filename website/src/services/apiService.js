const API_URL = 'http://localhost/solarpanel/api/index.php?path='

export async function register(email, password) {
  const response = await fetch(`${API_URL}login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, action: 'register' })
  })
  const data = await response.json()
  if (!response.ok) throw new Error(data.message || 'Registration failed')
  return data
}

export async function login(email, password) {
  const response = await fetch(`${API_URL}login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, action: 'login' })
  })
  const data = await response.json()
  if (!response.ok) throw new Error(data.message || 'Login failed')
  return data
}

export async function fetchCanFrames(filters = {}) {
  const params = new URLSearchParams(filters).toString();
  const res = await fetch(`${API_URL}can_frames${params ? '?' + params : ''}`);
  if (!res.ok) throw new Error('Error fetching data');
  return res.json();
}
