from .token import Token, TokenType

class EmptyToken(Token):
  def __init__(self):
    self.type = TokenType.NONE

  def to_string(self) -> str:
    return None