from .token import Token, TokenType

class CharConstToken(Token):
  def __init__(self, raw: str, val: str):
    self.raw = raw
    self.val = val
    self.type = TokenType.CHAR

  def to_string(self) -> str:
    return f'{self.type}: {self.raw}'
