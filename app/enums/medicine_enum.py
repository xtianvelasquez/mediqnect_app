from enum import Enum

class Medicine_Form_Enum(str, Enum):
  tablet = 'tablet'
  syrups = 'syrups'

class Dose_Component_Enum(str, Enum):
  tablet = 'tablet'
  milliliter = 'milliliter'
