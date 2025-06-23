from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database.base import Base

class Intake_History(Base):
  __tablename__ = 'intake_history'
  history_id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  schedule_id = Column(Integer, ForeignKey('schedule.schedule_id', ondelete='CASCADE'), nullable=False)
  history_datetime = Column(DateTime, nullable=True, index=True)
  modified_at = Column(DateTime, default=func.now(), onupdate=func.now())
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  user = relationship('User', back_populates='history')
  schedule = relationship('Schedule', back_populates='history')
  status = relationship('Statuses', back_populates='history')
