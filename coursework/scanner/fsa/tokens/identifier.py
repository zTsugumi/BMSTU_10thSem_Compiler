from .token import Token, TokenType

class IdentifierToken(Token):
  def __init__(self, val):
    self.val = val
    self.type = TokenType.IDENTIFIER

  def to_string(self) -> str:
    return f'{self.type}: {self.val}'
