# compactador

`home_c2_v2.db` é um snapshot completo do projeto `home-c2-v2` empacotado
num único arquivo SQLite (todos os arquivos do projeto, exceto `target/` e
`.idea/`, cada um como uma linha da tabela `arquivos`). Inclui um
`README.md` próprio com todas as queries SOQL usadas no projeto — ele só
existe dentro deste `.db`, não como arquivo solto no repositório.

## Reconstruir o projeto

```
python descompactar.py home_c2_v2.db ./home-c2-v2-restaurado
```

`descompactar.py` recria a árvore de diretórios/arquivos original e recusa
gravar qualquer arquivo cujo `sha256` não bata com o salvo no momento da
compactação — garante que o `.db` não foi corrompido/alterado.

## Estrutura do banco

Tabela única `arquivos`, uma linha por arquivo do projeto:

| coluna | tipo | descrição |
|---|---|---|
| `id` | INTEGER | chave primária |
| `caminho` | TEXT | caminho relativo à raiz do projeto (separador `/`) |
| `conteudo` | BLOB | bytes brutos do arquivo |
| `tamanho_bytes` | INTEGER | tamanho do conteúdo |
| `sha256` | TEXT | hash do conteúdo, verificado na reconstrução |
