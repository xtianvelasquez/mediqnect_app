from enum import Enum, auto

class Medicine_Form_Enum(str, Enum):
  tablet = auto()
  syrup = auto()

class Dose_Component_Enum(str, Enum):
  tablet = auto()
  mililiter = auto()
