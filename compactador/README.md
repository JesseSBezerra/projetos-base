# compactador

`conquista-auth-lwc.db` é um recorte do projeto Salesforce `organizacao`
(não o projeto inteiro — `organizacao` mistura vários componentes não
relacionados, ex. `tv2_pb_exibeFachada`) contendo **só** as classes Apex
de autenticação com o Gateway Conquista e o LWC que embute o `home-c2`,
empacotado num único arquivo SQLite.

## O que está incluído

- `classes/TV2_PB_ConquistaService.cls(+Test)` — autentica no Gateway
  (`POST /oauth/token`, client_credentials) e cacheia o Bearer token.
- `classes/TV2_PB_ConquistaController.cls(+Test)` — `autenticar()` (diagnóstico)
  e `obterToken()` (usado pelo LWC).
- `classes/TV2_PB_ConquistaRestResource.cls(+Test)` — endpoint REST de
  diagnóstico (`/services/apexrest/conquista/token`).
- `customMetadata/Conquista_Gateway_Setting.Default.md-meta.xml` +
  `objects/Conquista_Gateway_Setting__mdt/` — Custom Metadata Type com
  `Client_Id__c`/`Client_Secret__c` (o `.md-meta.xml` incluído tem
  `Client_Secret__c` como **placeholder**, não o segredo real).
- `namedCredentials/Conquista_Gateway_API.namedCredential-meta.xml` — aponta
  pro Gateway, protocolo `NoAuthentication` (auth manual no Apex).
- `permissionsets/TV2_PB_Conquista_Acesso.permissionset-meta.xml` — Apex
  Class Access necessário pro LWC conseguir chamar `obterToken()`.
- `cspTrustedSites/Home_C2_AWS_Frontend.cspTrustedSite-meta.xml` — libera o
  domínio CloudFront do `home-c2` pra rodar dentro do iframe.
- `lwc/homeC2Embed/` — o componente completo (JS, HTML, CSS, testes,
  README com o fluxo de handshake `postMessage` e a renovação de token).

Diretórios excluídos do compactador em geral (não relevantes aqui, mas
mantido por consistência com os demais `.db` deste repositório): `target`,
`.idea`, `.git`, `node_modules`, `dist`, `build`, `.angular`,
`__pycache__`, `.venv`, `venv`.

## Reconstruir

```
python descompactar.py conquista-auth-lwc.db ./conquista-auth-lwc-restaurado
```

Restaura com a MESMA estrutura relativa de pastas do projeto
`organizacao` (`classes/`, `lwc/homeC2Embed/`, etc.) — pode copiar direto
pra dentro de `force-app/main/default/` de um projeto sfdx.

`descompactar.py` recusa gravar qualquer arquivo cujo `sha256` não bata com
o salvo na compactação — garante que o `.db` não foi corrompido/alterado.

## Estrutura do banco

Tabela única `arquivos`, uma linha por arquivo:

| coluna | tipo | descrição |
|---|---|---|
| `id` | INTEGER | chave primária |
| `caminho` | TEXT | caminho relativo (separador `/`) |
| `conteudo` | BLOB | bytes brutos do arquivo |
| `tamanho_bytes` | INTEGER | tamanho do conteúdo |
| `sha256` | TEXT | hash do conteúdo, verificado na reconstrução |
