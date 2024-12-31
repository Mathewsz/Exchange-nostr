from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class OrderType(enum.Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(enum.Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    nostr_pubkey = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    orders = relationship("Order", back_populates="user")
    wallets = relationship("Wallet", back_populates="user")

class Wallet(Base):
    __tablename__ = 'wallets'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    currency = Column(String)
    balance = Column(Float, default=0.0)
    
    user = relationship("User", back_populates="wallets")

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    pair = Column(String)  # Exemplo: BTC/USDT
    type = Column(Enum(OrderType))
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    price = Column(Float)
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="orders")

class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True, index=True)
    buyer_order_id = Column(Integer, ForeignKey('orders.id'))
    seller_order_id = Column(Integer, ForeignKey('orders.id'))
    pair = Column(String)
    price = Column(Float)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
