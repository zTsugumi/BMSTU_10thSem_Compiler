from my_token import Tokenizer
from my_parser import Parser


def main():
  with open('./lab4/test/test0.txt', 'r') as f:
    src_code = f.read().replace('\n', '')

  with open('./lab4/_grammar.txt', 'r') as f:
    prods = f.readlines()

  tokenizer = Tokenizer(src_code)
  tokens = tokenizer.tokenize()

  try:
    Parser(tokens, prods)

  except Exception as e:
    print(e)
    print('\nRejected')


if __name__ == '__main__':
  main()
