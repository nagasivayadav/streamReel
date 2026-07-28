"""
Run with: pytest
Requires a running Postgres instance matching DATABASE_URL,
or point DATABASE_URL at a throwaway test database before running.
"""
from fastapi.testclient import TestClient
from streamreel_backend.app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "StreamReel backend is running"


def test_signup_and_login():
    email = "testuser@example.com"
    password = "supersecure123"

    # Clean slate isn't handled here — in a real suite, use a fixture
    # that resets the test database between runs.
    signup_response = client.post(
        "/api/auth/signup", json={"email": email, "password": password}
    )
    assert signup_response.status_code in (200, 400)  # 400 if user already exists from a prior run

    login_response = client.post(
        "/api/auth/login", json={"email": email, "password": password}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_login_wrong_password_rejected():
    response = client.post(
        "/api/auth/login",
        json={"email": "testuser@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401
