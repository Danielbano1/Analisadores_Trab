import os
import sys


sys.path.insert(0, '.')
from parser import transpilar, parser

PASTA_TESTES = 'testes'
PASTA_SAIDA = 'saida_testes'

def main():
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)

    arquivos_teste = [f for f in os.listdir(PASTA_TESTES) if f.endswith('.obsact')]
    arquivos_teste.sort()

    print(f"Encontrados {len(arquivos_teste)} testes na pasta '{PASTA_TESTES}'.\n")

    testes_com_sucesso = 0

    for arquivo in arquivos_teste:
        caminho_teste = os.path.join(PASTA_TESTES, arquivo)
        caminho_saida = os.path.join(PASTA_SAIDA, arquivo.replace('.obsact', '.c'))
        
        with open(caminho_teste, 'r', encoding='utf-8') as f:
            src = f.read()
        
        print(f"--- Rodando: {arquivo} ---")
        try:
            parser.parse(src)
            c_code = transpilar(src)
            
            with open(caminho_saida, 'w', encoding='utf-8') as f:
                f.write(c_code)
                
            print(f"[\033[92mSUCESSO\033[0m] Código C gerado em: {caminho_saida}")
            testes_com_sucesso += 1
        except Exception as e:
            print(f"[\033[91mERRO\033[0m] Falha ao processar {arquivo}: {e}")
        print()

    print(f"=== Resumo: {testes_com_sucesso}/{len(arquivos_teste)} testes passaram ===")

if __name__ == '__main__':
    main()
