from my_type import *
from helper import *
from my_graph import *
import igraph as ig


class Parser:
  def __init__(self, tokens):
    self._tokens = tokens
    self._current = 0
    self._g = Graph()

  def get_cur(self):
    return self._tokens[self._current]

  def move_next(self):
    self._current += 1
    return self._current < len(self._tokens)

  def display_graph(self, path, layout, styles):
    layout = self._g.graph.layout('rt', mode='in', root=0)
    ig.plot(self._g.graph, path, layout=layout, **styles)

  # <Program> -> <Block>
  def ParseProgram(self):
    root = self._g.add_vertex('program')
    block = self._g.add_vertex('block')
    self.ParseBlock(block)
    self._g.add_edges(root, [block])


  # <Block> -> { <OperatorList> }
  def ParseBlock(self, src):
    dsts = []

    dsts.append(self._g.add_vertex('{'))
    self.ParseOpenCurlyBracket()

    dsts.append(self._g.add_vertex('op list'))
    self.ParseOperatorList(dsts[-1])

    dsts.append(self._g.add_vertex('}'))
    self.ParseCloseCurlyBracket()

    self._g.add_edges(src, dsts)


  # <OperatorList> -> <Operator> <Tail>
  def ParseOperatorList(self, src):
    dsts = []

    dsts.append(self._g.add_vertex('op'))
    self.ParseOperator(dsts[-1])

    dsts.append(self._g.add_vertex('tail'))
    self.ParseTail(dsts[-1])

    self._g.add_edges(src, dsts)


  # <Operator> -> <Identifier> = <Expression> | <Block>
  @defers_collector
  def ParseOperator(self, src):
    dsts = []

    def reject(): # <Block>
      err = recover()
      if err:
        self._g.delete_vertices(dsts)
        dsts.clear()
        dsts.append(self._g.add_vertex('block'))
        self.ParseBlock(dsts[-1])
        self._g.add_edges(src, dsts)
    defer(lambda: reject())

    dsts.append(self._g.add_vertex(self.get_cur().val))
    self.ParseIdentifier()

    dsts.append(self._g.add_vertex('='))
    self.ParseAssignment()

    dsts.append(self._g.add_vertex('expr'))
    self.ParseExpression(dsts[-1])

    self._g.add_edges(src, dsts)


  # <Tail> -> ; <Operator> <Tail> | ε
  @defers_collector
  def ParseTail(self, src):
    dsts = []

    def reject(): # ε
      err = recover()
      if err:
        self._g.delete_vertices(dsts)
        dsts.clear()
        dsts.append(self._g.add_vertex('ε'))
        self._g.add_edges(src, dsts)
    defer(lambda: reject())

    dsts.append(self._g.add_vertex(';'))
    self.ParseSemicolon()

    dsts.append(self._g.add_vertex('op'))
    self.ParseOperator(dsts[-1])

    dsts.append(self._g.add_vertex('tail'))
    self.ParseTail(dsts[-1])

    self._g.add_edges(src, dsts)


  # <Expression> -> <AlgebraicExpression> <RelationOperator> <AlgebraicExpression> | <AlgebraicExpression>
  # Left refractor:
  #   <Expression>  -> <AlgebraicExpression> <Expression'>
  #   <Expression'> -> <RelationOperator> <AlgebraicExpression> | ε
  def ParseExpression(self, src):
    dsts = []

    dsts.append(self._g.add_vertex('alg expr'))
    self.ParseAlgebraicExpression(dsts[-1])

    dsts.append(self._g.add_vertex("expr'"))
    self.ParseExpression_(dsts[-1])

    self._g.add_edges(src, dsts)

  @defers_collector
  def ParseExpression_(self, src):
    dsts = []

    def reject(): # ε
      err = recover()
      if err:
        self._g.delete_vertices(dsts)
        dsts.clear()
        dsts.append(self._g.add_vertex('ε'))
        self._g.add_edges(src, dsts)
    defer(lambda: reject())

    dsts.append(self._g.add_vertex(self.get_cur().val))
    self.ParseRelation()

    dsts.append(self._g.add_vertex('alg expr'))
    self.ParseAlgebraicExpression(dsts[-1])

    self._g.add_edges(src, dsts)


  # <AlgebraicExpression> -> <AlgebraicExpression> <AdditionOperator> <Term> | <Term>
  # Eliminate Left Recursion, Left refractor:
  #   <AlgebraicExpression>  -> <Term> <AlgebraicExpression'>
  #   <AlgebraicExpression'> -> <AdditionOperator> <Term> <AlgebraicExpression'> | ε
  def ParseAlgebraicExpression(self, src):
    dsts = []

    dsts.append(self._g.add_vertex('term'))
    self.ParseTerm(dsts[-1])

    dsts.append(self._g.add_vertex("alg expr'"))
    self.ParseAlgebraicExpression_(dsts[-1])

    self._g.add_edges(src, dsts)

  @defers_collector
  def ParseAlgebraicExpression_(self, src):
    dsts = []

    def reject(): # ε
      err = recover()
      if err:
        self._g.delete_vertices(dsts)
        dsts.clear()
        dsts.append(self._g.add_vertex('ε'))
        self._g.add_edges(src, dsts)
    defer(lambda: reject())

    dsts.append(self._g.add_vertex(self.get_cur().val))
    self.ParseAddition()

    dsts.append(self._g.add_vertex('term'))
    self.ParseTerm(dsts[-1])

    dsts.append(self._g.add_vertex("alg expr'"))
    self.ParseAlgebraicExpression_(dsts[-1])

    self._g.add_edges(src, dsts)


  # <Term> -> <Term> <MultiplicationOperator> <Factor> | <Factor>
  # Eliminate Left Recursion, Left refractor:
  #   <Term>  -> <Factor> <Term'>
  #   <Term'> -> <MultiplicationOperator> <Factor> <Term'> | ε
  def ParseTerm(self, src):
    dsts = []

    dsts.append(self._g.add_vertex('factor'))
    self.ParseFactor(dsts[-1])

    dsts.append(self._g.add_vertex("term'"))
    self.ParseTerm_(dsts[-1])

    self._g.add_edges(src, dsts)

  @defers_collector
  def ParseTerm_(self, src):
    dsts = []

    def reject(): # ε
      err = recover()
      if err:
        self._g.delete_vertices(dsts)
        dsts.clear()
        dsts.append(self._g.add_vertex('ε'))
        self._g.add_edges(src, dsts)
    defer(lambda: reject())

    dsts.append(self._g.add_vertex(self.get_cur().val))
    self.ParseMultiplication()

    dsts.append(self._g.add_vertex('factor'))
    self.ParseFactor(dsts[-1])

    dsts.append(self._g.add_vertex("term'"))
    self.ParseTerm_(dsts[-1])

    self._g.add_edges(src, dsts)


  # <Factor> -> <Identifier> | <NumberConstant> | "(" <AlgebraicExpression> ")"
  @defers_collector
  def ParseFactor(self, src):
    dsts = []

    def reject1(): # <Identifier>
      err = recover()
      if err:
        self._g.delete_vertices(dsts)
        dsts.clear()
        dsts.append(self._g.add_vertex(self.get_cur().val))
        self.ParseIdentifier()
        self._g.add_edges(src, dsts)
    def reject2(): # <NumberConstant>
      err = recover()
      if err:
        self._g.delete_vertices(dsts)
        dsts.clear()
        dsts.append(self._g.add_vertex(self.get_cur().val))
        self.ParseNumber()
        self._g.add_edges(src, dsts)
    defer(lambda: reject1())
    defer(lambda: reject2())

    dsts.append(self._g.add_vertex('('))
    self.ParseOpenParenthesisBracket()

    dsts.append(self._g.add_vertex('alg expr'))
    self.ParseAlgebraicExpression(dsts[-1])

    dsts.append(self._g.add_vertex(')'))
    self.ParseCloseParenthesisBracket()

    self._g.add_edges(src, dsts)


  @defers_collector
  def ParseNumber(self):
    token = self.get_cur()
    if isinstance(token, NumberToken):
      self.move_next()
    else:
      panic('Expected a numeric constant')


  @defers_collector
  def ParseIdentifier(self):
    token = self.get_cur()
    if isinstance(token, IdentifierToken):
      self.move_next()
    else:
      panic('Expected an idenifier')


  @defers_collector
  def ParseMultiplication(self):
    token = self.get_cur()
    if isinstance(token, MultiplicationToken):
      self.move_next()
    else:
      panic('Expected a multiplicative operator')


  @defers_collector
  def ParseAddition(self):
    token = self.get_cur()
    if isinstance(token, AdditionToken):
      self.move_next()
    else:
      panic('Expected a additive operator')


  @defers_collector
  def ParseRelation(self):
    token = self.get_cur()
    if isinstance(token, RelationToken):
      self.move_next()
    else:
      panic('Expected a relational operator')


  @defers_collector
  def ParseAssignment(self, ):
    token = self.get_cur()
    if isinstance(token, AssignmentToken):
      self.move_next()
    else:
      panic('Expected "=" after identifier')


  @defers_collector
  def ParseSemicolon(self):
    token = self.get_cur()
    if isinstance(token, SemicolonToken):
      self.move_next()
    else:
      panic('Expected ";"')


  @defers_collector
  def ParseOpenCurlyBracket(self):
    token = self.get_cur()
    if isinstance(token, OpenCurlyBracketToken):
      self.move_next()
    else:
      panic('Expected "{"')


  @defers_collector
  def ParseCloseCurlyBracket(self):
    token = self.get_cur()
    if isinstance(token, CloseCurlyBracketToken):
      self.move_next()
    else:
      panic('Expected "}"')


  @defers_collector
  def ParseOpenParenthesisBracket(self):
    token = self.get_cur()
    if isinstance(token, OpenParenthesisToken):
      self.move_next()
    else:
      panic('Expected "("')


  @defers_collector
  def ParseCloseParenthesisBracket(self):
    token = self.get_cur()
    if isinstance(token, CloseParenthesisToken):
      self.move_next()
    else:
      panic('Expected ")"')