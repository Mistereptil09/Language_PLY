# -----------------------------------------------------------------------------
# language_ply_complete.py - Language to AST converter using PLY
# -----------------------------------------------------------------------------

reserved = {
    'sing': 'PRINT',
    'soundcheck': 'IF',
    'leek_spining': 'WHILE',
    'but_actually': 'ELSE',
    'tracklist': 'FOR',
    'compose': 'DEF_FUNCTION',
    'black_out': 'BREAK',
    'encore': 'CONTINUE',
    'arigato': 'RETURN',
    'banished': 'GOTO',
}


tokens = [
    'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 'MODULO',
    'PLUSEQUAL', 'MINUSEQUAL', 'TIMESEQUAL', 'DIVIDEEQUAL',
    'PLUSPLUS', 'MINUSMINUS',
    'EQEQUAL', 'NOTEQUAL', 'GRANDEQUAL', 'SMALLEQUAL', 'INF', 'SUP',
    'AND', 'OR',
    'EQUAL',
    'LPAREN', 'RPAREN',
    'BLOCK_START', 'BLOCK_END',
    'SEPARATOR',
    'END',
    'VARIABLE',
] + list(reserved.values())


# ----------- Tokens -----------

def t_COMMENT(t):
    r'\#.*'
    pass


t_PLUSEQUAL   = r'\+='
t_MINUSEQUAL  = r'-='
t_TIMESEQUAL  = r'\*='
t_DIVIDEEQUAL = r'/='
t_PLUSPLUS    = r'\+\+'
t_MINUSMINUS  = r'--'
t_AND         = r'@@'
t_OR          = r'!@'
t_NOTEQUAL    = r'!='
t_EQEQUAL     = r'=='
t_GRANDEQUAL  = r'>='
t_SMALLEQUAL  = r'<='
t_PLUS        = r'\+'
t_MINUS       = r'-'
t_TIMES       = r'\*'
t_DIVIDE      = r'/'
t_POWER       = r'\^'
t_MODULO      = r'%'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_END         = r'♪'
t_EQUAL       = r'='
t_INF         = r'<'
t_SUP         = r'>'
t_BLOCK_START = r'\?'
t_BLOCK_END   = r'\!'
t_SEPARATOR   = r'\|'
t_STRING      = r'"[^"]*"|\'[^\']*\''


precedence = (
    ('nonassoc', 'LOWER_THAN_ELSE'),  # dummy: for simple if rule
    ('nonassoc', 'ELSE'),
    ('nonassoc', 'LOWEST'),           # dummy: for statement : expression rule
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'INF', 'SUP', 'EQEQUAL', 'NOTEQUAL', 'GRANDEQUAL', 'SMALLEQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'POWER'),
    ('right', 'UMINUS'),              # dummy: for unary minus rule
)


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VARIABLE')
    return t


def t_NUMBER(t):
    r'\d+\.\d*|\d+'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


import ply.lex as lex
lexer = lex.lex()


# ----------- Parser rules -----------

def p_start(p):
    'start : bloc'
    p[0] = p[1]


def p_bloc(p):
    '''bloc : bloc statement END
            | statement END'''
    if len(p) == 4:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


# ============ Statements ============

def p_statement_assign(p):
    'statement : VARIABLE EQUAL expression'
    p[0] = ('assign', p[1], p[3])


def p_statement_plusequal(p):
    'statement : VARIABLE PLUSEQUAL expression'
    p[0] = ('assign', p[1], ('+', ('variable', p[1]), p[3]))


def p_statement_minusequal(p):
    'statement : VARIABLE MINUSEQUAL expression'
    p[0] = ('assign', p[1], ('-', ('variable', p[1]), p[3]))


def p_statement_timesequal(p):
    'statement : VARIABLE TIMESEQUAL expression'
    p[0] = ('assign', p[1], ('*', ('variable', p[1]), p[3]))


def p_statement_divideequal(p):
    'statement : VARIABLE DIVIDEEQUAL expression'
    p[0] = ('assign', p[1], ('/', ('variable', p[1]), p[3]))


def p_statement_plusplus(p):
    'statement : VARIABLE PLUSPLUS'
    p[0] = ('assign', p[1], ('+', ('variable', p[1]), 1))


def p_statement_minusminus(p):
    'statement : VARIABLE MINUSMINUS'
    p[0] = ('assign', p[1], ('-', ('variable', p[1]), 1))


def p_statement_print(p):
    'statement : PRINT LPAREN arg_list RPAREN'
    p[0] = ('print', p[3])


def p_statement_if_else(p):
    'statement : IF expression BLOCK_START bloc BLOCK_END ELSE BLOCK_START bloc BLOCK_END'
    p[0] = ('if', p[2], p[4], p[8])


def p_statement_if(p):
    'statement : IF expression BLOCK_START bloc BLOCK_END %prec LOWER_THAN_ELSE'
    p[0] = ('if', p[2], p[4], None)


def p_statement_while(p):
    'statement : WHILE expression BLOCK_START bloc BLOCK_END'
    p[0] = ('while', p[2], p[4])


def p_statement_for(p):
    'statement : FOR statement SEPARATOR expression SEPARATOR statement BLOCK_START bloc BLOCK_END'
    p[0] = ('for', p[2], p[4], p[6], p[8])


def p_statement_def_function(p):
    '''statement : DEF_FUNCTION VARIABLE LPAREN param_list RPAREN BLOCK_START bloc BLOCK_END
                 | DEF_FUNCTION VARIABLE LPAREN RPAREN BLOCK_START bloc BLOCK_END'''
    if len(p) == 9:
        p[0] = ('def', p[2], p[4], p[7])
    else:
        p[0] = ('def', p[2], [], p[6])


def p_statement_break(p):
    'statement : BREAK'
    p[0] = ('break',)


def p_statement_continue(p):
    'statement : CONTINUE'
    p[0] = ('continue',)


def p_statement_return(p):
    'statement : RETURN expression'
    p[0] = ('return', p[2])


def p_statement_goto(p):
    'statement : GOTO VARIABLE'
    p[0] = ('goto', p[2])


def p_statement_expr(p):
    'statement : expression %prec LOWEST'
    p[0] = p[1]


# ============ Expressions ============

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression
                  | expression MODULO expression
                  | expression INF expression
                  | expression SUP expression
                  | expression EQEQUAL expression
                  | expression NOTEQUAL expression
                  | expression GRANDEQUAL expression
                  | expression SMALLEQUAL expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = (p[2], p[1], p[3])


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = ('-', 0, p[2])


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_variable(p):
    'expression : VARIABLE'
    p[0] = ('variable', p[1])


def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1][1:-1]


def p_expression_call(p):
    '''expression : VARIABLE LPAREN arg_list RPAREN
                  | VARIABLE LPAREN RPAREN'''
    if len(p) == 5:
        p[0] = ('call', p[1], p[3])
    else:
        p[0] = ('call', p[1], [])


# ============ Lists ============

def p_arg_list(p):
    '''arg_list : expression SEPARATOR arg_list
                | expression'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_param_list(p):
    '''param_list : VARIABLE SEPARATOR param_list
                  | VARIABLE'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_error(p):
    if p is not None:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print('Syntax error: unexpected end of input')


import ply.yacc as yacc
parser = yacc.yacc()