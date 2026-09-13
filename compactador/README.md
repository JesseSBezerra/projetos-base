# compactador

`preparacao-conquista-bff-contract.db` é um snapshot completo do projeto
`preparacao-conquista-bff-contract` (contrato OpenAPI + Terraform do API
Gateway) empacotado num único arquivo SQLite — todos os arquivos do
projeto, exceto os diretórios abaixo, cada um como uma linha da tabela
`arquivos`.

Diretórios excluídos (gerados/dependências, não são "o projeto" em si):
`target`, `.idea`, `.git`, `node_modules`, `dist`, `build`, `.angular`,
`__pycache__`, `.venv`, `venv`.

## Reconstruir o projeto

```
python descompactar.py preparacao-conquista-bff-contract.db ./preparacao-conquista-bff-contract-restaurado
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
