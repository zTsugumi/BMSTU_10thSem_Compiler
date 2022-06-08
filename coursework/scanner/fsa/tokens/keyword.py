from enum import Enum
from .token import Token, TokenType

class KeywordVal(Enum):
  AUTO      = 'auto'
  DOUBLE    = 'double'
  INT       = 'int'
  STRUCT    = 'struct'
  BREAK     = 'break'
  ELSE      = 'else'
  LONG      = 'long'
  SWITCH    = 'switch'
  CASE      = 'case'
  ENUM      = 'enum'
  REGISTER  = 'register'
  TYPEDEF   = 'typedef'
  CHAR      = 'char'
  EXTERN    = 'extern'
  RETURN    = 'return'
  UNION     = 'union'
  CONST     = 'const'
  FLOAT     = 'float'
  SHORT     = 'short'
  UNSIGNED  = 'unsigned'
  CONTINUE  = 'continue'
  FOR       = 'for'
  SIGNED    = 'signed'
  VOID      = 'void'
  DEFAULT   = 'default'
  GOTO      = 'goto'
  SIZEOF    = 'sizeof'
  VOLATILE  = 'volatile'
  DO        = 'do'
  IF        = 'if'
  STATIC    = 'static'
  WHILE     = 'while'

class KeywordToken(Token):
  def __init__(self, val: KeywordVal):
    self.val = val
    self.type = TokenType.KEYWORD

  def to_string(self) -> str:
    return f'{self.type}: {self.val}'
