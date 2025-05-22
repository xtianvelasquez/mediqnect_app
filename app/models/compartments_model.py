from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class Compartment_Set(Base):
  __tablename__ = 'compartment_set'
  set_id = Column(Integer, primary_key=True, autoincrement=True)
  set_name = Column(String(10), nullable=False)

  compartments = relationship('Compartment', back_populates='set', cascade='all, delete-orphan')

class Compartment(Base):
  __tablename__ = 'compartment'
  compartment_id = Column(Integer, primary_key=True, autoincrement=True)
  compartment_name = Column(String(10), nullable=False)

  set_id = Column(Integer, ForeignKey('compartment_set.set_id', ondelete='CASCADE'), nullable=False)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  set = relationship('Compartment_Set', back_populates='compartments')
  medicine_compartment = relationship('Medicine_Compartment', back_populates='compartment', cascade='all, delete-orphan')
  status = relationship('Statuses', back_populates='compartments')
