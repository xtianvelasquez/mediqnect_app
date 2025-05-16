from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class Status_Type(Base):
  __tablename__ = 'status_type'
  type_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  type_name = Column(String(20), nullable=False)

  label = relationship('Statuses', back_populates='type', cascade='all, delete-orphan')

class Statuses(Base):
  __tablename__ = 'statuses'
  status_id = Column(Integer, primary_key=True, autoincrement=True)
  status_name = Column(String(20), nullable=False, index=True)

  type_id = Column(Integer, ForeignKey('status_type.type_id', ondelete='CASCADE'), nullable=False)

  type = relationship('Status_Type', back_populates='label')
