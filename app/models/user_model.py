from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from zoneinfo import ZoneInfo

from app.database.base import Base

class User(Base):
  __tablename__ = 'user'
  user_id = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String(50), unique=True, nullable=False, index=True)
  password_hash = Column(String(255), nullable=False)
  dispenser_code = Column(String(20))
  created_at = Column(DateTime, server_default=func.now())
  modified_at = Column(DateTime, default=func.now(), onupdate=func.now())

  token = relationship('Token', back_populates='user', uselist=False)
  medicine = relationship('Medicine', back_populates='user', cascade='all, delete-orphan')
  medicine_compartment = relationship('Medicine_Compartment', back_populates='user', cascade='all, delete-orphan')
  intake = relationship('Intake', back_populates='user', cascade='all, delete-orphan')
  schedule = relationship('Schedule', back_populates='user', cascade='all, delete-orphan')
  history = relationship('Intake_History', back_populates='user', cascade='all, delete-orphan')
