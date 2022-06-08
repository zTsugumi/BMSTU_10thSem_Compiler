from .tokens.int import IntSuffix, IntToken
from .fsa import FSA, FSAState
from ...utils.checker import *

class IntState(FSAState):
  START   = 'START'
  NONE    = 'NONE'
  END     = 'END'
  RUNNING = 'RUNNING'
  ERROR   = 'ERROR'
  Z       = 'Z'     # Zero
  ZX      = 'ZX'    # 0x - Hex
  H       = 'H'     # Hex digit
  O       = 'O'     # Oct digit
  D       = 'D'     # Dec digit
  L       = 'L'     # Long
  U       = 'U'     # Unsigned
  UL      = 'UL'    # Unsigned Long

class FSAInt(FSA):
  def __init__(self):
    self._state     = IntState.START
    self._val       = 0
    self._suffix    = IntSuffix.NONE
    self._scanned   = ''

  def reset(self) -> None:
    self._state     = IntState.START
    self._val       = 0
    self._suffix    = IntSuffix.NONE
    self._scanned   = ''

  def get_state(self) -> FSAState:
    match self._state:
      case IntState.START:
        return IntState.NONE
      case IntState.END:
        return IntState.END
      case IntState.ERROR:
        return IntState.ERROR
      case _:
        return IntState.RUNNING

  def get_token(self) -> IntToken:
    return IntToken(self._val, self._suffix, self._scanned[:-1])

  def read_char(self, ch: str) -> None:
    self._scanned += ch
    match self._state:
      case IntState.END | IntState.ERROR:
        self._state = IntState.ERROR

      case IntState.START:
        if ch == '0':
          self._state = IntState.Z
        elif ch.isdigit():
          self._state = IntState.D
          self._val += int(ch)
        else:
          self._state = IntState.ERROR

      case IntState.Z:
        if ch == 'x' or ch == 'X':
          self._state = IntState.ZX
        elif is_oct_digit(ch):
          self._val = self._val * 0o10 + int(ch, 8)
          self._state = IntState.O
        elif ch == 'u' or ch == 'U':
          self._suffix = IntSuffix.U
          self._state = IntState.U
        elif ch == 'l' or ch == 'L':
          self._suffix = IntSuffix.L
          self._state = IntState.L
        else:
          self._state = IntState.END

      case IntState.D:
        if ch.isdigit():
          self._val = self._val * 10 + int(ch)
          self._state = IntState.D
        elif ch == 'u' or ch == 'U':
          self._suffix = IntSuffix.U
          self._state = IntState.U
        elif ch == 'l' or ch == 'L':
          self._suffix = IntSuffix.L
          self._state = IntState.L
        else:
          self._state = IntState.END

      case IntState.ZX:
        if is_hex_digit(ch):
          self._val = self._val * 0x10 + int(ch, 16)
          self._state = IntState.H
        else:
          self._state = IntState.ERROR

      case IntState.H:
        if is_hex_digit(ch):
          self._val = self._val * 0x10 + int(ch, 16)
          self._state = IntState.H
        elif ch == 'u' or ch == 'U':
          self._suffix = IntSuffix.U
          self._state = IntState.U
        elif ch == 'l' or ch == 'L':
          self._suffix = IntSuffix.L
          self._state = IntState.L
        else:
          self._state = IntState.END

      case IntState.O:
        if is_oct_digit(ch):
          self._val = self._val * 0o10 + int(ch, 8)
          self._state = IntState.O
        elif ch == 'u' or ch == 'U':
          self._suffix = IntSuffix.U
          self._state = IntState.U
        elif ch == 'l' or ch == 'L':
          self._suffix = IntSuffix.L
          self._state = IntState.L
        else:
          self._state = IntState.END

      case IntState.L:
        if ch == 'u' or ch == 'U':
          self._suffix = IntSuffix.UL
          self._state = IntState.UL
        else:
          self._state = IntState.END

      case IntState.U:
        if ch == 'l' or ch == 'L':
          self._suffix = IntSuffix.UL
          self._state = IntState.UL
        else:
          self._state = IntState.END

      case IntState.UL:
        self._state = IntState.END

      case _:
        self._state = IntState.ERROR

  def read_eof(self) -> None:
    match self._state:
      case IntState.D | IntState.Z | IntState.O |\
           IntState.L | IntState.H | IntState.U |\
           IntState.UL:
        self._state = IntState.END
      case _:
        self._state = IntState.ERROR