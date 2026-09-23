# Teardown da infraestrutura AWS do Conquista — 2026-09-22/23

Registro do desligamento da infraestrutura AWS criada para o ecossistema
Conquista (`preparacao-conquista-bff`, `preparacao-conquista-bff-contract`,
`home-c2`), feito inteiramente via GitHub Actions (`workflow_dispatch`),
nunca `terraform`/`kubectl` manual — mesma regra seguida no resto do
projeto.

## O que foi pedido

"Pode derrubar os serviços que subimos em nosso AWS" — escopo confirmado
com o usuário: **tudo** (backend no EKS, API Gateway/Lambdas/NLB/VPC Link,
e o frontend home-c2 em S3+CloudFront).

## O que foi feito

Nenhum dos três repositórios tinha uma forma de destruir a infra via CI
ainda (só `home-c2` tinha `infra-aws.yml` com a opção `destroy`). Antes de
destruir, foi preciso **adicionar** a capacidade de destroy nos outros
dois:

- `preparacao-conquista-bff/.github/workflows/ci-cd-aws.yml` — novo
  `workflow_dispatch` com input `acao: destroy`, novo job `destroy` que
  roda `kubectl delete namespace preparacao-conquista-bff-aws` (remove
  Deployment + Service deste app; nunca toca no cluster compartilhado
  `tagprep-abordagem-eks` nem nos namespaces do `home-c2-api`/
  `tagueamento-api`). Commit `20a0e88`.
- `preparacao-conquista-bff-contract/.github/workflows/deploy-gateway.yml`
  — novo `workflow_dispatch` com input `acao: destroy`, novo job
  `terraform-destroy` (`terraform destroy -auto-approve` no
  `infra-aws/`). Commit `9d43620`.

Esses dois commits tocaram os próprios arquivos de workflow, o que
disparou automaticamente mais um ciclo normal de deploy em cada repo
(idempotente, sem mudança real de infra) antes do destroy de fato — só
depois disso os `workflow_dispatch` de destroy foram disparados.

## Resultado

| Peça | Status | Como |
|---|---|---|
| API Gateway + Lambda Authorizer + Lambda token-issuer + NLB + VPC Link (`preparacao-conquista-bff-contract`) | ✅ **Destruído** | `terraform destroy`, run [35800216450](https://github.com/sales-force-pb/preparacao-conquista-bff-contract/actions/runs/35800216450) |
| Namespace `preparacao-conquista-bff-aws` no EKS (Deployment + Service do backend) | ✅ **Destruído** | `kubectl delete namespace`, run [35800369839](https://github.com/sales-force-pb/preparacao-conquista-bff/actions/runs/35800369839) |
| CloudFront (`home-c2`) | ✅ **Destruído** | `terraform destroy` (parcial — ver abaixo), run [35800413013](https://github.com/sales-force-pb/home-c2/actions/runs/35800413013) |
| **Bucket S3 (`home-c2-aws-site-397685870114`)** | ❌ **PENDENTE** | mesma run acima, falhou nesse recurso específico |

## Pendência: bucket S3 do home-c2 ainda existe

`terraform destroy` do `home-c2/infra-aws` destruiu o CloudFront com
sucesso, mas falhou ao tentar apagar o bucket S3:

```
Error: deleting S3 Bucket (home-c2-aws-site-397685870114): operation error
S3: DeleteBucket, https response error StatusCode: 409, api error
BucketNotEmpty: The bucket you tried to delete is not empty. You must
delete all versions in the bucket.
```

**Causa**: o bucket tem versionamento habilitado
(`aws_s3_bucket_versioning` em `home-c2/infra-aws/main.tf`) e ainda
contém objetos/versões (o build do site publicado pelo `ci-cd-aws.yml`).
O recurso Terraform `aws_s3_bucket` não tem `force_destroy = true`
configurado, então o Terraform não esvazia o bucket sozinho antes de
tentar apagá-lo — e com versionamento ligado, um `aws s3 rm --recursive`
comum não basta (precisa apagar cada *version id*, não só a versão
"current").

**Como resolver** (nenhuma das opções foi executada ainda):

1. **Mais simples**: adicionar `force_destroy = true` ao
   `aws_s3_bucket.site` em `home-c2/infra-aws/main.tf`, dar
   `push`/`apply` uma vez (efeito nulo agora, já que o CloudFront já foi
   destruído — só prepara o bucket), depois rodar `destroy` de novo.
2. **Sem alterar o `.tf`**: esvaziar o bucket manualmente antes do
   destroy — via GitHub Actions (não local), um step que rode algo como:
   ```bash
   aws s3api list-object-versions --bucket home-c2-aws-site-397685870114 \
     --query '{Objects: Versions[].{Key:Key,VersionId:VersionId}}' --output json \
     | aws s3api delete-objects --bucket home-c2-aws-site-397685870114 --delete file:///dev/stdin
   # repetir pra DeleteMarkers também
   ```
   e só então `terraform destroy`.

Qualquer uma das duas via `workflow_dispatch` do `infra-aws.yml` (mesmo
padrão já usado) — nunca AWS CLI local.

## O que ficou pronto pra próxima vez

- `preparacao-conquista-bff` e `preparacao-conquista-bff-contract` agora
  têm capacidade de destroy reutilizável via CI, permanente (não foi um
  workflow descartável) — útil se precisar subir e derrubar de novo no
  futuro.
- Nenhum segredo (Secrets Manager, GitHub Secrets) foi removido — só
  infraestrutura de compute/rede. Os secrets
  `preparacao-conquista-bff-oauth-clients`,
  `preparacao-conquista-bff-jwt-signing-key` e o `tv-b1189-secret-us-east-1-hom`
  compartilhado continuam no AWS Secrets Manager (não foram destruídos
  pelo Terraform — `lifecycle.ignore_changes` neles, ver
  `preparacao-conquista-bff-contract/infra-aws/README.md`).
