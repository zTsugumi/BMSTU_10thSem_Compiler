from .fsa import FSA, FSAState
from .fsa_char import CharState, FSAChar
from .tokens.string import StringToken

class StringState(FSAState):
  START   = 'START'
  NONE    = 'NONE'
  END     = 'END'
  RUNNING = 'RUNNING'
  ERROR   = 'ERROR'
  L       = 'L'       # L - wchar_t uses 16bit to store
  Q       = 'Q'       # '
  QQ      = 'QQ'      # '...'

class FSAString(FSA):
  def __init__(self):
    self._state: StringState  = StringState.START
    self._fsachar: FSAChar    = FSAChar('\"') # quote
    self._scanned: str        = ''
    self._val: str            = ''

  def reset(self) -> None:
    self._state: StringState  = StringState.START
    self._fsachar.reset()
    self._scanned: str        = ''
    self._val: str            = ''

  def get_state(self) -> FSAState:
    match self._state:
      case StringState.START:
        return StringState.NONE
      case StringState.END:
        return StringState.END
      case StringState.ERROR:
        return StringState.ERROR
      case _:
        return StringState.RUNNING

  def get_token(self) -> StringToken:
    return StringToken(self._scanned, self._val)

  def read_char(self, ch: str) -> None:
    match self._state:
      case StringState.END | StringState.ERROR:
        self._state = StringState.ERROR

      case StringState.START:
        match ch:
          case 'L':
            self._state = StringState.L
          case '\"':
            self._state = StringState.Q
            self._fsachar.reset()
          case _:
            self._state = StringState.ERROR

      case StringState.L:
        match ch:
          case '\"':
            self._state = StringState.Q
            self._fsachar.reset()
          case _:
            self._state = StringState.ERROR

      case StringState.Q:
        if self._fsachar.get_state() == CharState.NONE and ch == '\"':
          self._state = StringState.QQ
          self._fsachar.reset()
        else:
          self._fsachar.read_char(ch)
          match self._fsachar.get_state():
            case CharState.END:
              self._state = StringState.Q
              self._scanned += self._fsachar.get_scanned()
              self._val += self._fsachar.get_char()
              self._fsachar.reset()
              self.read_char(ch)
            case CharState.ERROR:
              self._state = StringState.ERROR
            case _: pass

      case StringState.QQ:
        self._state = StringState.END

      case _:
        self._state = StringState.ERROR

  def read_eof(self) -> None:
    if self._state == StringState.QQ:
      self._state = StringState.END
    else:
      self._state = StringState.ERROR
