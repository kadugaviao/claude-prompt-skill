# Compressão de instruções e redução de tokens de execução (estado em nov/2026)

Escopo: técnicas para encurtar instruções (lado da entrada) e reduzir tokens de raciocínio e saída (lado da execução), julgadas para a skill `/prompt` (`skills/prompt/SKILL.md`: 1.825 palavras, 201 linhas). O modelo é fechado (Claude via Claude Code, assinatura), sem acesso a logits ou embeddings. A pesquisa anterior (`docs/research/prompt-engineering-research.md`) já cobre como escrever prompts, CoT inútil em modelos de raciocínio, "lost in the middle", contexto como recurso finito e os números "direcionais" da OpenAI (−41–66% de tokens). Esses pontos não se repetem aqui.

Medição local (fato, `wc`/`awk` em 12/11/2026): a seção "Tipos de tarefa" (9 templates, linhas 116–201) tem 795 das 1.825 palavras, cerca de 44% da skill. Em português, a tokenização costuma render mais tokens por palavra que em inglês, então a ordem de grandeza é de ~2,5–3 mil tokens (inferência, não contada com tokenizer).

Legenda: **[fato]** = dado publicado pela fonte; **[inferência]** = conclusão minha a partir dos dados; **[opinião]** = julgamento da fonte ou meu, sem medição.

## 1. Compressão automática de prompts (LLMLingua e família, Selective Context, 500xCompressor, gist tokens, soft prompts)

### Takeaway
Os compressores automáticos relatam de 2x a 20x (até 480x nos de "soft tokens"). Mas foram medidos em contextos longos (RAG, reuniões, documentos, demonstrações de CoT), não em instruções curtas e densas. Em contexto curto, toda compressão piora o resultado. Os métodos de soft prompt, gist e KV exigem acesso aos internos do modelo. Para uma skill de ~2,5k tokens lida pelo Claude via assinatura, nenhum deles se aplica na prática. No máximo serviria rodar o LLMLingua-2 offline para ter um rascunho comprimido e revisá-lo à mão, e mesmo isso é arriscado.

### Cited Findings
- **[fato]** LLMLingua (Jiang et al., EMNLP 2023, arXiv 9/10/2023): "up to 20x compression with little performance loss". Testado em GSM8K, BBH, ShareGPT e Arxiv, com um LM pequeno que escolhe os tokens a remover. — [arXiv 2310.05736](https://arxiv.org/abs/2310.05736)
- **[fato]** Exemplo do README: um prompt de 2.365 tokens foi comprimido para 211 (11,2x). O compressor roda localmente (padrão phi-2, ou Llama-2-7B quantizado em menos de 8 GB de GPU). O README diz que o LLM-alvo dispensa treino e que "GPT-4 can recover key information from compressed prompts". — [GitHub microsoft/LLMLingua](https://github.com/microsoft/LLMLingua) (consultado em 12/11/2026)
- **[fato]** LongLLMLingua (ACL 2024): até +21,4% em RAG com cerca de 1/4 dos tokens. É voltado justamente para "lost in the middle" em contexto longo. — [GitHub microsoft/LLMLingua](https://github.com/microsoft/LLMLingua)
- **[fato]** LLMLingua-2 (Pan et al., Findings ACL 2024, arXiv 19/3/2024): compressão de 2x a 5x, 3x a 6x mais rápido que os métodos anteriores e latência ponta a ponta 1,6x a 2,9x menor. Usa um encoder do tamanho do BERT (XLM-RoBERTa-large ou mBERT) destilado do GPT-4. Benchmarks: MeetingBank, LongBench, ZeroScrolls, GSM8K, BBH. O abstract não quantifica a perda de qualidade. — [arXiv 2403.12968](https://arxiv.org/abs/2403.12968)
- **[fato]** Estudo empírico (Zhang et al., arXiv abr/2025, workshop ICLR 2025): 6 métodos, 13 datasets, testados com GPT-3.5-turbo, GPT-4o-mini e Claude-3-Haiku. "All methods' performance decreases with increasing compression ratios for short contexts"; em contexto longo, compressão moderada pode até melhorar. Todos os métodos aumentam a alucinação, e a causa principal é a perda de informação. Os melhores foram (Long)LLMLingua e LLMLingua-2. — [arXiv 2505.00019](https://arxiv.org/abs/2505.00019)
- **[fato]** "Prompt Compression in the Wild" (Kummer et al., ECIR 2026, arXiv 3/4/2026): 30 mil queries. O LLMLingua chega a "up to 18% end-to-end speed-ups" só dentro de uma janela em que comprimento do prompt, taxa de compressão e hardware combinam. Fora dela, o custo da etapa de compressão anula o ganho. A qualidade ficou estatisticamente igual em sumarização, código e QA, com LLMs abertos. — [arXiv 2604.02985](https://arxiv.org/abs/2604.02985)
- **[fato]** Preprint de um único autor (Baxi, dez/2025): a conformidade com uma restrição de contagem de palavras falha mais em prompts de comprimento médio (~27 palavras). O autor nota que trabalhos de compressão como o LLMLingua "do not explicitly measure instruction-following robustness". Trate como preliminar. — [arXiv 2512.17920](https://arxiv.org/html/2512.17920v1)
- **[fato]** 500xCompressor (Li et al., arXiv 6/8/2024): de 6x a 480x, até 1 token especial, retendo 62,26–72,89% da capacidade do LLM. Os valores de KV preservam mais informação que embeddings, ou seja, o método exige acesso interno ao modelo. — [arXiv 2408.03094](https://arxiv.org/abs/2408.03094)
- **[fato, não reverificado nesta sessão; vem do abstract conhecido]** Gist tokens (Mu et al., NeurIPS 2023): comprimem o prompt em tokens "gist" aprendidos, com até 26x de compressão e até 40% menos FLOPs. Exigem fine-tuning do próprio modelo. — [arXiv 2304.08467](https://arxiv.org/abs/2304.08467)
- **[fato, não reverificado nesta sessão; vem do abstract conhecido]** Selective Context (Li et al., EMNLP 2023): poda por autoinformação calculada com um LM pequeno. Cerca de 50% menos contexto, 36% menos memória e 32% menos tempo de inferência, com queda pequena em BERTScore e fidelidade. Testado em artigos arXiv, notícias e conversas longas. — [arXiv 2310.06201](https://arxiv.org/abs/2310.06201)

### Inferences
- **[inferência]** Todos os ganhos grandes vêm de entradas com muita redundância: documentos recuperados, transcrições, demonstrações de CoT. A SKILL.md já é uma lista densa de regras, com nomes exatos de seções, limites como "no máximo 3 leituras" e cabeçalhos de templates. Remover tokens por perplexidade tende a cortar exatamente as palavras de controle ("não", "só", "nunca", números, nomes de seção), cuja perda o estudo de Zhang associa a alucinação.
- **[inferência]** Diferença de benchmark: os testes são de QA e sumarização, medidos por exatidão ou ROUGE, e não de seguir um procedimento de 6 passos com formato de saída rígido. Nenhum estudo encontrado mede a compressão de *system prompts* ou instruções de agente.
- **[inferência]** Modelo fechado via assinatura: soft prompts, gist tokens e 500xCompressor ficam excluídos, porque exigem pesos, embeddings ou KV. A família LLMLingua funciona com alvo caixa-preta, já que gera texto comprimido, mas só como etapa offline: o Claude Code não tem um ponto para comprimir a skill a cada uso. E o texto comprimido fica ilegível para quem mantém a skill.
- **[inferência]** Custo real na assinatura: a skill entra uma vez por invocação e depois é relida via cache de prompt (ver a seção 4). Cortar 1–1,5k tokens de entrada economiza pouco perto do raciocínio e da saída.

### Gaps
- Não encontrei avaliação de LLMLingua ou similares sobre instruções de agente, system prompts ou skills de ~2–3k tokens com métrica de seguir instruções.
- Não há números de qualidade do LLMLingua-2 por tarefa no abstract, e não li as tabelas completas.
- Não encontrei estudo de compressão de texto em português com esses métodos (o LLMLingua-2 é multilíngue via XLM-R, mas não foi avaliado aqui).

## 2. Encurtamento manual por ablação: tamanho das instruções vs. qualidade de cumprimento

### Takeaway
Há evidência forte de que muitas instruções e entradas longas degradam o cumprimento. Mas a degradação aparece em escalas bem acima da skill: centenas de instruções, ou milhares de tokens de enchimento irrelevante. Em ~10–50 regras, os modelos de fronteira ficam perto de 100%. Ou seja, encurtar a skill provavelmente não melhora a qualidade por si só, mas também não deve piorar se o corte for de redundância. Não achei estudo que isole o efeito de remover exemplos ou seções de uma instrução curta.

### Cited Findings
- **[fato]** IFScale (Jaroslawicz et al., arXiv 15/7/2025): de 10 a 500 instruções de inclusão de palavra-chave num relatório, com 20 modelos. Acurácia em 10/50/100/250/500 instruções:
  - gemini-2.5-pro: 100 / 99,6 / 98,4 / 84,8 / 68,9%
  - o3 (high): 100 / 99,6 / 98,2 / 97,8 / 62,8%
  - claude-3.7-sonnet: 100 / 99,6 / 94,8 / 72,9 / 52,7%
  - claude-sonnet-4: 100 / 98,0 / 94,4 / 77,2 / 42,9%
  - claude-opus-4 (com raciocínio): 92 / 99,6 / 81,8 / 81,5 / 52,1%
  - gpt-4o: 94 / 82,8 / 49,0 / 22,2 / 15,4%
  - claude-3.5-haiku: 98 / 78 / 43,4 / 16,6 / 8,5%

  Fonte: [arXiv 2507.11538](https://arxiv.org/html/2507.11538)
- **[fato]** IFScale, padrões de degradação: decaimento por limiar nos modelos de raciocínio (gemini-2.5-pro e o3 quase perfeitos até ~150 instruções), linear em gpt-4.1 e claude-3.7-sonnet, exponencial em modelos pequenos. Há viés de primazia: as instruções do terço final falham mais, com razão de até 3,37 no gpt-4.1-mini com 100 instruções, e o efeito é máximo em ~150–200 instruções. O erro dominante é omitir, não modificar. A latência dos modelos de raciocínio explode (o4-mini: 12 s com 10 instruções, 436 s com 250). — [arXiv 2507.11538](https://arxiv.org/html/2507.11538)
- **[fato]** IFScale, raciocínio: o3 high bate o3 medium por ~11 pontos com 500 instruções (62,8 vs 51,6%). O thinking do claude-opus-4 ganha ~7,5 pontos com 500, e o do claude-sonnet-4 fica um pouco pior com 500 (39,9 vs 42,9%). — [arXiv 2507.11538](https://arxiv.org/html/2507.11538)
- **[fato]** "Same Task, More Tokens" (Levy, Jacoby, Goldberg, ACL 2024, arXiv 19/2/2024): a acurácia média de raciocínio cai de ~0,92 para ~0,68 quando a entrada chega a ~3.000 tokens com enchimento. A queda ocorre mesmo quando o enchimento repete parágrafos relevantes e é maior com texto de outra fonte. CoT não fecha a diferença, exceto no GPT-4. — [arXiv 2402.14848](https://arxiv.org/html/2402.14848)
- **[fato / opinião do fornecedor]** Anthropic, Skill authoring best practices: "The context window is a public good"; "Default assumption: Claude is already very smart. Only add context Claude doesn't already have"; "Does this paragraph justify its token cost?". Recomenda testar em Haiku, Sonnet e Opus ("What works perfectly for Opus might need more detail for Haiku") e, para Opus, checar se a skill "avoid over-explaining". Sobre exemplos: "Examples convey the desired style and level of detail to Claude more clearly than descriptions alone". — [Anthropic docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (sem data na página; consultado em 12/11/2026)
- **[opinião do fornecedor]** O mesmo guia recomenda escrever avaliações antes ("Write minimal instructions: Create just enough content to address the gaps and pass evaluations") e iterar com base no comportamento observado. — [Anthropic docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

### Inferences
- **[inferência]** A skill tem dezenas de regras, não centenas. Pelo IFScale, nessa faixa os modelos Claude recentes ficam acima de 94–100%, e a degradação por densidade não é o gargalo. Encurtar se justifica por custo e manutenção, não por promessa de mais qualidade.
- **[inferência]** O IFScale difere deste caso: instruções independentes, homogêneas e verificáveis por palavra-chave, contra regras procedurais e interdependentes. O "Same Task" mede enchimento irrelevante, e a skill não tem enchimento irrelevante declarado. Os dois servem como limite superior de risco, não como previsão.
- **[inferência]** O viés de primazia e o "lost in the middle" sugerem que, se a skill crescer, as regras críticas (não executar antes da aprovação, só leitura, limite de 3 leituras) devem ficar no início, como já estão.
- **[inferência]** Para saber se exemplos ou seções ajudam, a evidência pública não resolve. O método recomendado é ablação local: remover uma seção por vez e rodar as fixtures existentes do projeto (`make_fixtures.sh` e as rodadas de aprovação 3/5 vistas no git log), medindo tokens e nota.

### Gaps
- Nenhum estudo encontrado mede o efeito de remover exemplos ou seções de uma instrução curta (~2k tokens) num modelo de 2026.
- O IFScale não testa os modelos Claude de 2026 (Opus 5.x, Sonnet 5.x, Fable).
- Não verifiquei de forma independente os números da OpenAI sobre prompts enxutos (já listados como "direcionais" na pesquisa anterior).

## 3. Carregamento condicional ("lazy") de instruções: progressive disclosure

### Takeaway
A Anthropic documenta e recomenda exatamente esse padrão para skills: SKILL.md como índice e arquivos de referência lidos só quando necessários, a um nível de profundidade. Os 9 templates de tipo de tarefa (44% das palavras da skill) são o caso típico do "Pattern 2: domain-specific organization". O ganho estimado é de ~35–40% das palavras de instrução por invocação, ao custo de uma leitura de arquivo e do risco de o modelo não ler ou ler parcialmente.

### Cited Findings
- **[fato]** Carregamento em três níveis: metadados (name e description) sempre no contexto, corpo da SKILL.md quando a skill é acionada, arquivos extras "only as needed"; "No context penalty for large files: Reference files... don't consume context tokens until actually read". — [Anthropic, Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **[fato]** "Pattern 2: Domain-specific organization... organize content by domain to avoid loading irrelevant context... This keeps token usage low and context focused." Também: "If workflows become large or complicated... consider pushing them into separate files and tell Claude to read the appropriate file based on the current task." — [Anthropic docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **[fato]** Riscos documentados: "Claude might partially read files when they're referenced from other referenced files... might use commands such as `head -100`". Daí a recomendação de manter as referências a um nível de profundidade e pôr um índice em arquivos com mais de 100 linhas. Se o Claude lê sempre o mesmo arquivo, "consider whether that content should be in the main SKILL.md instead". — [Anthropic docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **[fato]** Limite: "Keep the SKILL.md body under 500 lines for optimal performance". A skill tem 201 linhas, bem abaixo. — [Anthropic docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **[fato]** Claude Code: as skills carregam sob demanda, o CLAUDE.md fica carregado sempre ("Aim to keep CLAUDE.md under 200 lines"), e as definições de ferramentas MCP são adiadas por padrão (tool search). É o mesmo princípio aplicado a ferramentas. — [Claude Code, Manage costs](https://code.claude.com/docs/en/costs) (consultado em 12/11/2026)

### Inferences
- **[inferência]** Aplicação direta: mover os 9 templates para `tipos/<tipo>.md`, ou um único `tipos.md` com índice, e deixar no passo 1 da SKILL.md só a lista de nomes e os critérios de desempate. Lendo um template só, a entrada cai de ~1.825 para ~1.100 palavras. Mas cada leitura é uma chamada de ferramenta a mais, que reenvia o contexto (lido do cache) e gasta alguns tokens de saída. O saldo líquido é positivo, porém modesto.
- **[inferência]** Conflito com a própria skill: o passo 2 limita a 3 leituras. A leitura do template precisaria ficar fora dessa conta, ou o limite precisaria mudar. Senão o modelo pode pular o template para poupar leituras.
- **[inferência]** O critério "Empate" (combinar os itens de dois tipos) exige ler dois arquivos nesses casos, o que reduz a economia.
- **[inferência]** Risco específico de qualidade: com os 9 templates juntos, o modelo vê os contrastes entre eles na hora de classificar. Separados, a classificação passa a depender só da lista de nomes e critérios. É uma hipótese a medir nas fixtures, não um efeito documentado.

### Gaps
- Não achei medições públicas (acadêmicas ou da Anthropic) de economia de tokens ou de qualidade da progressive disclosure em skills. As fontes são guias de prática, sem números.
- Não verifiquei se, no Claude Code, a leitura de um arquivo da skill conta como chamada extra visível ao usuário nem como afeta o cache.

## 4. Redução do lado da execução: leituras, saída concisa, esforço/raciocínio, Chain of Draft

### Takeaway
No Claude atual, o controle mais eficaz e documentado é o parâmetro de esforço (`/effort` no Claude Code), e não texto no prompt. O esforço afeta raciocínio, chamadas de ferramenta e texto. Na literatura, o raciocínio conciso ("Chain of Draft", CCoT) corta de 50% a 90% dos tokens de raciocínio *visível* com pouca perda, mas só em few-shot e em modelos não-raciocinadores de 2024. Mais raciocínio também pode piorar o resultado ("inverse scaling").

### Cited Findings
- **[fato]** Chain of Draft (Xu et al., Zoom, arXiv 25/2/2025): "as little as only 7.6% of the tokens" do CoT. Few-shot, GPT-4o / Claude 3.5 Sonnet:
  - GSM8K: CoT 95,4 / 95,8% com 205 / 190 tokens; CoD 91,1 / 91,4% com 44 / 40 tokens.
  - Sports: CoD 98,3 / 97,3% com 15 / 14 tokens, contra CoT 95,9 / 93,2% com 29 / 189 tokens.
  - Coin flip: 100% nos dois métodos, com 17–19 tokens no CoD contra 52–135 no CoT.

  Fonte: [arXiv 2502.18600](https://arxiv.org/html/2502.18600)
- **[fato]** Limitações do CoD: em zero-shot GSM8K, o Claude 3.5 Sonnet cai de 90,4% (CoT) para 65,5% (CoD), só 3,6 pontos acima da resposta direta, e o GPT-4o cai de 94,8% para 84,4%. Em modelos com menos de 3B, o CoD fica 8–27 pontos abaixo do CoT. Os autores atribuem isso a dados de treino com pouco raciocínio no estilo CoD. — [arXiv 2502.18600](https://arxiv.org/html/2502.18600)
- **[fato]** Concise CoT (Renze & Guven, arXiv jan/2024, v3 out/2024): com GPT-3.5 e GPT-4, as respostas ficam 48,7% mais curtas, com impacto "negligible" em geral, mas −27,69% em matemática no GPT-3.5. O custo por token cai 22,67% em média. — [arXiv 2401.05618](https://arxiv.org/abs/2401.05618)
- **[fato, não reverificado nesta sessão; vem do abstract conhecido]** TALE, token-budget-aware reasoning (Han et al., arXiv dez/2024): um orçamento de tokens no prompt reduz ~68,6% dos tokens de saída com queda de acurácia abaixo de 5%. — [arXiv 2412.18547](https://arxiv.org/abs/2412.18547)
- **[fato]** Inverse Scaling in Test-Time Compute (Gema et al., Anthropic Fellows e colaboradores; arXiv 19/7/2025, TMLR dez/2025): estender o raciocínio de modelos de raciocínio (Claude e série o da OpenAI) "deteriorates performance" em contagem com distratores, regressão com features espúrias e dedução com restrições. Um dos modos de falha listados é a distração por detalhes irrelevantes. — [arXiv 2507.14417](https://arxiv.org/abs/2507.14417)
- **[fato]** Docs de esforço da Anthropic: o esforço "affects all tokens in the response", incluindo texto, chamadas de ferramenta e thinking. Esforço baixo leva a "fewer and terser tool calls", "Proceed directly to action without preamble". O Opus 5.5 e o Haiku 5.5 usam medium por padrão; os demais modelos, high. "Effort is a behavioral signal, not a strict token budget." No Opus 5.5 o thinking adaptativo não pode ser desligado, e o esforço é "the primary control". — [Anthropic, Effort](https://platform.claude.com/docs/en/build-with-claude/effort) (consultado em 12/11/2026)
- **[fato]** O mesmo doc diz que o esforço *não* encurta bem a resposta visível: no Fable 5.2, "Effort barely changes how long the model's replies are, so use your prompt to change reply length"; no Opus 5, "changing effort does not reliably shorten responses, so prompt for length instead". No Haiku 5.5 em esforço low, "the model is more likely to skip a search, stop early, or skip a check" em prompts longos de agente. — [Anthropic, Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- **[fato]** Claude Code: "Thinking tokens are billed as output tokens, and the default budget can be tens of thousands of tokens per request". Para tarefas simples, baixar com `/effort`. `MAX_THINKING_TOKENS` só vale em modelos com orçamento fixo, e os adaptativos o ignoram. "Write specific prompts: vague requests... trigger broad scanning". O cache de prompt barateia o conteúdo repetido, e cada uso de ferramenta reenvia o contexto. — [Claude Code, Manage costs](https://code.claude.com/docs/en/costs)
- **[fato, já na pesquisa anterior]** No Fable 5.2, instruções do tipo "responda sem deliberar" não impedem o thinking a partir do esforço medium; a recomendação é usar o parâmetro. — ver `docs/research/prompt-engineering-research.md`, seção B.8

### Inferences
- **[inferência]** Diferença de benchmark: CoD, CCoT e TALE medem raciocínio *visível* em modelos sem thinking nativo (GPT-4o, Claude 3.5) e em problemas de aritmética ou lógica. Em Claude 2026 com thinking adaptativo, pedir "rascunhos de 5 palavras" na saída não controla o thinking interno, segundo a documentação do esforço e a pesquisa anterior. O número de 7,6% não se transfere.
- **[inferência]** Para a skill, a tarefa (classificar, ler até 3 arquivos, preencher um template) é de baixa dificuldade de raciocínio. O maior ganho de execução viria de rodar a skill em esforço baixo ou médio. A Anthropic recomenda "Use low for speed-sensitive or simple tasks" e fazer uma varredura de esforço nas suas próprias avaliações. Porém o frontmatter atual tem `disable-model-invocation: true` e não fixa o esforço. Fixar esforço ou modelo por skill depende de suporte do Claude Code, que não verifiquei.
- **[inferência]** O limite "no máximo 3 leituras" já é uma redução de execução alinhada à orientação "specific prompts → minimal file reads". O inverse scaling e o "Same Task" sugerem que ler menos também evita distratores, e não só custo.
- **[inferência]** Risco: em esforço low, o Haiku pula verificações em prompts longos. O passo "5. Confira e entregue" da skill pode ser o primeiro a ser cortado em esforço baixo. É preciso medir nas fixtures.

### Gaps
- Não encontrei medição pública de quanto `/effort low` vs `medium` reduz os tokens no Claude Code para uma tarefa curta e estruturada como esta. A Anthropic só diz "significant token savings" e não dá percentuais.
- Não verifiquei se as skills do Claude Code aceitam um campo de frontmatter para esforço ou modelo, nem em qual versão.
- Não encontrei replicação do CoD em modelos de raciocínio de 2026.

## 5. Compressão do formato de saída: templates de entrega mais curtos, comprimento da saída vs. qualidade

### Takeaway
A saída é a parte que o prompt controla de fato: os docs da Anthropic dizem que o esforço não encurta bem a resposta e que o comprimento deve ser pedido no prompt. A evidência de 2024 mostra que pedir concisão corta ~50% da saída com perda pequena em tarefas gerais, mas grande em matemática nos modelos fracos. Os templates da skill já têm faixas de linhas por tipo (6–80). A alavanca restante é cortar seções fixas de entrega, não comprimir o prompt gerado.

### Cited Findings
- **[fato]** Pedir concisão reduz a saída em 48,7% com efeito desprezível em média (GPT-3.5/GPT-4), mas −27,69% em matemática no GPT-3.5. — [arXiv 2401.05618](https://arxiv.org/abs/2401.05618)
- **[fato]** CoD mostra que, em modelos grandes com few-shot, saídas de 7–20% do tamanho do CoT mantêm ou superam a acurácia. Sem exemplos, perde até 25 pontos (Claude 3.5 Sonnet em GSM8K). Ou seja, um formato curto funciona melhor quando há um exemplo do formato desejado. — [arXiv 2502.18600](https://arxiv.org/html/2502.18600)
- **[fato / orientação do fornecedor]** "Use your prompt to change reply length and tone" (Fable 5.2); "prompt for length instead" (Opus 5). — [Anthropic, Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- **[fato / orientação do fornecedor]** O padrão de template da Anthropic distingue um template estrito ("ALWAYS use this exact template structure") de um flexível ("use your best judgment"). Exemplos concretos transmitem estilo e nível de detalhe melhor que descrições. — [Anthropic docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **[fato]** Preprint de um autor: a falha de conformidade com um limite de palavras não é monotônica em relação ao comprimento do prompt (pico em ~27 palavras). É fraco e preliminar. — [arXiv 2512.17920](https://arxiv.org/html/2512.17920v1)

### Inferences
- **[inferência]** Na skill, a saída tem duas partes: a mensagem de entrega (passo 5) e o prompt gerado (por tipo). Encurtar o prompt gerado mexe no produto, e o critério de qualidade (aprovação 3/5 no histórico) é sobre ele. Encurtar a moldura de entrega (texto em volta, repetições de suposições) é economia "pura".
- **[inferência]** Como exemplos sustentam formatos curtos (CoD com few-shot vs zero-shot), remover os exemplos dos templates para poupar tokens de entrada pode aumentar a saída ou piorar a conformidade. Se os templates forem para arquivos lazy (seção 3), dá para manter os exemplos sem custo fixo.
- **[opinião]** A ordem de prioridade para esta skill seria: (1) esforço baixo ou médio na execução; (2) lazy loading dos 9 templates; (3) corte manual de redundância validado nas fixtures; (4) compressão automática: não usar.

### Gaps
- Nenhum estudo encontrado relaciona o comprimento de um *prompt gerado* (meta-prompting) com a qualidade da execução posterior.
- Não há dados sobre o comprimento de saída do Claude 2026 sob instruções de concisão; os números citados são de modelos de 2024.
