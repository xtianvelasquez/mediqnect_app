from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from zoneinfo import ZoneInfo

from app.database.base import Base

class Medicine_Form(Base):
  __tablename__ = 'medicine_form'
  form_id = Column(Integer, primary_key=True, autoincrement=True)
  form_name = Column(String(20), nullable=False)

  medicine = relationship('Medicine', back_populates='form', cascade='all, delete-orphan')

class Medicine(Base):
  __tablename__ = 'medicine'
  medicine_id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
  medicine_name = Column(String(50), nullable=False)
  form_id = Column(Integer, ForeignKey('medicine_form.form_id', ondelete='CASCADE'), nullable=False)
  net_content = Column(Integer)
  expiration_date = Column(Date)
  created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo('UTC')).replace(second=0, microsecond=0))
  modified_at = Column(DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo('UTC')).replace(second=0, microsecond=0), onupdate=lambda: datetime.now(ZoneInfo('UTC')).replace(second=0, microsecond=0))
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  user = relationship('User', back_populates='medicine')
  form = relationship('Medicine_Form', back_populates='medicine')
  medicine_compartment = relationship('Medicine_Compartment', back_populates='medicine', cascade='all, delete-orphan', uselist=False)
  intake = relationship('Intake', back_populates='medicine', cascade='all, delete-orphan', uselist=False)
  status = relationship('Statuses', back_populates='medicine')

class Medicine_Compartment(Base):
  __tablename__ = 'medicine_compartment'
  medicine_compartment_id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  compartment_id = Column(Integer, ForeignKey('compartment.compartment_id', ondelete='CASCADE'), nullable=False)
  medicine_id = Column(Integer, ForeignKey('medicine.medicine_id', ondelete='CASCADE'), nullable=False)

  user = relationship('User', back_populates='medicine_compartment')
  compartment = relationship('Compartment', back_populates='medicine_compartment')
  medicine = relationship('Medicine', back_populates='medicine_compartment')
