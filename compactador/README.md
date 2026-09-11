# compactador

Compacta um projeto inteiro (todos os arquivos, exceto `target/` e `.idea/`)
em um único arquivo SQLite, e reconstrói o projeto a partir dele.

## Uso

Compactar:
```
python compactar.py <diretorio_do_projeto> <saida.db>
```

Reconstruir:
```
python descompactar.py <arquivo.db> <diretorio_destino>
```

## Estrutura do banco

Tabela única `arquivos`, uma linha por arquivo do projeto:

| coluna | tipo | descrição |
|---|---|---|
| `id` | INTEGER | chave primária |
| `caminho` | TEXT | caminho relativo à raiz do projeto (separador `/`) |
| `conteudo` | BLOB | bytes brutos do arquivo |
| `tamanho_bytes` | INTEGER | tamanho do conteúdo |
| `sha256` | TEXT | hash do conteúdo, verificado na reconstrução |

`descompactar.py` recusa gravar qualquer arquivo cujo sha256 não bata com o
salvo — garante que o `.db` não foi corrompido/alterado entre a compactação
e a reconstrução.

## home_c2_v2.db

Snapshot completo do projeto `home-c2-v2` (branch `home-c2-v2` deste
repositório), incluindo um `README.md` próprio com todas as queries SOQL
usadas no projeto — ele só existe dentro deste `.db` (não como arquivo solto
no repositório). Para ler:

```
python descompactar.py home_c2_v2.db ./home-c2-v2-restaurado
```
