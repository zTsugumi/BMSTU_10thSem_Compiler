from enum import Enum
from abc import ABC, abstractmethod

class TokenType(Enum):
  def __str__(self):
    return str(self.value)
  NONE        = 'NONE'
  FLOAT       = 'FLOAT'
  INT         = 'INT'
  OPERATOR    = 'OPERATOR'
  CHAR        = 'CHAR'
  STRING      = 'STRING'
  IDENTIFIER  = 'IDENTIFIER'
  KEYWORD     = 'KEYWORD'

class Token(ABC):
  @abstractmethod
  def to_string(self) -> str: pass
