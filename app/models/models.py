from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean, Date, func
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.enums import Status_Type_Enum, Statuses_Enum, Compartment_Set_Enum, Compartment_Enum, Dose_Component_Enum, Medicine_Form_Enum

class Status_Type(Base):
  __tablename__ = 'status_type'
  type_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  type_name = Column(Enum(Status_Type_Enum, name='type_name_enum'), nullable=False)

  label = relationship('Status_Label', back_populates='type', cascade='all, delete-orphan')

class Statuses(Base):
  __tablename__ = 'statuses'
  status_id = Column(Integer, primary_key=True, autoincrement=True)
  status_name = Column(Enum(Statuses_Enum, name='status_name_enum'), nullable=False)

  type_id = Column(Integer, ForeignKey('status_type.type_id', ondelete='CASCADE'), nullable=False)

  type = relationship('Status_Type', back_populates='label')

class Compartment_Set(Base):
  __tablename__ = 'compartment_set'
  set_id = Column(Integer, primary_key=True, autoincrement=True)
  set_name = Column(Enum(Compartment_Set_Enum, name='set_name_enum'), nullable=False)

  compartments = relationship('Compartment', back_populates='set', cascade='all, delete-orphan')

class Compartment(Base):
  __tablename__ = 'compartment'
  compartment_id = Column(Integer, primary_key=True, autoincrement=True)
  compartment_name = Column(Enum(Compartment_Enum, name='compartment_name_enum'), nullable=False)

  set_id = Column(Integer, ForeignKey('compartment_set.set_id', ondelete='CASCADE'), nullable=False)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  set = relationship('Compartment_Set', back_populates='compartments')
  compartment_medicine = relationship('Compartment_Medicine', back_populates='compartment', cascade='all, delete-orphan')

class Dose_Component(Base):
  __tablename__ = 'dose_component'
  component_id = Column(Integer, primary_key=True, autoincrement=True)
  component_name = Column(Enum(Dose_Component_Enum, name='component_name_enum'), nullable=False)

class Medicine_Form(Base):
  __tablename__ = 'medicine_form'
  form_id = Column(Integer, primary_key=True, autoincrement=True)
  form_name = Column(Enum(Medicine_Form_Enum, name='form_name_enum'), nullable=False)

class Token(Base):
  __tablename__ = 'token'
  token_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  token_hash = Column(String, nullable=False)
  is_active = Column(Boolean)
  issued_at = Column(DateTime)
  expires_at = Column(DateTime)
  revoked_at = Column(DateTime)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='SET NULL'), nullabe=True)

  user = relationship('User', back_populates='token')

class User(Base):
  __tablename__ = 'user'
  user_id = Column(Integer, primary_key=True, autoincrement=True)
  dispenser_code = Column(Text(), unique=True, index=True)
  username = Column(String(50), unique=True, nullable=False)
  password = Column(String(50), nullable=False)
  date_created = Column(DateTime, default=func.current_timestamp())
  date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

  token = relationship('Token', back_populates='user', uselist=False)
  prescriptions = relationship('Prescription', back_populates='user', cascade='all, delete-orphan')
  schedules = relationship('Schedule', back_populates='user', cascade='all, delete-orphan')

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

class Medicine(Base):
  __tablename__ = 'medicine'
  medicine_id = Column(Integer, primary_key=True, autoincrement=True)
  medicine_name = Column(String(100), nullable=False)
  net_content = Column(Integer)
  expiration_date = Column(Date)
  created_at = Column(DateTime, default=func.current_timestamp())
  modified_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

  form_id = Column(Integer, ForeignKey('medicine_form.form_id', ondelete='CASCADE'), nullable=False)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  prescription = relationship('Prescription', back_populates='medicine', cascade='all, delete-orphan')

class Medicine_Compartment(Base):
  __tablename__ = 'medicine_compartment'
  medicine_compartment_id = Column(Integer, primary_key=True, autoincrement=True)
  compartment_id = Column(Integer, ForeignKey('compartment.compartment_id', ondelete='CASCADE'), nullable=False)
  medicine_id = Column(Integer, ForeignKey('medicine.medicine_id', ondelete='CASCADE'), nullable=False)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)

  compartment = relationship('Compartment', back_populates='compartment_medicine')
  medicine = relationship('Medicine', back_populates='compartment_medicine')

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

class Schedule(Base):
  __tablename__ = 'schedule' 
  schedule_id = Column(Integer, primary_key=True, autoincrement=True)
  scheduled_datetime = Column(DateTime, nullable=False)

  prescription_id = Column(Integer, ForeignKey('prescription.prescription_id', ondelete='CASCADE'), nullable=False)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)
  
  prescription = relationship('Prescription', back_populates='schedules')
  history = relationship('Intake_History', back_populates='schedule', cascade='all, delete-orphan')
  user = relationship('User', back_populates='schedules')

class Intake_History(Base):
  __tablename__ = 'intake_history'
  history_id = Column(Integer, primary_key=True, autoincrement=True)
  history_datetime = Column(DateTime, nullable=False)

  schedule_id = Column(Integer, ForeignKey('schedule.schedule_id', ondelete='CASCADE'), nullable=False)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  schedule = relationship('Schedule', back_populates='history')
  user = relationship('Schedule', back_populates='intake_history')
