from enum import Enum, auto

class Compartment_Set_Enum(str, Enum):
  tablet = auto()
  syrup = auto()

class Compartment_Enum(str, Enum):
  # tablet compartment
  a1 = auto()
  a2 = auto()
  a3 = auto()

  # syrup compartment
  b1 = auto()
  b2 = auto()
  b3 = auto()
  
# initialized
compartment_set_to_compartment = {
  Compartment_Set_Enum.tablet: [
    Compartment_Enum.a1,
    Compartment_Enum.a2,
    Compartment_Enum.a3
  ],
  Compartment_Set_Enum.syrup: [
    Compartment_Enum.b1,
    Compartment_Enum.b2,
    Compartment_Enum.b3
  ]
}
