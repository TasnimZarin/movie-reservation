import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API = 'http://127.0.0.1:8000';

function Login(props) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post(`${API}/auth/login`,
        new URLSearchParams({ username: email, password }),
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );
      localStorage.setItem('token', response.data.access_token);
      props.setToken(response.data.access_token);
      navigate('/movies');
    } catch (err) {
      setError('Invalid email or password');
    }
  };

  const handleRegister = async () => {
    try {
      await axios.post(`${API}/auth/register`, { email, password });
      handleLogin();
    } catch (err) {
      setError('Registration failed. Email may already exist.');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.box}>
        <h1 style={styles.title}>🎬 Movie Reservation</h1>
        {error && <p style={styles.error}>{error}</p>}
        <input
          style={styles.input}
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        <input
          style={styles.input}
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <button style={styles.button} onClick={handleLogin}>Login</button>
        <button style={{...styles.button, backgroundColor: '#555'}} onClick={handleRegister}>Register</button>
      </div>
    </div>
  );
}

const styles = {
  container: { display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#1a1a2e' },
  box: { backgroundColor: '#16213e', padding: '40px', borderRadius: '12px', width: '350px', display: 'flex', flexDirection: 'column', gap: '16px' },
  title: { color: '#e94560', textAlign: 'center', marginBottom: '10px' },
  input: { padding: '12px', borderRadius: '8px', border: '1px solid #444', backgroundColor: '#0f3460', color: 'white', fontSize: '16px' },
  button: { padding: '12px', borderRadius: '8px', border: 'none', backgroundColor: '#e94560', color: 'white', fontSize: '16px', cursor: 'pointer' },
  error: { color: '#e94560', textAlign: 'center' }
};

export default Login;