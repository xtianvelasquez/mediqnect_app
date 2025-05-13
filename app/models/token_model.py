from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

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
