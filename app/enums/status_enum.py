from enum import Enum

# Enums
class Status_Type_Enum(str, Enum):
  medicine = 'medicine'
  prescription = 'prescription'
  schedule = 'schedule'
  intake = 'intake'
  compartment = 'compartment'

class Statuses_Enum(str, Enum):
  # medicine
  available = 'available'
  unavailable = 'unavailable'
  expired = 'expired'

  # prescription
  ongoing = 'ongoing'
  ended = 'ended'

  # schedule
  pending = 'pending'
  fulfilled = 'fulfilled'

  # intake history
  completed = 'completed'
  delayed = 'delayed'
  missed = 'missed'

  # compartment
  vacant = 'vacant'
  occupied = 'occupied'
  
# initilized
status_type_to_values = {
  Status_Type_Enum.medicine: [
    Statuses_Enum.available,
    Statuses_Enum.unavailable,
    Statuses_Enum.expired
  ],
  Status_Type_Enum.prescription: [
    Statuses_Enum.ongoing,
    Statuses_Enum.ended
  ],
  Status_Type_Enum.schedule: [
    Statuses_Enum.pending,
    Statuses_Enum.fulfilled
  ],
  Status_Type_Enum.intake: [
    Statuses_Enum.completed,
    Statuses_Enum.delayed,
    Statuses_Enum.missed
  ],
  Status_Type_Enum.compartment: [
    Statuses_Enum.vacant,
    Statuses_Enum.occupied
  ]
}
