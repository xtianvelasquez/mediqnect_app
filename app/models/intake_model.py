from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database.base import Base

class Intake(Base):
  __tablename__ = 'intake'
  intake_id = Column(Integer, primary_key=True, autoincrement=True)
  start_datetime = Column(DateTime, nullable=False)
  end_date = Column(Date, nullable=False)
  hour_interval = Column(Integer, nullable=False)
  created_at = Column(DateTime, default=func.current_timestamp())
  modified_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  prescription = relationship('Prescription', back_populates='intake', cascade='all, delete-orphan')
  schedules = relationship('Schedule', back_populates='intake', cascade='all, delete-orphan')
