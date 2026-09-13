# compactador

`conquista-collections.db` é um snapshot completo da coleção Bruno
`conquista-collections` (testes manuais do API Gateway do BFF Conquista)
empacotado num único arquivo SQLite — todos os arquivos do projeto, exceto
os diretórios abaixo, cada um como uma linha da tabela `arquivos`.

Diretórios excluídos (gerados/dependências, não são "o projeto" em si):
`target`, `.idea`, `.git`, `node_modules`, `dist`, `build`, `.angular`,
`__pycache__`, `.venv`, `venv`.

> ⚠️ **Este snapshot contém segredos em texto puro**:
> `environments/Hom.bru` tem `clientSecret` (client OAuth2 de demonstração
> do ambiente hom) e um `accessToken` (JWT de curta duração) — mantidos de
> propósito a pedido, diferente da prática usual do restante deste
> repositório (`compactador` de outros projetos nunca inclui segredo real).
> Se este `.db` for compartilhado fora do time, rotacionar o client
> correspondente no AWS Secrets Manager
> (`preparacao-conquista-bff-oauth-clients`) antes.

## Reconstruir o projeto

```
python descompactar.py conquista-collections.db ./conquista-collections-restaurado
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
