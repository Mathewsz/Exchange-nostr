from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

from ..main import app
from ..database import get_db
from ..models import User
from ..auth import get_password_hash

def override_get_db():
    """Substituir dependência de banco de dados para testes"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_user(test_db):
    """Testar rota de criação de usuário"""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword123",
        "nostr_pubkey": "new_nostr_pubkey"
    }
    
    response = client.post("/api/v1/register", json=user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"

def test_login_user(test_db):
    """Testar rota de login"""
    # Criar usuário de teste
    hashed_password = get_password_hash("testpassword")
    test_user = User(
        username="loginuser",
        email="login@example.com",
        hashed_password=hashed_password,
        nostr_pubkey="login_nostr_pubkey"
    )
    test_db.add(test_user)
    test_db.commit()
    
    # Tentar login
    login_data = {
        "username": "loginuser",
        "password": "testpassword"
    }
    
    response = client.post("/api/v1/token", data=login_data)
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_get_user_profile(test_db):
    """Testar recuperação de perfil de usuário"""
    # Criar usuário de teste
    hashed_password = get_password_hash("testpassword")
    test_user = User(
        username="profileuser",
        email="profile@example.com",
        hashed_password=hashed_password,
        nostr_pubkey="profile_nostr_pubkey"
    )
    test_db.add(test_user)
    test_db.commit()
    
    # Fazer login para obter token
    login_data = {
        "username": "profileuser",
        "password": "testpassword"
    }
    
    login_response = client.post("/api/v1/token", data=login_data)
    access_token = login_response.json()["access_token"]
    
    # Recuperar perfil
    response = client.get(
        "/api/v1/users/me", 
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "profileuser"
    assert data["email"] == "profile@example.com"
