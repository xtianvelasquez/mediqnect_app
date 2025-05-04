from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import base
from ..enums import Medicine_Form_Enum

class Medicine_Form(base.Base):
  __tablename__ = 'medicine_form'
  form_id = Column(Integer, primary_key=True, autoincrement=True)
  form_name = Column(Enum(Medicine_Form_Enum, name='form_name_enum'), nullable=False)

class Medicine(base.Base):
  __tablename__ = 'medicine'
  medicine_id = Column(Integer, primary_key=True, autoincrement=True)
  compartment_id = Column(Integer, ForeignKey('compartment.compartment_id', ondelete='SET NULL'), nullable=True)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  medicine_name = Column(String(100), nullable=False, unique=True)
  medicine_form_id = Column(Integer, ForeignKey('medicine_form.form_id', ondelete='CASCADE'), nullable=False)
  net_content = Column(Integer, nullable=False)
  expiration_date = Column(Date)
  medicine_status_id = Column(Integer, ForeignKey('status_value.value_id', ondelete='SET NULL'), nullable=True)
  date_created = Column(DateTime, default=func.current_timestamp())
  date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

  compartment = relationship('Compartment', back_populates='medicine') # compartment
  user = relationship('User', back_populates='medicines') # user
