import sys
sys.path.insert(0, '.')
from parser import transpilar, parser

src = """
calcule 2 + 3
mostre resultado

calcule 10 - 4
mostre resultado

calcule 2 + 3 * 4
mostre resultado
"""

python_code = transpilar(src)
print("=== Python gerado ===")
print(python_code)
print("=== Executando ===")
exec(python_code, {})


ast = parser.parse(src)
print(ast)