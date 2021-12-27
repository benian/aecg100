from .base import _Aecg100Base
from .modules import _PpgModule


class Aecg100Client(_Aecg100Base, _PpgModule):
  pass
