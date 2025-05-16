from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class Medicine_Form(Base):
  __tablename__ = 'medicine_form'
  form_id = Column(Integer, primary_key=True, autoincrement=True)
  form_name = Column(String(10), nullable=False)

class Medicine(Base):
  __tablename__ = 'medicine'
  medicine_id = Column(Integer, primary_key=True, autoincrement=True)
  medicine_name = Column(String(50), nullable=False)
  net_content = Column(Integer)
  expiration_date = Column(Date)

  form_id = Column(Integer, ForeignKey('medicine_form.form_id', ondelete='CASCADE'), nullable=False)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  prescription = relationship('Prescription', back_populates='medicine', cascade='all, delete-orphan')
  medicine_compartment = relationship('Medicine_Compartment', back_populates='medicine', cascade='all, delete-orphan')

class Medicine_Compartment(Base):
  __tablename__ = 'medicine_compartment'
  medicine_compartment_id = Column(Integer, primary_key=True, autoincrement=True)
  compartment_id = Column(Integer, ForeignKey('compartment.compartment_id', ondelete='CASCADE'), nullable=False)
  medicine_id = Column(Integer, ForeignKey('medicine.medicine_id', ondelete='CASCADE'), nullable=False)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)

  compartment = relationship('Compartment', back_populates='medicine_compartment')
  medicine = relationship('Medicine', back_populates='medicine_compartment')
