from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class Intake_History(Base):
  __tablename__ = 'intake_history'
  history_id = Column(Integer, primary_key=True, autoincrement=True)
  history_datetime = Column(DateTime, nullable=False, index=True)
  
  schedule_id = Column(Integer, ForeignKey('schedule.schedule_id', ondelete='CASCADE'), nullable=False)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  schedule = relationship('Schedule', back_populates='history')
  user = relationship('User', back_populates='history')
