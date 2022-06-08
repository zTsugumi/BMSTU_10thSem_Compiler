from argparse import ArgumentError
from .token import Token, TokenType

class StringToken(Token):
  def __init__(self, raw: str, val: str):
    if not val:
      raise ArgumentError()

    self.raw = raw
    self.val = val
    self.type = TokenType.STRING

  def to_string(self) -> str:
    return f'{self.type}: "{self.raw}"\n"{self.val}"'
