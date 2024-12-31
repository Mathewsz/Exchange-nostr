import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..database import Base
from ..models import User, Order, Wallet

@pytest.fixture(scope="function")
def test_db():
    """Criar banco de dados de teste em memória"""
    engine = create_engine(
        "sqlite:///:memory:", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_user(test_db):
    """Criar usuário de teste"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        nostr_pubkey="sample_nostr_pubkey"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

@pytest.fixture
def sample_wallet(test_db, sample_user):
    """Criar carteira de teste"""
    wallet = Wallet(
        user_id=sample_user.id,
        currency="BTC",
        balance=1.0
    )
    test_db.add(wallet)
    test_db.commit()
    test_db.refresh(wallet)
    return wallet

@pytest.fixture
def sample_order(test_db, sample_user):
    """Criar ordem de teste"""
    order = Order(
        user_id=sample_user.id,
        pair="BTC/USDT",
        type="buy",
        status="pending",
        price=50000.0,
        amount=0.1
    )
    test_db.add(order)
    test_db.commit()
    test_db.refresh(order)
    return order
