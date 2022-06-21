LR(0) < SLR(1)    < LALR(1)       < CLR(1)
        Simple LR   Look Ahead LR   Canonical LR
Yacc LALR(1)

#
# C expression rules
#
expression_opt  : empty
                | expression

expression  : assignment_expression
            | expression COMMA assignment_expression

constant_expression_opt : empty
                        | constant_expression

constant_expression : conditional_expression

assignment_expression_opt : empty
                          | assignment_expression

assignment_expression : conditional_expression
                      | unary_expression assignment_operator assignment_expression

assignment_operator : EQUAL
                    | PLUSEQUAL
                    | MINUSEQUAL
                    | MULEQUAL
                    | DIVEQUAL
                    | MODEQUAL
                    | LSHIFTEQUAL
                    | RSHIFTEQUAL
                    | XOREQUAL
                    | ANDEQUAL
                    | OREQUAL

conditional_expression  : binary_expression

binary_expression : cast_expression
                  | binary_expression MUL binary_expression
                  | binary_expression DIV binary_expression
                  | binary_expression MOD binary_expression
                  | binary_expression PLUS binary_expression
                  | binary_expression MINUS binary_expression
                  | binary_expression RSHIFT binary_expression
                  | binary_expression LSHIFT binary_expression
                  | binary_expression LT binary_expression
                  | binary_expression LE binary_expression
                  | binary_expression GE binary_expression
                  | binary_expression GT binary_expression
                  | binary_expression EQ binary_expression
                  | binary_expression NE binary_expression
                  | binary_expression AND binary_expression
                  | binary_expression OR binary_expression
                  | binary_expression XOR binary_expression
                  | binary_expression LAND binary_expression
                  | binary_expression LOR binary_expression

cast_expression : unary_expression

unary_expression  : postfix_expression
                  | PLUSPLUS unary_expression
                  | MINUSMINUS unary_expression
                  | unary_operator cast_expression

unary_operator  : AND
                | TIMES
                | PLUS
                | MINUS
                | NOT
                | LNOT

postfix_expression  : primary_expression
                    | postfix_expression LBRACKET expression RBRACKET
                    | postfix_expression LPAREN argument_expression_list RPAREN
                    | postfix_expression LPAREN RPAREN
                    | postfix_expression PERIOD identifier
                    | postfix_expression ARROW identifier
                    | postfix_expression PLUSPLUS
                    | postfix_expression MINUSMINUS

primary_expression  : identifier
                    | constant
                    | unified_string_literal
                    | LPAREN expression RPAREN

unified_string_literal  : STRING_LITERAL
                        | unified_string_literal STRING_LITERAL

argument_expression_list  : assignment_expression
                          | argument_expression_list COMMA assignment_expression


#
# C declaration rules
#
declaration : declaration_specifiers init_declarator_list_opt SEMI

declaration_specifiers_opt  : empty
                            | declaration_specifiers

declaration_specifiers  : type_qualifier declaration_specifiers_opt
                        | type_specifier declaration_specifiers_opt
                        | storage_class_specifier declaration_specifiers_opt

init_declarator_list_opt  : empty
                          | init_declarator_list

init_declarator_list  : init_declarator
                      | init_declarator_list COMMA init_declarator

init_declarator : declarator
                | declarator EQUAL initializer

type_qualifier  : CONST

type_specifier  : INT
                | CHAR
                | VOID
                | struct_specifier

struct_specifier  : STRUCT identifier
                  | STRUCT brace_open struct_declaration_list brace_close
                  | STRUCT identifier brace_open struct_declaration_list brace_close

struct_declaration_list : struct_declaration
                        | struct_declaration_list struct_declaration

struct_declaration : specifier_qualifier_list struct_declarator_list SEMI

specifier_qualifier_list_opt  : empty
                              | specifier_qualifier_list

specifier_qualifier_list  : type_qualifier specifier_qualifier_list_opt
                          | type_specifier specifier_qualifier_list_opt

struct_declarator_list  : declarator
                        | struct_declarator_list COMMA declarator

storage_class_specifier : AUTO
                        | STATIC

declarator  : direct_declarator
            | pointer direct_declarator

pointer : MUL type_qualifier_list_opt
        | MUL type_qualifier_list_opt pointer

type_qualifier_list_opt : empty
                        | type_qualifier_list

type_qualifier_list : type_qualifier
                    | type_qualifier_list type_qualifier

direct_declarator : identifier
                  | direct_declarator LBRACKET assignment_expression_opt RBRACKET
                  | direct_declarator LPAREN parameter_list RPAREN
                  | direct_declarator LPAREN identifier_list_opt RPAREN

parameter_list  : parameter_declaration
                | parameter_list COMMA parameter_declaration

parameter_declaration : declaration_specifiers declarator

identifier_list_opt : empty
                    | identifier_list

identifier_list : identifier
                | identifier_list COMMA identifier

initializer_list_opt  : empty
                      | initializer_list

initializer_list  : initializer
                  | initializer_list COMMA initializer

initializer : assignment_expression
            | brace_open initializer_list_opt brace_close
            | brace_open initializer_list COMMA brace_close


#
# C statement rules
#
statement : labeled_statement
          | compound_statement
          | selection_statement
          | expression_statement
          | iteration_statement
          | jump_statement

labeled_statement : CASE constant_expression COLON statement
                  | DEFAULT COLON statement

compound_statement : brace_open block_item_list_opt brace_close

block_item_list_opt : empty
                    | block_item_list

block_item_list : block_item
                | block_item_list block_item

block_item  : declaration
            | statement

selection_statement : IF LPAREN expression RPAREN statement
                    | IF LPAREN expression RPAREN statement ELSE statement
                    | SWITCH LPAREN expression RPAREN statement

expression_statement  : expression_opt SEMI

iteration_statement : WHILE LPAREN expression RPAREN statement

jump_statement  : BREAK SEMI
                | CONTINUE SEMI
                | RETURN expression SEMI
                | RETURN SEMI

translation_unit_or_empty : translation_unit
                          | empty

translation_unit  : external_declaration
                  | translation_unit external_declaration

external_declaration  : function_definition
                      | declaration

function_definition : declaration_specifiers declarator declaration_list_opt compound_statement

declaration_list_opt  : empty
                      | declaration_list

declaration_list  : declaration
                  | declaration_list declaration

#
# C identifier rules
#
brace_open  : LBRACE

brace_close : RBRACE

constant  : INT_CONST_DEC
          | INT_CONST_OCT
          | CHAR_CONST

empty :

identifier  : ID




# Note
type qualifier: const, volatile
type modifier: long, short, signed, unsigned, long long
type specifier: type modifier + data type


# Missing
float, double
for loop
unary_op with (type_name). Ex: *(int *)a
sizeof
goto
typedef
argument list *argv[] (**argv is fine)

Assignment: only done =, others need to be implemented in llvm
Unary: ++, --, ... need to be implemented in llvm

