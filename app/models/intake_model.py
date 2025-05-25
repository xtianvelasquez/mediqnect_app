from sqlalchemy import Column, String, text, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from zoneinfo import ZoneInfo

from app.database.base import Base

class Dose_Component(Base):
  __tablename__ = 'dose_component'
  component_id = Column(Integer, primary_key=True, autoincrement=True)
  component_name = Column(String(20), nullable=False)

  intake = relationship('Intake', back_populates='component', cascade='all, delete-orphan')

class Color(Base):
  __tablename__ = 'color'
  color_id = Column(Integer, primary_key=True, autoincrement=True)
  color_name = Column(String(20), nullable=False, index=True)

  intake = relationship('Intake', back_populates='color')

class Intake(Base):
  __tablename__ = 'intake'
  intake_id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  medicine_id = Column(Integer, ForeignKey('medicine.medicine_id', ondelete='CASCADE'), nullable=False)
  start_datetime = Column(DateTime(timezone=True), nullable=False)
  end_datetime = Column(DateTime(timezone=True), nullable=False)
  hour_interval = Column(Integer, nullable=False)
  dose = Column(Integer, nullable=False)
  component_id = Column(Integer, ForeignKey('dose_component.component_id', ondelete='CASCADE'), nullable=False)
  color_id = Column(Integer, ForeignKey('color.color_id', ondelete='SET NULL'), nullable=True)
  is_scheduled = Column(Boolean, default=False, server_default=text('false'))
  created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo('UTC')))
  modified_at = Column(DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo('UTC')), onupdate=lambda: datetime.now(ZoneInfo('UTC')))
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  user = relationship('User', back_populates='intake')
  medicine = relationship('Medicine', back_populates='intake')
  component = relationship('Dose_Component', back_populates='intake')
  color = relationship('Color', back_populates='intake')
  schedule = relationship('Schedule', back_populates='intake', cascade='all, delete-orphan')
  status = relationship('Statuses', back_populates='intake')
