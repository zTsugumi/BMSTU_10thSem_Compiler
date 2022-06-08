from enum import Enum
from .token import Token, TokenType

class FloatSuffix(Enum):
    NONE  = 'NONE'
    F     = 'F'
    L     = 'L'

class FloatToken(Token):
  def __init__(self, val, suffix, raw):
    self.val = val
    self.suffix = suffix
    self.raw = raw
    self.type = TokenType.FLOAT

  def to_string(self) -> str:
    res = self.type
    match self.suffix:
      case FloatSuffix.F:
        res += '(float)'
      case FloatSuffix.L:
        res += '(long double)'
      case _:
        res += '(double)'

    return f'{res}: {self.val} "{self.raw}"'