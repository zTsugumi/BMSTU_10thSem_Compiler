import os
from .components.parser import Parser
from .components.gen_llvm import LLVMGenerator
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int


class Compiler():
  def __init__(self):
    self.parser = Parser()
    self.generator = LLVMGenerator()

  def parse_file(self, filepath, verbose=0):
    ''' Parse a C file
        Args:
          filepath: Path to the file containing source code.
        Returns: When successful, an AST is returned.
                 ParseError can be thrown otherwise.
    '''
    if os.path.exists(filepath):
      with open(filepath, mode='r', encoding='utf-8') as f:
        src_code = f.read()
    else:
      raise FileNotFoundError(f'{filepath} does not exist.')

    return self.parser.parse(src_code, filepath=filepath, verbose=verbose)

  def gen_llvm_ir(self, filepath, ast):
    ''' Generate LLVM IR from AST nodes based on llvmlite
        Args:
          ast: AST structure
        Returns:
          ir
    '''
    gen_code = self.generator.generate(ast)

    with open(filepath, mode='w', encoding='utf-8') as f:
      print(gen_code, file=f)

    return gen_code

  def run(self, filepath):
    with open(filepath, 'r') as f:
      llvm_ir = f.read()

    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly('')
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # Add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()

    # Look up the function pointer (a Python int)
    func_ptr = engine.get_function_address('main')

    # Run the function via ctypes
    cfunc = CFUNCTYPE(c_int)(func_ptr)
    cfunc()
