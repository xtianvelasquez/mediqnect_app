from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.orm import relationship

from app.database.base import Base

class User(Base):
  __tablename__ = 'user'
  user_id = Column(Integer, primary_key=True, autoincrement=True)
  dispenser_code = Column(String(10), unique=True)
  username = Column(String(50), unique=True, nullable=False, index=True)
  password_hash = Column(String(255), nullable=False)
  created_at = Column(DateTime, default=func.current_timestamp())
  modified_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

  token = relationship('Token', back_populates='user', uselist=False)
  prescriptions = relationship('Prescription', back_populates='user', cascade='all, delete-orphan')
  schedules = relationship('Schedule', back_populates='user', cascade='all, delete-orphan')
  history = relationship('Intake_History', back_populates='user', cascade='all, delete-orphan')
