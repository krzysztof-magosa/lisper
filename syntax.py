import ply.lex as lex
import ply.yacc as yacc

# Tokens types
class Symbol(str):
    pass

# Tokens list
tokens = (
    'LPAREN',
    'RPAREN',
    'NUMBER',
    'STRING',
    'SYMBOL'
)

# Lexer rules
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    print(t.value)
    return t

def t_SYMBOL(t):
    r'(\w+|\+|\-|\/|\*|%)'
    t.value = Symbol(t.value)
    return t

def t_error(t):
    print("Illegal character '{}'".format(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()

# Parser rules
def p_expr_atom(p):
    'expr : atom'
    p[0] = p[1]

def p_expr_list(p):
    'expr : list'
    p[0] = p[1]

def p_atom(p):
    '''
    atom : NUMBER
         | STRING
         | SYMBOL
    '''
    p[0] = p[1]

def p_list_empty(p):
    'list : LPAREN RPAREN'
    p[0] = []

def p_list_nonempty(p):
    'list : LPAREN expr_list RPAREN'
    p[0] = p[2]

def p_expr_list_item(p):
    'expr_list : expr'
    p[0] = [p[1]]

def p_expr_list_items(p):
    'expr_list : expr_list expr'
    p[0] = p[1] + [p[2]]

def p_error(p):
    if p:
         print("Syntax error at token", p.type)
         # Just discard the token and tell the parser it's okay.
#         parser.errok()
    else:
         print("Syntax error at EOF")

parser = yacc.yacc()
