class Token: pass

class ParenthesisToken(Token): pass
class OpenParenthesisToken(ParenthesisToken):
  def __init__(self):
    self.val = '('
class CloseParenthesisToken(ParenthesisToken):
  def __init__(self):
    self.val = ')'

class CurlyBracket(Token): pass
class OpenCurlyBracketToken(CurlyBracket):
  def __init__(self):
    self.val = '{'
class CloseCurlyBracketToken(CurlyBracket):
  def __init__(self):
    self.val = '}'

class RelationToken(Token): pass
class LessToken(RelationToken):
  def __init__(self):
    self.val = '<'
class LessEqualToken(RelationToken):
  def __init__(self):
    self.val = '<='
class GreaterToken(RelationToken):
  def __init__(self):
    self.val = '>'
class GreaterEqualToken(RelationToken):
  def __init__(self):
    self.val = '>='
class EqualToken(RelationToken):
  def __init__(self):
    self.val = '=='
class NotEqualToken(RelationToken):
  def __init__(self):
    self.val = '!='

class AdditionToken(Token): pass
class PlusToken(AdditionToken):
  def __init__(self):
    self.val = '+'
class MinusToken(AdditionToken):
  def __init__(self):
    self.val = '-'

class MultiplicationToken(Token): pass
class MultiplyToken(MultiplicationToken):
  def __init__(self):
    self.val = '*'
class DivideToken(MultiplicationToken):
  def __init__(self):
    self.val = '/'

class RelationValueToken(Token): pass
class TrueToken(RelationValueToken): pass
class FalseToken(RelationValueToken): pass

class AssignmentToken(Token):
  def __init__(self):
    self.val = '='
class SemicolonToken(Token):
  def __init__(self):
    self.val = ';'

class NumberToken(Token):
  def __init__(self, val):
    self.val = 'c'
    self.val1 = val

class IdentifierToken(Token):
  def __init__(self, val):
    self.val = 'i'
    self.val1 = val

class EndToken(Token):
  def __init__(self):
    self.val = '$'

class ErrorToken(Token): pass