from sqlalchemy.orm import Session

from app.models import Status_Type, Statuses, Compartment_Set, Compartment, Medicine_Form, Dose_Component
from app.enums import status_enum, medicine_enum, compartments_enum

# medicine
def form_initializer(db: Session):
  forms_to_add = []
  for form_enum in medicine_enum.Medicine_Form_Enum:
    existing_form = db.query(Medicine_Form).filter_by(form_name=form_enum).first()
    if not existing_form:
      forms_to_add.append(Medicine_Form(form_name=form_enum))

  if forms_to_add:
    db.bulk_save_objects(forms_to_add)
    db.commit()

def dose_initializer(db: Session):
  doses_to_add = []
  for dose_enum in medicine_enum.Dose_Component_Enum:
    existing_dose = db.query(Dose_Component).filter_by(component_name=dose_enum).first()
    if not existing_dose:
      doses_to_add.append(Dose_Component(component_name=dose_enum))

  if doses_to_add:
    db.bulk_save_objects(doses_to_add)
    db.commit()

# status
def status_initializer(db: Session):
  for type_enum, value_enums in status_enum.status_type_to_values.items():
    existing_type = db.query(Status_Type).filter_by(type_name=type_enum).first()
    if not existing_type:
      existing_type = Status_Type(type_name=type_enum)
      db.add(existing_type)
      db.commit()
      db.refresh(existing_type)

    values_to_add = []
    for enum_value in value_enums:
      existing_value = db.query(Statuses).filter_by(status_name=enum_value, type_id=existing_type.type_id).first()
      if not existing_value:
        values_to_add.append(Statuses(status_name=enum_value, type_id=existing_type.type_id))

    if values_to_add:
      db.bulk_save_objects(values_to_add)
      db.commit()

# compartments
def compartment_initializer(db: Session):
  default_status = db.query(Statuses).filter_by(status_name='vacant').first()

  for set_enum, compartments in compartments_enum.compartment_set_to_compartment.items():
    existing_set = db.query(Compartment_Set).filter_by(set_name=set_enum).first()
    if not existing_set:
      existing_set = Compartment_Set(set_name=set_enum)
      db.add(existing_set)
      db.commit()
      db.refresh(existing_set)

    compartments_to_add = []
    for compartment_enum in compartments:
      existing_compartment = db.query(Compartment).filter_by(compartment_name=compartment_enum).first()
      if not existing_compartment:
        compartments_to_add.append(Compartment(
          set_id=existing_set.set_id,
          compartment_name=compartment_enum,
          status_id=default_status.status_id
        ))
            
    if compartments_to_add:
      db.bulk_save_objects(compartments_to_add)
      db.commit()
