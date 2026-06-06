import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import ply.yacc as yacc
from lexer import tokens

# Nós da AST:
#   ('calcule', expr_node)
#   ('mostre',)
#   ('binop', op, esq, dir)
#   ('num', valor)

def p_programa(p):
    'programa : stmts'
    p[0] = p[1]

def p_stmts_multi(p):
    'stmts : stmts stmt'
    p[0] = p[1] + ([p[2]] if p[2] else [])

def p_stmts_single(p):
    'stmts : stmt'
    p[0] = [p[1]] if p[1] else []

def p_stmt_calcule(p):
    'stmt : CALCULE expr NEWLINE'
    p[0] = ('calcule', p[2])

def p_stmt_mostre(p):
    'stmt : MOSTRE RESULTADO NEWLINE'
    p[0] = ('mostre',)

def p_stmt_newline(p):
    'stmt : NEWLINE'
    p[0] = None

def p_expr_binop(p):
    '''expr : expr PLUS  termo
            | expr MINUS termo'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expr_termo(p):
    'expr : termo'
    p[0] = p[1]

def p_termo_binop(p):
    '''termo : termo TIMES  fator
             | termo DIVIDE fator'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_termo_fator(p):
    'termo : fator'
    p[0] = p[1]

def p_fator_num(p):
    'fator : NUMBER'
    p[0] = ('num', p[1])

def p_error(p):
    if p:
        print(f"[Sintaxe] Erro em '{p.value}' na linha {p.lineno}")
    else:
        print("[Sintaxe] Fim de arquivo inesperado")

parser = yacc.yacc(debug=False, write_tables=False)

def gerar_expr(no):
    if no[0] == 'num':
        v = no[1]
        return str(int(v)) if v == int(v) else str(v)
    elif no[0] == 'binop':
        _, op, esq, dir_ = no
        return f"({gerar_expr(esq)} {op} {gerar_expr(dir_)})"

def gerar(ast):
    linhas = ["resultado = 0"]
    for no in ast:
        if no[0] == 'calcule':
            linhas.append(f"resultado = {gerar_expr(no[1])}")
        elif no[0] == 'mostre':
            linhas.append('print(f"Resultado: {resultado:g}")')
    return "\n".join(linhas)

def transpilar(src):
    if not src.endswith('\n'):
        src += '\n'
    ast = parser.parse(src)
    return gerar(ast) if ast is not None else ""