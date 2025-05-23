from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class Status_Type(Base):
  __tablename__ = 'status_type'
  type_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  type_name = Column(String(20), nullable=False)

  status = relationship('Statuses', back_populates='type', cascade='all, delete-orphan')

class Statuses(Base):
  __tablename__ = 'statuses'
  status_id = Column(Integer, primary_key=True, autoincrement=True)
  status_name = Column(String(20), nullable=False, index=True)

  type_id = Column(Integer, ForeignKey('status_type.type_id', ondelete='CASCADE'), nullable=False)

  type = relationship('Status_Type', back_populates='status')
  compartments = relationship('Compartment', back_populates='status')
  medicine = relationship('Medicine', back_populates='status')
  prescriptions = relationship('Prescription', back_populates='status')
  schedules = relationship('Schedule', back_populates='status')
  history = relationship('Intake_History', back_populates='status')
