# projetos-base

Repositório privado com projetos de apoio/utilitários. Cada projeto/base de
código vive na sua própria branch — ver branches disponíveis no repositório.

## Arquitetura

[`arquitetura/conquista-arquitetura.drawio`](arquitetura/conquista-arquitetura.drawio)
— diagrama (draw.io / diagrams.net) da arquitetura completa do ecossistema
Conquista: Salesforce (LWC `homeC2Embed` + Apex `TV2_PB_Conquista*` +
dados `Visita__c`/`Event__c`/`PerfilTabulacao__c`), `home-c2` (Angular,
AWS S3+CloudFront), o API Gateway (`preparacao-conquista-bff-contract`,
Lambda Authorizer + token-issuer), o backend em EKS
(`preparacao-conquista-bff`), AWS Secrets Manager, e os 3 pipelines de
CI/CD — incluindo as duas cadeias de autenticação independentes
(consumidor↔Gateway via JWT, backend↔Salesforce via TV2-STS).

Fica na branch `main` (não é um snapshot de código pra compactar como os
`.db` do `compactador/` — é um artefato próprio que descreve o conjunto
de todos os projetos). Abrir em [app.diagrams.net](https://app.diagrams.net)
(File → Open From → Device) ou na extensão Draw.io Integration do VS Code.

Mantê-lo atualizado é responsabilidade de quem mexer na arquitetura —
não há automação que o gere a partir do código.

