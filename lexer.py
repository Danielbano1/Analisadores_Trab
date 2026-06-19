import ply.lex as lex

tokens = (
    "DISPOSITIVO" ,"SET" ,"SE" ,"ENTAO" ,"SENAO" ,
    "LIGAR" ,"DESLIGAR" ,"VERIFICAR" ,"ENVIAR" ,"ALERTA" ,"PARA" ,
    "TODOS" ,"GT" ,"LT" ,"GE" ,"LE" ,"EQ" ,
    "NE" ,"AND" ,"EQUALS" ,"LBRACE" ,"RBRACE" ,"LPAREN" ,
    "RPAREN" ,"COLON" ,"COMMA" ,"DOT" ,"NUM" ,"TRUE" ,
    "FALSE" ,"STRING" ,"ID"  
)

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

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)   # converte string → int
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # remove as aspas: "msg" → msg
    return t

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
t_ignore = ' \t'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"[Léxico] Caractere desconhecido: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()