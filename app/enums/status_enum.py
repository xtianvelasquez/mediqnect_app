from enum import Enum

# Enums
class Status_Type_Enum(str, Enum):
  medicine = 'medicine'
  intake = 'intake'
  schedule = 'schedule'
  compartment = 'compartment'

class Statuses_Enum(str, Enum):
  # compartment
  vacant = 'vacant'
  occupied = 'occupied'

  # medicine
  available = 'available'
  unavailable = 'unavailable'
  expired = 'expired'

  # intake
  pending = 'pending'
  fulfilled = 'fulfilled'

  # schedule
  ongoing = 'ongoing'
  ended = 'ended'
  
  # history
  completed = 'completed'
  late = 'late'
  missed = 'missed'
  
# initilized
status_type_to_values = {
  Status_Type_Enum.compartment: [
    Statuses_Enum.vacant,
    Statuses_Enum.occupied
  ],
  Status_Type_Enum.medicine: [
    Statuses_Enum.available,
    Statuses_Enum.unavailable,
    Statuses_Enum.expired
  ],
  Status_Type_Enum.intake: [
    Statuses_Enum.pending,
    Statuses_Enum.fulfilled
  ],
  Status_Type_Enum.schedule: [
    Statuses_Enum.ongoing,
    Statuses_Enum.ended
  ],
  Status_Type_Enum.intake: [
    Statuses_Enum.completed,
    Statuses_Enum.late,
    Statuses_Enum.missed
  ]
}
