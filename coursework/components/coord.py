class Coord(object):
  ''' Coordinates of a syntactic element. It contains:
      - File name
      - Line number
      - column number (optional)
  '''
  __slots__ = ('file', 'line', 'column', '__weakref__')

  def __init__(self, file, line, column=None):
    self.file = file
    self.line = line
    self.column = column

  def __str__(self):
    info = f'{self.file}:{self.line}'
    if self.column:
      info += f':{self.column}'
    return info