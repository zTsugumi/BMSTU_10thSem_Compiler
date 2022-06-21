# op <• a
# a •> op | $ | )
# op <• (
# ( <• op | a | (
# op •> )
# ) •> op | $ | )
# op •> $
# $ <• op | a |(
# ( =• )
# if priority of op1 > op2:
#   op1 •> op2 and op2 <• op1
# if priority of op1 == op2:
#   if left associative:
#     op1 •> op2 and op2 •> op1
#   elif right associative:
#     op1 <• op2 and op2 <• op1

from my_type import *

table = {
    '<':  {'<': ' ', '<=': ' ', '==': ' ',  '!=': ' ',  '>=': ' ',  '>': ' ',  '+': '<',  '-': '<',  '*': '<',  '/': '<',  '(': '<',  ')': '>',  'i': '<',  'c': '<',  '$': '>'},
    '<=': {'<': ' ', '<=': ' ', '==': ' ',  '!=': ' ',  '>=': ' ',  '>': ' ',  '+': '<',  '-': '<',  '*': '<',  '/': '<',  '(': '<',  ')': '>',  'i': '<',  'c': '<',  '$': '>'},
    '==': {'<': ' ', '<=': ' ', '==': ' ',  '!=': ' ',  '>=': ' ',  '>': ' ',  '+': '<',  '-': '<',  '*': '<',  '/': '<',  '(': '<',  ')': '>',  'i': '<',  'c': '<',  '$': '>'},
    '!=': {'<': ' ', '<=': ' ', '==': ' ',  '!=': ' ',  '>=': ' ',  '>': ' ',  '+': '<',  '-': '<',  '*': '<',  '/': '<',  '(': '<',  ')': '>',  'i': '<',  'c': '<',  '$': '>'},
    '>=': {'<': ' ', '<=': ' ', '==': ' ',  '!=': ' ',  '>=': ' ',  '>': ' ',  '+': '<',  '-': '<',  '*': '<',  '/': '<',  '(': '<',  ')': '>',  'i': '<',  'c': '<',  '$': '>'},
    '>':  {'<': ' ', '<=': ' ', '==': ' ',  '!=': ' ',  '>=': ' ',  '>': ' ',  '+': '<',  '-': '<',  '*': '<',  '/': '<',  '(': '<',  ')': '>',  'i': '<',  'c': '<',  '$': '>'},
    '+':  {'<': '>', '<=': '>', '==': '>',  '!=': '>',  '>=': '>',  '>': '>',  '+': '>',  '-': '>',  '*': '<',  '/': '<',  '(': '<',  ')': '>',  'i': '<',  'c': '<',  '$': '>'},
    '-':  {'<': '>', '<=': '>', '==': '>',  '!=': '>',  '>=': '>',  '>': '>',  '+': '>',  '-': '>',  '*': '<',  '/': '<',  '(': '<',  ')': '>',  'i': '<',  'c': '<',  '$': '>'},
    '*':  {'<': '>', '<=': '>', '==': '>',  '!=': '>',  '>=': '>',  '>': '>',  '+': '>',  '-': '>',  '*': '>',  '/': '>',  '(': '<',  ')': '>',  'i': '<',  'c': '<',  '$': '>'},
    '/':  {'<': '>', '<=': '>', '==': '>',  '!=': '>',  '>=': '>',  '>': '>',  '+': '>',  '-': '>',  '*': '>',  '/': '>',  '(': '<',  ')': '>',  'i': '<',  'c': '<',  '$': '>'},
    '(':  {'<': '<', '<=': '<', '==': '<',  '!=': '<',  '>=': '<',  '>': '<',  '+': '<',  '-': '<',  '*': '<',  '/': '<',  '(': '<',  ')': '=',  'i': '<',  'c': '<',  '$': ' '},
    ')':  {'<': '>', '<=': '>', '==': '>',  '!=': '>',  '>=': '>',  '>': '>',  '+': '>',  '-': '>',  '*': '>',  '/': '>',  '(': ' ',  ')': '>',  'i': ' ',  'c': ' ',  '$': '>'},
    'i':  {'<': '>', '<=': '>', '==': '>',  '!=': '>',  '>=': '>',  '>': '>',  '+': '>',  '-': '>',  '*': '>',  '/': '>',  '(': ' ',  ')': '>',  'i': ' ',  'c': ' ',  '$': '>'},
    'c':  {'<': '>', '<=': '>', '==': '>',  '!=': '>',  '>=': '>',  '>': '>',  '+': '>',  '-': '>',  '*': '>',  '/': '>',  '(': ' ',  ')': '>',  'i': ' ',  'c': ' ',  '$': '>'},
    '$':  {'<': '<', '<=': '<', '==': '<',  '!=': '<',  '>=': '<',  '>': '<',  '+': '<',  '-': '<',  '*': '<',  '/': '<',  '(': '<',  ')': ' ',  'i': '<',  'c': '<',  '$': ' '},
}

# This is actually Shunting yard algorithm
class Parser:
  def __init__(self, tokens, prods):
    self.tokens = tokens
    self.tokens.append(EndToken())
    self.prods = {}
    self.state = []
    self.parse(prods)

  def update_state(self, stack, input, precedence, action):
    self.state.append({
        'stack': stack,
        'input': input,
        'precedence': precedence,
        'action': action
    })

  def parse(self, prods):
    non_terminal = []

    for row in prods:
      if ':' in row:  # new prod
        non_terminal.append(row.lstrip(' ')[0])
        prod = row.lstrip(' ')[1:].lstrip(f' :').rstrip(' \n')
        self.prods[prod] = non_terminal[-1]
      elif '|' in row:
        prod = row.lstrip('| ').rstrip(' \n')
        self.prods[prod] = non_terminal[-1]

    # Algo
    # Terminal on top of the stack is a
    # Next input symbol is b
    # If a<•b or a=•b:
    #   shift
    # If a>•b:
    #   pop until top stack termial is <• to the popped item
    #   reduce
    stack = [EndToken()]
    input = self.tokens.copy()
    polish = ''

    while len(stack) > 1 or input[0].val != '$':
      lookahead = input[0].val
      idx = -1
      while stack[idx].val in non_terminal:
        idx -= 1
      top_stack = stack[idx].val
      precedence = table[top_stack][lookahead]

      if precedence in ['<', '=']:  # 'shift'
        stack.append(input[0])
        input = input[1:]
      elif precedence == '>':  # 'reduce'
        cond = True
        while cond:
          if stack[-1].val not in ['(', ')']:
            if hasattr(stack[-1], 'val1'):
              polish += f'{stack[-1].val1} '
            else:
              polish += f'{stack[-1].val} '
          cond = table[stack[-2].val][stack[-1].val] != '<'
          stack.pop()
      else:
        raise RuntimeError(f'Relation of{top_stack} and {lookahead} invalid')

    print('Accepted')
    print(polish)
