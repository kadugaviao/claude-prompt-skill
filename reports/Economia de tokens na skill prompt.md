# Corte os tipos, troque o modelo, meça certo

Legenda usada em todo o relatório: **[fato]** = dito por fonte citada ou medido nos arquivos do repositório; **[inferência]** = conclusão tirada desses fatos; **[opinião]** = julgamento sem medição.

## 1. Resposta direta

Os dois métodos para testar primeiro são **trocar o modelo da skill para Sonnet 5.5 pelo frontmatter** (`model: sonnet`), que corta ~50% do custo de lista por execução, e **mover os 9 templates de "Tipos de tarefa" para arquivos lidos sob demanda**, que corta ~6–8% líquidos. Os dois funcionam com assinatura e sem infraestrutura nova. Antes de qualquer um, **fixe e registre o effort**: todas as execuções aprovadas rodaram em **medium**, não em high como dizem o harness e `resultados.md`, e esse é o baseline real de comparação.

## Os evals rodaram em effort medium, não high

**[fato]** `evals/rodar.py` grava `{'model': 'opus', 'effortLevel': 'high'}` no `settings.json` do HOME temporário, com o comentário "Opus com esforço alto". Mas a documentação do Claude Code diz que "a top-level `effortLevel` in user settings doesn't apply to Opus 5.5": essa chave é antiga e só vale para Opus 5, Fable 5.1 e anteriores. Os níveis por modelo agora ficam em `modelSettings`, e o padrão do Opus 5.5 é `medium` ([Model config](https://code.claude.com/docs/en/model-config)). As transcrições confirmam: em `evals/tmp-home/{v1,v2,v21,v22}/.claude/projects/*/*.jsonl` há **297, 372, 42 e 60 ocorrências de `"effort":"medium"` e nenhuma de `"high"`** (contagem refeita em 12/11/2026). O thinking por execução ficou em **170–625 tokens (média de 330 na v2.2)**, o que é coerente com medium.

**[inferência]** As aprovações registradas (v2 com 14/15 na rodada 3, validação com 4/4, v2.2 adotada) valem para **Opus 5.5 em medium**. Três consequências. Primeiro, qualquer teste de economia precisa comparar contra medium, ou vai confundir o efeito do método com o efeito de subir o effort. Segundo, um teste de `effort: low` mede a distância de um degrau só, não de dois. Terceiro, se o usuário real usa `/effort high` (salvo por modelo), a `/prompt` dele gasta mais e se comporta diferente do que foi validado. Para testar high de verdade é preciso `--effort high`, `CLAUDE_CODE_EFFORT_LEVEL=high` ou `modelSettings`. A ordem de precedência é: variável de ambiente > `/effort` na sessão > `--effort` > settings > padrão do modelo. O `effort` do frontmatter vale enquanto a skill roda e perde só para a variável de ambiente ([Model config](https://code.claude.com/docs/en/model-config)). **[opinião]** Corrija o comentário e a chave em `rodar.py` e passe a gravar o effort de cada execução no `.md` gerado, antes de rodar qualquer comparação nova.

## Escrita de cache a preço de 1 hora domina o custo, e o corpo da skill pesa ~29%

**[fato, dados locais]** O `total_cost_usd` do `claude -p` sai a preço de lista. Um ajuste sobre todas as execuções locais bate exatamente com US$ 8/M de escrita de cache de 1h, US$ 0,20/M de leitura e US$ 20/M de saída, que são os preços do Opus 5.5 ([Pricing](https://platform.claude.com/docs/en/about-claude/pricing)). Na assinatura, a conversa principal, incluindo execuções `-p`, usa TTL de 1 hora, e a escrita custa 2x a entrada ([Prompt caching](https://code.claude.com/docs/en/prompt-caching)). A média da v2.2 (5 casos) é **US$ 0,143 por execução: ~66% escrita de cache, ~28% saída (thinking ≈ 5%) e ~6% leitura**, com 2,4 requisições por execução. Cada caso roda numa fixture diferente, então diretório, git status e corpo da skill são reescritos (~11 mil tokens) a cada vez. Só ~11,4 mil tokens do system prompt vêm de cache de outra execução.

**[inferência]** O corpo injetado da v2.2 tem 10.984 caracteres. Comparando v1 e v2 nos mesmos 15 pedidos, a taxa fica em ~2,2 caracteres/token, o que dá **~4.800–5.000 tokens de corpo**, com "Tipos de tarefa" (~46% dos caracteres) em **~2.200–2.300 tokens**. Esse corpo custa ~US$ 0,041 por execução, **~29% do total**, e só os templates custam ~US$ 0,018 (~13%), dos quais 8/9 servem a tipos não usados. O "piso" do Claude Code (system prompt, 25 ferramentas, listagens) fica em ~17,5 mil tokens e não depende do autor da skill. Uma das notas de pesquisa estimou o corpo em apenas US$ 0,0002–0,004 por execução porque supôs entrada barata e cacheada. Os dados locais desmentem isso: a skill entra como escrita de cache de 1h, não como leitura. Sem API key não há `count_tokens`, então esses números são aproximados.

**[fato]** A Anthropic recomenda corpo de SKILL.md abaixo de 500 linhas e de ~5 mil tokens, e conteúdo específico em arquivos lidos "only as needed" ([Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview); [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)). A `/prompt` está no limite de tokens, embora bem abaixo do de linhas, e já usa `disable-model-invocation: true`, o que zera o custo da descrição por turno ([Claude Code: Skills](https://code.claude.com/docs/en/skills)).

## Tabela de métodos

| Método | Aplicável aqui? | Economia esperada | Efeito na qualidade (evidência) | Esforço | Como medir nos evals |
|---|---|---|---|---|---|
| **`model: sonnet` no frontmatter** | Sim. Uma linha. Em `-p` não há histórico, então a troca de modelo não custa cache extra. Numa sessão longa, o turno relê o histórico sem cache. | **~50% do custo de lista** [inferência a partir dos preços: Sonnet 5.5 custa metade do Opus 5.5 em todas as categorias]. Na assinatura, também poupa o limite específico de Opus [fato]. | Desconhecido para esta tarefa. A doc diz que Sonnet "handles most coding tasks well" [fato/opinião do fornecedor]. Não há benchmark público de reescrita de prompt. | Baixo | `rodar.py` nos 15 + 4 casos, `checar.py`, correção cega como em `comparar_versoes.py`. Confirmar o modelo em `modelUsage` do stream-json. |
| **`model: haiku`** | Sim, igual ao anterior. | **~97,5%** (1/40 do preço) [inferência] | Risco alto: na doc de effort, Haiku 5.5 em low "is more likely to skip a search, stop early, or skip a check" [fato]. No IFScale, modelos pequenos degradam exponencialmente com mais instruções [fato, modelos de 2025]. | Baixo | Igual. Olhar sobretudo C2, C7, tipo e "inventado". |
| **Progressive disclosure: templates em `tipos/<tipo>.md`** | Sim, é o padrão documentado ("Pattern 2"). Conflita com o limite de 3 leituras e com a regra de "Empate", que exige ler dois tipos. | Escrita de ~1.800–2.000 tokens a menos (~US$ 0,015), menos ~US$ 0,005–0,007 da leitura extra = **~6–8% líquido** [inferência] | Sem medição pública. A v1 tinha `tipos.md` separado e leu o arquivo em todas as execuções em que tentou [fato, `resultados.md`]. A D17 fundiu os arquivos. Hipótese de risco: perder o contraste entre tipos ao classificar [inferência]. | Médio | `checar.py` já exclui a leitura de `tipos.md` do C2. Medir C7/tipo, a nota cega e `cache_creation_input_tokens` da 1ª requisição. |
| **Corte manual de redundância (ablação por seção)** | Sim | Proporcional ao corte. Cada 1 mil tokens de corpo ≈ US$ 0,008 (~5,6%) [inferência] | IFScale: Claude recente fica em 94–100% até 50 instruções [fato], então encurtar não deve melhorar a qualidade. "Same Task, More Tokens" mostra queda com enchimento, mas em ~3 mil tokens irrelevantes [fato]. Exemplos sustentam formatos curtos (CoD few-shot vs zero-shot) [fato]. | Médio | Uma seção removida por rodada, com a régua da v2.2 (≥4/5, nenhum "inventado", nenhuma regressão contra v2.0) |
| **Encurtar a moldura de entrega (passo 5)** | Sim | A saída responde por ~28% (~2 mil tokens, ~US$ 0,04). O corte possível é uma fração disso [inferência] | Pedir concisão cortou 48,7% da saída com perda "negligible" em GPT-3.5/4 [fato, 2024]. A doc do Claude manda controlar o comprimento pelo prompt, não pelo effort [fato]. | Baixo | Tokens de saída no evento `result`. C6 (tetos de linhas) e o critério de enchimento. |
| **`effort: low` no frontmatter** | Sim | Teto pequeno: thinking é 5–9% do custo. Pode haver ganho extra com menos ferramentas e menos texto [inferência]. A Anthropic não publica percentuais [fato]. | Effort baixo leva a "fewer and terser tool calls" e menos verificação [fato]. Risco para o passo "Confira e entregue" [inferência]. | Baixo | C2, C5/conferência, nota cega. Thinking e saída no `usage`. |
| **`effort: medium` explícito no frontmatter** | Sim | Zero contra os evals. Evita gasto maior se o usuário usa `/effort high` [inferência] | Fixa o comportamento que foi validado [inferência] | Mínimo | Conferir `"effort":"medium"` nas transcrições |
| **TTL de cache 5m (`CLAUDE_CODE_PROMPT_CACHE_TTL=5m`)** | Sim (v2.1.242+). Vale para a sessão, não para a skill. | −37,5% na escrita, **~−25% do custo de lista** de uma execução isolada [inferência] | Nenhum na saída. Piora o reaproveitamento em sessões com pausas acima de 5 min [inferência]. Não se sabe como o limite da assinatura pondera escrita de 1h contra 5m [lacuna]. | Mínimo | Só muda o custo. Comparar `total_cost_usd` mantendo a qualidade igual. |
| **`context: fork` + subagente** | Parcial. Quebra o passo 6 (executar após aprovação), que depende da conversa principal. | Nenhuma em `-p`: o subagente paga o próprio system prompt e não lê o cache do pai [fato + inferência]. Ajuda só a tirar ~5 mil tokens do contexto de sessões longas. | Não medido | Médio | Exigiria um caso de sessão longa, que os evals atuais não têm |
| **Otimização automática estilo GEPA** | Só como laço próprio chamando `claude -p`. DSPy/LiteLLM com o token OAuth fere a política [fato]. | Os prompts do GEPA saíram até 9,2x mais curtos que os do MIPROv2 [fato]. Custo: ~US$ 45 para 20 candidatos × 15 casos; US$ 275–1.060 num orçamento de paper [inferência]. | GEPA: +10% sobre MIPROv2 [fato, outros benchmarks]. Risco de "ganhar" cortando conteúdo se a métrica for só mecânica [inferência]. | Alto | Métrica = aprovação no `checar.py` − λ·tokens, com `casos-validacao.tsv` como holdout |
| **Compressão automática (LLMLingua-2, Selective Context)** | Só offline, como rascunho. O resultado fica ilegível para quem mantém a skill. | 2–5x no papel [fato], medido em contextos longos | Em contexto curto, "all methods' performance decreases" e todos aumentam a alucinação [fato]. Tende a cortar palavras de controle ("não", números) [inferência]. | Médio | Não recomendado |
| **Soft prompts, gist tokens, 500xCompressor** | Não: exigem pesos, embeddings ou KV do modelo | — | — | — | — |
| **RAG vetorial / MCP de instruções** | Possível (MCP local funciona com OAuth), mas desproporcional para 9 seções fixas | Igual à progressive disclosure, com mais infraestrutura | RAG-MCP: −50% de tokens de prompt em seleção de ferramentas [fato, outro problema] | Alto | — |
| **Few-shot dinâmico recuperado** | Não há banco de exemplos. Criar um aumenta a entrada. | Negativa | KATE melhora a seleção, mas não reduz tokens [fato] | Alto | — |
| **Fine-tuning / destilação** | Não. O único Claude com fine-tuning no Bedrock é o Claude 3 Haiku (fim de vida relatado em 10/9/2026). Modelo customizado não roda como `model` de skill na assinatura. Exigiria AWS, GPU, dados e hospedagem. | — | Distilling step-by-step: T5 de 770M supera PaLM de 540B [fato, outra tarefa]. Com 19 casos, faltam dados [opinião]. | Muito alto | — |
| **Cascata barato→caro (FrugalGPT)** | Só improvisada: subagente Haiku e escalada para Opus se reprovar. Não há router nativo. | Até 98% no paper [fato, benchmarks de 2023]. Aqui depende da taxa de escalada. | Mantém GPT-4 no paper [fato] | Alto | Taxa de escalada × nota |

Duas alavancas já estão em uso e não devem ser desfeitas: `disable-model-invocation: true` e o limite "no máximo 3 leituras". Cada leitura extra custa uma requisição que relê ~23 mil tokens (~US$ 0,005) [inferência].

## O que a evidência externa não transfere

**[inferência]** Quase todos os números grandes da literatura vêm de cenários diferentes deste. LLMLingua (até 20x), LongLLMLingua e Selective Context foram medidos em RAG, reuniões e documentos longos, cheios de redundância ([arXiv 2310.05736](https://arxiv.org/abs/2310.05736); [arXiv 2403.12968](https://arxiv.org/abs/2403.12968)). O estudo empírico com Claude-3-Haiku conclui que, em contexto curto, a compressão sempre piora o resultado ([arXiv 2505.00019](https://arxiv.org/abs/2505.00019)). Chain of Draft corta o raciocínio para 7,6% dos tokens, mas é raciocínio visível em modelos sem thinking nativo. Em zero-shot, o Claude 3.5 Sonnet caiu de 90,4% para 65,5% no GSM8K ([arXiv 2502.18600](https://arxiv.org/html/2502.18600)). No Opus 5.5, o thinking é adaptativo, não pode ser desligado, e o effort é "the primary control" ([Effort](https://platform.claude.com/docs/en/build-with-claude/effort)). RouteLLM e FrugalGPT dão 35–98% de economia com roteamento, mas com routers aprendidos sobre GPT-4 ([LMSYS](https://lmsys.org/blog/2024-07-01-routellm/); [arXiv 2305.05176](https://arxiv.org/abs/2305.05176)). Aqui o roteamento seria estático, por skill, e a qualidade do Sonnet ou do Haiku nesta tarefa só a suíte local mede. Também falta saber como os limites da assinatura (5h, semanal, limite de Opus) ponderam cada tipo de token. A Anthropic diz só que o valor em dólar "isn't relevant for billing purposes" para assinantes e que leituras de cache "still draw usage" ([Manage costs](https://code.claude.com/docs/en/costs)). Por isso, cada comparação deve registrar tokens por categoria (escrita, leitura, saída, thinking), não só `total_cost_usd`.

## 3. Recomendação e ordem de testes

**Passo 0: corrigir a régua (confiança alta).** Troque `effortLevel` em `rodar.py` por `--effort medium` explícito ou por `modelSettings`, grave o effort e o modelo de cada execução no `.md` e rode a v2.2 de novo nos 5 casos da régua (12, 16–19) para ter um baseline de tokens e nota no mesmo harness. O porquê: a evidência é direta (doc + 771 registros de medium, nenhum de high), e sem isso toda comparação mistura variáveis. Observação [inferência]: `comparar_versoes.py` tem `FONTES` e `CASOS` fixos em v2.0/v2.1/v2.2, então cada candidato novo precisa de uma entrada lá.

**Teste 1: `model: sonnet` + `effort: medium` no frontmatter (confiança média de que mantém a nota; alta de que corta ~50%).** É uma linha, tem a maior economia viável e a orientação oficial aponta o Sonnet para a maior parte do trabalho. A dúvida é a qualidade em julgamento (classificar o tipo, não inventar conteúdo). Critério: a régua da v2.2 (≥4/5, nenhum "inventado" em falha, nenhuma regressão contra a v2.0) nos 15 + 4 casos. Se passar folgado, teste `model: haiku` (confiança baixa).

**Teste 2: templates em arquivos sob demanda (confiança média).** O padrão é documentado, a economia (~6–8%) é previsível pelos dados locais e o `checar.py` já não conta a leitura do tipo no C2. A confiança não é alta porque a própria história do projeto (D17) desfez essa separação, e o "Empate" exige duas leituras. Instrua a ler o arquivo do tipo fora do limite de 3 leituras e mantenha no SKILL.md a lista de nomes e os critérios de desempate.

**Teste 3: encurtar a moldura de entrega e cortar redundância por ablação (confiança média para a moldura, baixa para cortes no corpo).** Remova uma seção por rodada e meça tokens de saída e C6. Não espere ganho de qualidade com isso, só de custo.

**Teste 4: `effort: low` (confiança baixa).** O ganho máximo é pequeno (thinking ≈ 5–9%) e a doc liga effort baixo a menos verificação. Só vale se os testes 1–2 deixarem margem na nota.

**Para os evals, não para a skill: `CLAUDE_CODE_PROMPT_CACHE_TTL=5m` (confiança média).** Corta ~25% do custo de lista de cada execução isolada sem mexer na saída. Mas não se sabe se reduz o consumo do limite da assinatura. **Não testar:** compressão automática, soft prompts, RAG vetorial, fine-tuning e otimização automática em escala. Ou faltam acesso e infraestrutura, ou o custo em rollouts estoura os limites, ou a evidência é contrária para instruções curtas. **[opinião]** Um laço no estilo GEPA com ~20 candidatos só se justifica depois que os testes 1–3 estabilizarem a régua.

## Conclusão

O ponto que muda o quadro é este: o maior custo desta skill não é "ler instruções", é **reescrevê-las no cache a preço de 1 hora em toda execução**. Por isso o tamanho do corpo pesa mais do que a intuição de "entrada cacheada é barata" sugere, e a escolha do modelo pesa mais do que qualquer truque de texto. A outra consequência é de método: a v2.2 foi aprovada em medium, e quem comparar uma versão enxuta contra uma suposta régua em high vai atribuir ao corte uma perda que vem do effort, ou vice-versa. Medir de novo com o effort fixo vem antes de qualquer otimização.

## 4. Fontes

As páginas de documentação não mostram data de publicação. A data indicada nelas é a de acesso (12/11/2026), e o comportamento descrito vale para o Claude Code v2.1.3xx usado nos evals.

- Anthropic, Claude Code: Skills, https://code.claude.com/docs/en/skills (acesso 12/11/2026)
- Anthropic, How Claude Code uses prompt caching, https://code.claude.com/docs/en/prompt-caching (acesso 12/11/2026)
- Anthropic, Manage costs effectively, https://code.claude.com/docs/en/costs (acesso 12/11/2026)
- Anthropic, Model config, https://code.claude.com/docs/en/model-config (acesso 12/11/2026)
- Anthropic, Subagents, https://code.claude.com/docs/en/sub-agents (acesso 12/11/2026)
- Anthropic, Authentication, https://code.claude.com/docs/en/authentication (acesso 12/11/2026)
- Anthropic, Agent SDK overview, https://code.claude.com/docs/en/agent-sdk/overview (acesso 12/11/2026)
- Anthropic, Agent Skills overview, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview (acesso 12/11/2026)
- Anthropic, Skill authoring best practices, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices (acesso 12/11/2026)
- Anthropic, Effort, https://platform.claude.com/docs/en/build-with-claude/effort (acesso 12/11/2026)
- Anthropic, Pricing, https://platform.claude.com/docs/en/about-claude/pricing (acesso 12/11/2026)
- Anthropic Engineering, Equipping agents for the real world with Agent Skills, https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills (16/10/2025)
- Anthropic, Prompt improver, https://www.anthropic.com/news/prompt-improver (out/2024)
- Jiang et al., LLMLingua, https://arxiv.org/abs/2310.05736 (9/10/2023)
- Pan et al., LLMLingua-2, https://arxiv.org/abs/2403.12968 (19/3/2024)
- Zhang et al., estudo empírico de compressão de prompt, https://arxiv.org/abs/2505.00019 (abr/2025)
- Kummer et al., Prompt Compression in the Wild, https://arxiv.org/abs/2604.02985 (3/4/2026)
- Jaroslawicz et al., IFScale, https://arxiv.org/html/2507.11538 (15/7/2025)
- Levy, Jacoby, Goldberg, Same Task, More Tokens, https://arxiv.org/html/2402.14848 (19/2/2024)
- Xu et al., Chain of Draft, https://arxiv.org/html/2502.18600 (25/2/2025)
- Renze & Guven, Concise CoT, https://arxiv.org/abs/2401.05618 (jan/2024, v3 out/2024)
- Gema et al., Inverse Scaling in Test-Time Compute, https://arxiv.org/abs/2507.14417 (19/7/2025)
- Chen, Zaharia, Zou, FrugalGPT, https://arxiv.org/abs/2305.05176 (9/5/2023)
- LMSYS, RouteLLM, https://lmsys.org/blog/2024-07-01-routellm/ (1/7/2024); paper https://arxiv.org/abs/2406.18665 (26/6/2024)
- Agrawal et al., GEPA, https://arxiv.org/abs/2507.19457 (25/7/2025)
- Opsahl-Ong et al., MIPRO, https://arxiv.org/abs/2406.11695 (17/6/2024)
- RAG-MCP, https://arxiv.org/abs/2505.03275 (6/5/2025)
- Liu et al., KATE, https://arxiv.org/abs/2101.06804 (17/1/2021)
- Hsieh et al., Distilling step-by-step, https://arxiv.org/abs/2305.02301 (3/5/2023)
- AWS, Bedrock: supported models for fine-tuning, https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-supported.html (acesso 12/11/2026)
- AWS, fine-tuning do Claude 3 Haiku GA, https://aws.amazon.com/about-aws/whats-new/2024/11/fine-tuning-anthropics-claude-3-haiku-amazon-bedrock (nov/2024)
- The Register, Anthropic clarifies ban on third-party Claude access, https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access (20/2/2026)
- Dados locais: `evals/rodar.py` (linha 35), `evals/runs-{3,val,v22}/raw/*.jsonl`, `evals/tmp-home/*/.claude/projects/*/*.jsonl`, `evals/resultados.md`, `v2/prompt/SKILL.md` (contagens de 12/11/2026)
