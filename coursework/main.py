import os
from .core.compiler import Compiler


def main():
  test_dir = os.path.abspath('./coursework/tests')
  files = [f'{test_dir}\{file}' for file in os.listdir(test_dir)
            if file.endswith('.c')]

  for file in files:
    compiler = Compiler(file)
    compiler.compile()


if __name__ == '__main__':
  main()
