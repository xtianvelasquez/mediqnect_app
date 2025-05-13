from enum import Enum

class Medicine_Form_Enum(str, Enum):
  tablet = 'tablet'
  syrup = 'syrup'

class Dose_Component_Enum(str, Enum):
  tablet = 'tablet'
  mililiter = 'mililiter'
