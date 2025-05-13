from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship

from app.database.base import Base

class User(Base):
  __tablename__ = 'user'
  user_id = Column(Integer, primary_key=True, autoincrement=True)
  dispenser_code = Column(Text(), unique=True, index=True)
  username = Column(String(50), unique=True, nullable=False)
  password = Column(String(50), nullable=False)
  date_created = Column(DateTime, default=func.current_timestamp())
  date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

  token = relationship('Token', back_populates='user', uselist=False)
  prescriptions = relationship('Prescription', back_populates='user', cascade='all, delete-orphan')
  schedules = relationship('Schedule', back_populates='user', cascade='all, delete-orphan')
