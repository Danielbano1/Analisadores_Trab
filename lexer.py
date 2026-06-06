import ply.lex as lex

tokens = (
    'CALCULE', 'MOSTRE', 'RESULTADO',
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'NEWLINE',
)

reserved = {
    'calcule'   : 'CALCULE',
    'mostre'    : 'MOSTRE',
    'resultado' : 'RESULTADO',
}

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_WORD(t):
    r'[a-zA-Z]+'
    t.type = reserved.get(t.value.lower())
    return t if t.type else None

t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_ignore = ' \t'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_error(t):
    print(f"[Léxico] Caractere desconhecido: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()