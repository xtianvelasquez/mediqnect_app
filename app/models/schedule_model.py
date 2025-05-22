from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class Schedule(Base):
  __tablename__ = 'schedule' 
  schedule_id = Column(Integer, primary_key=True, autoincrement=True)
  scheduled_datetime = Column(DateTime, nullable=False, index=True)

  prescription_id = Column(Integer, ForeignKey('prescription.prescription_id', ondelete='CASCADE'), nullable=False)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)
  
  prescription = relationship('Prescription', back_populates='schedules')
  history = relationship('Intake_History', back_populates='schedule', cascade='all, delete-orphan')
  user = relationship('User', back_populates='schedules')
  status = relationship('Statuses', back_populates='schedules')
