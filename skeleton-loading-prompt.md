# Prompt — Skeleton Loading (Home + Pipeline) no home-c2

Prompt pronto pra colar numa IA que vá implementar diretamente no código
do projeto Angular `home-c2` (não Figma). Adaptado a partir de um pedido
original de design em Figma, traduzido pra código real com base nos
componentes/arquivos que já existem no projeto.

## Contexto de quem for usar este prompt

- Repositório: `home-c2` (Angular 18, standalone components).
- Descoberta importante ao adaptar: **não existe** cabeçalho com
  avatar/busca/notificações neste projeto — a Home roda dentro de um
  `<iframe>` embutido num LWC no Lightning (`homeC2Embed`), sem esse
  chrome. O prompt abaixo já reflete isso (não pede pra criar esse
  cabeçalho).
- `tela-00.component.ts` já tem duas flags de carregamento reais, hoje
  sem nenhuma representação visual além do texto "Carregando...":
  `loading` (carregamento inicial) e `carregandoPipeline` (troca de
  filtro Em atraso/Hoje/Próximos 7 dias).

## O prompt

```
Crie estados de carregamento com Skeleton Loading para as telas Home e
Pipeline do projeto home-c2 (Angular 18, standalone components).

Use os componentes e templates REAIS já existentes como fonte visual e
estrutural. Não redesenhe a aplicação, não altere a identidade visual e
não modifique o comportamento ou o markup dos componentes oficiais
existentes — apenas ADICIONE os novos componentes de skeleton ao lado
deles.

CONTEXTO REAL DO PROJETO (não inventar nada fora disso)

- src/app/pages/tela-00/tela-00.component.ts já tem duas flags de
  carregamento:
  - `loading` (true no boot, até usuário + pipeline info carregarem) —
    hoje só renderiza `<p class="tela-00__status">Carregando...</p>` e
    esconde TODO o resto da tela (`*ngIf="!loading && !loadError"`).
  - `carregandoPipeline` (true ao trocar de filtro — Em atraso/Hoje/
    Próximos 7 dias) — hoje não tem nenhuma representação visual.
- Não existe cabeçalho com avatar/busca/notificações neste projeto — a
  Home roda dentro de um <iframe> embutido no Lightning (LWC
  homeC2Embed), sem esse chrome. NÃO crie esse cabeçalho.
- Componentes reais a espelhar (classes CSS BEM exatas, reaproveitar o
  SCSS existente de cada um como referência de dimensão/espaçamento):
  - tela-00.component.html: `.tela-00__day`, `.tela-00__date`,
    `.tela-00__message`, `.tela-00__section-title`,
    `.tela-00__quick-actions-grid`, `.tela-00__tabs`, `.tela-00__tab`,
    `.tela-00__tabs-line`.
  - quick-action-card.component.html: `.quick-action-card__badge`
    (círculo), `.quick-action-card__count`, `.quick-action-card__label`.
  - pipeline-stage.component.html: `.pipeline-stage__header`,
    `.pipeline-stage__title`, `.pipeline-stage__badge` (círculo),
    `.pipeline-stage__count`, `.pipeline-stage__chevron`.
  - company-card.component.html: `.company-card__name`,
    `.company-card__cnpj`, `.company-card__datetime`,
    `.company-card__action-btn`, `.company-card__chevron`.
  - filter-chip.component.html: `.filter-chip`.

OBJETIVO

Criar dois novos componentes standalone:

1. `SkeletonHomeComponent` (src/app/components/skeleton-home/) —
   substitui o texto "Carregando..." durante `loading=true` em tela-00.
2. `SkeletonPipelineComponent` (src/app/components/skeleton-pipeline/) —
   exibido durante `carregandoPipeline=true`, no lugar da lista de
   `<app-pipeline-stage>`, mantendo cabeçalho/saudação/ações rápidas/abas
   já carregados e visíveis por trás.

REGRAS GERAIS

- Não altere nenhum arquivo de componente oficial existente (tela-00,
  quick-action-card, pipeline-stage, company-card, filter-chip) além do
  mínimo necessário em tela-00.component.html/ts para: (a) trocar
  `*ngIf="loading"` pra renderizar `<app-skeleton-home>` em vez do texto
  "Carregando...", e (b) renderizar `<app-skeleton-pipeline>` quando
  `carregandoPipeline` for true, sem remover a lógica/estrutura existente.
- Preserve exatamente: dimensões dos cards/frames existentes, cores da
  aplicação, espaçamentos, margens, grid, cantos arredondados, tipografia
  Inter (já global em styles.scss), estrutura visual das telas reais.
- Não use spinner central bloqueando a interface inteira.
- Skeleton contextual, só nas áreas cujo conteúdo depende da API
  (usuário, pipeline) — nunca em elementos estáticos.
- Os placeholders devem antecipar a estrutura e o tamanho aproximado do
  conteúdo real (mesma largura/altura dos elementos que substituem).
- Não exiba textos falsos dentro dos skeletons.
- Não desloque nenhum elemento na transição entre skeleton e conteúdo
  real carregado — mesmas dimensões/posições.
- Tons: skeleton principal `#D4DEE0`, skeleton secundário `#E4ECEE`,
  cartões `#FFFFFF`, fundo da página mantém o oficial (`#edf4f4`, ver
  styles.scss).
- Cantos arredondados entre 6px e 18px, acompanhando o elemento real
  representado (círculo pro badge, retângulo arredondado pro card).
- Resultado moderno, limpo, discreto, condizente com o restante da UI.

COMPONENTE 1 — SkeletonHomeComponent

Estrutura (mesmo grid/espaçamento de tela-00.component.html):

- `.skeleton-home__greeting-card` — mesmas dimensões/arredondamento do
  card branco de saudação real.
  - `.skeleton-home__date` — barra de skeleton no lugar de
    `{{ greeting.day }}` + `{{ greeting.date }}`.
  - `.skeleton-home__message` — barra menor no lugar de
    `{{ greeting.message }}`.
- `.skeleton-home__section-title` — barra curta no lugar de "Ações
  rápidas".
- `.skeleton-home__quick-actions` — MESMA quantidade, tamanho e posição
  dos `<app-quick-action-card>` reais (hoje são 2: Oportunidades, Agenda
  SDR). Cada item:
  - `.skeleton-home__badge` — círculo (mesma dimensão do
    `.quick-action-card__badge`).
  - `.skeleton-home__action-label` — barra horizontal.
- `.skeleton-home__tabs` — duas barras curtas no lugar de "Pipeline" /
  "Agenda", preservando `.tela-00__tabs-line` (divisor) real por baixo.

COMPONENTE 2 — SkeletonPipelineComponent

Estrutura (mesmo grid/espaçamento da seção Pipeline em
tela-00.component.html):

- `.skeleton-pipeline__description` — barra horizontal no lugar de
  `{{ pipelineDescription }}`.
- `.skeleton-pipeline__filters`:
  - `.skeleton-pipeline__filter-title` — barra no lugar de "Filtrar
    período".
  - 3x `.skeleton-pipeline__filter` (mesma dimensão de `.filter-chip`) —
    cada um com `.skeleton-pipeline__filter-label` (barra menor dentro).
  - `.skeleton-pipeline__help` — barra curta alinhada à direita, no
    lugar de "Sobre o Pipeline".
- Repita 3x `.skeleton-pipeline__stage` (mesmo card branco externo,
  dimensões e arredondamento de `.pipeline-stage`):
  - `.skeleton-pipeline__stage-title` — barra no lugar do nome da etapa.
  - `.skeleton-pipeline__stage-count` — círculo no lugar do badge de
    contagem.
  - `.skeleton-pipeline__stage-chevron` — espaço reservado (sem ícone
    real).
  - Dentro do primeiro (representando o grupo expandido), 3x
    `.skeleton-pipeline__card` (mesmo espaçamento vertical de
    `.company-card`):
    - `.skeleton-pipeline__card-name` — barra (nome da empresa).
    - `.skeleton-pipeline__card-cnpj` — barra menor (CNPJ).
    - `.skeleton-pipeline__card-datetime` — barra (data/hora).
    - `.skeleton-pipeline__card-action` — bloco branco (botão de ação).
  - `.skeleton-pipeline__pagination` — barra discreta.

ESTRUTURA E IMPLEMENTAÇÃO

- Angular standalone component, cada um com seu próprio .ts/.html/.scss,
  seguindo o mesmo padrão dos componentes existentes (ex.
  quick-action-card).
- Um partial SCSS reutilizável (ex. `_skeleton.scss` ou mixin) para o
  retângulo/círculo base de skeleton, evitando duplicar o mesmo bloco de
  CSS nos dois componentes — mas sem criar nenhum estilo global que
  afete componentes existentes.
- Elementos editáveis/normais do DOM — nada de imagem estática.
- Reaproveite as classes BEM dos componentes reais como referência de
  medida, mas com prefixo `skeleton-` pra não colidir com os estilos
  oficiais.

ANIMAÇÃO OPCIONAL (shimmer)

Se fizer sentido, aplique um efeito shimmer horizontal discreto via CSS
puro (`@keyframes` + `background: linear-gradient(...)`), duração entre
1.2s e 1.8s, contínuo, sem pulsação forte. Se não quiser implementar
agora, deixe o skeleton estático (nunca um spinner).

VALIDAÇÃO FINAL

- tela-00.component.ts/html/scss e todos os componentes filhos
  (quick-action-card, pipeline-stage, company-card, filter-chip)
  continuam funcionando exatamente como antes quando `loading=false` e
  `carregandoPipeline=false`.
- `ng build --configuration=aws` compila sem erros.
- Nenhum skeleton ultrapassa os limites do card/seção que representa.
- Não existem textos falsos nem elementos sobrepostos.
- O conteúdo real, ao carregar, substitui o skeleton sem deslocar nada
  na tela (mesmas dimensões).
```

## Origem

Adaptado a partir de um prompt original escrito para Figma (duplicar
frames oficiais, nomear camadas `Skeleton / ...`, etc.) — a versão acima
troca "frame"/"camada" por "componente Angular"/"classe CSS", e troca
todas as referências de UI genéricas pelas que realmente existem no
código do `home-c2` nesta data.
