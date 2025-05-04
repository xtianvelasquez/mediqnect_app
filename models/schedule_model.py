from sqlalchemy import Column, Integer, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from ..database import base

class Schedule(base.Base):
  __tablename__ = 'schedule'
  schedule_id = Column(Integer, primary_key=True, autoincrement=True)
  prescription_id = Column(Integer, ForeignKey('prescription.prescription_id', ondelete='CASCADE'), nullable=False)
  scheduled_time = Column(Time, nullable=False)
  scheduled_date = Column(Date, nullable=False)
  schedule_status_id = Column(Integer, ForeignKey('status_value.value_id', ondelete='SET NULL'), nullable=True)

  prescription = relationship('Prescription', back_populates='schedules') # prescription
  intakes = relationship('Intake_History', back_populates='schedule', cascade='all, delete-orphan') # intakes