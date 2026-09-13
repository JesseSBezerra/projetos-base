"""Reconstrói um projeto a partir de um arquivo SQLite gerado por compactar.py.

Lê a tabela `arquivos` e recria a árvore de diretórios/arquivos original,
validando a integridade de cada arquivo pelo sha256 gravado no momento da
compactação — se o conteúdo não bater com o hash salvo, a reconstrução para
e aponta o arquivo corrompido em vez de gravar dado inconsistente.

Uso:
    python descompactar.py <arquivo_origem.db> <diretorio_destino>
"""
import argparse
import hashlib
import os
import sqlite3


def descompactar(origem, destino):
    destino = os.path.abspath(destino)
    conn = sqlite3.connect(origem)
    cursor = conn.execute("SELECT caminho, conteudo, sha256 FROM arquivos ORDER BY caminho")

    total = 0
    for caminho_relativo, conteudo, sha256_esperado in cursor:
        sha256_real = hashlib.sha256(conteudo).hexdigest()
        if sha256_real != sha256_esperado:
            raise ValueError(f"Integridade violada em '{caminho_relativo}': sha256 não confere")

        caminho_absoluto = os.path.join(destino, caminho_relativo)
        os.makedirs(os.path.dirname(caminho_absoluto), exist_ok=True)
        with open(caminho_absoluto, "wb") as f:
            f.write(conteudo)
        total += 1

    conn.close()
    print(f"{total} arquivos restaurados em {destino}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("origem", help="Arquivo .db gerado por compactar.py")
    parser.add_argument("destino", help="Diretório onde o projeto será reconstruído")
    args = parser.parse_args()
    descompactar(args.origem, args.destino)
