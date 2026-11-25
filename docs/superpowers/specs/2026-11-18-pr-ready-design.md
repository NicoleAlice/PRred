# pr-ready — design

Data: 2026-11-18 · Autora: Nicole Danni · Nome provisório: `pr-ready`

Base: o método "Building review-ready PRs with an agent" (Nicole Danni, 2026-11-18), em versão genérica em [`docs/source/building-review-ready-prs.md`](../../source/building-review-ready-prs.md). Ele é a fonte do prompt de cold review, do checklist, do formato da descrição e das armadilhas genéricas. O builder copia o conteúdo dali, sem reinventar.

**Restrição dura:** nada do repositório do empregador da autora entra no projeto. Isso inclui nomes de projeto, arquivos, comandos, tickets, números de PR, incidentes e configurações de ambiente. Exemplos, perfis e casos de teste são inventados do zero.

Marcações: **(decisão minha)** indica uma escolha que fiz e que a autora pode corrigir.

## 1. Intenção e porquê

Agentes de código produzem PRs grandes, mal explicadas e não validadas, e o custo de preparar a revisão passa para quem revisa. Pesquisas de 2026 (Linux Foundation; arXiv 2610.11179, 2610.21144) mostram que os revisores não rejeitam código por ser de IA, e sim mudanças amplas, sem explicação e sem prova.

`pr-ready` é um conjunto de skills que leva um dev do ticket até uma PR pronta para revisão, **transformando cada afirmação em evidência antes que um revisor abra a PR**. Os cinco hábitos do guia são o núcleo:

1. PRs pequenas e empilhadas (cerca de 500 linhas escritas à mão).
2. Plano antes do código, aprovado por uma pessoa.
3. Cada afirmação checada no código (`file:line` ou o comando que provou).
4. Testes que podem falhar (mutações e caminhos de ponta a ponta).
5. Cold review por um agente sem contexto antes de uma pessoa.

**Para quem:** qualquer dev, em qualquer projeto, independente de tracker (Jira, Linear, GitHub Issues, Azure Boards, nenhum) e de host (GitHub, GitLab, Bitbucket, Azure Repos, nenhum).

**Sucesso para a autora:** (a) devs de fora instalam e usam; (b) o projeto serve de vitrine do trabalho dela. Consequência: precisa de instalação fácil, valor no primeiro uso com uma peça só, README que mostra o método e evidência de que funciona (evals com antes e depois).

## 2. Objetivos, não objetivos e antiobjetivos

**Objetivos**
- Cada skill é útil sozinha e também encadeada pelo orquestrador.
- Funciona sem nenhum conector ou CLI de plataforma: na pior das hipóteses, produz texto para o dev colar.
- Respeita as regras do projeto-alvo acima das próprias.
- O rigor se ajusta ao risco da mudança.
- Provas de que funciona: evals por skill e um caso de antes e depois no README.

**Não objetivos**
- Revisar PRs de outras pessoas. Já existem `/code-review` e ferramentas como CodeRabbit. A cold review aqui é sobre a PR do próprio dev, antes de abrir.
- Substituir o CI ou ser um bot de CI.
- Fazer merge automático, aprovar ou dar push forçado.
- Gerenciar segredos ou credenciais de qualquer forma.

**Antiobjetivos** (é fracasso mesmo que funcione)
- Gerar mais texto e ruído para o revisor ler. Descrições longas, comentários óbvios, perguntas ao revisor.
- Afirmar algo como verificado sem ter visto a prova nesta sessão.
- Violar a política de IA ou de contribuição do projeto, por exemplo escrever a descrição da PR num projeto que proíbe isso.
- Fazer o dev entender menos a própria PR.
- Agir no remoto (abrir PR, push, mudar a base, disparar CI) sem confirmação explícita.

## 3. Restrições

- Formato aberto de Agent Skills (`SKILL.md` com frontmatter `name` e `description`, mais arquivos de referência e scripts). O Claude Code é o alvo principal. Outros agentes que leem `SKILL.md` devem funcionar com degradação: sem subagente, a cold review roda em contexto separado quando possível e, caso contrário, em uma segunda passada declarada como "não fria".
- Distribuição como plugin do Claude Code (marketplace num repositório git), com instalação manual (copiar a pasta `skills/`) documentada.
- Scripts sem dependências além de git e do Python ≥ 3.9 (só a biblioteca padrão; 3.9 porque é o que vem no macOS). Tudo precisa rodar em Windows, macOS e Linux.
- Repositório, skills e README em inglês. README em pt-BR opcional.
- Licença MIT (decisão minha).
- Nenhum dado real de cliente ou empresa. **(decisão minha)** O caso de antes e depois do README é **sintético**: um repositório de exemplo inventado, com falhas plantadas nas categorias do prompt de cold review (por exemplo, um comentário que contradiz o código, uma premissa de segurança falsa, um segredo exposto a um passo que não precisa dele, e uma configuração ausente que deixa um job verde sem testar nada). O plano inclui criar esse caso e rodá-lo com e sem a skill.

## 4. Abordagens consideradas

| | Abordagem | Troca | Decisão |
|---|---|---|---|
| A | Uma skill única, do ticket ao merge | Simples, mas tudo ou nada, gatilho vago e difícil de testar | Rejeitada |
| **B** | **Plugin com skills pequenas que funcionam juntas ou separadas, perfil compartilhado e scripts** | Mais trabalho e risco de contradição entre skills, mas adoção por partes, gatilhos claros, testável e boa vitrine | **Escolhida pela autora** |
| C | CLI com uma skill fina por cima | Roda no CI, mas investe no mecânico e esconde o diferencial (julgamento) | Rejeitada. Os scripts entram dentro de B. |

## 5. Arquitetura

```
pr-ready/
  .claude-plugin/plugin.json        # manifesto do plugin + marketplace.json
  skills/
    pr-setup/        SKILL.md        # cria/atualiza o perfil do projeto
    pr-plan/         SKILL.md        # lê ticket+código, propõe plano e divisão
    pr-prove/        SKILL.md        # evidência: CI local, mutações, ponta a ponta
    pr-cold-review/  SKILL.md        # revisão fria por subagente
    pr-write/        SKILL.md        # descrição da PR + checagem contra o diff
    pr-ready/        SKILL.md        # orquestrador: encadeia tudo com portões
    references/                      # compartilhado (ver 5.4)
    scripts/                         # checagens mecânicas (ver 5.5)
  examples/profiles/                 # perfis de exemplo inventados (ex.: Node+GitLab, Python sem CI, Go no Bitbucket)
  evals/                             # casos de teste por skill (ver 7)
  README.md
```

Os nomes são provisórios. A pasta compartilhada pode ser duplicada por skill se o formato de plugin exigir. Decisão do builder.

### 5.1 Perfil do projeto (`.pr-ready/profile.md` no repo-alvo)

Um arquivo Markdown com seções fixas e legíveis por humanos, criado por `pr-setup` e revisado pelo dev antes de ser salvo. Pode ir para o git e ser compartilhado com o time. As outras skills leem o perfil. Se ele não existir, cada skill funciona com detecção na hora e sugere rodar `pr-setup`.

Seções:
- **Platform**: host (detectado pelo remote e pelos CLIs `gh`, `glab`, `az`, `bb`), tracker (pelos conectores disponíveis, padrão de chave em branches e commits, ou "none") e ferramenta de stack (`gh stack`, Graphite, Sapling ou branches simples).
- **Project rules**: caminhos de `CONTRIBUTING.md`, template de PR, política de IA (`AI_POLICY*`, `AI*.md`, seções do CONTRIBUTING, `.github/`, `docs/`), formato de commit observado no histórico e regras do agente (`CLAUDE.md`, `AGENTS.md`, `.claude/rules/`). **(decisão minha)** A política de IA vira campos explícitos que o dev confirma no `pr-setup`, cada um com a citação do trecho de onde veio:
  - `ai_description`: `allowed` | `forbidden` | `unclear`
  - `ai_disclosure`: `none` | `required-in-description` | `required-in-trailer` | `forbidden-trailer` | `unclear`
  - `prior_approval`: `required` | `not-required` | `unclear` (issue ou discussão aprovada antes da PR)
  - Quando o valor é `unclear`, ou quando não há perfil, vale a opção segura: o `pr-write` entrega a lista de fatos, não a descrição pronta, e pergunta ao dev se e como declarar o uso de IA.
- **Base branch**: **(decisão minha)** o branch padrão do remote (`origin/HEAD`); senão, `main` ou `master`, o que existir; senão, o dev diz.
- **Commands**: como reproduzir o CI localmente (derivado dos arquivos de workflow), testes, build e checagens de arquivos gerados.
- **Generated files**: globs que não contam no orçamento de linhas e que precisam bater com o que o build gera.
- **Budget**: limite de linhas por PR (padrão 500, ajustável). **(decisão minha)** "Linhas escritas à mão" é igual a adicionadas mais removidas (`git diff --numstat` contra o merge-base), excluindo arquivos gerados (globs do perfil), lockfiles, binários e vendor. Testes **contam**, porque o revisor lê. Arquivo renomeado conta só as linhas alteradas (`-M`).
- **Risk paths**: globs que forçam o nível "arriscado" (auth, segredos, migrações, contrato público). **(decisão minha)** Sem perfil, vale uma lista padrão embutida no script (por exemplo `**/auth*/**`, `**/*secret*`, `**/migrations/**`, `**/*.sql`, workflows de CI, `openapi*`, `*.proto`, `Dockerfile`).
- **Known traps**: tabela no formato sintoma, causa e o que fazer (como no guia). As skills consultam essa tabela antes de diagnosticar uma falha.

### 5.2 Níveis de rigor

O nível é proposto pelo `pr-plan` ou, quando a skill roda sozinha, pelo script `classify_risk` a partir do diff, e é sempre confirmado pelo dev. **(decisão minha)** Regra do script: qualquer arquivo em risk paths leva a "arriscado"; só docs, comentários ou arquivos não executáveis (`*.md`, `*.txt`, imagens), ou diff com 10 linhas ou menos sem mudança de lógica detectável, leva a "trivial"; o resto é "normal". O agente pode propor subir o nível, nunca baixar sem o dev.

| Nível | Quando | O que roda |
|---|---|---|
| Trivial | Docs, typo, config sem efeito em comportamento | Leitura do diff, `pr-write` curto, sem mutação e sem cold review |
| Normal | Padrão | Tudo, com mutações nos testes novos e cold review |
| Arriscado | Toca risk paths, auth, autorização, segredos, entrada externa ou contrato público | Normal, mais ponta a ponta obrigatório, diff de contrato quando houver e um aviso explícito de que uma pessoa deve ler o trecho linha a linha |

### 5.3 Precedência de regras

1. Política de IA e de contribuição do projeto-alvo.
2. Regras do agente no repo (`CLAUDE.md`, `AGENTS.md`, `.claude/rules/`) e o perfil.
3. Regras de `pr-ready`.

Consequências concretas:
- Se o projeto proíbe descrição escrita por IA, `pr-write` não escreve a descrição. Ele produz uma lista de fatos verificados (o que mudou, comandos e contagens, mutações, ponto fraco) para o dev escrever com as próprias palavras.
- Se o projeto exige declarar o uso de IA, isso é incluído no lugar que ele pede (descrição ou trailer).
- A regra do guia "sem rodapé de gerado-por" vale só quando o projeto não diz nada.
- Se o projeto exige issue ou discussão aprovada antes da PR, `pr-plan` verifica e para se não houver.

### 5.4 Responsabilidade de cada skill

**`pr-setup`**: detecta a plataforma, as regras, os comandos e os arquivos gerados, e escreve um rascunho do perfil. Mostra ao dev e só salva com aprovação. Rodar de novo atualiza o perfil sem perder edições manuais (mescla por seção).

**`pr-plan`**: lê o ticket (pelo conector ou CLI disponível, ou colado pelo dev), os critérios de aceite, os arquivos afetados e um "irmão" que já faz algo parecido. Se os critérios forem fracos demais para construir em cima, ele para e diz o que falta. Checa se a `main` e as PRs abertas mudaram algo relevante. Propõe:
- a divisão em PRs, cada uma com cerca do orçamento de linhas, cortada onde um revisor poderia aprovar uma parte e rejeitar a próxima;
- o que cada PR prova;
- pontos fracos e alternativas rejeitadas;
- o nível de rigor;
- convenções novas que precisam ir para o time antes.

**Portão:** nenhum arquivo é alterado até o dev aprovar.

**`pr-prove`**:
- Reproduz o CI localmente pelo perfil, de preferência no commit de merge com a base, e registra o comando e as contagens.
- Confere se os arquivos gerados batem com o build (ignorando CR/LF).
- Roda mutações: o agente propõe N quebras que os testes novos deveriam pegar, aplica uma por vez, roda de novo e reverte. Se o projeto já tem uma ferramenta de mutação (Stryker, PIT, mutmut, cargo-mutants), usa a ferramenta. Mutantes sobreviventes viram achados.
- **Portão:** o dev confirma o que é "correto" quando um teste novo define comportamento. O agente não escolhe a asserção e depois confirma que o próprio código a satisfaz.
- Regra das duas falhas: se o mesmo teste falhar do mesmo jeito duas vezes, para e reformula ou pede para o dev ler o erro.
- Quando não há testes nem CI, declara o que não pôde provar. Isso alimenta o `pr-write` como "evidência ausente", nunca como "passou".
- Produz um registro de evidência (ver 5.6).

**`pr-cold-review`**: dispara um subagente sem a conversa, só com a worktree, os arquivos de contexto e a regra que a mudança precisa manter, sem as conclusões do agente principal. Usa o prompt do guia, generalizado (categorias 1 a 6, "no finding" por categoria, evidência `file:line`). O agente principal verifica cada achado no código antes de agir, e depois roda de novo os testes e as mutações. Se a plataforma não tiver subagentes, faz uma segunda passada declarada como não fria.

**`pr-write`**: escreve a descrição seguindo, nesta ordem, o template do projeto, se houver, e depois o formato do guia: título no formato de commit, link do ticket, What, Why, Impact, Focus (o ponto mais fraco e o que foi checado), Out of Scope (só lacunas que pareceriam bug) e Tests (só a evidência do registro). Regras:
- Nenhum número de teste que não esteja no registro desta sessão.
- Nenhuma pergunta ao revisor.
- Uma linha por parágrafo.
- Checagem da descrição contra o diff final antes de entregar.
- Também roda o "teste de compreensão": aponta de 3 a 5 trechos do diff que um revisor provavelmente questionaria e pede que o dev explique cada um com as próprias palavras. Se o dev não souber explicar, o trecho volta para revisão ou vira o Focus. Isso é opcional e pode ser pulado, mas sempre é oferecido.
- Salva a descrição num arquivo, porque mudar a base de uma PR pode apagar a descrição.

**Portão:** abrir a PR (sempre como rascunho, quando o host permite) só com confirmação. Sem CLI ou conector, entrega o texto.

**`pr-ready`** (orquestrador): mostra o checklist do guia, generalizado, com o estado de cada item, e chama as skills na ordem, respeitando os portões e o nível de rigor. Retoma de onde parou lendo o registro de evidência.

### 5.5 Scripts (checagens mecânicas)

O agente roda os scripts e lê a saída. Ele não refaz essas contas de memória.
- `count_lines`: linhas escritas à mão no diff contra a base, excluindo os globs de arquivos gerados do perfil. Saída: total e por arquivo.
- `compare_generated`: compara o arquivo commitado com o gerado, ignorando CR/LF.
- `warning_delta`: compara a contagem de warnings únicos com a base, a partir de dois logs de build passados como argumento.
- `detect_platform`: remote, CLIs instalados, arquivos de política e template, e workflows de CI. Saída em JSON para o `pr-setup`.
- `classify_risk`: aplica a regra de 5.2 ao diff e devolve o nível sugerido com os arquivos que o justificam.

### 5.6 Registro de evidência (`.pr-ready/evidence/<branch>.md`, fora do git por padrão)

É anexado a cada passo e contém:
- comandos rodados, com código de saída e contagens;
- mutações, com o que quebrou e o que sobreviveu;
- achados da cold review e o que foi feito com cada um;
- itens marcados como não verificados.

O `pr-write` e o `pr-ready` leem esse arquivo. É o que garante "só números vistos nesta sessão" e permite retomar o trabalho.

**(decisão minha)** Toda skill escreve no registro, mesmo rodando sozinha. Cada entrada leva data e hora e o SHA do `HEAD` (e o da base) em que foi produzida. O nome do arquivo usa branch mais o caminho da worktree (hash curto), então duas worktrees não se misturam. Ao ler, entradas com `HEAD` diferente do atual são tratadas como **vencidas**: o `pr-write` não as usa como evidência e o `pr-ready` marca esses itens para rodar de novo.

### 5.7 Adaptadores de plataforma

Não são código: são instruções por plataforma em `references/platforms/*.md` (github, gitlab, bitbucket, azure-devops, none), com os comandos para buscar o ticket, abrir a PR como rascunho, atualizar a branch e mexer em stacks, e as armadilhas conhecidas de cada uma. Por exemplo, no GitHub: PR com base em outra branch não roda CI, mudar a base pode apagar a descrição e a exclusão automática de branches é o que move a base. Trackers usam o conector MCP disponível. Sem conector, o dev cola o ticket.

### 5.8 Portões humanos (fixos, valem em todas as skills)

- Aprovar o plano antes de qualquer edição.
- Definir o que é "correto" nos testes de comportamento novo.
- Leitura humana, linha a linha, de auth, autorização, segredos e entrada externa (a skill avisa e lista os trechos).
- Qualquer ação no remoto: push, abrir PR, mudar a base, atualizar a branch, disparar CI.
- Nunca: ler, escrever ou rodar credenciais; chamar ambientes implantados; fechar e reabrir PR; push forçado em branch já revisada; colocar dados reais de cliente em testes, prompts ou PR.

## 6. Escopo da v1 (decisão minha)

**v1:** `pr-setup`, `pr-plan`, `pr-prove`, `pr-cold-review`, `pr-write`, `pr-ready`, os scripts, os adaptadores github, gitlab e none, um perfil de exemplo, as evals e o README com o caso de antes e depois.

**Stacks na v1 (decisão minha):** o `pr-plan` divide o trabalho em PRs ordenadas, e a v1 constrói **uma PR por vez**, criando cada branch a partir da anterior com git puro. Isso funciona igual em qualquer host, e sem host nenhum. Nada no fluxo de stack pressupõe GitHub: o comportamento de cada host (CI em PR com base em outra branch, retarget automático, edição de base) vem do adaptador da plataforma, e o adaptador `none` entrega a ordem de merge e as bases em texto. Abrir cada PR com a base certa usa o adaptador da plataforma, com confirmação. Integração com ferramentas de stack (`gh stack`, Graphite, Sapling) fica para depois. O `pr-setup` só detecta e registra essas ferramentas.

**Depois:** `pr-address-review` (verificar cada comentário de revisão no código, corrigir, provar de novo e atualizar a descrição), mecânica guiada de merge de stack, e os adaptadores bitbucket e azure-devops. O design já reserva lugar para eles (o registro de evidência e os adaptadores servem para todos).

## 7. Como provar que funciona (evals)

Para cada skill, de 3 a 5 casos em repositórios de exemplo pequenos, criados para isso, com uma rubrica objetiva. Exemplos:
- `pr-plan` com uma mudança de cerca de 1.500 linhas: divide em PRs de no máximo cerca de 500 linhas com cortes defensáveis?
- `pr-prove` com um teste que não assere nada: alguma mutação sobrevive e vira achado?
- `pr-cold-review` com um comentário falso plantado: ele encontra?
- `pr-write` num repo cuja política proíbe descrição por IA: ele não escreve a descrição?
- `pr-write` sem registro de evidência: ele não inventa contagens?

Cada caso roda com e sem a skill, e o README publica a comparação. **(decisão minha)** São 3 execuções por caso, e o caso passa quando a rubrica passa em pelo menos 2 das 3. O README mostra a taxa de acerto com e sem a skill. As evals rodam manualmente antes de cada release, não no CI, na v1. Também entram evals de disparo: frases que devem e que não devem ativar cada skill. A ferramenta de eval é decisão do builder (por exemplo, o fluxo do `skill-creator` ou `claude plugin eval`).

## 8. O que fica para o builder

- Linguagem dos scripts (Python só com a biblioteca padrão, ou shell mais PowerShell).
- Layout exato do plugin e onde ficam as referências compartilhadas.
- Texto das `description` de cada skill (gatilhos), validado pelas evals de disparo.
- Formato exato do registro de evidência, desde que cubra o que está em 5.6.
- Ferramenta de eval e repositórios de exemplo.
- Nome final do projeto.
