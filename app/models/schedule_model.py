from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class Schedule(Base):
  __tablename__ = 'schedule' 
  schedule_id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  intake_id = Column(Integer, ForeignKey('intake.intake_id', ondelete='CASCADE'), nullable=False)
  scheduled_datetime = Column(DateTime(timezone=True), nullable=False, index=True)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  user = relationship('User', back_populates='schedule')
  intake = relationship('Intake', back_populates='schedule')
  history = relationship('Intake_History', back_populates='schedule', cascade='all, delete-orphan')
  status = relationship('Statuses', back_populates='schedule')
