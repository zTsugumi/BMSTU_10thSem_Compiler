import os
from ..scanner.scanner import Scanner


class Compiler:
  def __init__(self, src_path):
    if os.path.exists(src_path):
      with open(src_path) as f:
        self._src_code = f.read()
        self._scanner = Scanner(self._src_code)       # Lexer
    else:
      raise FileNotFoundError(f'{src_path} does not exist.')

  def compile(self):
    tokens = self._scanner.lex()
    
    pass