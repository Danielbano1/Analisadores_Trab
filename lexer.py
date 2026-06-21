import ply.lex as lex

reserved = {
    "dispositivo": "DISPOSITIVO",
    "set": "SET",
    "se": "SE",
    "entao": "ENTAO",
    "senao": "SENAO",
    "ligar": "LIGAR",
    "desligar": "DESLIGAR",
    "verificar": "VERIFICAR",
    "enviar": "ENVIAR",
    "alerta": "ALERTA",
    "para": "PARA",
    "todos": "TODOS",
    "True": "TRUE",
    "False": "FALSE"
}

tokens = (
    "GT", "LT", "GE", "LE", "EQ", "NE", "AND", "EQUALS",
    "LBRACE", "RBRACE", "LPAREN", "RPAREN", "COLON", "COMMA", "DOT",
    "NUM", "STRING", "ID"
) + tuple(reserved.values())

t_GE = r'>='
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='
t_AND = r'&&'
t_GT = r'>'
t_LT = r'<'
t_EQUALS = r'='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"[Léxico] Caractere desconhecido: '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()