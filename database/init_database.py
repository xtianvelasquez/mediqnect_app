from . import session
from . import Base
from ..enums import (
  form_initializer,
  dose_initializer,
  status_initializer,
  compartment_initializer
)

def init_db():
  db = session.SessionLocal()

  try:
    Base.metadata.create_all(bind=session.engine)
    form_initializer(db)
    dose_initializer(db)
    status_initializer(db)
    compartment_initializer(db)
    db.commit()

  finally:
    db.close()
