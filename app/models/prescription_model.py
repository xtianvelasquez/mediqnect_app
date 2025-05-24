from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database.base import Base

class Prescription(Base):
  __tablename__ = 'prescription'
  prescription_id = Column(Integer, primary_key=True, autoincrement=True)
  medicine_id = Column(Integer, ForeignKey('medicine.medicine_id', ondelete='CASCADE'), nullable=False)
  intake_id = Column(Integer, ForeignKey('intake.intake_id', ondelete='CASCADE'), nullable=False)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)
  created_at = Column(DateTime, default=func.current_timestamp())
  modified_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

  medicine = relationship('Medicine', back_populates='prescription', cascade='all, delete')
  intake = relationship('Intake', back_populates='prescription', cascade='all, delete')
  schedules = relationship('Schedule', back_populates='prescription', cascade='all, delete-orphan')
  user = relationship('User', back_populates='prescriptions')
  status = relationship('Statuses', back_populates='prescriptions')
