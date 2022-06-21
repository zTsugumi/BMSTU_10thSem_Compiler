# https://llvmlite.readthedocs.io/en/latest/user-guide/

from llvmlite import ir
from . import ast


class LLVMGenerator(object):
  def __init__(self):
    # LLVM Module, that holds all IR code
    self.llvm_module = ir.Module('C Compiler')

    # LLVM instruction builder. Created whenever
    # a new function is entered
    self.llvm_builder = None

    # Dicts that keep track of which values are
    # defined in the current scope and what their
    # LLVM representation is
    self.named_arg = {}
    self.named_mem = {}
    self.named_func = {}
    self.global_var = {}
    self.type_define = {}

    self.current_func = None

    self.loop_block_start_stack = []
    self.loop_block_end_stack = []

  def generate(self, head):
    self.visit(head)
    return self.llvm_module

  # Visit methods
  def visit(self, node, status=0):
    method = f'visit_{node.__class__.__name__}'
    return getattr(self, method, self.error_visit)(node, status)

  def error_visit(self, node, status=0):
    raise RuntimeError(f'Node {node.__class__.__name__} not implemented')

  def visit_FileAST(self, node, status=0):
    for ext in node.ext:
      if isinstance(ext, ast.FuncDef):
        self.visit(ext, status=0)
      elif isinstance(ext, ast.Decl):
        self.visit(ext, status=1)

  #
  # Declaration
  #
  def visit_Decl(self, node, status=0):  # Tested
    '''
      Declare and allocate the declared variables
      Args:
        node:
          type -> FuncDecl | ArrayDecl | PtrDecl | Struct | IdentifierType
          init -> expr
        status:
          0 -> local
          1 -> global
          2 -> function | return element type
    '''
    # Handle decleration
    decl = self.generate_declaration(node, status, [])

    # Handle initializer if exist
    if node.init:
      if status == 0:
        init = self.visit(node.init, 1)
        self.llvm_builder.store(
            init,
            self.named_mem[node.name])
      elif status == 1:
        self.global_var[node.name].initializer = self.visit(
            node.init, node.name)
      else:
        pass
    else:
      if status == 1:
        if isinstance(node.type, ast.Struct):
          if node.name:
            self.global_var[node.name].linkage = 'common'
            self.global_var[node.name].align = 4
          else:
            pass
        else:
          self.global_var[node.name].linkage = 'common'
          self.global_var[node.name].align = 4

    if status == 2:
      return decl

  def visit_FuncDef(self, node, status=0):  # Tested
    '''
      Generate function
      Args:
        node:
          decl -> Decl -> FuncDecl
          body -> Compound
    '''
    self.named_arg.clear()
    func = self.visit(node.decl, status=2)
    self.current_func = func

    if node.body:
      block = func.append_basic_block(name='entry')
      self.llvm_builder = ir.IRBuilder(block)

      # Allocate and store all arguments
      for arg in func.args:
        name = arg.name
        self.named_mem[name] = self.llvm_builder.alloca(arg.type, name=name)
        self.llvm_builder.store(arg, self.named_mem[name])

      # Generate body content (Compound)
      self.visit(node.body)
    else:
      self.current_func = None
      func.is_declaration = True

  #
  # Expression
  #

  def visit_IdentifierType(self, node, status=0):  # Tested
    '''
      This is used in expression to get a ptr or
      load the value in that ptr
      Args:
        status:
          0 -> get ptr
          1 -> get value in that ptr
    '''
    if node.spec:  # Decl type
      spec = node.spec
      if spec == 'int':
        return ir.IntType(32)
      elif spec == 'char':
        return ir.IntType(8)
      elif spec == 'void':
        return ir.VoidType()
      elif spec in self.type_define:
        context = self.llvm_module.context
        return context.get_identified_type(spec)
      else:
        raise RuntimeError(f'Type {spec} not implemented')
    else:  # Variable ID
      if node.name in self.named_mem:
        if status == 0:
          return self.named_mem[node.name]
        elif status == 1:
          return self.llvm_builder.load(self.named_mem[node.name])
        else:
          pass
      elif node.name in self.global_var:
        return self.global_var[node.name]
      else:
        raise RuntimeError(f'Undefined variable {node.name}')

  def visit_Assignment(self, node, status=0):  # Tested
    '''
      1. Get ptr of left operand
      2. Get value of the right operand
      3. Store the loaded value to left ptr
      Right operand can be IdentifierType, BinaryOp, UnaryOp
    '''
    if node.op == '=':
      left = self.visit(node.lvalue, 0)   # Get ptr of left operand
      right = self.visit(node.rvalue, 1)  # Load value to ptr of right operand

      if right == 'NULL':
        right = ir.Constant(ir.IntType(32), 0).bitcast(left.type)

      self.llvm_builder.store(right, left)  # Store loaded value to ptr
    else:  # WIP +=, -=, *=, /=
      raise RuntimeError(f'Assignment op {node.op} not implemented')

  def visit_BinaryOp(self, node, status=1):  # Tested
    '''
      Terminology is similar to visit_Assignment
    '''
    left = self.visit(node.left, status)
    right = self.visit(node.right, 1)

    if right == 'NULL':
      right = ir.Constant(ir.IntType(32), 0).bitcast(left.type)
    if left == 'NULL':
      left = ir.Constant(ir.IntType(32), 0).bitcast(right.type)

    match node.op:
      case '+':
        # ptr + int -> get the address
        if isinstance(left.type, ir.PointerType):
          if isinstance(left.type.pointee, ir.ArrayType):
            zero = ir.Constant(ir.IntType(32), 0)
            first_addr = self.llvm_builder.gep(
                left, [zero, zero], inbounds=True)
            return self.llvm.builder.gep(first_addr, [right], inbounds=True)
          if isinstance(right.type, ir.PointerType):
            left = self.llvm_builder.load(left)
            right = self.llvm_builder.load(right)
        return self.llvm_builder.add(left, right)
      case '-':
        if isinstance(left.type, ir.PointerType):
          if isinstance(right.type, ir.PointerType):
            left = self.llvm_builder.load(left)
            right = self.llvm_builder.load(right)
        return self.llvm_builder.sub(left, right)
      case '*':
        if isinstance(left.type, ir.PointerType):
          if isinstance(right.type, ir.PointerType):
            left = self.llvm_builder.load(left)
            right = self.llvm_builder.load(right)
        return self.llvm_builder.mul(left, right)
      case '/':
        if isinstance(left.type, ir.PointerType):
          if isinstance(right.type, ir.PointerType):
            left = self.llvm_builder.load(left)
            right = self.llvm_builder.load(right)
        return self.llvm_builder.sdiv(left, right)
      case '%':
        if isinstance(left.type, ir.PointerType):
          if isinstance(right.type, ir.PointerType):
            left = self.llvm_builder.load(left)
            right = self.llvm_builder.load(right)
        return self.llvm_builder.srem(left, right)
      case '<' | '<=' | '==' | '!=' | '>=' | '>':
        if isinstance(left.type, ir.PointerType):
          if isinstance(right.type, ir.PointerType):
            left = self.llvm_builder.load(left)
            right = self.llvm_builder.load(right)
        return self.llvm_builder.icmp_signed(node.op, left, right)
      case '&&':
        if isinstance(left.type, ir.PointerType):
          if isinstance(right.type, ir.PointerType):
            left = self.llvm_builder.load(left)
            right = self.llvm_builder.load(right)
        left = self.llvm_builder.icmp_signed(
            '!=', left, ir.Constant(left.type, 0))
        right = self.llvm_builder.icmp_signed(
            '!=', right, ir.Constant(right.type, 0))
        return self.llvm_builder.and_(left, right)
      case '||':
        if isinstance(left.type, ir.PointerType):
          if isinstance(right.type, ir.PointerType):
            left = self.llvm_builder.load(left)
            right = self.llvm_builder.load(right)
        left = self.llvm_builder.icmp_signed(
            '!=', left, ir.Constant(left.type, 0))
        right = self.llvm_builder.icmp_signed(
            '!=', right, ir.Constant(right.type, 0))
        return self.llvm_builder.or_(left, right)
      case _:
        raise RuntimeError(f'Binary op {node.op} not implemented')

  def visit_UnaryOp(self, node, status=0):  # Tested
    match node.op:
      case '&':  # Tested
        return self.visit(node.expr, 0)
      case '*':  # Tested
        return self.visit(node.expr, 1)
      case '!':
        expr = self.visit(node.expr, 1)
        return self.llvm_builder.icmp_signed('==', expr, ir.Constant(expr.type, 0))
      case '-':
        expr = self.visit(node.expr, 1)
        return self.llvm_builder.neg(expr)
      case _:
        raise RuntimeError(f'Unary op {node.op} not implemented')

  def visit_ArrayRef(self, node, status=0):  # Tested
    '''
      Return an element in an array
      Args:
        status:
          0 -> get ptr
          1 -> get value in that ptr
    '''
    arr = self.visit(node.name, 0)      # Visit_IdentifierType - get ptr
    idx = self.visit(node.subscript, 1)  # Visit_IdentifierType - get val

    zero = ir.Constant(ir.IntType(32), 0)
    ele = self.llvm_builder.gep(arr, [zero, idx], inbounds=True)
    if status == 0:
      return ele
    elif status == 1:
      return self.llvm_builder.load(ele)
    else:
      pass

  def visit_StructRef(self, node, status=0):
    '''
      Return struct
      Args:
        status:
          0 -> get ptr
          1 -> get value of that ptr
    '''
    if node.type == '->':
      id = self.visit(node.name, 1)
      # id = self.llvm_builder.load(id)
    elif node.type == '.':
      id = self.visit(node.name, 0)
    else:
      raise RuntimeError(f'Struct ref {node.type} not implemented')

    st_name = id.type.pointee.name
    st_field = node.field.name.name
    # context = self.llvm_module.context
    # st = context.get_identified_type(st_name)
    if st_field not in self.type_define[st_name]:
      raise RuntimeError(f'Struct field {st_field} not defined')
    zero = ir.Constant(ir.IntType(32), 0)
    idx = ir.Constant(ir.IntType(
        32), self.type_define[st_name].index(st_field))
    ele = self.llvm_builder.gep(id, [zero, idx], inbounds=True)

    if status == 0:
      return ele
    elif status == 1:
      return self.llvm_builder.load(ele)
    else:
      pass

  def visit_FuncCall(self, node, status=0):
    func_name = node.name.name

    if func_name not in self.named_func:
      func, args = self.extern_function(node)
    else:
      func = self.named_func[func_name]
      args = [] if node.args is None else self.visit(node.args, 1)
      for i, (param, arg) in enumerate(zip(args, func.args)):
        if isinstance(arg.type, ir.IntType) and isinstance(param.type, ir.IntType):
          if arg.type.width > param.type.width:
            args[i] = self.llvm_builder.sext(param, arg.type)
          elif arg.type.width < param.type.width:
            args[i] = self.llvm_builder.trunc(param, arg.type)

    return self.llvm_builder.call(func, args)

  def visit_ExprList(self, node, status=0):
    '''
        Return a list of FuncCall arguments
    '''
    arlist = []
    for arg in node.exprs:
      arlist.append(self.visit(arg, status))
    return arlist

  def visit_InitList(self, node, status=0):
    return ir.Constant.literal_array([self.visit(ele) for ele in node.exprs])

  #
  # Statement
  #

  def visit_Compound(self, node, status=0):
    if node.block_items:
      for item in node.block_items:
        self.visit(item, status=0)

  def visit_If(self, node, status=0):
    cond = self.visit(node.cond, 1)

    if type(cond) is not ir.IntType(1):
      cond = self.llvm_builder.icmp_signed(
          '!=', cond, ir.Constant(cond.type, 0))
    if node.iffalse:
      with self.llvm_builder.if_else(cond) as (then, otherwise):
        with then:
          self.visit(node.iftrue)
        with otherwise:
          self.visit(node.iffalse)
    else:
      with self.llvm_builder.if_then(cond):
        self.visit(node.iftrue)

  def visit_While(self, node, status=0):
    while_cmp = self.current_func.append_basic_block()
    while_entry = self.current_func.append_basic_block()
    while_end = self.current_func.append_basic_block()

    self.loop_block_start_stack.append(while_cmp)
    self.loop_block_end_stack.append(while_end)

    self.llvm_builder.branch(while_cmp)
    self.llvm_builder.position_at_end(while_cmp)

    cond = self.visit(node.cond, 1)
    if type(cond) is not ir.IntType(1):
      cond = self.llvm_builder.icmp_signed(
          '!=', cond, ir.Constant(cond.type, 0))
    self.llvm_builder.cbranch(cond, while_entry, while_end)
    self.llvm_builder.position_at_end(while_entry)

    self.visit(node.stmt)

    self.llvm_builder.branch(while_cmp)
    self.loop_block_start_stack.pop()
    self.loop_block_end_stack.pop()
    self.llvm_builder.position_at_end(while_end)

  def visit_Continue(self, node, status=0):
    self.llvm_builder.branch(self.loop_block_start_stack[-1])

  def visit_Break(self, node, status=0):
    self.llvm_builder.branch(self.loop_block_end_stack[-1])

  def visit_Return(self, node, status=0):
    if node.expr:
      ret = self.visit(node.expr, 1)
      func_ret = self.current_func.return_value
      if isinstance(ret.type, ir.IntType) and isinstance(func_ret.type, ir.IntType):
        if func_ret.type.width > ret.type.width:
          ret = self.llvm_builder.sext(ret, func_ret.type)
        elif func_ret.type.width < ret.type.width:
          ret = self.llvm_builder.trunc(ret, func_ret.type)
      self.llvm_builder.ret(ret)
    else:
      self.llvm_builder.ret_void()

  #
  # Operation
  #

  def visit_Constant(self, node, status=0):
    match node.type:
      case 'int':
        c = ir.Constant(ir.IntType(32), node.value)
      # case 'float':
      #   c = ir.Constant(ir.FloatType(), node.value)
      # case 'double':
      #   c = ir.Constant(ir.DoubleType(), node.value)
      case 'char':
        c = ir.Constant(ir.IntType(8), self.char_to_int(node.value))
      case 'string':  # ???
        string = self.remove_quotes(node.value)
        string = string.replace('\\n', '\n')
        string += '\0'

        type = ir.ArrayType(ir.IntType(8), len(string))
        name = '.str' + str(len(self.global_var))

        tmp = ir.GlobalVariable(self.llvm_module, type, name=name)
        tmp.initializer = ir.Constant(type, bytearray(string, 'utf8'))
        tmp.global_constant = True
        self.global_var[name] = tmp

        zero = ir.Constant(ir.IntType(32), 0)
        c = self.llvm_builder.gep(tmp, [zero, zero], inbounds=True)
      case _:
        raise RuntimeError(f'Constant type {node.type} not implement')

    return c

  def visit_ID(self, node, status=0):
    '''
        Return variable.
        Args:
          status:
            0 -> get ptr
            1 -> get value of that ptr
    '''
    if node.name == 'NULL' or node.name == 'null':
      return 'NULL'
    if node.name in self.named_mem:
      if status == 0:
        return self.named_mem[node.name]
      elif status == 1:
        return self.llvm_builder.load(self.named_mem[node.name])
    elif node.name in self.global_var:
      if status == 0:
        return self.global_var[node.name]
      elif status == 1:
        return self.global_var[node.name]
    else:
      raise RuntimeError(f'Variable {node.name} undefined')

  #
  # Custom methods
  #

  def get_element(self, node, arg=None):
    if arg:
      match type(node):
        case ast.PtrDecl:
          return ir.PointerType(arg)
        case ast.ArrayDecl:
          return ir.ArrayType(arg, int(node.dim.value))
        case ast.FuncDecl:
          if node.args:
            paramtypes = [self.generate_declaration(param, status=2)
                          for param in node.args.params]
          else:
            paramtypes = []
          return ir.FunctionType(arg, paramtypes)
        case _:
          return None
    else:
      if node == 'int':
        return ir.IntType(32)
      elif node == 'char':
        return ir.IntType(8)
      elif node == 'void':
        return ir.VoidType()
      elif node in self.type_define:  # Struct
        context = self.llvm_module.context
        return context.get_identified_type(node.name)
      else:
        return None

  def generate_declaration(self, node, status=0, modifiers=[]):
    '''
      status:
        0 -> allocate local                       # Tested
        1 -> allocate global                      # Tested
        2 -> function | return element type       # Not tested
    '''
    match type(node):
      case ast.IdentifierType:
        cur_type = self.get_element(node.spec[0], None)
        decl = modifiers.pop(0)
        name = decl.name

        for m in modifiers:
          cur_type = self.get_element(m, cur_type)

        match status:
          case 0:
            self.named_mem[name] = self.llvm_builder.alloca(
                cur_type, name=name)
          case 1:
            self.global_var[name] = ir.GlobalVariable(
                self.llvm_module,
                cur_type,
                name=name)
            self.global_var[name].initializer = ir.Constant(cur_type, None)
          case 2:
            if len(modifiers) > 0 and isinstance(modifiers[0], ast.FuncDecl):
              func = ir.Function(self.llvm_module, cur_type, name=name)
              if modifiers[0].args:
                param_names = [
                    param.name for param in modifiers[0].args.params]
                for arg, param_name in zip(func.args, param_names):
                  arg.name = param_name
                  self.named_arg[param_name] = arg
                  # Set signed extension for char
                  if isinstance(arg.type, ir.IntType) and arg.type.width == 8:
                    arg.add_attribute('signext')
              self.named_func[name] = func
              return func
            else:
              return cur_type

      case ast.Struct:
        context = self.llvm_module.context
        cur_type = context.get_identified_type(node.name)

        # define struct if it is not defined
        if node.name not in self.type_define:
          self.type_define[node.name] = [ele.name for ele in node.decls]
          ele_types = [self.generate_declaration(ele, status=2)
                       for ele in node.decls]
          cur_type.set_body(*ele_types)

        decl = modifiers.pop(0)
        name = decl.name

        for m in modifiers:
          cur_type = self.get_element(m, cur_type)

        match status:
          case 0:
            if name:
              self.named_mem[name] = self.llvm_builder.alloca(
                  cur_type, name=name)
            else:
              return cur_type
          case 1:
            if name:
              self.global_var[name] = ir.GlobalVariable(
                  self.llvm_module, cur_type, name=name)
            else:
              return cur_type
          case 2:
            if len(modifiers) > 0 and isinstance(modifiers[0], ast.FuncDecl):
              func = ir.Function(self.llvm_module, cur_type, name=name)
              if modifiers[0].args:
                param_names = [param.name for param in modifiers[0].args]
                for arg, param_name in zip(func.args, param_names):
                  arg.name = param_name
                  self.named_arg[param_name] = arg
                self.named_func[name] = func
                return func
            else:
              return cur_type

      case ast.ArrayDecl | ast.FuncDecl | ast.PtrDecl | ast.Decl:
        return self.generate_declaration(node.type, status, modifiers+[node])

  def remove_quotes(self, str):
    return str[1:-1]

  def char_to_int(self, str):
    return ord(self.remove_quotes(str))

  #
  # Custom headers
  #
  # Since we don't have pre-processing, we write some hard code for
  # the following external functions: printf, gets, isdigit, atoi,
  # memcpy, strlen

  def extern_function(self, node):
    match node.name.name:
      case 'printf':
        func_type = ir.FunctionType(
            ir.IntType(32),
            [ir.IntType(8).as_pointer()],
            var_arg=True)
        args = []

        for idx, arg in enumerate(node.args.exprs):
          if idx == 0:
            args.append(self.visit(arg))
          else:
            args.append(self.visit(arg, status=1))

        return self.llvm_module.declare_intrinsic(node.name.name, (), func_type), args

      case 'gets':
        func_type = ir.FunctionType(
            ir.IntType(32),
            [],
            var_arg=True)
        args = []

        for arg in node.args.exprs:
          zero = ir.Constant(ir.IntType(32), 0)
          ptr = self.llvm_builder.gep(
              self.visit(arg, status=0), [zero, zero], inbounds=True)
          args.append(ptr)

        return self.llvm_module.declare_intrinsic(node.name.name, (), func_type), args

      case 'isdigit':
        func_type = ir.FunctionType(
            ir.IntType(32),
            [ir.IntType(32)],
            var_arg=False)
        args = []

        for arg in node.args.exprs:
          ext = self.llvm_builder.sext(
              self.visit(arg, status=1), ir.IntType(32))
          args.append(ext)

        return self.llvm_module.declare_intrinsic(node.name.name, (), func_type), args

      case 'atoi':
        func_type = ir.FunctionType(
            ir.IntType(32),
            [],
            var_arg=True)
        args = []

        for arg in node.args.exprs:
          zero = ir.Constant(ir.IntType(32), 0)
          ptr = self.llvm_builder.gep(
              self.visit(arg, status=0), [zero, zero], inbounds=True)
          args.append(ptr)

        return self.llvm_module.declare_intrinsic(node.name.name, (), func_type), args

      case 'memcpy':
        args = []
        for idx, arg in enumerate(node.args.exprs):
          if idx == 2:
            args.append(self.visit(arg, status=1))
          else:
            array_addr = self.visit(arg, status=0)
            if isinstance(array_addr.type, ir.PointerType) and \
                    isinstance(array_addr.type.pointee, ir.ArrayType):
              zero = ir.Constant(ir.IntType(32), 0)
              array_addr = self.llvm_builder.gep(
                  array_addr, [zero, zero], inbounds=True)
            args.append(array_addr)

        args.append(ir.Constant(ir.IntType(32), 1))
        args.append(ir.Constant(ir.IntType(1), 0))

        pint8 = ir.PointerType(ir.IntType(8))
        k = self.llvm_module.declare_intrinsic(
            'llvm.memcpy', [pint8, pint8, ir.IntType(32)]), args
        return k

      case 'strlen':  # only works with str[], *str doesn't work now
        func_type = ir.FunctionType(
            ir.IntType(32),
            [ir.IntType(8).as_pointer()],
            var_arg=False)
        args = []

        for arg in node.args.exprs:
          zero = ir.Constant(ir.IntType(32), 0)
          ptr = self.llvm_builder.gep(
              self.visit(arg, status=0), [zero, zero], inbounds=True)
          args.append(ptr)

        return self.llvm_module.declare_intrinsic(node.name.name, (), func_type), args

      case _:
        pass


# # ---------- check & handle error ----------
# def declaration_verify(self, name):
#   if name in self.named_mem.keys() \
#           or name in self.named_arg.keys() \
#           or name in self.global_var.keys():
#       raise RuntimeError("Duplicate variable declaration!")

# def visit_ArrayDecl(self, node, status=0):
#   '''
#     Allocate new array
#   '''
#   d = self.get_type(node.type)
#   name = d['dname']
#   type = d['dtype']

#   self.declaration_verify(name)

#   self.named_mem[name] = self.llvm_builder.alloca(
#     ir.ArrayType(type, int(name.dim.value)),
#     name=name
#   )

#   return self.named_mem[name]

# def declaration_verify(self, name):
#   if name in self.named_mem.keys() or\
#      name in self.named_arg.keys() or\
#      name in self.global_var.keys():
#     raise RuntimeError('Duplicate variable declaration')
