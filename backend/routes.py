from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from .database import get_db
from .models import User, Wallet
from .auth import (
    authenticate_user, 
    create_access_token, 
    get_current_active_user, 
    get_password_hash
)
from .config import settings
from .schemas import UserCreate, UserResponse, Token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar se usuário já existe
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Criar novo usuário
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        nostr_pubkey=user.nostr_pubkey
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Criar carteira inicial para Bitcoin e USDT
    wallets = [
        Wallet(user_id=db_user.id, currency='BTC', balance=0.0),
        Wallet(user_id=db_user.id, currency='USDT', balance=0.0)
    ]
    db.add_all(wallets)
    db.commit()
    
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        nostr_pubkey=db_user.nostr_pubkey
    )

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        nostr_pubkey=current_user.nostr_pubkey
    )
