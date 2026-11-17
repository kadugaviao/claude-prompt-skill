# Mecânica de custo de tokens de uma skill no Claude Code (assinatura, nov/2026)

Convenções: cada item traz **[fato]**, **[inferência]** ou **[opinião]**. As páginas de docs de code.claude.com e platform.claude.com não mostram data de publicação. Todas foram acessadas em 12/11/2026, e o comportamento citado vale para o Claude Code v2.1.3xx, que é o usado nos evals (`claude_code_version: 2.1.322` no evento `init`; local `2.1.323`). "Dados locais" são números calculados por mim a partir de `evals/runs-*/raw/*.jsonl` e das transcrições em `evals/tmp/home/*/.claude/projects/`.

## 1. Como o Claude Code carrega uma skill (frontmatter x corpo, progressive disclosure, números)

### Takeaway
A `description` fica na listagem de skills em todo turno. O corpo do SKILL.md entra só na invocação, como **uma mensagem de usuário**, e fica no contexto pelo resto da sessão. Arquivos referenciados só custam tokens quando são lidos. A Anthropic recomenda SKILL.md com menos de 500 linhas e corpo com menos de ~5 mil tokens. Pelos dados locais, o corpo da `/prompt` v2.2 (10.984 caracteres injetados) fica em ~5 mil tokens, ou seja, no limite dessa recomendação.

### Cited Findings
- [fato] A `description` está "sempre no contexto" para o Claude saber que a skill existe. O corpo carrega só quando a skill é invocada (por `/nome` ou automaticamente). `description` + `when_to_use` são truncados em 1.536 caracteres na listagem. — [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [fato] Com `disable-model-invocation: true`, a descrição **não** entra no contexto, e a skill carrega só quando o usuário a chama. A doc diz que "every skill in the skill listing adds to your context on every turn, whether or not Claude ever uses it". `/skill-doctor` reporta o custo de contexto de cada skill. — [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [fato] Depois de invocado, o SKILL.md renderizado "enters the conversation as a single message and stays there across later turns". O Claude Code não relê o arquivo nos turnos seguintes. Se a skill for invocada de novo com o mesmo conteúdo, entra só uma nota "already loaded", sem segunda cópia. — [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [fato] Na auto-compactação, a invocação mais recente de cada skill é re-anexada, até os primeiros 5.000 tokens de cada uma, com orçamento conjunto de 25.000 tokens. — [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [fato] "Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files." Arquivos de apoio referenciados no SKILL.md são lidos só quando necessário. Scripts em `scripts/` são executados, e só a saída entra no contexto. — [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [fato] A tabela de três níveis da Anthropic: metadados ~100 tokens por skill (sempre), corpo do SKILL.md "Under 5k tokens" (ao disparar), recursos sem custo até serem acessados. — [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [fato] Boas práticas de autoria: "Keep the SKILL.md body under 500 lines for optimal performance", dividir o conteúdo ao se aproximar desse limite, manter as referências **a um nível de profundidade** (referências aninhadas podem ser lidas parcialmente, com `head -100`) e pôr sumário em arquivos de referência com mais de 100 linhas. O "Pattern 2: Domain-specific organization" existe "to avoid loading irrelevant context". A dica é colocar workflows grandes em arquivos separados e "tell Claude to read the appropriate file based on the current task". A doc também mostra exemplo conciso (~50 tokens) contra prolixo (~150 tokens), com a pergunta "Does this paragraph justify its token cost?". — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [fato] Blog de engenharia (16/10/2025, Barry Zhang, Keith Lazuka e Mahesh Murag): "Progressive disclosure is the core design principle". "When the SKILL.md file becomes unwieldy, split its content into separate files and reference them". Para contextos mutuamente exclusivos, "keeping the paths separate will reduce the token usage". — [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [fato] Os docs de custos sugerem levar instruções de fluxos específicos do CLAUDE.md para skills, porque skills "load on-demand only when invoked". Meta: CLAUDE.md com menos de 200 linhas. — [Manage costs effectively](https://code.claude.com/docs/en/costs)
- [fato, dados locais] A `/prompt` já usa `disable-model-invocation: true` (`skills/prompt/SKILL.md`), então a descrição dela não custa nada por turno. Na transcrição de v22-17, a mensagem injetada começa com `Base directory for this skill: …` e tem 10.984 caracteres: o corpo sem frontmatter, com `$ARGUMENTS` substituído. O arquivo tem 11.452 bytes, 201 linhas e 1.825 palavras.
- [fato, dados locais] A seção "Tipos de tarefa" tem ~5.059 caracteres, **~46% do corpo**, e cada chamada usa só 1 dos 9 tipos. A segunda maior seção é "Formato da resposta" (~1.986 caracteres).

### Inferences
- [inferência] **Tokens do corpo da skill, medidos indiretamente.** Na rodada 3, v1 e v2 rodaram os mesmos 15 pedidos. A 1ª requisição tinha em média 19.925 tokens de entrada na v1 (corpo injetado de ~4.940 caracteres) e 22.444 na v2 (~10.540 caracteres). São +2.519 tokens para +~5.600 caracteres, ≈ **2,2 caracteres/token** (português com acentos, markdown e crases tokeniza mal). Aplicando essa taxa, o corpo da v2.2 ≈ **4.800–5.000 tokens**, e a seção "Tipos de tarefa" ≈ **2.200–2.300 tokens**. A estimativa é aproximada, porque descrição, pedido e fixture também variam. Sem chave de API não dá para chamar `count_tokens` e confirmar.
- [inferência] Como a `/prompt` é um fluxo de um tiro (`-p`, 1 a 4 requisições), o custo de "ficar no contexto nos turnos seguintes" pesa pouco. O que pesa é escrever o corpo no cache uma vez (ver seção 3). Numa sessão interativa longa, depois de `/prompt` o corpo segue sendo relido a cada turno, mas no preço de cache read.
- [inferência] Mover os 8 tipos não usados para `references/tipos/<tipo>.md`, com 1 leitura sob demanda, cortaria ~1.800–2.000 tokens escritos no cache por execução. Mas acrescenta uma chamada Read (+1 requisição que relê ~23 mil tokens de prefixo e gera tokens de tool call). A v1 já tinha o `tipos.md` separado, e a decisão D17 o fundiu no SKILL.md (ver `evals/results.md`). Separar de novo é uma troca entre custo e confiabilidade, a ser testada nos evals.

### Gaps
- Não encontrei número oficial de tokens por caractere para português, nem tokenizer público dos modelos 5.5. A taxa de 2,2 caracteres/token é empírica e local.
- A doc da skill listing não dá orçamento total da listagem (% da janela). Achei só o truncamento de 1.536 caracteres por skill.

## 2. Prompt caching no Claude Code (inclusive assinatura)

### Takeaway
O cache é automático, inclusive com login OAuth de assinatura. Dentro do uso do plano, a conversa principal (inclusive `-p`) recebe TTL de 1 hora. Skills entram como mensagens anexadas, então não invalidam o prefixo e passam a ser cacheadas a partir do turno em que entram. Entre sessões, o cache só é reaproveitado se o prefixo for idêntico (mesmo diretório, git status, modelo e versão do Claude Code). Por isso cada eval em fixture diferente reescreve ~11 mil tokens.

### Cited Findings
- [fato] "Claude Code handles prompt caching for you, unless you disable it". O cache é por prefixo exato, sem cache por arquivo ou segmento. A ordem das camadas é: system prompt (instruções + definições de ferramentas), contexto do projeto (CLAUDE.md, memória) e conversa. — [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching)
- [fato] Com chave de API ou assinatura Claude, o cache fica na infraestrutura da Anthropic. — [Prompt caching (Claude Code)](https://code.claude.com/docs/en/prompt-caching)
- [fato] "Skills and commands inject their instructions as user messages at the point of invocation. Nothing earlier in the conversation changes." Invocar uma skill está na lista de "Actions that keep the cache". Exceção: se o frontmatter define um `model` diferente do modelo da sessão, aquele turno é uma troca de modelo e relê a conversa inteira sem cache. — [Prompt caching (Claude Code)](https://code.claude.com/docs/en/prompt-caching)
- [fato] TTL: numa assinatura Claude, dentro do uso do plano, a "Main conversation" (turnos interativos, **execuções `-p` não interativas** e Agent SDK) usa **1 hora**. Subagentes, forks, compactação etc. usam 5 minutos. Com créditos de uso, chave de API ou nuvem, tudo usa 5 minutos. Dá para mudar com `promptCacheTtl` / `CLAUDE_CODE_PROMPT_CACHE_TTL` e `subagentPromptCacheTtl` (v2.1.242+). — [Prompt caching (Claude Code)](https://code.claude.com/docs/en/prompt-caching)
- [fato] Escopo: "the cache is effectively scoped to one machine and directory". O system prompt traz os caminhos da memória automática, e a conversa abre anunciando diretório, plataforma, shell e SO. Sessões sequenciais só compartilham o prefixo se o snapshot do git status for o mesmo. — [Prompt caching (Claude Code)](https://code.claude.com/docs/en/prompt-caching)
- [fato] Invalidam o cache: trocar de modelo, mudar o effort (exceto em Opus/Sonnet/Haiku 5.5 e Fable 5.1+, com API ou assinatura, onde o cache é mantido), ligar o fast mode, mudar o conjunto de ferramentas/MCP (com tool search ativa, o padrão, a lista de ferramentas fica congelada), compactar e atualizar o Claude Code. — [Prompt caching (Claude Code)](https://code.claude.com/docs/en/prompt-caching)
- [fato] Um subagente começa conversa própria e **não lê o cache do pai**. Um fork herda system prompt, ferramentas e histórico, e lê o cache do pai. — [Prompt caching (Claude Code)](https://code.claude.com/docs/en/prompt-caching)
- [fato] Preços de lista do Opus 5.5 por milhão de tokens: entrada US$ 4; escrita de cache 5m US$ 5 (1,25x); escrita 1h US$ 8 (2x); leitura de cache US$ 0,20 (**0,05x**, metade do multiplicador padrão de 0,1x); saída US$ 20. Sonnet 5.5: 2 / 2,50 / 4 / 0,10 / 10. Haiku 5.5 (≤100 mil tokens): 0,10 / 0,125 / 0,20 / 0,01 / 0,50. — [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [fato] Para assinantes, a cifra de custo do `/usage` "isn't relevant for billing purposes". O Claude Code calcula esse valor localmente, a preço de lista. Numa sessão longa, o histórico é relido "at the cached token rate, so a one-line question in a session that has been open all day still draws usage". Cache reads, portanto, contam para os limites do plano. O `/usage` da assinatura mostra a atribuição de uso a skills, subagentes e MCP, e uma linha `Prompt cache (main)` (v2.1.251+). — [Manage costs effectively](https://code.claude.com/docs/en/costs)
- [fato, dados locais] Os ajustes de mínimos quadrados sobre `total_cost_usd` de todas as execuções locais dão exatamente US$ 8/M (escrita 1h), US$ 0,20/M (leitura) e US$ 20/M (saída), com erro máximo de 2e-6. Isso confirma que o `claude -p` calcula o custo a preço de lista (`costBasis: "list"`) e que **todas as escritas de cache foram de 1h** (`ephemeral_1h_input_tokens`, nenhuma de 5m).
- [fato, dados locais] Na 1ª requisição de cada execução v2.2, ~11.370 tokens vêm do cache (leitura) e ~11.100 são escritos (ex.: v22-17: 11.382 lidos e 11.249 escritos). Em v22-19, foram 13.259 lidos e 9.364 escritos.

### Inferences
- [inferência] Os ~11,4 mil tokens lidos do cache já na 1ª requisição são o trecho estável do system prompt + definições de ferramentas, reaproveitado entre execuções em menos de 1h, porque o HOME temporário e a versão são os mesmos. O restante (~11 mil) é reescrito em toda execução porque, depois desse ponto, entram o diretório da fixture, o git status, a listagem de skills/agentes e a mensagem com o corpo da skill. Como cada caso roda numa fixture diferente, nada disso se repete.
- [inferência] Para um usuário real que chama `/prompt` várias vezes no mesmo diretório e na mesma sessão, a 2ª chamada com conteúdo idêntico só ganha a nota "already loaded". Mas o `$ARGUMENTS` muda o conteúdo renderizado, então cada chamada injeta uma cópia nova (~5 mil tokens escritos e depois relidos). Em sessão longa, com várias chamadas, isso se acumula no contexto.
- [inferência] Na assinatura, o TTL de 1h dobra o preço da escrita (2x em vez de 1,25x). Para execuções curtas e isoladas como os evals, `CLAUDE_CODE_PROMPT_CACHE_TTL=5m` reduziria a escrita de US$ 8 para US$ 5/M (−37,5% na parcela de escrita, ~−25% no custo de lista da execução). Isso só faz sentido se o "custo" que importa for o equivalente em preço de lista ou o consumo do limite. Não está documentado se o limite do plano pondera a escrita de 1h de forma diferente da de 5m (ver Gaps).

### Gaps
- Não achei fonte primária dizendo **como** os limites de 5 horas e semanais da assinatura ponderam cada tipo de token (entrada, escrita 1h/5m, leitura, saída). A doc diz só que cache reads "still draw usage" e que o `/usage` mostra barras e atribuição. Não dá para converter US$ de lista em % do limite.
- O post "Lessons from building Claude Code: Prompt caching is everything" (citado pela doc) redireciona para claude.dev e não foi lido.

## 3. O que domina o custo de uma execução como esta (medição local)

### Takeaway
Numa execução v2.2 (US$ 0,143 de lista, média de 5 casos), **~66% é escrita de cache de 1h**, ~28% é saída (thinking ≈ 5%) e ~6% é leitura de cache. O corpo da skill (~5 mil tokens) responde por **~28–30% do custo** de cada execução. O "piso" do Claude Code (system prompt + 25 ferramentas + listagens) é de ~17,5 mil tokens e custa sobretudo pela parte reescrita a cada fixture.

### Cited Findings
- [fato, dados locais] Médias por execução, calculadas do evento `result` (`usage`, `total_cost_usd`) dos JSONL:

| Grupo | n | Requisições/exec. | Escrita cache | Leitura cache | Saída (thinking) | Custo médio | Escrita / leitura / saída (% do custo) |
|---|---|---|---|---|---|---|---|
| runs/v2.2-validation | 5 | 2,4 | 11.902 | 43.678 | 1.973 (330) | US$ 0,1434 | 66% / 6% / 28% (thinking 5%) |
| runs/v2.0-validation (v2) | 4 | 2,8 | 10.286 | 53.306 | 2.181 (625) | US$ 0,1366 | 60% / 8% / 32% (thinking 9%) |
| runs/v1-vs-v2.0-round3 (v2) | 15 | 2,9 | 8.796 | 57.830 | 1.758 (405) | US$ 0,1171 | 60% / 10% / 30% (thinking 7%) |

  Os tokens de entrada sem cache são desprezíveis (2 a 6 por execução).
- [fato, dados locais] 1ª requisição: em média 22.444 tokens de entrada (rodada 3, v2), 22.563 (v2.2) e 19.925 (v1, corpo menor). Pelo evento `init`, o contexto base tem 25 ferramentas, 20 skills listadas, 5 agentes, 54 slash commands e 0 servidores MCP.
- [fato, dados locais] Leituras de arquivo nos evals são pequenas: resultados de ferramenta de 132 a 1.846 caracteres (ex.: v22-12: 631 + 1.432 + 132). Depois da 1ª requisição, cada requisição escreve só 363–1.504 tokens novos.
- [fato] O custo das ferramentas MCP é diferido por padrão (tool search): só nomes e instruções entram no contexto até o uso. `/context` mostra o que ocupa espaço. — [Manage costs effectively](https://code.claude.com/docs/en/costs)
- [fato] "Token costs scale with context size". Cada uso de ferramenta gera mais uma requisição que carrega o histórico inteiro. — [Manage costs effectively](https://code.claude.com/docs/en/costs)

### Inferences
- [inferência] **Parcela do corpo da skill:** ~5 mil tokens × US$ 8/M = ~US$ 0,040 de escrita, mais ~1,4 releitura × 5 mil × US$ 0,20/M ≈ US$ 0,0014. Total ≈ **US$ 0,041 de US$ 0,143 (~29%)**. A seção "Tipos de tarefa" sozinha custa ≈ US$ 0,018 por execução (~13%), dos quais ~8/9 servem a tipos não usados.
- [inferência] **Piso do Claude Code:** 22,5 mil − ~5 mil da skill ≈ ~17,5 mil tokens (system prompt, ferramentas, listagens, ambiente, pedido). O autor da skill não controla esse piso. Dele, ~11,4 mil saem do cache de outra execução, e ~6 mil (ambiente/listagens) são escritos a US$ 8/M (≈ US$ 0,05).
- [inferência] **Saída:** ~2 mil tokens por execução (≈ US$ 0,04). O prompt gerado é a entrega da skill, então a margem de corte está em tetos de linhas e em evitar enchimento (já medido como "Enchimento" em `results.md`). Thinking é pequeno (170–625 tokens), coerente com effort `medium` (ver seção 5).
- [inferência] **Requisições:** cada leitura extra (passo "Colete contexto, no máximo 3 leituras") custa ~1 requisição, que relê ~23 mil tokens (≈ US$ 0,0046) e escreve o resultado da ferramenta. Esse limite de 3 leituras já é uma alavanca de custo eficaz.
- [opinião] Para baixar o custo, a ordem de alavancas para esta skill é: (1) encolher o corpo, sobretudo "Tipos de tarefa"; (2) modelo/effort do turno (seção 4); (3) tetos de saída. Leituras de arquivo pesam pouco aqui.

### Gaps
- Não achei número público e oficial do tamanho do system prompt nem das definições de ferramentas do Claude Code 2.1.3xx. A doc só manda usar `/context`. Os ~17,5 mil tokens acima são inferência dos dados locais, e rodar `/context` numa sessão interativa confirmaria a divisão.
- O `stream-json` não separa, dentro de `cache_creation_input_tokens`, quanto é skill e quanto é ambiente. A divisão acima vem da comparação v1 × v2.

## 4. Opções de frontmatter e mecanismos que mudam o custo

### Takeaway
Em nov/2026, o frontmatter da skill aceita `model`, `effort`, `context: fork` + `agent`, `allowed-tools`, `disallowed-tools`, `disable-model-invocation`, `user-invocable` e `paths`. Para a `/prompt`, as alavancas reais são `model` e `effort`. `context: fork` isola o contexto, mas perde o histórico e não lê o cache do pai. `allowed-tools` só dispensa pedidos de permissão e não economiza tokens.

### Cited Findings
- [fato] `model`: o modelo vale "for the current turn only". Aceita valores do `/model` ou `inherit`. Com `context: fork`, define o modelo do subagente. `effort` (`low` a `max`): vale para o turno atual ou, com fork, para o subagente. `CLAUDE_CODE_EFFORT_LEVEL` sobrepõe o `effort` do frontmatter. — [Claude Code: Skills](https://code.claude.com/docs/en/skills); [Model config](https://code.claude.com/docs/en/model-config)
- [fato] `model` diferente do modelo da sessão = troca de modelo naquele turno. "The next request reads the entire conversation history with no cache hits. The session model resumes on your next prompt." — [Prompt caching (Claude Code)](https://code.claude.com/docs/en/prompt-caching)
- [fato] `context: fork` + `agent` (ex.: `Explore`, `Plan`, `general-purpose` ou agente próprio): o subagente recebe o conteúdo renderizado da skill como prompt e **não** recebe o histórico da conversa. Carrega o CLAUDE.md conforme o tipo de agente (Explore e Plan começam sem CLAUDE.md nem git status). Devolve um resumo ao contexto principal. `background` é `true` por padrão, mas em `-p` sempre espera. — [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [fato] O subagente não lê o cache do pai e usa TTL de 5 minutos mesmo na assinatura. — [Prompt caching (Claude Code)](https://code.claude.com/docs/en/prompt-caching)
- [fato] `allowed-tools`: ferramentas usáveis "without asking during the invoking turn. Does not restrict other tools". A permissão expira na mensagem seguinte. `disallowed-tools`: remove ferramentas do pool enquanto a skill está ativa. — [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [fato] Um deny de ferramenta inteira só muda as definições enviadas (e invalida o cache) quando a tool search está desligada. Com a tool search padrão, o prefixo se mantém. — [Prompt caching (Claude Code)](https://code.claude.com/docs/en/prompt-caching)
- [fato] Injeção dinâmica `` !`comando` ``: roda antes de enviar a skill, e a saída substitui o placeholder. Saídas longas viram caminho de arquivo + prévia. — [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [fato] Fora do Claude Code (claude.ai, Skills API), só `name`, `description`, `license`, `compatibility`, `metadata` e `allowed-tools` são aceitos. Os demais causam erro no upload. — [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [fato] Docs de custos: Sonnet "handles most coding tasks well and costs less than Opus". Para subagentes simples, `model: haiku`. Subagentes servem para isolar saídas volumosas, mas "still draw on your usage". — [Manage costs effectively](https://code.claude.com/docs/en/costs)
- [fato] Na assinatura, "You've hit your Opus limit" é um limite específico da família, e trocar para outra família com `/model` permite continuar. Os limites de sessão e semanal são compartilhados entre modelos. — [Manage costs effectively](https://code.claude.com/docs/en/costs)

### Inferences
- [inferência] `model: sonnet` na `/prompt`: a preço de lista, Sonnet 5.5 custa metade do Opus 5.5 em todas as categorias. Uma execução sairia por ~US$ 0,07 em vez de ~US$ 0,14. Em `-p` não há histórico anterior, então a "troca de modelo" não custa nada extra. Já numa sessão interativa longa, chamar `/prompt` com `model: sonnet` relê o histórico inteiro sem cache no Sonnet, e o próximo prompt volta ao Opus. Isso pode anular a economia em sessões longas. Exige reavaliar a qualidade nos evals (a doc de boas práticas manda testar com cada modelo).
- [inferência] `model: haiku` (Haiku 5.5 a 1/40 do preço do Opus) teria o maior corte, mas o maior risco de qualidade numa tarefa de julgamento (classificar e escrever um prompt estruturado). Só vale se passar nos evals.
- [inferência] `context: fork` não serve bem à `/prompt`: o passo 6 (executar o prompt se o usuário aprovar) depende da conversa principal, e o fork não vê o histórico. Num uso isolado também não economiza, porque o subagente paga o próprio system prompt e reescreve tudo no cache (TTL de 5m, mais barato que 1h). A vantagem real é manter as ~5 mil tokens da skill **fora** do contexto principal numa sessão longa.
- [inferência] `disable-model-invocation: true` (já em uso) elimina o custo por turno da descrição em todas as sessões, inclusive as que não usam `/prompt`.
- [opinião] Mexer em `allowed-tools` não reduz tokens. Só reduz pedidos de permissão (e, em `-p`, comandos bloqueados que geram uma nova tentativa, pendência 3 de `results.md`). Ainda assim, evitar uma nova tentativa poupa uma requisição.

### Gaps
- A doc não diz se `context: fork` com `agent: Explore`/`Plan` tem system prompt menor que o da sessão principal, nem quanto menor.
- Não há dado público de qualidade da `/prompt` com Sonnet ou Haiku. Isso precisa de eval local.

## 5. Effort / extended thinking: efeito em tokens e qualidade

### Takeaway
No Opus 5.5, o thinking é adaptativo e não dá para desligá-lo. O effort controla quanto o modelo pensa, e o padrão é `medium`. **Achado crítico local:** o harness grava `effortLevel: "high"` no settings.json, mas a doc diz que o `effortLevel` de nível superior não vale para o Opus 5.5, e todas as transcrições registram `"effort":"medium"`. Os custos de US$ 0,12–0,16 por execução são, portanto, de effort **medium**, não high.

### Cited Findings
- [fato] Padrões: Fable 5.2, Opus 5.5, Sonnet 5.5 e Haiku 5.5 → `medium`. "A top-level `effortLevel` in user settings doesn't apply to Opus 5.5. That key is an older form, and it still applies to Opus 5, Fable 5.1, and earlier models." Os níveis por modelo vão em `modelSettings`. — [Model config](https://code.claude.com/docs/en/model-config)
- [fato] Ordem de resolução do effort: `CLAUDE_CODE_EFFORT_LEVEL` > nível escolhido na sessão (`/effort`, `/model`) > `--effort` > settings (`modelSettings`/`effortLevel`) > padrão do modelo. O `effort` do frontmatter da skill vale enquanto a skill roda e é sobreposto pela variável de ambiente. — [Model config](https://code.claude.com/docs/en/model-config)
- [fato] Recomendações: `low` para trocas rápidas e mudanças pequenas; `medium` (padrão dos 5.5) para "day-to-day engineering with a clear scope, or cost-sensitive work"; `high` quando verificação e casos de borda importam; `xhigh` para raciocínio mais profundo "at higher token spend"; `max` "may show diminishing returns and tends to overthink". Nos testes da Anthropic, Opus 5.5 em `medium` "matches or exceeds Opus 5 at `high`" em avaliações de código e trabalho de conhecimento. Em níveis mais altos, o modelo "tested more edge cases, verified more of the work". — [Model config](https://code.claude.com/docs/en/model-config)
- [fato] "Thinking tokens are billed as output tokens". Não dá para desligar o thinking no Opus/Sonnet/Haiku 5.5. `MAX_THINKING_TOKENS` só vale para modelos com orçamento fixo, e modelos adaptativos ignoram orçamentos diferentes de zero. — [Manage costs effectively](https://code.claude.com/docs/en/costs); [Model config](https://code.claude.com/docs/en/model-config)
- [fato] Mudar o effort no meio da sessão mantém o cache no Opus/Sonnet/Haiku 5.5 com API ou assinatura. Em outros modelos, invalida. — [Prompt caching (Claude Code)](https://code.claude.com/docs/en/prompt-caching)
- [fato] O `/usage` da assinatura pode recomendar mudanças de effort (ex.: "Switch from max to high effort · /effort high"), e a tecla `f` aplica. — [Manage costs effectively](https://code.claude.com/docs/en/costs)
- [fato, dados locais] `evals/run.py`, linha 35: `json.dump({'model': 'opus', 'effortLevel': 'high'}, …)`. As transcrições em `evals/tmp/home/{v1,v2,v21,v22}/.claude/projects/*/*.jsonl` têm 297 / 372 / 42 / 60 ocorrências de `"effort":"medium"` e **nenhuma** de `"high"`. O evento `init` traz `per_turn_effort_active: true`, mas não informa o nível.
- [fato, dados locais] Thinking por execução: 170–625 tokens (média de 330 em v2.2), ~5–9% do custo.

### Inferences
- [inferência] As afirmações "Opus com esforço alto" em `results.md` e no harness estão erradas para o Opus 5.5: as execuções aprovadas (v2 14/15, validação 4/4) rodaram em `medium`. Para testar `high` de fato, é preciso `--effort high`, `CLAUDE_CODE_EFFORT_LEVEL=high` ou `modelSettings` no settings.json. Para fixar o comportamento validado, vale pôr `effort: medium` no frontmatter da skill.
- [inferência] Se o usuário real usa `effortLevel: high` no próprio settings.json com Opus 5.5, ele também está em `medium` sem saber. Se usa `/effort high` (salvo por modelo), está em `high`, e o custo e o comportamento da `/prompt` vão diferir dos evals. Thinking em `high` deve crescer, e a doc não quantifica quanto.
- [inferência] `effort: low` no frontmatter cortaria parte dos ~330 tokens de thinking e talvez da saída. A economia máxima é limitada (thinking ≈ 5–9% do custo). O ganho maior, se houver, viria de menos leituras e verificações. Precisa de eval, porque a doc liga effort menor a menos verificação.

### Gaps
- A doc não publica tokens de thinking nem custo por nível de effort. O efeito de `low` ou `high` na `/prompt` só sai com eval local.
- Não está documentado se o nível de effort muda o peso dos tokens no limite da assinatura (presumo que não: só muda a quantidade de tokens gerados).
