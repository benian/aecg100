from .base import _Aecg100Base
from .modules import _EcgModule, _PpgModule, _PwttModule


class Aecg100Client(_Aecg100Base, _EcgModule, _PpgModule, _PwttModule):
  """The client to communicate the AECG100 device."""
  pass
