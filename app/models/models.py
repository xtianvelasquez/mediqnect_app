from sqlalchemy import Column, String, text, Integer, DECIMAL, Date, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database.base import Base

class Status_Type(Base):
  __tablename__ = 'status_type'
  type_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  type_name = Column(String(20), nullable=False)

  status = relationship('Statuses', back_populates='type', cascade='all, delete-orphan')

class Statuses(Base):
  __tablename__ = 'statuses'
  status_id = Column(Integer, primary_key=True, autoincrement=True)
  type_id = Column(Integer, ForeignKey('status_type.type_id', ondelete='CASCADE'), nullable=False)
  status_name = Column(String(20), nullable=False, index=True)

  type = relationship('Status_Type', back_populates='status')
  compartment = relationship('Compartment', back_populates='status')
  medicine = relationship('Medicine', back_populates='status')
  intake = relationship('Intake', back_populates='status')
  schedule = relationship('Schedule', back_populates='status')
  history = relationship('Intake_History', back_populates='status')

class Compartment_Set(Base):
  __tablename__ = 'compartment_set'
  set_id = Column(Integer, primary_key=True, autoincrement=True)
  set_name = Column(String(20), nullable=False)

  compartment = relationship('Compartment', back_populates='set', cascade='all, delete-orphan')

class Compartment(Base):
  __tablename__ = 'compartment'
  compartment_id = Column(Integer, primary_key=True, autoincrement=True)
  set_id = Column(Integer, ForeignKey('compartment_set.set_id', ondelete='CASCADE'), nullable=False)
  compartment_name = Column(String(20), nullable=False)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  set = relationship('Compartment_Set', back_populates='compartment')
  medicine_compartment = relationship('Medicine_Compartment', back_populates='compartment', cascade='all, delete-orphan')
  status = relationship('Statuses', back_populates='compartment')

class User(Base):
  __tablename__ = 'user'
  user_id = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String(50), unique=True, nullable=False, index=True)
  password_hash = Column(String(255), nullable=False)
  dispenser_code = Column(String(20), unique=True)
  created_at = Column(DateTime, default=func.current_timestamp())
  modified_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

  token = relationship('Token', back_populates='user', uselist=False)
  medicine = relationship('Medicine', back_populates='user', cascade='all, delete-orphan')
  medicine_compartment = relationship('Medicine_Compartment', back_populates='user', cascade='all, delete-orphan')
  intake = relationship('Intake', back_populates='user', cascade='all, delete-orphan')
  schedule = relationship('Schedule', back_populates='user', cascade='all, delete-orphan')
  history = relationship('Intake_History', back_populates='user', cascade='all, delete-orphan')

class Token(Base):
  __tablename__ = 'token'
  token_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='SET NULL'), nullable=True) 
  token_hash = Column(String(255), nullable=False)
  is_active = Column(Boolean, default=True, server_default=text('true'))
  issued_at = Column(DateTime)
  expires_at = Column(DateTime)
  revoked_at = Column(DateTime)

  user = relationship('User', back_populates='token')

class Medicine_Form(Base):
  __tablename__ = 'medicine_form'
  form_id = Column(Integer, primary_key=True, autoincrement=True)
  form_name = Column(String(20), nullable=False)

  medicine = relationship('Medicine', back_populates='form', cascade='all, delete-orphan')

class Medicine(Base):
  __tablename__ = 'medicine'
  medicine_id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('user.user_id'), ondelete='CASCADE')
  medicine_name = Column(String(50), nullable=False)
  form_id = Column(Integer, ForeignKey('medicine_form.form_id', ondelete='CASCADE'), nullable=False)
  net_content = Column(Integer)
  expiration_date = Column(Date)
  created_at = Column(DateTime, default=func.current_timestamp())
  modified_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  user = relationship('User', back_populates='medicine')
  form = relationship('Medicine_Form', back_populates='medicine')
  medicine_compartment = relationship('Medicine_Compartment', back_populates='medicine', cascade='all, delete-orphan')
  intake = relationship('Intake', back_populates='medicine', cascade='all, delete-orphan')
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

class Dose_Component(Base):
  __tablename__ = 'dose_component'
  component_id = Column(Integer, primary_key=True, autoincrement=True)
  component_name = Column(String(20), nullable=False)

  intake = relationship('Intake', back_populates='component', cascade='all, delete-orphan')

class Color(Base):
  __tablename__ = 'color'
  color_id = Column(Integer, primary_key=True, autoincrement=True)
  color_name = Column(String(20), nullable=False, index=True)

  intake = relationship('Intake', back_populates='color')

class Intake(Base):
  __tablename__ = 'intake'
  intake_id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  start_datetime = Column(DateTime, nullable=False)
  end_date = Column(Date, nullable=False)
  hour_interval = Column(Integer, nullable=False)
  dose = Column(DECIMAL(4,2), nullable=False)
  component_id = Column(Integer, ForeignKey('dose_component.component_id', ondelete='CASCADE'), nullable=False)
  color_id = Column(Integer, ForeignKey('color.color_id', ondelete='SET NULL'), nullable=True)
  is_scheduled = Column(Boolean, default=False, server_default=text('false'))
  created_at = Column(DateTime, default=func.current_timestamp())
  modified_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  user = relationship('User', back_populates='intake')
  medicine = relationship('Medicine', back_populates='intake')
  component = relationship('Dose_Component', back_populates='intake')
  color = relationship('Intake_Color', back_populates='intake')
  schedule = relationship('Schedule', back_populates='intake', cascade='all, delete-orphan')
  status = relationship('Statuses', back_populates='intake')

class Schedule(Base):
  __tablename__ = 'schedule' 
  schedule_id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  intake_id = Column(Integer, ForeignKey('intake.intake_id', ondelete='CASCADE'), nullable=False)
  scheduled_datetime = Column(DateTime, nullable=False, index=True)
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  user = relationship('User', back_populates='schedule')
  intake = relationship('Intake', back_populates='schedule')
  history = relationship('Intake_History', back_populates='schedule', cascade='all, delete-orphan')
  status = relationship('Statuses', back_populates='schedule')

class Intake_History(Base):
  __tablename__ = 'intake_history'
  history_id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
  schedule_id = Column(Integer, ForeignKey('schedule.schedule_id', ondelete='CASCADE'), nullable=False)
  history_datetime = Column(DateTime, nullable=False, index=True)
  modified_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
  status_id = Column(Integer, ForeignKey('statuses.status_id', ondelete='SET NULL'), nullable=True)

  user = relationship('User', back_populates='history')
  schedule = relationship('Schedule', back_populates='history')
  status = relationship('Statuses', back_populates='history')
