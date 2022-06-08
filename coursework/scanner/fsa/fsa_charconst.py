from .fsa import FSA, FSAState
from .fsa_char import FSAChar
from .tokens.charconst import CharConstToken

class CharConstState(FSAState):
  START   = 'START'
  NONE    = 'NONE'
  END     = 'END'
  RUNNING = 'RUNNING'
  ERROR   = 'ERROR'
  L       = 'L'       # L - wchar_t uses 16bit to store
  Q       = 'Q'       # '
  QC      = 'QC'      # 'a
  QCQ     = 'QCQ'     # 'a'

class FSACharConst(FSA):
  def __init__(self):
    self._state: CharConstState = CharConstState.START
    self._fsachar: FSAChar      = FSAChar('\'') # quote
    self._scanned: str          = ''
    self._val: str              = ''

  def reset(self) -> None:
    self._state: CharConstState = CharConstState.START
    self._fsachar.reset()

  def get_state(self) -> FSAState:
    match self._state:
      case CharConstState.START:
        return CharConstState.NONE
      case CharConstState.END:
        return CharConstState.END
      case CharConstState.ERROR:
        return CharConstState.ERROR
      case _:
        return CharConstState.RUNNING

  def get_token(self) -> CharConstToken:
    return CharConstToken(self._scanned, self._val)

  def read_char(self, ch: str) -> None:
    match self._state:
      case CharConstState.END | CharConstState.ERROR:
        self._state = CharConstState.ERROR

      case CharConstState.START:
        match ch:
          case 'L':
            self._state = CharConstState.L
          case '\'':
            self._state = CharConstState.Q
            self._fsachar.reset()
          case _:
            self._state = CharConstState.ERROR

      case CharConstState.L:
        match ch:
          case '\'':
            self._state = CharConstState.Q
            self._fsachar.reset()
          case _:
            self._state = CharConstState.ERROR

      case CharConstState.Q:
        self._fsachar.read_char(ch)
        match self._fsachar.get_state():
          case FSAState.END:
            self._state = CharConstState.QC
            self._scanned = self._fsachar.get_scanned()
            self._val = self._fsachar.get_char()
            self.read_char(ch)
          case FSAState.ERROR:
            self._state = CharConstState.ERROR
          case _: pass

      case CharConstState.QC:
        match ch:
          case '\'':
            self._state = CharConstState.QCQ
          case _:
            self._state = CharConstState.ERROR

      case CharConstState.QCQ:
        self._state = CharConstState.END

      case _:
        self._state = CharConstState.ERROR

  def read_eof(self) -> None:
    if self._state == CharConstState.QCQ:
      self._state = CharConstState.END
    else:
      self._state = CharConstState.ERROR
