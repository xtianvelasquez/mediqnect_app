from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class Dose_Component(Base):
  __tablename__ = 'dose_component'
  component_id = Column(Integer, primary_key=True, autoincrement=True)
  component_name = Column(String(10), nullable=False)

class Intake(Base):
  __tablename__ = 'intake'
  intake_id = Column(Integer, primary_key=True, autoincrement=True)
  start_datetime = Column(DateTime, nullable=False)
  end_date = Column(Date, nullable=False)
  hour_interval = Column(Integer, nullable=False)
  dose = Column(Integer, nullable=False)

  dose_component_id = Column(Integer, ForeignKey('dose_component.component_id', ondelete='CASCADE'), nullable=False) # change to component_id
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  prescription = relationship('Prescription', back_populates='intake', cascade='all, delete-orphan')
  status = relationship('Statuses', back_populates='intake')
