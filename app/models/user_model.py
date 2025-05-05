from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship

from app.database.base import Base

class User(Base):
  __tablename__ = 'user'
  user_id = Column(Integer, primary_key=True, autoincrement=True)
  dispenser_code = Column(Text(), unique=True, index=True)
  username = Column(String(200), nullable=False, unique=True)
  user_password = Column(String(100), nullable=False)
  date_created = Column(DateTime, default=func.current_timestamp())
  date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

  medicines = relationship('Medicine', back_populates='user', cascade='all, delete-orphan') # medicine_model
