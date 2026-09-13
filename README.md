# projetos-base

Repositório privado com projetos de apoio/utilitários. Cada projeto/base de
código vive na sua própria branch — ver branches disponíveis no repositório.

## Arquitetura

[`arquitetura/conquista-arquitetura.drawio`](arquitetura/conquista-arquitetura.drawio)
— diagrama (draw.io / diagrams.net) da arquitetura completa do ecossistema
Conquista, organizado em **4 páginas** (abas na parte de baixo do
diagrams.net):

1. **Visão Geral** — as duas cadeias de autenticação independentes
   (consumidor↔Gateway via JWT, backend↔Salesforce via TV2-STS) e como os
   3 projetos se conectam, num nível bem alto.
2. **Salesforce** — LWC `homeC2Embed`, Apex `TV2_PB_Conquista*` (+testes),
   Named Credential/Custom Metadata/Permission Set/CSP Trusted Site, e os
   dados (`Visita__c`, `Event__c`, `PerfilTabulacao__c`, Account/Lead/User).
3. **Microfrontend (home-c2)** — `AuthService`/renovação de token,
   interceptor, services (Usuário/Pipeline/Agenda/Tabulação), ambientes,
   deploy AWS + estágio de testes E2E (Cypress).
4. **BFF (backend + API Gateway)** — endpoints do Gateway, Lambda
   Authorizer/token-issuer, VPC Link/NLB, o backend em EKS
   (`PipelineC2UseCase` paralelizado, `POST /visitas`), AWS Secrets
   Manager e os pipelines de CI/CD.

Fica na branch `main` (não é um snapshot de código pra compactar como os
`.db` do `compactador/` — é um artefato próprio que descreve o conjunto
de todos os projetos). Abrir em [app.diagrams.net](https://app.diagrams.net)
(File → Open From → Device) ou na extensão Draw.io Integration do VS Code.

Mantê-lo atualizado é responsabilidade de quem mexer na arquitetura —
não há automação que o gere a partir do código.

