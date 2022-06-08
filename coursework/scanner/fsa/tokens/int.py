from enum import Enum
from .token import Token, TokenType

class IntSuffix(Enum):
  NONE  = 'NONE'
  U     = 'U'
  L     = 'L'
  UL    = 'UL'

class IntToken(Token):
  def __init__(self, val, suffix, raw):
    self.val = val
    self.suffix = suffix
    self.raw = raw
    self.type = TokenType.INT

  def to_string(self) -> str:
    res = self.type
    match self.suffix:
      case IntSuffix.L:
        res += '(long)'
      case IntSuffix.U:
        res += '(unsigned)'
      case IntSuffix.UL:
        res += '(unsigned long)'
      case _:
        pass

    return f'{res}: {self.val} "{self.raw}"'