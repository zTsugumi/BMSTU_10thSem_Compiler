from .fsa.tokens.token import TokenType
from .fsa.tokens.empty import EmptyToken
from .fsa.fsa import FSAState
from .fsa.fsa_string import FSAString
from .fsa.fsa_charconst import FSACharConst
from .fsa.fsa_space import FSASpace
from .fsa.fsa_identifier import FSAIdentifier
from .fsa.fsa_op import FSAOp
from .fsa.fsa_int import FSAInt
from .fsa.fsa_float import FSAFloat

class Scanner:
  def __init__(self, src_code):
    self._src_code = src_code
    self._fsa = [
      FSAFloat(),
      FSAInt(),
      FSAOp(),
      FSAIdentifier(),
      FSASpace(),
      FSACharConst(),
      FSAString()
    ]

  def find_state(self, state):
    return list(filter(
      lambda fsa: fsa.get_state() == state,
      self._fsa
    ))

  def lex(self) -> None:
    tokens = []

    # Traverse through text
    ptr = 0
    while ptr < len(self._src_code):
      ch = self._src_code[ptr]
      list(map(lambda fsa: fsa.read_char(ch), self._fsa))

      if not self.find_state('RUNNING'):
        end = self.find_state('END')
        if end:
          token = end[0].get_token()
          if token.type != TokenType.NONE:
            tokens.append(token)
          list(map(lambda fsa: fsa.reset(), self._fsa))
          continue
        else:
          raise ValueError('source code invalid')

      ptr += 1

    # End Of File
    list(map(lambda fsa: fsa.read_eof(), self._fsa))
    end = self.find_state('END')
    if end:
      token = end[0].get_token()
      if token.type != TokenType.NONE:
        tokens.append(token)
      else:
        raise ValueError('source code invalid')

    tokens.append(EmptyToken())

    return tokens


if __name__ == '__main__':
  pass
