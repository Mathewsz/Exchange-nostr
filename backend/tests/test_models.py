import pytest
from sqlalchemy.exc import IntegrityError

def test_create_user(test_db, sample_user):
    """Testar criação de usuário"""
    assert sample_user.username == "testuser"
    assert sample_user.email == "test@example.com"
    assert sample_user.nostr_pubkey == "sample_nostr_pubkey"

def test_create_wallet(test_db, sample_wallet, sample_user):
    """Testar criação de carteira"""
    assert sample_wallet.user_id == sample_user.id
    assert sample_wallet.currency == "BTC"
    assert sample_wallet.balance == 1.0

def test_create_order(test_db, sample_order, sample_user):
    """Testar criação de ordem"""
    assert sample_order.user_id == sample_user.id
    assert sample_order.pair == "BTC/USDT"
    assert sample_order.type == "buy"
    assert sample_order.status == "pending"
    assert sample_order.price == 50000.0
    assert sample_order.amount == 0.1

def test_unique_username(test_db, sample_user):
    """Testar restrição de username único"""
    from ..models import User
    
    duplicate_user = User(
        username="testuser",
        email="another@example.com",
        hashed_password="another_password",
        nostr_pubkey="another_pubkey"
    )
    
    test_db.add(duplicate_user)
    
    with pytest.raises(IntegrityError):
        test_db.commit()
