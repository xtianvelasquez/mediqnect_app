from sqlalchemy import Column, String, text, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class Token(Base):
  __tablename__ = 'token'
  token_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('user.user_id', ondelete='SET NULL'), nullable=True) 
  token_hash = Column(String(255), nullable=False)
  is_active = Column(Boolean, default=True, server_default=text('true'))
  issued_at = Column(DateTime(timezone=True))
  expires_at = Column(DateTime(timezone=True))
  revoked_at = Column(DateTime(timezone=True))

  user = relationship('User', back_populates='token')
