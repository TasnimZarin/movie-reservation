# 🎬 Movie Reservation System

A full-stack movie reservation web application with JWT authentication, real-time seat booking, and PostgreSQL row-level locking to prevent double-bookings.

🔴 **Live Demo:** [movie-reservation-five.vercel.app](https://movie-reservation-five.vercel.app)

---

## 🛠 Tech Stack

**Frontend:** React, Axios, React Router  
**Backend:** FastAPI, SQLAlchemy, Alembic  
**Database:** PostgreSQL  
**Auth:** JWT (python-jose), bcrypt  
**Deployment:** Vercel (frontend), Render (backend)  
**Testing:** pytest  
**Containerization:** Docker, Docker Compose  

---

## ✨ Features

- User registration and login with JWT authentication
- Browse movies with showtimes
- Interactive seat map with real-time availability
- Seat booking with PostgreSQL row-level locking (`SELECT FOR UPDATE`) to prevent concurrent double-bookings
- View and cancel bookings
- Fully deployed and accessible online

---

## 🏗 Architecture
```
React Frontend (Vercel)
        ↓
FastAPI Backend (Render)
        ↓
PostgreSQL Database (Render)
```

---

## 🚀 Running Locally

### Backend
```bash
cd movie-reservation
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
npm install
npm start
```

### Docker
```bash
docker-compose up --build
```

---

## 🧪 Tests
```bash
pytest tests/
```

10 tests covering auth, movies, bookings, and seat locking.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Register user |
| POST | /auth/login | Login and get JWT |
| GET | /movies/ | List all movies |
| GET | /showtimes/{id}/seats | Get seat availability |
| POST | /bookings/ | Book a seat |
| DELETE | /bookings/{id} | Cancel booking |