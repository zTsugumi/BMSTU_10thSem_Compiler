from .tokens.empty import EmptyToken
from .fsa import FSA, FSAState
from ...utils.checker import *

class CharState(FSAState):
  START   = 'START'
  NONE    = 'NONE'
  END     = 'END'
  RUNNING = 'RUNNING'
  ERROR   = 'ERROR'
  S       = 'S'         # Backslash \
  C       = 'C'         # Character
  SO      = 'SO'        # Oct \1
  SOO     = 'SOO'       # Oct \12
  SOOO    = 'SOOO'      # Oct \123
  SX      = 'SX'        # Hex \x
  SXH     = 'SXH'       # Hex \xa
  SXHH    = 'SXHH'      # Hex \xab

class FSAChar(FSA):
  ''' The FSA for scanning a C character.
      Note that this FSA doesn't scan the surrounding quotes.
      It is used in both FSACharConst and FSAString.
  '''
  def __init__(self, quote: str):
    self._state: CharState  = CharState.START
    self._scanned: str      = ''
    self._quote: str        = quote

  def reset(self) -> None:
    self._state: CharState  = CharState.START
    self._scanned: str      = ''

  def get_state(self) -> FSAState:
    match self._state:
      case CharState.START:
        return CharState.NONE
      case CharState.END:
        return CharState.END
      case CharState.ERROR:
        return CharState.ERROR
      case _:
        return CharState.RUNNING

  def get_scanned(self) -> str:
    return self._scanned[:-1]

  def get_char(self) -> str:
    if len(self._scanned) == 3:
      match self._scanned[1]:
        case 'a': return '\a'
        case 'b': return '\b'
        case 'f': return '\f'
        case 'n': return '\n'
        case 'r': return '\r'
        case 't': return '\t'
        case 'v': return '\v'
        case '\'': return '\''
        case '\"': return '\"'
        case '\\': return '\\'
        case '?': return '?'
        case _: return self._scanned[1]
    else:
      return self._scanned[0]

  def get_token(self) -> EmptyToken:
    '''This method never gets used, because FSAChar
       is an inner FSA that will be used by other FSAs.
    '''
    return EmptyToken()

  def read_char(self, ch: str) -> None:
    self._scanned += ch
    match self._state:
      case CharState.END | CharState.ERROR:
        self._state = CharState.ERROR

      case CharState.START:
        if self.is_char(ch):
          self._state = CharState.C
        elif ch == '\\':
          self._state = CharState.S
        else:
          self._state = CharState.ERROR

      case CharState.C:
        self._state = CharState.END

      case CharState.S:
        if is_escape_char(ch):
          self._state = CharState.C
        elif is_oct_digit(ch):
          self._state = CharState.SO
        elif ch == 'x' or ch == 'X':
          self._state = CharState.SX
        else:
          self._state = CharState.ERROR

      case CharState.SX:
        if is_hex_digit(ch):
          self._state = CharState.SXH
        else:
          self._state = CharState.ERROR

      case CharState.SXH:
        if is_hex_digit(ch):
          self._state = CharState.SXHH
        else:
          self._state = CharState.END

      case CharState.SXHH:
        self._state = CharState.END

      case CharState.SO:
        if is_oct_digit(ch):
          self._state = CharState.SOO
        else:
          self._state = CharState.END

      case CharState.SOO:
        if is_oct_digit(ch):
          self._state = CharState.SOOO
        else:
          self._state = CharState.END

      case CharState.SOOO:
        self._state = CharState.END

      case _:
        self._state = CharState.ERROR

  def read_eof(self) -> None:
    self._scanned += '0'
    match self._state:
      case CharState.C | CharState.SXH | CharState.SXHH |\
           CharState.SO | CharState.SOO | CharState.SOOO:
        self._state = CharState.END
      case _:
        self._state = CharState.ERROR

  def is_char(self, ch: str) -> bool:
    return ch not in [self._quote, '\\', '\n']
