from enum import Enum

class Compartment_Set_Enum(str, Enum):
  tablet = 'tablet'
  syrups = 'syrups'

class Compartment_Enum(str, Enum):
  # tablet compartment
  a1 = 'a1'
  a2 = 'a2'
  a3 = 'a3'

  # syrup compartment
  b1 = 'b1'
  b2 = 'b2'
  b3 = 'b3'
  
# initialized
compartment_set_to_compartment = {
  Compartment_Set_Enum.tablet: [
    Compartment_Enum.a1,
    Compartment_Enum.a2,
    Compartment_Enum.a3
  ],
  Compartment_Set_Enum.syrups: [
    Compartment_Enum.b1,
    Compartment_Enum.b2,
    Compartment_Enum.b3
  ]
}
