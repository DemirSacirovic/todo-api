from database import SessionLocal, engine
from models import Base, User
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/docs")
    assert response.status_code == 200


def test_register_user():
    db = SessionLocal()
    db.query(User).filter(User.username == "testuser").delete()
    db.commit()
    db.close()

    response = client.post(
        "/register",
        json={"email": "test@test.com", "username": "testuser", "password": "test123"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login_user():
    db = SessionLocal()
    db.query(User).filter(User.username == "testuser").delete()
    db.commit()
    db.close()

    client.post("/register", json={
    "email": "login@test.com",
    "username": "logintest",
    "password": "pass123"
    })

      # Testiraj login
    response = client.post("/login", json={
    "username": "logintest",
    "password": "pass123"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
