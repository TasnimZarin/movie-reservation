import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Movies from './pages/Movies';
import Bookings from './pages/Bookings';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login setToken={setToken} />} />
        <Route path="/movies" element={token ? <Movies /> : <Navigate to="/login" />} />
        <Route path="/bookings" element={token ? <Bookings /> : <Navigate to="/login" />} />
        <Route path="/" element={<Navigate to="/movies" />} />
      </Routes>
    </Router>
  );
}

export default App;