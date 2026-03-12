import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// const API = 'http://127.0.0.1:8000';
const API = 'https://movie-reservation-po09.onrender.com';

function Movies() {
  const [movies, setMovies] = useState([]);
  const [showtimes, setShowtimes] = useState([]);
  const [seats, setSeats] = useState([]);
  const [selectedShowtime, setSelectedShowtime] = useState(null);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  useEffect(() => {
    axios.get(`${API}/movies/`).then(res => setMovies(res.data));
    axios.get(`${API}/showtimes/`).then(res => setShowtimes(res.data));
  }, []);

  const loadSeats = (showtimeId) => {
    setSelectedShowtime(showtimeId);
    axios.get(`${API}/showtimes/${showtimeId}/seats`).then(res => setSeats(res.data));
  };

  const bookSeat = async (seatId) => {
    try {
      await axios.post(`${API}/bookings/`, 
        { showtime_id: selectedShowtime, seat_id: seatId },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setMessage('✅ Seat booked successfully!');
      loadSeats(selectedShowtime);
    } catch (err) {
      setMessage(err.response?.data?.detail || '❌ Booking failed');
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>🎬 Movies</h1>
        <div>
          <button style={styles.navBtn} onClick={() => navigate('/bookings')}>My Bookings</button>
          <button style={{...styles.navBtn, backgroundColor: '#555'}} onClick={logout}>Logout</button>
        </div>
      </div>

      {message && <p style={styles.message}>{message}</p>}

      <div style={styles.grid}>
        {movies.map(movie => (
          <div key={movie.id} style={styles.card}>
            <h2 style={styles.movieTitle}>{movie.title}</h2>
            <p style={styles.desc}>{movie.description}</p>
            <p style={styles.duration}>⏱ {movie.duration_mins} mins</p>
            <h4 style={styles.showtimeLabel}>Showtimes:</h4>
            {showtimes.filter(s => s.movie_id === movie.id).map(s => (
              <button key={s.id} style={styles.showtimeBtn} onClick={() => loadSeats(s.id)}>
                {new Date(s.start_time).toLocaleString()}
              </button>
            ))}
          </div>
        ))}
      </div>

      {selectedShowtime && (
        <div style={styles.seatSection}>
          <h2 style={styles.seatTitle}>🪑 Select a Seat</h2>
          <div style={styles.seatGrid}>
            {seats.map(seat => (
              <button
                key={seat.id}
                style={{...styles.seat, backgroundColor: seat.status === 'available' ? '#e94560' : '#555'}}
                onClick={() => seat.status === 'available' && bookSeat(seat.id)}
                disabled={seat.status !== 'available'}
              >
                {seat.row}{seat.seat_number}
              </button>
            ))}
          </div>
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
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' },
  card: { backgroundColor: '#16213e', padding: '20px', borderRadius: '12px' },
  movieTitle: { color: '#e94560', marginBottom: '8px' },
  desc: { color: '#aaa', marginBottom: '8px' },
  duration: { color: '#888', marginBottom: '12px' },
  showtimeLabel: { color: '#ccc', marginBottom: '8px' },
  showtimeBtn: { display: 'block', width: '100%', padding: '8px', marginBottom: '8px', borderRadius: '6px', border: 'none', backgroundColor: '#0f3460', color: 'white', cursor: 'pointer' },
  seatSection: { marginTop: '40px' },
  seatTitle: { color: '#e94560', marginBottom: '16px' },
  seatGrid: { display: 'flex', flexWrap: 'wrap', gap: '10px' },
  seat: { width: '60px', height: '60px', borderRadius: '8px', border: 'none', color: 'white', fontSize: '14px', cursor: 'pointer' },
};

export default Movies;