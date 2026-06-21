import sys
import os
sys.path.insert(0, '.')
from parser import transpilar, parser

src = """\
dispositivo: {lampada, potenciaLampada}
dispositivo: {umidificador, potenciaUmidificador}
dispositivo: {Monitor}
set {lampada, potenciaLampada} = 100 .
se umidade < 40 entao
    enviar alerta ("Ar seco detectado") Monitor .
    se verificar(umidificador) == 0 entao
        ligar umidificador .
        set potenciaUmidificador = 100 .

se movimento == True entao ligar lampada senao desligar lampada .
"""

c_code = transpilar(src)
print("=== C gerado ===")
print(c_code)

print("\n=== Executando parser ===")
try:
    ast = parser.parse(src)
    print("AST gerada com sucesso!")
except Exception as e:
    print("Erro no parser:", e)