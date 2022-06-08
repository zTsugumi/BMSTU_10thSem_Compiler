from .fsa import FSA, FSAState
from .tokens.token import Token
from .tokens.keyword import KeywordToken, KeywordVal
from .tokens.identifier import IdentifierToken

class IdentifierState(FSAState):
  START   = 'START'
  NONE    = 'NONE'
  END     = 'END'
  RUNNING = 'RUNNING'
  ERROR   = 'ERROR'
  ID      = 'ID'

class FSAIdentifier(FSA):
  def __init__(self):
    self._state: IdentifierState  = IdentifierState.START
    self._scanned: str            = ''

  def reset(self) -> None:
    self._state: IdentifierState  = IdentifierState.START
    self._scanned: str            = ''

  def get_state(self) -> FSAState:
    match self._state:
      case IdentifierState.START:
        return IdentifierState.NONE
      case IdentifierState.END:
        return IdentifierState.END
      case IdentifierState.ERROR:
        return IdentifierState.ERROR
      case _:
        return IdentifierState.RUNNING

  def get_token(self) -> Token:
    name = self._scanned[:-1]
    if name in [item.value for item in KeywordVal]:
      return KeywordToken(KeywordVal(name))
    else:
      return IdentifierToken(name)

  def read_char(self, ch: str) -> None:
    self._scanned += ch
    match self._state:
      case IdentifierState.END | IdentifierState.ERROR:
        self._state = IdentifierState.ERROR

      case IdentifierState.START:
        if ch == '_' or ch.isalpha():
          self._state = IdentifierState.ID
        else:
          self._state = IdentifierState.ERROR

      case IdentifierState.ID:
        if ch == '_' or ch.isalpha() or ch.isdigit():
          self._state = IdentifierState.ID
        else:
          self._state = IdentifierState.END

  def read_eof(self) -> None:
    self._scanned += '0'
    match self._state:
      case IdentifierState.ID:
        self._state = IdentifierState.END
      case _:
        self._state = IdentifierState.ERROR
