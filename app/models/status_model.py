from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.enums import Status_Type_Enum, Status_Value_Enum

class Status_Type(Base):
  __tablename__ = 'status_type'
  type_id = Column(Integer, primary_key=True, autoincrement=True)
  type_name = Column(Enum(Status_Type_Enum, name='type_name_enum'), nullable=False)

  values = relationship('Status_Value', back_populates='type', cascade='all, delete-orphan')

class Status_Value(Base):
  __tablename__ = 'status_value'
  value_id = Column(Integer, primary_key=True, autoincrement=True)
  status_type_id = Column(Integer, ForeignKey('status_type.type_id', ondelete='CASCADE'), nullable=False)
  value_label = Column(Enum(Status_Value_Enum, name='status_label_enum'), nullable=False)

  type = relationship('Status_Type', back_populates='values')
