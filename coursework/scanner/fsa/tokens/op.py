from enum import Enum
from .token import Token, TokenType

class OpVal(Enum):
  LBRACKET      = '['
  RBRACKET      = ']'
  LPAREN        = '('
  RPAREN        = ')'
  PERIOD        = '.'
  COMMA         = ','
  QUESTION      = '?'
  COLON         = ':'
  TILDE         = '~'
  SUB           = '-'
  RARROW        = '->'
  DEC           = '--'
  SUBASSIGN     = '-='
  ADD           = '+'
  INC           = '++'
  ADDASSIGN     = '+='
  BITAND        = '&'
  AND           = '&&'
  ANDASSIGN     = '&='
  MULT          = '*'
  MULTASSIGN    = '*='
  LT            = '<'
  LEQ           = '<='
  LSHIFT        = '<<'
  LSHIFTASSIGN  = '<<='
  GT            = '>'
  GEQ           = '>='
  RSHIFT        = '>>'
  RSHIFTASSIGN  = '>>='
  ASSIGN        = '='
  EQ            = '=='
  BITOR         = '|'
  OR            = '||'
  ORASSIGN      = '|='
  NOT           = '!'
  NEQ           = '!='
  DIV           = '/'
  DIVASSIGN     = '/='
  MOD           = '%'
  MODASSIGN     = '%='
  XOR           = '^'
  XORASSIGN     = '^='
  SEMICOLON     = ';'
  LCURL         = '{'
  RCURL         = '}'

class OpToken(Token):
  def __init__(self, val: OpVal):
    self.val = val
    self.type = TokenType.OPERATOR

  def to_string(self) -> str:
    return f'{self.type} [{self.val}]: {self.val.value}'