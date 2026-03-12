from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Use a separate test database
SQLALCHEMY_TEST_DATABASE_URL = "postgresql://zarintasnim:@localhost:5432/moviedb_test"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def setup_module():
    Base.metadata.create_all(bind=engine)

def teardown_module():
    Base.metadata.drop_all(bind=engine)


# ── AUTH TESTS ──────────────────────────────────────────────
def test_register():
    response = client.post("/auth/register", json={
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

def test_register_duplicate():
    client.post("/auth/register", json={"email": "dup@example.com", "password": "pass123"})
    response = client.post("/auth/register", json={"email": "dup@example.com", "password": "pass123"})
    assert response.status_code == 400

def test_login():
    client.post("/auth/register", json={"email": "login@example.com", "password": "pass123"})
    response = client.post("/auth/login", data={"username": "login@example.com", "password": "pass123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    client.post("/auth/register", json={"email": "wrong@example.com", "password": "pass123"})
    response = client.post("/auth/login", data={"username": "wrong@example.com", "password": "wrongpass"})
    assert response.status_code == 401


# ── HELPER ──────────────────────────────────────────────────
def get_admin_token():
    client.post("/auth/register", json={"email": "admin@example.com", "password": "admin123"})
    # Manually set admin role in test db
    db = TestingSessionLocal()
    from app.models.user import User
    user = db.query(User).filter(User.email == "admin@example.com").first()
    user.role = "admin"
    db.commit()
    db.close()
    response = client.post("/auth/login", data={"username": "admin@example.com", "password": "admin123"})
    return response.json()["access_token"]

def get_user_token():
    client.post("/auth/register", json={"email": "user@example.com", "password": "user123"})
    response = client.post("/auth/login", data={"username": "user@example.com", "password": "user123"})
    return response.json()["access_token"]


# ── MOVIE TESTS ─────────────────────────────────────────────
def test_create_movie_as_admin():
    token = get_admin_token()
    response = client.post("/movies/", json={
        "title": "Inception",
        "description": "A mind-bending thriller",
        "duration_mins": 148
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Inception"

def test_create_movie_as_user():
    token = get_user_token()
    response = client.post("/movies/", json={
        "title": "Interstellar",
        "description": "Space travel",
        "duration_mins": 169
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

def test_get_movies():
    response = client.get("/movies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ── THEATER TESTS ────────────────────────────────────────────
def test_create_theater_as_admin():
    token = get_admin_token()
    response = client.post("/theaters/", json={
        "name": "Theater A",
        "total_seats": 5
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Theater A"

def test_get_theaters():
    response = client.get("/theaters/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ── BOOKING TESTS ────────────────────────────────────────────
def test_double_booking_prevented():
    token1 = get_admin_token()

    # Create movie, theater, showtime
    movie = client.post("/movies/", json={"title": "Test Movie", "description": "desc", "duration_mins": 120},
                        headers={"Authorization": f"Bearer {token1}"}).json()
    theater = client.post("/theaters/", json={"name": "Theater B", "total_seats": 5},
                          headers={"Authorization": f"Bearer {token1}"}).json()
    showtime = client.post("/showtimes/", json={
        "movie_id": movie["id"],
        "theater_id": theater["id"],
        "start_time": "2025-06-01T18:00:00",
        "end_time": "2025-06-01T20:00:00"
    }, headers={"Authorization": f"Bearer {token1}"}).json()

    # Get a seat
    seats = client.get(f"/showtimes/{showtime['id']}/seats").json()
    seat_id = seats[0]["id"]

    # First booking
    r1 = client.post("/bookings/", json={"showtime_id": showtime["id"], "seat_id": seat_id},
                     headers={"Authorization": f"Bearer {token1}"})
    assert r1.status_code == 200

    # Second booking same seat — should fail
    token2 = get_user_token()
    r2 = client.post("/bookings/", json={"showtime_id": showtime["id"], "seat_id": seat_id},
                     headers={"Authorization": f"Bearer {token2}"})
    assert r2.status_code == 409