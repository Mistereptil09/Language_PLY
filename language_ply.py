# -----------------------------------------------------------------------------
# calc.py - Expressions arithmétiques avec variables
# -----------------------------------------------------------------------------
reserved = {
    'sing' : 'PRINT',
    'soundcheck' : 'IF',
    'leek_spining' : 'WHILE',
    'but_actually' : 'ELSE',
    'tracklist' : 'FOR',
    'compose' : 'DEF_FUNCTION',
    'black_out' : 'BREAK',
    'encore' : 'CONTINUE',
    'arigato' : 'RETURN',
    'banished' : 'GOTO', # banished to the nether realm
}


tokens = [
    'NUMBER', 'MINUS', 'PLUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'AND', 'OR', 'END',
    'VARIABLE', 'EQUAL', 'INF', 'STRING', 'SUP',
    'SEPARATOR', 'BLOCK_START', 'BLOCK_END', 'EQEQUAL',
    'PLUSEQUAL', 'PLUSPLUS', 'NOTEQUAL', 'GRANDEQUAL', 'SMALLEQUAL',
    'MINUSEQUAL', 'TIMESEQUAL',
] + list(reserved.values())


# ----------- Tokens -----------

def t_COMMENT(t):
    r'\#.*'
    pass  # Ignore les commentaires

t_PLUSEQUAL = r'\+='
t_PLUSPLUS = r'\+\+'
t_MINUSEQUAL = r'-='
t_TIMESEQUAL = r'\*='
t_AND = r'@@'
t_OR = r'!@'
t_NOTEQUAL = r'!='
t_EQEQUAL = r'=='
t_GRANDEQUAL = r'>='
t_SMALLEQUAL = r'<='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_END = r'♪'
t_EQUAL = r'='
t_INF = r'<'
t_SUP = r'>'
t_BLOCK_START = r'\?'
t_BLOCK_END = r'\!'
t_SEPARATOR = r'\|'
t_STRING = r'\"[^\"]*\"|\'[^\']*\'' # takes any character inbetween " " or ' '

# Précédence et associativité des opérateurs (du plus faible au plus fort)
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'INF', 'SUP', 'EQEQUAL', 'NOTEQUAL'),  # ← EQEQUAL au lieu de EQUAL
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_,]*'
    t.type = reserved.get(t.value, 'VARIABLE')  # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+\.\d*|\d+'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t



# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex

lex.lex()

# ----------- Règles du Parser -----------

# ============ STATEMENTS (instructions) ============
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

def p_statement_assign(p):
    'statement : VARIABLE EQUAL expression'
    p[0] = ('assign', p[1], p[3])

def p_statement_print(p):
    'statement : PRINT LPAREN tuple RPAREN'
    p[0] = ('print', p[3])

def p_statement_expr(p):
    'statement : expression'
    p[0] = p[1]  # ← Garde seulement si une expression seule est valide

def p_tuple(p):
    '''tuple : expression SEPARATOR tuple
             | expression'''
    if len(p) == 4:
        p[0] = (p[1],) + p[3]  # Combine l'expression avec le reste du tuple
    else:
        p[0] = (p[1],)  # Un tuple avec un seul élément

# ============ EXPRESSIONS ============
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression INF expression
                  | expression SUP expression
                  | expression EQEQUAL expression
                  | expression AND expression
                  | expression OR expression
                  | expression NOTEQUAL expression
                  | expression GRANDEQUAL expression
                  | expression SMALLEQUAL expression'''
    p[0] = (p[2], p[1], p[3])

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
    p[0] = p[1][1:-1]  # Enlève les guillemets

def p_expression_call(p):
    '''expression : VARIABLE LPAREN tuple RPAREN
                | VARIABLE LPAREN RPAREN'''
    if len(p) == 5:
        p[0] = ('call', p[1], p[3])
    else:
        p[0] = ('call', p[1], [])

def p_statement_if_else(p):
    'statement : IF expression BLOCK_START bloc BLOCK_END ELSE BLOCK_START bloc BLOCK_END'
    p[0] = ('if', p[2], p[4], p[8])

def p_statement_if(p):
    'statement : IF expression BLOCK_START bloc BLOCK_END'
    p[0] = ('if', p[2], p[4], None)

def p_statement_while(p):
    'statement : WHILE expression BLOCK_START bloc BLOCK_END'
    p[0] = ('while', p[2], p[4])

def p_statement_for(p):
    'statement : FOR statement SEPARATOR expression SEPARATOR statement BLOCK_START bloc BLOCK_END'
    p[0] = ('for', p[2], p[4], p[6], p[8])

def p_statement_plusequal(p):
    'statement : VARIABLE PLUSEQUAL expression'
    p[0] = ('assign', p[1], ('+', ('variable', p[1]), p[3]))

def p_statement_minusequal(p):
    'statement : VARIABLE MINUSEQUAL expression'
    p[0] = ('assign', p[1], ('-', ('variable', p[1]), p[3]))

def p_statement_timesequal(p):
    'statement : VARIABLE TIMESEQUAL expression'
    p[0] = ('assign', p[1], ('*', ('variable', p[1]), p[3]))

def p_statement_plusplus(p):
    'statement : VARIABLE PLUSPLUS'
    p[0] = ('assign', p[1], ('+', ('variable', p[1]), 1))

def p_param_list(p):
    '''param_list : VARIABLE SEPARATOR param_list
                  | VARIABLE'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]  # Liste de noms
    else:
        p[0] = [p[1]]  # Un seul nom

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

def p_error(p):
    if p is not None:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error: unexpected end of input")
