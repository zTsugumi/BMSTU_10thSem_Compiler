from lib2to3.pgen2.token import OP
from .fsa import FSA, FSAState
from .tokens.op import OpToken, OpVal

class OpState(FSAState):
  START   = 'START'
  NONE    = 'NONE'
  END     = 'END'
  RUNNING = 'RUNNING'
  ERROR   = 'ERROR'
  OK    = 'OK'
  ADD   = 'ADD'
  SUB   = 'SUB'
  AMP   = 'AMP'
  MUL   = 'MUL'
  DIV   = 'DIV'
  MOD   = 'MOD'
  LT    = 'LT'
  LTE   = 'LTE'
  GT    = 'GT'
  GTE   = 'GTE'
  EQ    = 'EQ'
  OR    = 'OR'
  NOT   = 'NOT'
  XOR   = 'XOR'

class FSAOp(FSA):
  def __init__(self):
    self._state: OpState  = OpState.START
    self._scanned: str    = ''

  def reset(self) -> None:
    self._state: OpState  = OpState.START
    self._scanned: str    = ''

  def get_state(self) -> FSAState:
    match self._state:
      case OpState.START:
        return OpState.NONE
      case OpState.END:
        return OpState.END
      case OpState.ERROR:
        return OpState.ERROR
      case _:
        return OpState.RUNNING

  def get_token(self) -> OpToken:
    return OpToken(OpVal(self._scanned[:-1]))

  def read_char(self, ch: str) -> None:
    self._scanned += ch
    oplist = [item.value for item in OpVal]
    match self._state:
      case OpState.END | OpState.ERROR:
        self._state = OpState.ERROR

      case OpState.START:
        if ch in oplist:
          match ch:
            case '+':
              self._state = OpState.ADD
            case '-':
              self._state = OpState.SUB
            case '&':
              self._state = OpState.AMP
            case '*':
              self._state = OpState.MUL
            case '/':
              self._state = OpState.DIV
            case '%':
              self._state = OpState.MOD
            case '<':
              self._state = OpState.LT
            case '>':
              self._state = OpState.GT
            case '=':
              self._state = OpState.EQ
            case '|':
              self._state = OpState.OR
            case '!':
              self._state = OpState.NOT
            case '^':
              self._state = OpState.XOR
            case _:
              self._state = OpState.OK
        else:
          self._state = OpState.ERROR

      case OpState.OK:
        self._state = OpState.END

      case OpState.ADD:
        match ch:
          case '+' | '=':
            self._state = OpState.OK
          case _:
            self._state = OpState.END

      case OpState.SUB:
        match ch:
          case '>' | '-' | '=':
            self._state = OpState.OK
          case _:
            self._state = OpState.END

      case OpState.AMP:
        match ch:
          case '&' | '=':
            self._state = OpState.OK
          case _:
            self._state = OpState.END

      case OpState.MUL | OpState.DIV | OpState.MOD | OpState.EQ |\
           OpState.NOT | OpState.XOR | OpState.LTE | OpState.GTE:
        match ch:
          case '=':
            self._state = OpState.OK
          case _:
            self._state = OpState.END

      case OpState.LT:
        match ch:
          case '=':
            self._state = OpState.OK
          case '<':
            self._state = OpState.LTE
          case _:
            self._state = OpState.END

      case OpState.GT:
        match ch:
          case '=':
            self._state = OpState.OK
          case '>':
            self._state = OpState.GTE
          case _:
            self._state = OpState.END

      case OpState.OR:
        match ch:
          case '|' | '=':
            self._state = OpState.OK
          case _:
            self._state = OpState.END

      case _:
        self._state = OpState.ERROR

  def read_eof(self) -> None:
    self._scanned += '0'
    match self._state:
      case OpState.OK | OpState.SUB | OpState.ADD |\
           OpState.AMP | OpState.MUL | OpState.DIV | OpState.MOD |\
           OpState.LT | OpState.LTE | OpState.GT | OpState.GTE |\
           OpState.EQ | OpState.OR | OpState.NOT | OpState.XOR:
        self._state = OpState.END
      case _:
        self._state = OpState.ERROR