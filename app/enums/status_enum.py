from enum import Enum, auto

# Enums
class Status_Type_Enum(str, Enum):
  medicine = auto()
  prescription = auto()
  schedule = auto()
  intake = auto()
  compartment = auto()

class Status_Value_Enum(str, Enum):
  # medicine
  available = auto()
  unavailable = auto()
  expired = auto()

  # prescription
  ongoing = auto()
  ended = auto()

  # schedule
  pending = auto()
  completed = auto()

  # intake history
  fulfilled = auto()
  delayed = auto()
  missed = auto()

  # compartment
  vacant = auto()
  occupied = auto()
  
# initilized
status_type_to_values = {
  Status_Type_Enum.medicine: [
    Status_Value_Enum.available,
    Status_Value_Enum.unavailable,
    Status_Value_Enum.expired
  ],
  Status_Type_Enum.prescription: [
    Status_Value_Enum.ongoing,
    Status_Value_Enum.ended
  ],
  Status_Type_Enum.schedule: [
    Status_Value_Enum.pending,
    Status_Value_Enum.completed
  ],
  Status_Type_Enum.intake: [
    Status_Value_Enum.fulfilled,
    Status_Value_Enum.delayed,
    Status_Value_Enum.missed
  ],
  Status_Type_Enum.compartment: [
    Status_Value_Enum.vacant,
    Status_Value_Enum.occupied
  ]
}
