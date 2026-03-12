import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// const API = 'http://127.0.0.1:8000';
const API = 'https://movie-reservation-po09.onrender.com';

function Bookings() {
  const [bookings, setBookings] = useState([]);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  useEffect(() => {
    axios.get(`${API}/bookings/me`, {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setBookings(res.data));
  }, []);

  const cancelBooking = async (id) => {
    try {
      await axios.delete(`${API}/bookings/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessage('✅ Booking cancelled!');
      setBookings(bookings.filter(b => b.id !== id));
    } catch (err) {
      setMessage('❌ Could not cancel booking');
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>🎟 My Bookings</h1>
        <div>
          <button style={styles.navBtn} onClick={() => navigate('/movies')}>Movies</button>
          <button style={{...styles.navBtn, backgroundColor: '#555'}} onClick={logout}>Logout</button>
        </div>
      </div>

      {message && <p style={styles.message}>{message}</p>}

      {bookings.length === 0 ? (
        <p style={styles.empty}>No bookings yet. Go book a seat! 🎬</p>
      ) : (
        <div style={styles.grid}>
          {bookings.map(booking => (
            <div key={booking.id} style={styles.card}>
              <p style={styles.info}>🎬 Showtime ID: {booking.showtime_id}</p>
              <p style={styles.info}>🪑 Seat ID: {booking.seat_id}</p>
              <p style={styles.status}>Status: {booking.status}</p>
              <button style={styles.cancelBtn} onClick={() => cancelBooking(booking.id)}>
                Cancel Booking
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: { backgroundColor: '#1a1a2e', minHeight: '100vh', padding: '20px', color: 'white' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' },
  title: { color: '#e94560' },
  navBtn: { padding: '10px 20px', borderRadius: '8px', border: 'none', backgroundColor: '#e94560', color: 'white', cursor: 'pointer', marginLeft: '10px' },
  message: { color: '#4caf50', textAlign: 'center', fontSize: '18px' },
  empty: { color: '#aaa', textAlign: 'center', fontSize: '18px', marginTop: '40px' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' },
  card: { backgroundColor: '#16213e', padding: '20px', borderRadius: '12px' },
  info: { color: '#ccc', marginBottom: '8px' },
  status: { color: '#4caf50', marginBottom: '16px' },
  cancelBtn: { padding: '10px 20px', borderRadius: '8px', border: 'none', backgroundColor: '#e94560', color: 'white', cursor: 'pointer' },
};

export default Bookings;