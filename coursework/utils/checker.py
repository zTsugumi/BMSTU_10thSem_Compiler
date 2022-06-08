def is_oct_digit(ch: str) -> bool:
  '''Tested'''
  return ch.isdigit() and 0 <= int(ch) <= 7

def is_hex_digit(ch: str) -> bool:
  '''Tested'''
  return ch in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'a', 'b', 'c', 'd', 'e', 'f',
                'A', 'B', 'C', 'D', 'E', 'F']

def is_escape_char(ch: str) -> bool:
  '''Tested'''
  return ch in ['a', 'b', 'f', 'n', 'r', 't', 'v',
                '\'', '\"', '\\', '?']


if __name__ == '__main__':
  print(is_escape_char('?'))