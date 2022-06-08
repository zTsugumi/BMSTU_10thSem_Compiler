from .tokens.float import FloatSuffix, FloatToken
from .fsa import FSA, FSAState

class FloatState(FSAState):
  START   = 'START'
  NONE    = 'NONE'
  END     = 'END'
  RUNNING = 'RUNNING'
  ERROR   = 'ERROR'
  D       = 'D'         # Digit
  P       = 'P'         # Point
  DP      = 'DP'        # Digit Point
  PD      = 'PD'        # Point Digit
  DE      = 'DE'        # Digit E
  DES     = 'DES'       # Digit E Sign
  DED     = 'DED'       # Digit E Digit
  DPF     = 'DPF'       # Digit Point Float
  DPL     = 'DPL'       # Digit Point LongDouble

class FSAFloat(FSA):
  def __init__(self):
    self._state: FloatState   = FloatState.START
    self._whole: int          = 0
    self._decimal: int        = 0
    self._ndecimal: int       = 0
    self._exp: int            = 0
    self._exp_pos: bool       = True    # Positive / Negative
    self._suffix: FloatSuffix = FloatSuffix.NONE
    self._scanned: str            = ''

  def reset(self) -> None:
    self._state     = FloatState.START
    self._whole     = 0
    self._decimal   = 0
    self._ndecimal  = 0
    self._exp       = 0
    self._exp_pos   = True    # Positive / Negative
    self._suffix    = FloatSuffix.NONE
    self._scanned   = ''

  def get_state(self) -> FSAState:
    match self._state:
      case FloatState.START:
        return FloatState.NONE
      case FloatState.END:
        return FloatState.END
      case FloatState.ERROR:
        return FloatState.ERROR
      case _:
        return FloatState.RUNNING

  def get_token(self) -> FloatToken:
    val = 0
    if self._exp_pos:
      val = (self._whole + self._decimal * 0.1**self._ndecimal) * 10**self._exp
    else:
      val = (self._whole + self._decimal * 0.1**self._ndecimal) * 10**(-self._exp)
    return FloatToken(val, self._suffix, self._scanned[:-1])

  def read_char(self, ch: str) -> None:
    self._scanned += ch
    match self._state:
      case FloatState.END | FloatState.ERROR:
        self._state = FloatState.ERROR

      case FloatState.START:
        if ch.isdigit():
          self._whole = int(ch)
          self._state = FloatState.D
        elif ch == '.':
          self._state = FloatState.P
        else:
          self._state = FloatState.ERROR

      case FloatState.D:
        if ch.isdigit():
          self._whole = self._whole * 10 + int(ch)
          self._state = FloatState.D
        elif ch == 'e' or ch == 'E':
          self._state = FloatState.DE
        elif ch == '.':
          self._state = FloatState.DP
        else:
          self._state = FloatState.ERROR

      case FloatState.P:
        if ch.isdigit():
          self._decimal = int(ch)
          self._ndecimal = 1
          self._state = FloatState.PD
        else:
          self._state = FloatState.ERROR

      case FloatState.DP:
        if ch.isdigit():
          self._decimal = int(ch)
          self._ndecimal = 1
          self._state = FloatState.PD
        elif ch == 'e' or ch == 'E':
          self._state = FloatState.DE
        elif ch == 'f' or ch == 'F':
          self._suffix = FloatSuffix.F
          self._state = FloatState.DPF
        elif ch == 'l' or ch == 'L':
          self._suffix = FloatSuffix.L
          self._state = FloatState.DPL
        else:
          self._state = FloatState.END

      case FloatState.PD:
        if ch.isdigit():
          self._decimal = self._decimal * 10 + int(ch)
          self._decimal += 1
          self._state = FloatState.PD
        elif ch == 'e' or ch == 'E':
          self._state = FloatState.DE
        elif ch == 'f' or ch == 'F':
          self._suffix = FloatSuffix.F
          self._state = FloatState.DPF
        elif ch == 'l' or ch == 'L':
          self._suffix = FloatSuffix.L
          self._state = FloatState.DPL
        else:
          self._state = FloatState.END

      case FloatState.DE:
        if ch.isdigit():
          self._exp = int(ch)
          self._state = FloatState.DED
        elif ch == '+':
          self._exp_pos = True
          self._state = FloatState.DES
        elif ch == '-':
          self._exp_pos = False
          self._state = FloatState.DES
        else:
          self._state = FloatState.ERROR

      case FloatState.DES:
        if ch.isdigit():
          self._exp = int(ch)
          self._state = FloatState.DED
        else:
          self._state = FloatState.ERROR

      case FloatState.DPL:
        self._suffix = FloatSuffix.L
        self._state = FloatState.END

      case FloatState.DED:
        if ch.isdigit():
          self._exp = self._exp * 10 + int(ch)
          self._state = FloatState.DED
        elif ch == 'f' or ch == 'F':
          self._suffix = FloatSuffix.F
          self._state = FloatState.DPF
        elif ch == 'l' or ch == 'L':
          self._suffix = FloatSuffix.L
          self._state = FloatState.DPL
        else:
          self._state = FloatState.END

      case FloatState.DPF:
        self._state = FloatState.END

      case _:
        self._state = FloatState.ERROR

  def read_eof(self) -> None:
    match self._state:
      case FloatState.DP | FloatState.PD |\
           FloatState.DED | FloatState.DPF| \
           FloatState.DPL:
        self._state = FloatState.END
      case _:
        self._state = FloatState.ERROR
