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

  component_id = Column(Integer, ForeignKey('dose_component.component_id', ondelete='CASCADE'), nullable=False)

  prescription = relationship('Prescription', back_populates='intake')
  color = relationship('Intake_Color', back_populates='intake', cascade='all, delete-orphan')

class Intake_Color(Base):
  __tablename__ = 'intake_color'
  color_id = Column(Integer, primary_key=True, autoincrement=True)
  color_name = Column(String(10), nullable=False)
  intake_id = Column(Integer, ForeignKey('intake.intake_id', ondelete='CASCADE'), nullable=False)

  intake = relationship('Intake', back_populates='color')
  schedule = relationship('Schedule', back_populates='color')
