from sqlalchemy import Column, Integer, Date, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.enums import Dose_Component_Enum

class Dose_Component(Base):
  __tablename__ = 'dose_component'
  component_id = Column(Integer, primary_key=True, autoincrement=True)
  component_name = Column(Enum(Dose_Component_Enum, name='dose_type_enum'), nullable=False)

class Prescription(Base):
  __tablename__ = 'prescription'
  prescription_id = Column(Integer, primary_key=True, autoincrement=True)
  medicine_id = Column(Integer, ForeignKey('medicine.medicine_id', ondelete='CASCADE'), nullable=False)
  dose = Column(Integer, nullable=False)
  dose_component_id = Column(Integer, ForeignKey('dose_component.component_id', ondelete='CASCADE'), nullable=False)
  hour_interval = Column(Integer, nullable=False)
  start_date = Column(DateTime, nullable=False)
  end_date = Column(Date, nullable=False)
  prescription_status_id = Column(Integer, ForeignKey('status_value.value_id', ondelete='SET NULL'), nullable=True)
  date_created = Column(DateTime, default=func.current_timestamp())
  date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

  schedules = relationship('Schedule', back_populates='prescription', cascade='all, delete-orphan') # schedule
