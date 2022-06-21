from ..ply import lex
from ..ply.lex import TOKEN


class Lexer(object):
  ''' An object class that wraps lex and provides
      needed information for lex.lex
  '''

  def __init__(self, lbrace_func, rbrace_func):
    self.lbrace_func = lbrace_func
    self.rbrace_func = rbrace_func

  def build(self, **kwargs):
    self.lexer = lex.lex(object=self, **kwargs)

  def input(self, src_code):
    self.lexer.input(src_code)

  def token(self):
    return self.lexer.token()

  def reset_lineno(self):
    self.lexer.lineno = 1

  keywords = {
      'static': 'STATIC',
      'const': 'CONST',
      'int': 'INT',           # Done
      'void': 'VOID',
      'char': 'CHAR',         # Done
      'case': 'CASE',         # Done
      'switch': 'SWITCH',     # Parser Done, llvm not done
      'break': 'BREAK',       # Done
      'return': 'RETURN',     # Done
      'continue': 'CONTINUE',  # Done
      'default': 'DEFAULT',   # Done
      'if': 'IF',             # Done
      'while': 'WHILE',       # Done
      'else': 'ELSE',         # Done
      'auto': 'AUTO',
      'struct': 'STRUCT',     # Done
  }

  tokens = list(keywords.values()) + [
      'ID',
      'INT_CONST_DEC',
      'INT_CONST_OCT',
      'CHAR_CONST',
      'STRING_LITERAL',
      # Operators
      'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
      'OR', 'AND', 'NOT', 'XOR',
      'LSHIFT', 'RSHIFT',
      'LOR', 'LAND', 'LNOT',
      'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
      # Assignment
      'EQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
      'MULEQUAL', 'DIVEQUAL', 'MODEQUAL',
      'LSHIFTEQUAL', 'RSHIFTEQUAL',
      'ANDEQUAL', 'XOREQUAL', 'OREQUAL',
      # Increment/decrement
      'PLUSPLUS', 'MINUSMINUS',
      # Structure dereference (->)
      'ARROW',
      # Conditional operator (?)
      # 'CONDOP',
      # Delimeters
      'LPAREN', 'RPAREN',         # ( )
      'LBRACKET', 'RBRACKET',     # [ ]
      'LBRACE', 'RBRACE',         # { }
      'COMMA', 'PERIOD',          # . ,
      'SEMI', 'COLON',            # ; :
  ]

  # Operators
  t_PLUS = r'\+'    # because lex use regex to parse so we need \+   # Done
  t_MINUS = r'-'    # Done
  t_MUL = r'\*'     # Done
  t_DIV = r'/'      # Done
  t_MOD = r'%'      # Done
  t_OR = r'\|'
  t_AND = r'&'      # Done
  t_NOT = r'~'
  t_XOR = r'\^'
  t_LSHIFT = r'<<'
  t_RSHIFT = r'>>'
  t_LOR = r'\|\|'   # Done
  t_LAND = r'&&'    # Done
  t_LNOT = r'!'     # Done
  t_LT = r'<'       # Done
  t_GT = r'>'       # Done
  t_LE = r'<='      # Done
  t_GE = r'>='      # Done
  t_EQ = r'=='      # Done
  t_NE = r'!='      # Done

  # Assignment operators
  t_EQUAL = r'='          # Done
  t_PLUSEQUAL = r'\+='
  t_MINUSEQUAL = r'-='
  t_MULEQUAL = r'\*='
  t_DIVEQUAL = r'/='
  t_MODEQUAL = r'%='
  t_LSHIFTEQUAL = r'<<='
  t_RSHIFTEQUAL = r'>>='
  t_ANDEQUAL = r'&='
  t_OREQUAL = r'\|='
  t_XOREQUAL = r'\^='

  # Increment/decrement
  t_PLUSPLUS = r'\+\+'
  t_MINUSMINUS = r'--'

  # Structure dereference (->)
  t_ARROW = r'->'         # Done

  # Delimeters
  t_LPAREN = r'\('        # Done
  t_RPAREN = r'\)'        # Done
  t_LBRACKET = r'\['      # Done
  t_RBRACKET = r'\]'      # Done
  t_COMMA = r','          # Done
  t_PERIOD = r'\.'        # Done
  t_SEMI = r';'           # Done
  t_COLON = r':'          # Done

  id = r'[a-zA-Z_$][0-9a-zA-Z_$]*'

  # WIP
  int_suffix = r'(([uU](ll|LL))|((ll|LL)[uU]?)|([uU][lL])|([lL][uU]?)|[uU])?'
  int_const_dec = rf'(0{int_suffix})|([1-9][0-9]*{int_suffix})'
  int_const_oct = rf'0[0-7]*{int_suffix}'

  simple_escape = r'''([a-zA-Z._~!=&\^\-\\?'"])'''
  dec_escape = r'([0-9]+)'
  hex_escape = r'(x[0-9a-fA-F]+)'
  escape_sequence = rf'(\\({simple_escape}|{dec_escape}|{hex_escape}))'
  char_const = rf"'([^'\\\n]|{escape_sequence})'"
  string_literal = rf'"([^"\\\n]|{escape_sequence})*"'

  t_STRING_LITERAL = string_literal

  @TOKEN(id)
  def t_ID(self, t):
    t.type = self.keywords.get(t.value, 'ID')
    return t

  @TOKEN(int_const_dec)
  def t_INT_CONST_DEC(self, t):
    return t

  @TOKEN(int_const_oct)
  def t_INT_CONST_OCT(self, t):
    return t

  @TOKEN(r'\{')
  def t_LBRACE(self, t):
    self.lbrace_func()
    return t

  @TOKEN(r'\}')
  def t_RBRACE(self, t):
    self.rbrace_func()
    return t

  @TOKEN(char_const)
  def t_CHAR_CONST(self, t):
    return t

  def t_newline(self, t):     # Rule to track line number
    r'\n+'
    t.lexer.lineno += len(t.value)

  def t_comment(self, t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

  # A string containing ignored characters (spaces and tabs)
  t_ignore = ' \t'

  # Error handling rule
  def t_error(self, t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)
