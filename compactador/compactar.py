"""Compacta um diretório de projeto inteiro em um único arquivo SQLite.

Percorre recursivamente o diretório de origem e grava cada arquivo (caminho
relativo + conteúdo bruto em bytes) como uma linha na tabela `arquivos`.
Diretórios listados em EXCLUDE_DIRS são pulados por completo.

Uso:
    python compactar.py <diretorio_origem> <arquivo_destino.db>
"""
import argparse
import hashlib
import os
import sqlite3

EXCLUDE_DIRS = {"target", ".idea"}

SCHEMA = """
CREATE TABLE IF NOT EXISTS arquivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caminho TEXT UNIQUE NOT NULL,
    conteudo BLOB NOT NULL,
    tamanho_bytes INTEGER NOT NULL,
    sha256 TEXT NOT NULL
);
"""


def deve_ignorar(caminho_relativo):
    partes = caminho_relativo.replace("\\", "/").split("/")
    return any(parte in EXCLUDE_DIRS for parte in partes)


def _inserir(conn, caminho_relativo, conteudo):
    conn.execute(
        "INSERT OR REPLACE INTO arquivos (caminho, conteudo, tamanho_bytes, sha256) "
        "VALUES (?, ?, ?, ?)",
        (caminho_relativo, conteudo, len(conteudo), hashlib.sha256(conteudo).hexdigest()),
    )


def compactar(origem, destino, extras=None):
    """Compacta `origem` em `destino`. `extras` é um dict opcional
    {caminho_relativo: bytes} de arquivos virtuais adicionados além dos
    encontrados em disco (ex.: documentação gerada que não deve existir
    como arquivo solto no projeto). Sempre recria `destino` do zero — uma
    compactação anterior nunca deixa linhas obsoletas (ex.: caminhos que
    existiam antes de uma renomeação) misturadas com a atual."""
    origem = os.path.abspath(origem)
    if os.path.exists(destino):
        os.remove(destino)
    conn = sqlite3.connect(destino)
    conn.executescript(SCHEMA)

    total = 0
    for raiz, dirs, arquivos in os.walk(origem):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for nome in arquivos:
            caminho_absoluto = os.path.join(raiz, nome)
            caminho_relativo = os.path.relpath(caminho_absoluto, origem).replace("\\", "/")
            if deve_ignorar(caminho_relativo):
                continue
            with open(caminho_absoluto, "rb") as f:
                conteudo = f.read()
            _inserir(conn, caminho_relativo, conteudo)
            total += 1

    for caminho_relativo, conteudo in (extras or {}).items():
        _inserir(conn, caminho_relativo, conteudo)
        total += 1

    conn.commit()
    conn.close()
    print(f"{total} arquivos compactados em {destino}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("origem", help="Diretório do projeto a compactar")
    parser.add_argument("destino", help="Caminho do arquivo .db de saída")
    args = parser.parse_args()
    compactar(args.origem, args.destino)
