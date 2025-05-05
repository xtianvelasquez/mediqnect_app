from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.enums import Compartment_Set_Enum, Compartment_Enum

class Compartment_Set(Base):
  __tablename__ = 'compartment_set'
  set_id = Column(Integer, primary_key=True, autoincrement=True)
  set_name = Column(Enum(Compartment_Set_Enum, name='set_name_enum'), nullable=False)

  compartments = relationship('Compartment', back_populates='set', cascade='all, delete-orphan')

class Compartment(Base):
  __tablename__ = 'compartment'
  compartment_id = Column(Integer, primary_key=True, autoincrement=True)
  compartment_set_id = Column(Integer, ForeignKey('compartment_set.set_id', ondelete='CASCADE'), nullable=False)
  compartment_name = Column(Enum(Compartment_Enum, name='compartment_name_enum'), nullable=False)
  compartment_status_id = Column(Integer, ForeignKey('status_value.value_id', ondelete='SET NULL'), nullable=True)

  set = relationship("Compartment_Set", back_populates="compartments")
  medicine = relationship('Medicine', back_populates='compartment', cascade='all, delete-orphan') # medicine_model
