# # from lexer import Lexer
# from ply import yacc

# # def test_lexer():
# #   lexer = Lexer(lambda: None, lambda: None)
# #   lexer.build()
# #   with open('./coursework/tests/prog_struct_return.c', mode='r', encoding='utf-8') as f:
# #     src_code = f.read()
# #   lexer.input(src_code)
# #   while True:
# #     token = lexer.token()
# #     if not token:
# #       break
# #     print(token)

# tokens = ['INT', 'FLOAT']

# def p_calc(p):
#   '''
#   calc  : expression
#         | empty
#   '''
#   print(p[1])

# def p_expression(p):
#   '''
#   expression  : INT
#               | FLOAT
#   '''
#   p[0] = p[1]

# def p_empty(p):
#   '''
#   empty :
#   '''
#   pass

# parser = yacc.yacc()

# while True:
#   try:
#     s = input('')
#   except EOFError:
#     break
#   parser.parse(s)


print(dict(qual=['test'], spec=[], storage=[]))