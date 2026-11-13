# Abordagens de ML mais pesadas para baratear a skill `/prompt`: RAG de instruções, fine-tuning/destilação, roteamento/cascatas e otimização automática de prompt (estado em nov/2026)

Legenda: **[fato]** = afirmado pela fonte citada; **[inferência]** = conclusão minha a partir das fontes e do repositório; **[opinião]** = julgamento meu ou de terceiro, sem medição.
Contexto local: `v2/prompt/SKILL.md` tem 1.825 palavras. A seção "Tipos de tarefa" (linhas 116 ao fim, 9 subseções) tem cerca de 795 palavras e o resto tem 1.030 (contagem com `wc -w` em 2026-11-12). O harness `evals/rodar.py` executa `claude -p "/prompt <pedido>"` com `{'model': 'opus', 'effortLevel': 'high'}` e o token OAuth da assinatura (`~/.claude/.credentials.json`, `claudeAiOauth`). Ele registra `total_cost_usd`, um valor calculado localmente a preço de tabela. Há 15 casos em `casos.tsv` e 4 em `casos-validacao.tsv`.

## 1. RAG / recuperação de instruções ou de exemplos few-shot

### Takeaway
A versão local de "RAG" já vem pronta no Claude Code: arquivos de apoio da skill que o modelo só lê quando precisa (progressive disclosure). Ela não exige infraestrutura nem API key. Para esta skill, porém, o ganho em tokens é pequeno: tira cerca de 700 palavras de entrada, que já é barata e em grande parte cacheada, e acrescenta uma chamada de ferramenta. RAG vetorial de verdade, com MCP ou vector store, não se justifica para 9 seções fixas.

### Cited Findings
- [fato] O Claude Code aceita arquivos extras no diretório da skill para que "SKILL.md" fique com o essencial: "Large reference docs, API specifications, or example collections don't need to load into context every time the skill runs". Os arquivos são referenciados no SKILL.md e carregados "only when needed". Scripts em `scripts/` são executados, não carregados. Recomendação: "Keep SKILL.md under 500 lines" — [Claude Code docs, Skills](https://code.claude.com/docs/en/skills) (consultado em 2026-11-12)
- [fato] Só a descrição da skill fica sempre no contexto. O SKILL.md renderizado entra como uma mensagem quando a skill é invocada e "stays there across later turns" — [Claude Code docs, Skills](https://code.claude.com/docs/en/skills) (2026-11-12)
- [fato] A Anthropic recomenda tirar instruções específicas do CLAUDE.md e colocá-las em skills, porque "Skills load on-demand only when invoked" — [Claude Code docs, Manage costs](https://code.claude.com/docs/en/costs) (2026-11-12)
- [fato] As definições de ferramentas MCP ficam "deferred by default": só os nomes entram no contexto até o uso. A mesma página diz que ferramentas CLI continuam "more context-efficient than MCP servers" — [Claude Code docs, Manage costs](https://code.claude.com/docs/en/costs) (2026-11-12)
- [fato] RAG-MCP (arXiv, 6/mai/2025): recuperar só as ferramentas relevantes antes de chamar o LLM reduziu os tokens do prompt em "over 50%" e subiu a acurácia de seleção de ferramenta de 13,62% para 43,13% — [arXiv 2505.03275](https://arxiv.org/abs/2505.03275)
- [fato] Escolher exemplos in-context por similaridade (KATE, Liu et al., 17/jan/2021) trouxe ganhos de 41,9% no ToTTo e 45,5% no NQ sobre a seleção aleatória. O abstract não diz se os ganhos são relativos ou absolutos — [arXiv 2101.06804](https://arxiv.org/abs/2101.06804)
- [opinião de terceiros, sem metodologia verificável] Blogs falam em cerca de 30% menos tokens e 25% mais relevância com few-shot dinâmico. Também relatam casos em que a seleção dinâmica piora o resultado ("few-shot collapse") — [tianpan.co, 12/abr/2026](https://tianpan.co/blog/2026-04-12-dynamic-few-shot-retrieval-static-examples-accuracy). Não encontrei o paper primário dessas cifras.

### Inferences
- [inferência] Mapeamento direto: mover as 9 subseções de "Tipos de tarefa" para `tipos/<tipo>.md` e instruir no passo 1 a ler só o arquivo do tipo escolhido. A parte de tipos cairia de cerca de 795 para cerca de 90 palavras, uma redução de mais ou menos 38% do SKILL.md total. Isso é "RAG" por roteamento determinístico (classificação seguida de leitura de arquivo), sem embeddings, MCP ou vector store.
- [inferência] O efeito em dólar é pequeno. 700 palavras dão cerca de 1.000 tokens de entrada. No Opus 5.5, a US$4/MTok de entrada (US$0,20/MTok com cache hit), isso vale de US$0,0002 a US$0,004 por execução, contra US$0,14–0,16 medidos ([preços Anthropic](https://platform.claude.com/docs/en/about-claude/pricing), 2026-11-12). Em cada execução o custo vem principalmente de saída e thinking (US$20/MTok de saída). A leitura extra é mais um turno de ferramenta e reenvia o contexto, o que pode anular o ganho. Só medindo com `rodar.py`/`comparar_versoes.py` dá para saber.
- [inferência] Há risco de qualidade. Na regra de "Empate" (passo 1), o modelo precisa ver o outro tipo para "Acrescente os itens dele". Se só um arquivo for carregado, ele pode deixar de ler o segundo. Os critérios de `casos.md` deveriam acusar isso.
- [inferência] Few-shot dinâmico não se aplica bem hoje, porque a skill não tem banco de exemplos. Seria preciso criar um, e cada exemplo acrescentado aumenta a entrada em vez de reduzi-la.

### Gaps
- Não encontrei medição publicada de economia de tokens com progressive disclosure de skills no Claude Code. A documentação descreve o mecanismo sem números.
- Não verifiquei se a Anthropic publicou números para o "tool search" de MCP deferido.

## 2. Fine-tuning / destilação para um modelo menor

### Takeaway
Pela literatura, destilação pode cortar muito o custo de inferência (por exemplo, um T5 de 770M superando o PaLM de 540B). No cenário desta skill, porém, ela é inviável: o único Claude que aceita fine-tuning no Bedrock é o Claude 3 Haiku, já em fim de vida, e um modelo fine-tunado ou open-weight não roda como modelo de uma skill no Claude Code com assinatura. Tudo isso exige conta AWS ou GPUs, dados de treino e hospedagem própria.

### Cited Findings
- [fato] "Distilling step-by-step" (Hsieh et al., 3/mai/2023): um T5 de 770M fine-tunado com rationales supera um PaLM de 540B few-shot usando "80% of available data" em um benchmark, em 4 benchmarks de NLP no total — [arXiv 2305.02301](https://arxiv.org/abs/2305.02301)
- [fato] O fine-tuning do Claude 3 Haiku no Amazon Bedrock ficou GA em nov/2024, só em US West (Oregon), e só para texto — [AWS What's New, nov/2024](https://aws.amazon.com/about-aws/whats-new/2024/11/fine-tuning-anthropics-claude-3-haiku-amazon-bedrock); [Anthropic, anúncio GA](https://www.anthropic.com/news/fine-tune-claude-3-haiku-ga)
- [fato] A tabela atual de modelos com fine-tuning no Bedrock lista, da Anthropic, apenas "Claude 3 Haiku" (`anthropic.claude-3-haiku-20240307-v1:0:200k`, us-west-2). Os demais são Amazon Nova/Titan e Meta Llama 3.x — [AWS Bedrock User Guide, Supported models for fine-tuning](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-supported.html) (2026-11-12)
- [fato, verificação parcial] Um post do AWS ML Blog traz aviso de que o Claude 3 Haiku chegou ao fim de vida em 10/set/2026. Vi o aviso por meio do resultado de busca e não conferi na página oficial de ciclo de vida do Bedrock — [AWS ML Blog](https://aws.amazon.com/blogs/aws/fine-tuning-for-anthropics-claude-3-haiku-model-in-amazon-bedrock-is-now-generally-available)
- [fato, fonte secundária] Modelo customizado no Bedrock precisa de Provisioned Throughput para servir — [pieces.app](https://pieces.app/blog/claude-fine-tuning) (não verificado na doc AWS)
- [fato] Para comparar, o Haiku 5.5 custa US$0,10/MTok de entrada e US$0,50/MTok de saída (prompts de até 100k tokens), contra US$4/US$20 do Opus 5.5, ou seja, 40x mais barato por token — [preços Anthropic](https://platform.claude.com/docs/en/about-claude/pricing) (2026-11-12)
- [fato] O Claude Code aceita como credenciais claude.ai, Claude API, Bedrock, Vertex e Foundry. Para trocar de endpoint é preciso `ANTHROPIC_BASE_URL`/gateway, e Bedrock entra via `CLAUDE_CODE_USE_BEDROCK` — [Claude Code docs, Authentication](https://code.claude.com/docs/en/authentication) (2026-11-12)

### Inferences
- [inferência] A assinatura não tem como usar um modelo fine-tunado. O campo `model` da skill aceita só aliases ou IDs Claude servidos pela Anthropic. Um Haiku fine-tunado no Bedrock exigiria rodar o Claude Code com credenciais AWS, que são pagas por token, fora da assinatura, além de Provisioned Throughput. E o modelo base está em fim de vida.
- [inferência] Modelo open-weight destilado (Llama ou Qwen pequeno) exige GPU para treinar e servir, um gateway compatível com a API Anthropic e a disposição de trocar o Claude Code por esse endpoint. Ficaria fora da assinatura e perderia o comportamento agêntico (ler `pom.xml`, `git diff --stat`, AskUserQuestion) que a skill pressupõe.
- [inferência] O caminho mais barato e próximo de "destilação" no cenário assinatura é usar o Haiku 5.5 ou o Sonnet 5.5 com a mesma skill (seção 3). Os outputs aprovados do Opus podem virar exemplos dentro da skill, mas isso é prompt e não treino.
- [opinião] A skill tem 15+4 casos de eval. Isso é pouco para fine-tuning, que costuma exigir centenas a milhares de pares. Não achei número oficial da Anthropic ou da AWS para o mínimo.

### Gaps
- Não encontrei, até nov/2026, fine-tuning de Claude 3.5 Haiku, Haiku 4.5 ou Haiku 5.5 em nenhum provedor, nem fine-tuning direto na API Anthropic. A tabela da AWS lista só o Claude 3 Haiku.
- Não encontrei o preço atual de treino ou de Provisioned Throughput para Claude customizado.

## 3. Roteamento de modelos / cascatas

### Takeaway
É a abordagem com a evidência mais forte (de 35% a 98% de redução de custo com qualidade parecida, em benchmarks) e a única que se encaixa direto no Claude Code com assinatura. Basta o campo `model` (e `effort`) no frontmatter da skill, ou `context: fork` com subagente em `model: haiku|sonnet`. O roteamento é estático, por skill ou subtarefa: o Claude Code não tem um router aprendido por consulta.

### Cited Findings
- [fato] FrugalGPT (Chen, Zaharia, Zou; 9/mai/2023): uma cascata de LLMs alcança o desempenho do GPT-4 com "up to 98% cost reduction", ou melhora a acurácia em 4% pelo mesmo custo — [arXiv 2305.05176](https://arxiv.org/abs/2305.05176)
- [fato] RouteLLM (LMSYS, 1/jul/2024): routers aprendidos entre um modelo forte e um fraco cortaram custo em "over 85% on MT Bench, 45% on MMLU, and 35% on GSM8K", mantendo 95% do desempenho do GPT-4 — [LMSYS blog](https://lmsys.org/blog/2024-07-01-routellm/); o abstract do paper fala em redução "by over 2 times in certain cases" — [arXiv 2406.18665](https://arxiv.org/abs/2406.18665) (v1 26/jun/2024, v4 23/fev/2025)
- [fato] Frontmatter de skill: `model` define o modelo "for the rest of the current turn" e aceita os valores de `/model` ou `inherit`. `effort` aceita `low`…`max`. Com `context: fork`, os dois valem para o subagente criado pelo fork. `agent` escolhe o tipo de subagente — [Claude Code docs, Skills](https://code.claude.com/docs/en/skills) (2026-11-12)
- [fato] O `model` de um subagente aceita `sonnet`, `opus`, `haiku`, `fable`, um ID completo ou `inherit`. A ordem de resolução é: parâmetro da invocação, frontmatter, `CLAUDE_CODE_SUBAGENT_MODEL`, modelo da conversa. Cada subagente começa "with a fresh, isolated context window" e carrega a hierarquia de CLAUDE.md, o git status e as skills listadas em `skills` — [Claude Code docs, Subagents](https://code.claude.com/docs/en/sub-agents) (2026-11-12)
- [fato] Orientação oficial: "Sonnet handles most coding tasks well and costs less than Opus… For simple subagent tasks, specify `model: haiku`". A doc também diz: "The subagent's own requests still draw on your usage" — [Claude Code docs, Manage costs](https://code.claude.com/docs/en/costs) (2026-11-12)
- [fato] Preço por MTok (entrada/saída): Opus 5.5 US$4/US$20; Sonnet 5.5 US$2/US$10; Haiku 5.5 US$0,10/US$0,50 (até 100k tokens) — [preços Anthropic](https://platform.claude.com/docs/en/about-claude/pricing) (2026-11-12)
- [fato] Thinking é cobrado como saída. Opus 5.5, Sonnet 5.5 e Haiku 5.5 "always use extended thinking". Baixar o `effort` é a forma indicada de reduzir esse custo — [Claude Code docs, Manage costs](https://code.claude.com/docs/en/costs) (2026-11-12)
- [fato] Com assinatura, a mensagem "You've hit your Opus limit" pode ser contornada trocando de família com `/model`. Isso indica limites separados por família de modelo, além dos limites de sessão e semanais compartilhados — [Claude Code docs, Manage costs](https://code.claude.com/docs/en/costs) (2026-11-12)

### Inferences
- [inferência] Pela tabela de preços, a mesma execução sairia a cerca de 50% do custo atual com Sonnet 5.5 e a cerca de 2,5% com Haiku 5.5, supondo o mesmo número de tokens. Daria de US$0,07–0,08 e de US$0,004 por execução. A qualidade é a incógnita e precisa ser medida com `casos.md`. Fazer isso custa umas 2–3 execuções da suíte de 15 casos: cerca de US$2–5 em valores de tabela.
- [inferência] Para a skill, o mapeamento mais simples é acrescentar `model: sonnet` (ou `haiku`) e `effort: medium` no frontmatter de `SKILL.md`, uma linha cada, e rodar a suíte. Atenção: `rodar.py` grava `{'model': 'opus','effortLevel':'high'}` no settings do home temporário, mas o frontmatter da skill sobrescreve isso no turno. Seria preciso confirmar no `modelUsage` do stream-json.
- [inferência] A cascata "barato primeiro, caro se falhar" do FrugalGPT precisa de um juiz automático de confiança. No Claude Code, a aproximação seria uma skill que roda em subagente Haiku e escala para Opus quando o passo 5 ("Confira") reprova. Isso soma chamadas e só compensa se a taxa de escalonamento for baixa. Não há suporte nativo a router aprendido.
- [inferência] O fork (`context: fork`) dá à skill um contexto limpo, sem o histórico da conversa. Em sessões longas isso pode economizar mais do que trocar de modelo, porque o custo de entrada cresce com o histórico.

### Gaps
- Não há números públicos de qualidade de Haiku 5.5 ou Sonnet 5.5 contra Opus 5.5 em tarefas de reescrita de prompt. Só a suíte local responde isso.
- A Anthropic não publica quanto cada modelo consome dos limites da assinatura (peso de Opus contra Sonnet).

## 4. Otimização automática de prompt (DSPy/MIPROv2, GEPA, TextGrad, OPRO, prompt improver)

### Takeaway
Os otimizadores melhoram a métrica de forma comprovada. O GEPA produziu prompts até 9,2x mais curtos que os do MIPROv2. Mas eles pedem centenas a milhares de execuções avaliadas e normalmente rodam via API (DSPy/LiteLLM com API key). Com execuções de cerca de US$0,15 e uma métrica que depende de julgamento, uma otimização completa custaria de centenas a mais de mil dólares em valor de tabela. A alternativa viável com assinatura é um laço manual ou semiautomático no estilo GEPA: o próprio Claude Code reflete sobre as falhas de `checar.py` e propõe edições, com orçamento de dezenas de execuções.

### Cited Findings
- [fato] MIPRO (Opsahl-Ong et al., 17/jun/2024, EMNLP 2024) otimiza instruções e demonstrações few-shot de cada módulo sem rótulos por módulo, maximizando uma métrica final. Superou os baselines em 5 de 7 programas com Llama-3-8B, com ganho de até 13% de acurácia — [arXiv 2406.11695](https://arxiv.org/abs/2406.11695)
- [fato] GEPA (25/jul/2025; ICLR 2026 oral) supera o GRPO em 6% na média e em até 20%, "while using up to 35x fewer rollouts", e o MIPROv2 em mais de 10% (+12% no AIME-2025). Os prompts do GEPA são "up to 9.2× shorter than those from MIPROv2" — [arXiv 2507.19457](https://arxiv.org/abs/2507.19457), [HTML](https://arxiv.org/html/2507.19457)
- [fato] Orçamento do GEPA (+Merge) com Qwen3 8B, em rollouts: HotpotQA 6.871; IFBench 3.593; HoVer 7.051; PUPA 2.426; AIME-2025 1.839; LiveBench-Math 1.839; agregado 3.936. O GRPO usou 24.000 por benchmark — [arXiv 2507.19457 (HTML), Tabela 1](https://arxiv.org/html/2507.19457)
- [fato] O prompt improver do Console Anthropic (out/2024) aumentou a acurácia em 30% num teste de classificação multilabel com Claude 3 Haiku e levou a aderência a contagem de palavras a 100% numa sumarização feita com 10 artigos. Ele acrescenta uma seção de raciocínio passo a passo e reformata exemplos em XML — [Anthropic, Prompt improver](https://www.anthropic.com/news/prompt-improver); [claude.com resources](https://claude.com/resources/articles/prompt-improver)
- [fato] A URL antiga da doc do prompt improver hoje redireciona para "Prompting best practices" — [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompt-improver) (consultado em 2026-11-12). Não confirmei se a ferramenta continua no Console.

### Inferences
- [inferência] Dá para otimizar por prompt mais curto: DSPy e GEPA aceitam qualquer métrica Python. Bastaria `score = aprovação em checar.py − λ·palavras(SKILL.md)`. O GEPA, que já tende a gerar prompts mais curtos, é o que mais se encaixa.
- [inferência] Custo em valor de tabela: uma passada da suíte custa 15 × US$0,15 ≈ US$2,25. Um orçamento no estilo GEPA de 1.839 a 7.051 rollouts daria cerca de US$275 a US$1.060. Um laço enxuto de 20 candidatos × 15 casos sairia por volta de US$45. Ao custo atual por execução, só um orçamento pequeno faz sentido. Com Haiku 5.5 como executor, o rollout ficaria cerca de 40x mais barato, mas aí se otimiza para o Haiku e não para o Opus.
- [inferência] Barreira prática: DSPy, GEPA, TextGrad e OPRO chamam LLMs por bibliotecas cliente (LiteLLM), o que exige API key. Colocar o token OAuth da assinatura nessas bibliotecas fere a política citada na seção 5. O caminho dentro das regras é o otimizador chamar `claude -p`, como `rodar.py` já faz. É o próprio Claude Code e consome a cota da assinatura.
- [inferência] Os critérios de `casos.md` incluem julgamento qualitativo. Se `checar.py` não cobrir tudo, a métrica fica fraca e o otimizador pode "ganhar" cortando conteúdo que importa. O commit 8a1b403 ("sem conteúdo inventado") sugere que esse risco já apareceu. Validar em `casos-validacao.tsv` (holdout) é obrigatório.
- [opinião] O prompt improver tende a alongar prompts (acrescenta seção de raciocínio e XML), o oposto do objetivo daqui.

### Gaps
- Não encontrei medição de TextGrad ou OPRO com redução de comprimento de prompt como objetivo, nem custo por rollout comparável. Não busquei esses papers diretamente.
- Não há relato público de otimizadores aplicados a skills do Claude Code.

## 5. Assinatura vs. API: modelo de custo e o que exige API key

### Takeaway
Com assinatura, o custo não é em dólar: são limites de uso (janela de 5h e semanal, e por família de modelo), com créditos extras opcionais. O `total_cost_usd` que `rodar.py` registra é só um equivalente a preço de tabela. Roteamento de modelo, progressive disclosure e laços de otimização via `claude -p` funcionam com assinatura. Fine-tuning, DSPy/GEPA via SDK e qualquer uso do token OAuth fora do Claude Code exigem API key, AWS ou GPU.

### Cited Findings
- [fato] "Claude Pro, Max, and Ultra subscribers have usage included in their subscription, so the session cost figure isn't relevant for billing purposes". O valor em dólar do `/usage` é calculado localmente "at list price" — [Claude Code docs, Manage costs](https://code.claude.com/docs/en/costs) (2026-11-12)
- [fato] Nos planos Team/Enterprise, a franquia por assento "resets on a rolling five-hour window and a weekly window" e é compartilhada com o chat. Os limites de sessão e semanais valem para todos os modelos. Há limites específicos de Opus e de Sonnet. O `/usage` mostra a atribuição de consumo por skill e por subagente — [Claude Code docs, Manage costs](https://code.claude.com/docs/en/costs) (2026-11-12)
- [fato] Créditos de uso (`/usage-credits`) permitem passar do limite do plano. O comando "isn't available with API key authentication" — [Claude Code docs, Manage costs](https://code.claude.com/docs/en/costs) (2026-11-12)
- [fato] Precedência de credenciais: `ANTHROPIC_API_KEY` vem antes do OAuth da assinatura. `claude setup-token` gera um token OAuth de 1 ano para scripts e CI, que "authenticates with your Claude subscription" e "can only make model requests". O `--bare` não lê esse token — [Claude Code docs, Authentication](https://code.claude.com/docs/en/authentication) (2026-11-12)
- [fato] "Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Use the API key authentication methods" — [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) (2026-11-12)
- [fato, fontes secundárias] Em fev/2026 a Anthropic esclareceu que tokens OAuth de Free/Pro/Max servem só para Claude Code e Claude.ai. Há relatos de bloqueio de harnesses de terceiros em 4/abr/2026 — [The Register, 20/fev/2026](https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access). Um relato não confirmado fala em restauração parcial com pool de créditos separado a partir de 15/jun/2026 — [tech-insider.org](https://tech-insider.org/ie/?p=560). As fontes divergem e não confirmei esse ponto.

### Inferences
- [inferência] Resumo de aplicabilidade no cenário assinatura (OAuth, sem API key):
  - **Progressive disclosure de instruções:** funciona, sem infraestrutura. Ganho de tokens pequeno.
  - **RAG vetorial/MCP local:** é possível (MCP local funciona com o token OAuth), mas é infraestrutura desproporcional para 9 seções.
  - **Fine-tuning/destilação:** não funciona. Exige AWS Bedrock (pago por token, Provisioned Throughput, modelo base em fim de vida) ou GPUs, mais dados de treino.
  - **Roteamento (`model`/`effort` no frontmatter, subagente Haiku/Sonnet):** funciona e é o maior ganho potencial. Com assinatura, o ganho aparece como menos consumo do limite, sobretudo do limite de Opus.
  - **Otimização automática:** com DSPy/GEPA via SDK, precisa de API key. Um laço próprio chamando `claude -p` funciona, mas cada rollout consome a cota da assinatura, e milhares de rollouts estouram os limites de 5h e semanais.
- [inferência] Como em assinatura o custo marginal em dólar é zero até o limite, "barato" quer dizer caber no limite e não estourar o limite de Opus. Isso favorece ainda mais o roteamento para Sonnet ou Haiku.
- [inferência] O próprio `rodar.py` lê o token OAuth de `~/.credentials.json` e chama o binário `claude`. Isso é uso do Claude Code e está dentro da política citada. Levar o mesmo token para DSPy/LiteLLM não estaria.

### Gaps
- A Anthropic não publica quantos tokens cabem em cada janela por plano nem o peso relativo de Opus, Sonnet e Haiku.
- O status atual (nov/2026) de uso do OAuth em `claude -p`/Agent SDK com pool de créditos separado não foi confirmado por fonte primária.
