from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.enums.medicine_enum import Dose_Component_Enum

class Dose_Component(Base):
  __tablename__ = 'dose_component'
  component_id = Column(Integer, primary_key=True, autoincrement=True)
  component_name = Column(Enum(Dose_Component_Enum, name='component_name_enum'), nullable=False)

class Prescription(Base):
  __tablename__ = 'prescription'
  dose = Column(Integer, nullable=False)
  dose_component_id = Column(Integer, ForeignKey('dose_component.component_id', ondelete='CASCADE'), nullable=False)
  medicine_id = Column(Integer, ForeignKey('medicine.medicine_id', ondelete='CASCADE'), nullable=False)
  intake_id = Column(Integer, ForeignKey('intake.intake_id', ondelete='CASCADE'), nullable=False)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  medicine = relationship('Medicine', back_populates='prescription')
  intake = relationship('Intake', back_populates='prescription')
  user = relationship('User', back_populates='prescriptions')