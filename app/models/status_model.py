from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.enums import Status_Type_Enum, Statuses_Enum

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
