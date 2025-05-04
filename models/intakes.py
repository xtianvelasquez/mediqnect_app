from sqlalchemy import Column, Integer, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from ..database import base

class Intake_History(base.Base):
  __tablename__ = 'intake_history'
  history_id = Column(Integer, primary_key=True, autoincrement=True)
  schedule_id = Column(Integer, ForeignKey('schedule.schedule_id', ondelete='CASCADE'), nullable=False)
  intake_time = Column(Time, nullable=False)
  intake_date = Column(Date, nullable=False)
  intake_status_id = Column(Integer, ForeignKey('status_value.value_id', ondelete='SET NULL'), nullable=True)
  
  schedule = relationship('Schedule', back_populates='intakes')
