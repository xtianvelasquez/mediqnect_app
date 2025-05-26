from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class Compartment_Set(Base):
  __tablename__ = 'compartment_set'
  set_id = Column(Integer, primary_key=True, autoincrement=True)
  set_name = Column(String(20), nullable=False)

  compartment = relationship('Compartment', back_populates='set', cascade='all, delete-orphan')

class Compartment(Base):
  __tablename__ = 'compartment'
  compartment_id = Column(Integer, primary_key=True, autoincrement=True)
  set_id = Column(Integer, ForeignKey('compartment_set.set_id', ondelete='CASCADE'), nullable=False)
  compartment_name = Column(String(20), nullable=False)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  set = relationship('Compartment_Set', back_populates='compartment')
  medicine_compartment = relationship('Medicine_Compartment', back_populates='compartment', cascade='all, delete-orphan')
  status = relationship('Statuses', back_populates='compartment')
