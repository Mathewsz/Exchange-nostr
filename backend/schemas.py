from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    nostr_pubkey: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    nostr_pubkey: str

class Token(BaseModel):
    access_token: str
    token_type: str

class OrderCreate(BaseModel):
    pair: str
    type: str
    price: float
    amount: float

class OrderResponse(BaseModel):
    id: int
    pair: str
    type: str
    status: str
    price: float
    amount: float
    created_at: datetime
