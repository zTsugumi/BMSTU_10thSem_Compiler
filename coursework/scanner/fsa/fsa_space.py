from .fsa import FSA, FSAState
from .tokens.empty import EmptyToken

class SpaceState(FSAState):
  START   = 'START'
  NONE    = 'NONE'
  END     = 'END'
  RUNNING = 'RUNNING'
  ERROR   = 'ERROR'
  SPACE   = 'SPACE'

class FSASpace(FSA):
  def __init__(self):
    self._state: SpaceState = SpaceState.START

  def reset(self) -> None:
    self._state: SpaceState = SpaceState.START

  def get_state(self) -> FSAState:
    match self._state:
      case SpaceState.START:
        return SpaceState.NONE
      case SpaceState.END:
        return SpaceState.END
      case SpaceState.ERROR:
        return SpaceState.ERROR
      case _:
        return SpaceState.RUNNING

  def get_token(self) -> EmptyToken:
    return EmptyToken()

  def read_char(self, ch: str) -> None:
    match self._state:
      case SpaceState.END | SpaceState.ERROR:
        self._state = SpaceState.ERROR

      case SpaceState.START:
        if ch.isspace():
          self._state = SpaceState.SPACE
        else:
          self._state = SpaceState.ERROR

      case SpaceState.SPACE:
        if ch.isspace():
          self._state = SpaceState.SPACE
        else:
          self._state = SpaceState.END

  def read_eof(self) -> None:
    match self._state:
      case SpaceState.SPACE:
        self._state = SpaceState.END
      case _:
        self._state = SpaceState.ERROR