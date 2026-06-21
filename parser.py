import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import ply.yacc as yacc
from lexer import tokens

def p_programa(p):
    'programa : devices cmds'
    p[0] = ('program', p[1], p[2])

def p_devices_multi(p):
    'devices : device devices'
    p[0] = [p[1]] + p[2]

def p_devices_single(p):
    'devices : device'
    p[0] = [p[1]]

def p_device_obs(p):
    'device : DISPOSITIVO COLON LBRACE ID COMMA ID RBRACE'
    p[0] = ('device', p[4], p[6])

def p_device_simple(p):
    'device : DISPOSITIVO COLON LBRACE ID RBRACE'
    p[0] = ('device', p[4], None)

def p_cmds_multi(p):
    'cmds : cmd cmds'
    p[0] = [p[1]] + p[2]

def p_cmds_single(p):
    'cmds : cmd'
    p[0] = [p[1]]

def p_cmd(p):
    '''cmd : attrib opt_dot
           | obsact opt_dot
           | act opt_dot'''
    p[0] = p[1]

def p_attrib_var(p):
    'attrib : SET ID EQUALS var'
    p[0] = ('attrib', p[2], p[4])

def p_attrib_act(p):
    'attrib : SET ID EQUALS actexecute'
    p[0] = ('attrib', p[2], p[4])

def p_attrib_complex(p):
    'attrib : SET LBRACE ID COMMA ID RBRACE EQUALS var'
    p[0] = ('attrib', p[5], p[8])

def p_obsact_if(p):
    'obsact : SE obs ENTAO cmds_opt_dot'
    p[0] = ('ifelse', p[2], p[4], None)

def p_obsact_ifelse(p):
    'obsact : SE obs ENTAO cmds SENAO cmds_opt_dot'
    p[0] = ('ifelse', p[2], p[4], p[6])

def p_cmds_opt_dot(p):
    'cmds_opt_dot : cmds opt_dot'
    p[0] = p[1]

def p_act(p):
    '''act : actexecute
           | actalert'''
    p[0] = p[1]

def p_obs_simple(p):
    'obs : ID oplogic var'
    p[0] = ('obs', p[1], p[2], p[3])

def p_obs_verificar(p):
    'obs : VERIFICAR LPAREN ID RPAREN oplogic var'
    p[0] = ('obs_verificar', p[3], p[5], p[6])

def p_obs_and(p):
    'obs : obs AND obs'
    p[0] = ('and', p[1], p[3])

def p_oplogic(p):
    '''oplogic : GT
               | LT
               | GE
               | LE
               | EQ
               | NE'''
    p[0] = p[1]

def p_var(p):
    '''var : NUM
           | TRUE
           | FALSE'''
    if str(p[1]).lower() == 'true':
        p[0] = 'True'
    elif str(p[1]).lower() == 'false':
        p[0] = 'False'
    else:
        p[0] = p[1]

def p_actexecute(p):
    'actexecute : ACTION ID'
    p[0] = ('act_exe', p[1], p[2])

def p_action(p):
    '''ACTION : LIGAR
              | DESLIGAR
              | VERIFICAR'''
    p[0] = p[1]

def p_actalert_simple(p):
    'actalert : ENVIAR ALERTA LPAREN STRING RPAREN ID'
    p[0] = ('act_alert', p[4], p[6], None)

def p_actalert_obs(p):
    'actalert : ENVIAR ALERTA LPAREN STRING COMMA ID RPAREN ID'
    p[0] = ('act_alert', p[4], p[8], p[6])

def p_actalert_broadcast(p):
    'actalert : ENVIAR ALERTA LPAREN STRING RPAREN PARA TODOS COLON id_list'
    p[0] = ('act_broadcast', p[4], p[9], None)

def p_actalert_broadcast_obs(p):
    'actalert : ENVIAR ALERTA LPAREN STRING COMMA ID RPAREN PARA TODOS COLON id_list'
    p[0] = ('act_broadcast', p[4], p[11], p[6])

def p_id_list_multi(p):
    'id_list : ID COMMA id_list'
    p[0] = [p[1]] + p[3]

def p_id_list_single(p):
    'id_list : ID'
    p[0] = [p[1]]

def p_opt_dot_dot(p):
    'opt_dot : DOT'
    pass

def p_opt_dot_empty(p):
    'opt_dot : empty'
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"[Sintaxe] Erro em '{p.value}' na linha {p.lineno}")
    else:
        print("[Sintaxe] Fim de arquivo inesperado")

precedence = (
    ('right', 'SENAO'),
    ('left', 'AND'),
)

parser = yacc.yacc(debug=False, write_tables=False)

def gerar_obs(obs_node):
    tipo = obs_node[0]
    if tipo == 'obs':
        val = obs_node[3]
        if str(val) == 'True': val = 1
        elif str(val) == 'False': val = 0
        return f"{obs_node[1]} {obs_node[2]} {val}"
    elif tipo == 'obs_verificar':
        val = obs_node[3]
        if str(val) == 'True': val = 1
        elif str(val) == 'False': val = 0
        return f"verificar(\"{obs_node[1]}\") {obs_node[2]} {val}"
    elif tipo == 'and':
        return f"({gerar_obs(obs_node[1])}) && ({gerar_obs(obs_node[2])})"

def gerar_cmds(cmds, indent):
    res = ""
    for cmd in cmds:
        res += gerar_cmd(cmd, indent)
    return res

def gerar_cmd(cmd, indent):
    tipo = cmd[0]
    if tipo == 'attrib':
        obs = cmd[1]
        val = cmd[2]
        if isinstance(val, tuple) and val[0] == 'act_exe':
            res_val = f"{val[1].lower()}(\"{val[2]}\")"
        else:
            if str(val) == 'True': res_val = "1"
            elif str(val) == 'False': res_val = "0"
            else: res_val = str(val)
        return f"{indent}{obs} = {res_val};\n"
    elif tipo == 'ifelse':
        cond = gerar_obs(cmd[1])
        res = f"{indent}if ({cond}) {{\n"
        res += gerar_cmds(cmd[2], indent + "    ")
        if cmd[3]:
            res += f"{indent}}} else {{\n"
            res += gerar_cmds(cmd[3], indent + "    ")
        res += f"{indent}}}\n"
        return res
    elif tipo == 'act_exe':
        return f"{indent}{cmd[1].lower()}(\"{cmd[2]}\");\n"
    elif tipo == 'act_alert':
        msg = cmd[1]
        dev = cmd[2]
        obs = cmd[3]
        if obs:
            return f"{indent}alerta(\"{dev}\", \"{msg}\", {obs}, 1);\n"
        else:
            return f"{indent}alerta(\"{dev}\", \"{msg}\", 0, 0);\n"
    elif tipo == 'act_broadcast':
        msg = cmd[1]
        devs = cmd[2]
        obs = cmd[3]
        res = ""
        for dev in devs:
            if obs:
                res += f"{indent}alerta(\"{dev}\", \"{msg}\", {obs}, 1);\n"
            else:
                res += f"{indent}alerta(\"{dev}\", \"{msg}\", 0, 0);\n"
        return res

def gerar_c(ast):
    codigo = """\
#include <stdio.h>
#include <string.h>

int ligar(const char* namedevice) {
    printf("%s ligado!\\n", namedevice);
    return 1;
}

int desligar(const char* namedevice) {
    printf("%s desligado!\\n", namedevice);
    return 0;
}

int verificar(const char* namedevice) {
    printf("%s est ligado.\\n", namedevice);
    return 1;
}

void alerta(const char* namedevice, const char* msg, int var, int has_var) {
    if (has_var) {
        printf("%s recebeu o alerta:\\n%s %d\\n", namedevice, msg, var);
    } else {
        printf("%s recebeu o alerta:\\n%s\\n", namedevice, msg);
    }
}

int main() {
"""
    devices = ast[1]
    cmds = ast[2]
    
    # Declarar variáveis das observações com valor 0 inicial
    for dev in devices:
        if dev[2]:
            codigo += f"    int {dev[2]} = 0;\n"
    
    codigo += "\n    // Execucao\n"
    codigo += gerar_cmds(cmds, indent="    ")
    codigo += "    return 0;\n}\n"
    return codigo

def transpilar(src):
    if not src.endswith('\n'):
        src += '\n'
    ast = parser.parse(src)
    return gerar_c(ast) if ast is not None else ""