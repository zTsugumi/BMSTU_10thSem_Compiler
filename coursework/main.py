from llvmlite import binding
import os
import logging
import traceback
import argparse
from .compiler import Compiler

parser = argparse.ArgumentParser('C Compiler')
parser.add_argument('--verbose', default=0, help='Verbosity mode')
parser.add_argument('--show_ast', default=True, help='Display AST')
parser.add_argument('--show_llvm', default=True, help='Display LLVM IR')
parser.add_argument('--test_dir', default='./coursework/tests',
                    help='Directory containing test code')
parser.add_argument('--out_dir', default='./coursework/out',
                    help='Directory containing output')

args = parser.parse_args()


if __name__ == '__main__':
  files = [(f'{args.test_dir}\{file}', f'{args.out_dir}\{file[:-2]}.ll')
           for file in os.listdir(args.test_dir)
           if file.endswith('.c')]

  compiler = Compiler()

  # ERROR:
  # int: handle ull ul ll ...
  # ptr handle is still shit
  # Init string with [], [n] is shit
  # Global Struct default initializer not done
  files = [(args.test_dir+'\prog_sort.c',
            args.out_dir+'\prog_sort.ll')]
  for (fi, fo) in files:
    print(fi)
    try:
      ast = compiler.parse_file(fi, verbose=args.verbose)
      if args.show_ast:
        print(f'\n----------------------AST----------------------\n')
        ast.show()
        print('--------------------END AST--------------------\n')

      gen_code = compiler.gen_llvm_ir(fo, ast)
      if args.show_llvm:
        print(f'\n--------------------LLVM IR--------------------\n')
        print(gen_code)
        print('------------------END LLVM IR------------------\n')

      print(f'\nRESULT:')
      compiler.run(fo)

    except Exception as e:
      logging.error(traceback.format_exc())
