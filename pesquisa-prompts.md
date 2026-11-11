# Padrões de escrita de prompts e boas práticas (nov/2026): base de pesquisa para a skill /prompt

Nos modelos atuais (Claude Fable 5.2/Opus 5.5, GPT-6 Astra, Gemini 3.x), a regra que vale é esta: o prompt bom é um briefing claro, enxuto e verificável. Ele diz objetivo, contexto com o porquê, escopo, critério de pronto e formato de saída. Truques de 2023 não fazem mais esse papel: persona elaborada, CAIXA ALTA, "pense passo a passo", prefill, gorjeta ou ameaça. A skill /prompt deve, portanto, montar um briefing, não "turbinar" o texto com técnicas. Ela também precisa evitar copiar a receita dos prompt improvers de 2024, que hoje está parcialmente obsoleta.

## TL;DR

- **O que funciona, com consenso entre Anthropic, OpenAI, Google e a pesquisa:** instruções claras e explícitas, contexto com o motivo de cada regra, exemplos bem escolhidos, separação estrutural (tags XML ou seções), formato de saída especificado e critério de pronto e verificação. Em contexto longo (~20 mil tokens ou mais, segundo a Anthropic), os documentos vão no topo e a pergunta no fim. Também ajuda calibrar o esforço de raciocínio pelo parâmetro da API, e não por texto no prompt.
- **O que deixou de valer:** CoT manual ("pense passo a passo") em modelos com raciocínio embutido, que tem ganho marginal, custo de 20–80% a mais de tempo e pode até ser recusado nos Claude mais novos. Também caíram a ênfase agressiva ("CRITICAL: You MUST"), que agora causa *overtriggering*, e o prefill, que dá erro 400 a partir do Claude 4.6. Personas "você é um especialista" e gorjetas ou ameaças não melhoram a acurácia em estudos controlados da Wharton GAIL (2025): segundo o PSR 4 (arXiv 2512.05858), "persona prompts generally did not improve accuracy relative to a no-persona baseline", e segundo o PSR 3 (arXiv 2508.00614), "threatening or tipping a model generally has no significant effect on benchmark performance".
- **Para a skill /prompt:** gerar um prompt com objetivo na primeira linha, depois contexto, insumos, escopo, restrições com motivo, critério de pronto, política de autonomia (perguntar vs. assumir) e formato de saída padronizado por tipo de tarefa. Perguntar só quando a resposta mudaria materialmente o resultado; fora disso, assumir e listar as suposições. Manter o prompt curto e de alto sinal.

## Key Findings

### A. Princípios consolidados (onde fontes oficiais e pesquisa concordam)

| # | Princípio | Por quê | Fontes | Confiança |
|---|---|---|---|---|
| 1 | **Ser claro, específico e explícito.** Diga o que quer, incluindo o "ir além" se for o caso. | Os modelos atuais seguem instruções de forma mais literal. A Anthropic propõe o "teste do colega": se um colega sem contexto ficaria confuso, o modelo também ficará. | Anthropic, Prompting best practices; OpenAI, GPT-5/GPT-6 guides; Google, Gemini 3 ("responde melhor a instruções diretas e claras") | Alta |
| 2 | **Explicar o porquê das regras.** | O modelo generaliza a partir da justificativa. No exemplo da Anthropic, "NEVER use ellipses" funciona pior do que explicar que a saída vai para um sintetizador de voz. | Anthropic, Prompting best practices | Alta, mas a evidência é de fornecedor |
| 3 | **Dizer o que fazer, não o que evitar.** | Instruções positivas direcionam melhor o formato. Boonstra (Google) chama isso de "Use Instructions over Constraints". | Anthropic; Boonstra, whitepaper Google (fev/2025) | Média-alta |
| 4 | **Exemplos (few-shot) relevantes, diversos e delimitados.** | Os exemplos estão entre as formas mais confiáveis de fixar formato e tom. A Anthropic recomenda 3–5, dentro de `<example>`. O Google recomenda "sempre incluir" exemplos. A ressalva: exemplos são copiados com fidelidade, inclusive nos defeitos. | Anthropic; Google, Prompt design strategies; Boonstra | Alta para formato e estilo; média para raciocínio |
| 5 | **Separar estruturalmente instruções, contexto, dados e exemplos** (tags XML ou seções Markdown). | Reduz a ambiguidade em prompts que misturam tipos de conteúdo. | Anthropic (XML); OpenAI (meta-prompt em Markdown; delimitadores); Google (ordem, rótulos e delimitadores "afetam a qualidade") | Alta |
| 6 | **Especificar o formato de saída**, incluindo comprimento, estrutura e esquema. | É a alavanca mais barata de consistência. O GPT-5.2 segue bem limites concretos, como "3–6 frases ou ≤5 bullets". O Google lista como erro comum "deixar o modelo adivinhar a estrutura". | OpenAI GPT-5.1/5.2 guides; Google; Boonstra ("Be specific about the output") | Alta |
| 7 | **Em contexto longo (~20 mil tokens ou mais), documentos no topo e pergunta no fim**, com metadados em tags e citações extraídas antes da análise. | A Anthropic relata ganho de "até 30%" com a pergunta no fim em entradas multidocumento. O Google recomenda o mesmo padrão para o Gemini 3. A pesquisa mostra degradação com contexto longo ("lost in the middle", Liu et al., TACL 2024; "Context Rot", Chroma, 2025). | Anthropic; Google; Liu et al.; Chroma | Alta |
| 8 | **Dar ao modelo como verificar o próprio trabalho** (testes, critérios, comandos). | Em tarefas autônomas longas, o critério de pronto substitui o feedback humano. "Give Claude a way to verify its work" abre o guia de boas práticas do Claude Code. | Anthropic, Claude Code best practices e Prompting best practices; OpenAI GPT-6 | Alta |
| 9 | **Contexto é recurso finito: o menor conjunto de tokens de alto sinal.** | "Context engineering" (Anthropic, 29/09/2025) recomenda recuperação just-in-time, compactação, notas estruturadas e subagentes. A OpenAI relata que prompts de sistema mais enxutos em agentes de código melhoraram as notas de avaliação em cerca de 10–15% e reduziram tokens em 41–66%. A própria OpenAI chama esses números de "direcionais". | Anthropic, Effective context engineering; OpenAI, Using GPT-5.6 (via Count.co) | Alta para o princípio; média para os números |
| 10 | **Iterar com avaliação (evals), não por intuição.** | A sensibilidade a variações é alta e imprevisível por pergunta. Wharton mostra oscilações de até ±35% por questão. Sclar et al. (ICLR 2024) mediram, em cenário few-shot, até 76 pontos de diferença entre formatações equivalentes no LLaMA-2-13B. | Wharton PSR 1–4 (2025); Sclar et al. 2024; OpenAI e Anthropic (seções de evals); Boonstra ("Document the various prompt attempts") | Alta |

### B. Divergências e o que mudou em 2025–2026

**1. Chain-of-thought explícito: deixou de valer nos modelos com raciocínio.**
- OpenAI (Reasoning best practices): "Avoid chain-of-thought prompts", porque pedir "think step by step" é desnecessário e pode atrapalhar.
- Google (Gemini 3): migrar o CoT de prompt para `thinking_level: "high"` com prompts simplificados.
- Anthropic: prefira instruções gerais ("think thoroughly") a planos passo a passo escritos à mão. O CoT manual fica como *fallback* para quando o thinking está desligado. No Claude Fable 5.x, no Opus 5/5.5 e no Sonnet 5.5, pedir que o modelo escreva o raciocínio na resposta (por exemplo, em tags `<thinking>`) "might be declined": existe até a categoria de recusa `reasoning_extraction`.
- Evidência: Wharton (Prompting Science Report 2, 08/06/2025, arXiv 2506.07142) achou ganhos pequenos e mais variância em modelos sem raciocínio. Nos modelos de raciocínio testados no GPQA Diamond (o3-mini, o4-mini e Gemini 2.5 Flash; 198 questões, 25 tentativas cada), o relatório conclui que "CoT prompting often results in only marginal, if any, gains… However, it significantly increases the time and tokens", com 20–80% a mais de tempo.
- Na skill: nunca inserir "pense passo a passo" nem pedir o raciocínio na saída. Se a tarefa for difícil, sugerir subir o *effort*.

**2. Ênfase em CAIXA ALTA e linguagem agressiva: agora atrapalha.**
- A Anthropic diz que modelos desde o Opus 4.5 são mais responsivos ao system prompt. "CRITICAL: You MUST use this tool" passou a causar overtriggering, e a orientação é usar linguagem normal.
- No Fable 5.2, regras rígidas de estilo como "20 palavras ou menos" deixam a prosa picotada, e regras "nunca" acumuladas em memórias e notas tornam o agente excessivamente cauteloso.
- Exceção pontual: o guia de Realtime (voz) da OpenAI ainda recomenda capitalizar regras-chave. Não generalize isso para texto e código.

**3. Prefill: removido.** A partir dos modelos Claude 4.6, o prefill no último turno do assistente retorna erro 400. Formato e supressão de preâmbulo agora se resolvem com instrução direta ou structured outputs.

**4. Personas ("Você é um especialista…"): a pesquisa e a documentação divergem.**
- A Anthropic e o Google continuam recomendando definir um papel no system prompt, para foco e tom.
- Wharton (PSR 4, 07/12/2025, arXiv 2512.05858; seis modelos, GPQA Diamond e MMLU-Pro) concluiu que "persona prompts generally did not improve accuracy relative to a no-persona baseline"; a única exceção nomeada para personas especialistas no próprio domínio foi o Gemini 2.0 Flash. Personas de baixo conhecimento pioram, e personas fora do domínio às vezes pioram.
- Zheng et al. (arXiv 2311.10054) testaram personas em system prompts e acharam efeitos sem significância. Prompts que descrevem a *audiência* funcionaram um pouco melhor do que prompts que descrevem o *falante*.
- Síntese: use no máximo uma linha de papel ou contexto para tom e escopo, e invista o esforço em contexto, critérios e exemplos. Confiança alta para "persona não aumenta acurácia"; média para "persona ajuda no tom".

**5. Gorjeta, ameaça e apelo emocional: sem efeito.** Wharton (PSR 3, 01/08/2025) testou a afirmação que Sergey Brin fez no podcast All-In (maio/2025) de que "models tend to do better if you threaten them" e não encontrou efeito agregado significativo, com oscilações imprevisíveis por questão. Confiança alta.

**6. XML vs. Markdown: uma diferença de convenção, não de princípio.**
- Anthropic: XML para separar componentes.
- OpenAI: o meta-prompt oficial gera Markdown (`# Steps`, `# Output Format`, `# Examples`, `# Notes`), e os guias do GPT-5 usam blocos com tags.
- Google: pede estrutura consistente.
- Detalhe útil da Anthropic: o estilo do prompt contamina o estilo da saída. Menos Markdown no prompt resulta em menos Markdown na resposta.
- Recomendação: seções com cabeçalhos Markdown para as instruções e tags XML para insumos (código, logs, documentos). Confiança média, por falta de estudo comparativo direto nos modelos atuais.

**7. Exemplos vs. instruções.** O Google é o mais pró-exemplos ("always include"). Para modelos de raciocínio, a OpenAI sugere tentar zero-shot primeiro. A Anthropic avisa que os modelos novos imitam detalhes dos exemplos, inclusive os indesejados. Na skill, inclua exemplos só quando o formato for não óbvio ou o usuário fornecer um.

**8. Verbosidade e verificação: o comportamento varia por modelo, e instruções antigas podem virar ruído.**
- Claude Opus 5 é mais verboso e verifica o próprio trabalho sem pedir. Instruções de "verifique" herdadas de prompts antigos causam *over-verification*, e a Anthropic recomenda removê-las.
- GPT-6 Astra testa bastante por conta própria. A OpenAI recomenda calibrar o volume de testes ao tamanho da mudança e revisar AGENTS.md e skills, porque "prior models needed encouragement to run tests… the same instructions can lead to unnecessary testing".
- O Gemini 3 é menos verboso por padrão.
- Claude Fable 5.2: instruções do tipo "responda sem deliberar" não impedem o thinking a partir do esforço *medium*. Use o parâmetro `effort`.

**9. Autonomia: perguntar vs. agir.**
- O GPT-6 Astra tende a perguntar quando a informação faltante "could materially change the result". O guia sugere tratar "can you…/help me…" como pedido de ação e pedir aprovação apenas sobre "a concrete, reviewable result".
- O Claude, por sua vez, só *sugere* se você escrever "can you suggest changes". Para ele implementar, a instrução tem de ser imperativa.
- O Fable 5.2 às vezes encerra cedo em tarefas longas, e a Anthropic fornece um bloco "Finishing work".

**10. Parâmetros de amostragem.** O Gemini 3 pede temperatura 1.0, porque valores menores podem causar loops. O Gemini 3.6+ e o 4 ignoram temperature, top_p e top_k. A recomendação clássica de "temperatura 0.2" (Boonstra, 2025) não vale mais para eles.

**Diferenças práticas entre fornecedores (resumo):**

| Tema | Claude (Anthropic) | GPT (OpenAI) | Gemini (Google) |
|---|---|---|---|
| Delimitação | Tags XML | Markdown e tags | Delimitadores e estrutura consistente |
| Raciocínio | Adaptive thinking e `effort`; pedir o raciocínio na saída pode ser recusado | `reasoning_effort`; evitar CoT no prompt | `thinking_level`; simplificar o prompt |
| Exemplos | 3–5, em `<example>` | Zero-shot primeiro em modelos de raciocínio | "Sempre incluir" |
| Prefill | Removido (4.6+) | Não se aplica | Não se aplica |
| Comportamento típico | Literal; tende a overengineering (Opus 4.5/4.6); ownership do código muda o escopo (Fable 5.2) | Astra pergunta mais e testa mais; é sensível a AGENTS.md e skills | Conciso por padrão; temperatura fixa |

### C. Frameworks de prompt: comparação

Nenhum desses frameworks tem validação experimental robusta. São mnemônicos de praticantes. O único estudo encontrado que compara CO-STAR e RISEN (arXiv 2603.29953, 2026) achou diferenças mínimas (+0,05 ponto) e não controlou o tamanho do prompt. A Prompt Report (Schulhoff et al., arXiv 2406.06608, versão de 26/02/2025; revisão sistemática PRISMA de 1.565 artigos, com taxonomia de 58 técnicas de texto, 40 técnicas para outras modalidades e vocabulário de 33 termos) cataloga *técnicas*, não esses acrônimos.

| Framework | Componentes | Serve para | Pontos fortes | Pontos fracos | Evidência |
|---|---|---|---|---|---|
| **CO-STAR** | Context, Objective, Style, Tone, Audience, Response | Texto e comunicação | Separa estilo, tom e audiência; força o formato da resposta | Não tem critério de pronto, verificação nem escopo; é fraco para código e agentes | Venceu uma competição (GovTech Singapura, Sheila Teo, 2023); anedótica |
| **RISEN** | Role, Instructions, Steps, End goal, Narrowing | Processos sequenciais | "End goal" e "Narrowing" equivalem a pronto e escopo | "Steps" prescritivos conflitam com modelos de raciocínio; Role tem valor baixo | Nenhuma controlada |
| **RTF** | Role, Task, Format | Pedidos rápidos | Mínimo viável | Sem contexto nem critérios | Nenhuma |
| **CRISPE** | Capacity/Role, Insight, Statement, Personality, Experiment | Copy e criação com variações | "Experiment" pede variantes | Persona demais; impreciso para técnica | Nenhuma (origem em listas comunitárias) |
| **CARE** | Context, Action, Result, Example | Tarefas gerais | Inclui resultado esperado e exemplo | Pouco sobre formato e restrições | Nenhuma |
| **TAG** | Task, Action, Goal | Pedidos curtos | Simples | Redundante e raso | Nenhuma |
| **APE (acrônimo)** | Action, Purpose, Expectation | Pedidos curtos | Inclui o propósito (o "porquê") | Raso. Não confundir com APE = Automatic Prompt Engineer (Zhou et al.) | Nenhuma |

**Leitura crítica:** os frameworks acertam ao forçar contexto, objetivo e formato, que são os princípios 1, 2 e 6. Erram por ênfase: dão peso a persona, tom e passos, e não cobrem o que mais importa em agentes de código, ou seja, escopo, critério de pronto, verificação, autonomia e fontes da verdade. Não empilhe frameworks. Para a skill, o melhor "framework" é o esqueleto implícito nos guias oficiais de 2026, detalhado na seção G.

## Details

### D. Padrões por tipo de tarefa

Todos os tipos usam o mesmo esqueleto (seção G). A tabela mostra só o que muda.

| Tipo | O prompt deve conter | Formato de saída a pedir |
|---|---|---|
| **Implementar código** | Comportamento esperado e critérios de aceite; arquivos e módulos relevantes (referenciar, não colar tudo); convenções do projeto (Spring Boot: camadas, DTOs, testes JUnit/Mockito; Python: tipagem, pytest); escopo explícito contra overengineering ("não adicione abstrações e configurabilidade não pedidas"); comando de teste e build para verificar; ownership do código, se refatorar for desejado (Fable 5.2) | Resumo de 1–3 frases; arquivos alterados e o porquê; como foi verificado (comandos e resultados); riscos e pendências |
| **Corrigir bug** | Sintoma, passos de reprodução, stack trace e logs dentro de tags; esperado vs. obtido; ambiente e versões; o que já foi tentado; pedido de causa raiz, não só do sintoma; proibição de "ajustar o teste para passar" ou fixar valores em código | Causa raiz com evidência; correção mínima (diff); teste que reproduz e passa; efeitos colaterais possíveis |
| **Revisar ou auditar** | O que revisar (diff, PR, módulo); critérios (segurança, concorrência, transações, N+1, tratamento de erros); severidades; "não altere código" quando for só revisão; investigar antes de afirmar | Lista de achados por severidade (crítico, alto, médio, baixo) com arquivo:linha, problema, evidência e sugestão; veredito final |
| **Pesquisar ou comparar** | Pergunta de decisão; critérios de comparação e pesos; restrições (licença, custo, compatibilidade com Java 21 ou Spring Boot 3, por exemplo); exigência de fontes primárias com data; separar fato, inferência e opinião | Resposta direta primeiro; tabela comparativa; recomendação com nível de confiança; fontes com data |
| **Explicar ou ensinar** | Nível do leitor (a audiência, que tem mais suporte empírico do que persona); o que já sabe; profundidade e comprimento; uso de exemplo de código do contexto do usuário | Resumo em 2–3 frases, explicação progressiva, exemplo mínimo executável e armadilhas comuns |
| **Escrever texto** | Audiência, objetivo, tom (aqui o estilo do CO-STAR é útil); comprimento-alvo; exemplos de estilo, se houver; palavras e clichês a evitar (a OpenAI publicou uma lista de "slop words" para o GPT-6 Astra) | O texto final, sem meta-comentário; variantes só se pedidas |
| **Analisar dados** | Esquema e amostra dos dados, ou caminho do arquivo; pergunta de negócio; como calcular (ou pedir para executar código, em vez de calcular "de cabeça"); tratamento de nulos e outliers | Achados principais primeiro; tabela de números; método e código usados; limitações |
| **Planejar ou decidir** | Objetivo, restrições, alternativas já consideradas, critérios de decisão, horizonte; pedir premissas explícitas | Recomendação; opções com prós e contras; riscos; próximos passos; o que mudaria a decisão |
| **Agêntica longa** | Objetivo e critério de pronto verificável; arquivos de estado (progress.txt, tests.json, git); permissões (o que pode fazer sem perguntar e o que exige confirmação, como push, migrações e deleções); bloco "terminar a tarefa"; atualizações de progresso; política de subagentes | Atualizações curtas durante o trabalho; relatório final autocontido para um leitor sem contexto, com resultado na primeira frase, o que foi feito, verificação e pendências |

### E. Anti-padrões (com evidência)

1. **"Pense passo a passo" e pedir o raciocínio na saída** em modelos com raciocínio: ganho marginal, custo alto, possível recusa no Claude. Fontes: OpenAI, Google, Anthropic; Wharton PSR 2.
2. **CAIXA ALTA e "CRITICAL/MUST"**: overtriggering nos Claude atuais. Fonte: Anthropic.
3. **Persona elaborada como alavanca de qualidade**: sem ganho de acurácia; personas "leigas" pioram. Fontes: Wharton PSR 4; Zheng et al.
4. **Gorjeta, ameaça e "isso é muito importante para minha carreira"**: sem efeito agregado. Fonte: Wharton PSR 3.
5. **Prefill**: erro 400 a partir do Claude 4.6.
6. **Instruções herdadas de modelos antigos**, como "sempre verifique", "use subagentes", "se em dúvida, use a ferramenta X", orçamento de tokens escrito no prompt ou "responda sem pensar": causam over-verification, delegação excessiva, overtriggering e custo maior. Fontes: Anthropic (Opus 5, Fable 5.2); OpenAI (GPT-6 Astra).
7. **Regras negativas absolutas sem motivo e cautelas acumuladas** em memória, notas e CLAUDE.md: o modelo segura trabalho rotineiro. No teste da Anthropic, uma única nota "nunca tente de novo" derrubou as novas tentativas de quase 100% para cerca de 40%.
8. **"Você pode sugerir…" quando se quer ação**: o Claude só sugere. Fonte: Anthropic.
9. **Contexto inchado** (colar o repositório, histórico irrelevante): degradação por contexto longo e custo. Fontes: Anthropic (context engineering); Chroma; Liu et al.
10. **Empilhar frameworks e seções vazias**: mais tokens sem sinal; conflitos de instrução são especialmente danosos no GPT-6 Astra.
11. **Formato ambíguo**: o modelo adivinha a estrutura. Fonte: Google.
12. **Aprovações vagas**: o Fable 5.2 aplica regras de aprovação literalmente. Nomeie as ações exatas.

### F. Como funcionam os meta-prompts e prompt improvers oficiais

**Anthropic Console Prompt Improver (lançado em 14/11/2024; aposentado junto com o Workbench legado em 17/08/2026).** Rodava em quatro etapas:
1. *Example identification*: extrai os exemplos do template.
2. *Initial draft*: cria um template estruturado com seções e tags XML.
3. *Chain of thought refinement*: adiciona instruções detalhadas de raciocínio.
4. *Example enhancement*: reescreve os exemplos para demonstrar o novo raciocínio.

O resultado trazia instruções de CoT detalhadas, organização em XML, exemplos padronizados e "strategic prefills". O lançamento citava +30% de acurácia em classificação multirrótulo (no Claude 3 Haiku) e 100% de aderência a contagem de palavras em sumarização. A própria documentação admitia o trade-off: "longer, more thorough, but slower responses".

**Leitura crítica:** dois dos quatro ingredientes estão obsoletos para os modelos atuais. CoT escrito no prompt é desaconselhado e pode ser recusado; prefill dá erro 400. Os ganhos medidos eram em Claude 3 Haiku. **A skill /prompt não deve reproduzir essa receita.** Deve aproveitar o que segue válido: extrair e preservar o que o usuário já deu, estruturar em seções e tags, padronizar exemplos e aceitar feedback sobre problemas observados.

**Anthropic Metaprompt (cookbook, 2024).** É um prompt longo, multi-shot, com cerca de seis exemplos de bons prompts. Abre com "Today you will be writing instructions to an eager, helpful, but inexperienced and unworldly AI assistant…" e segue três passos:
1. Listar em `<Inputs>` o conjunto mínimo e não sobreposto de variáveis.
2. Planejar em `<Instructions Structure>` a ordem das instruções, com variáveis longas antes das diretrizes sobre elas.
3. Escrever em `<Instructions>`.

O lembrete final é que você não está executando a tarefa, está escrevendo o prompt.

**OpenAI Prompt Generation (meta-prompt, out/2024).** Seu princípio declarado: "Given a task description or existing prompt, produce a detailed system prompt…". As diretrizes centrais:
- *Minimal Changes*: melhorar só prompts simples; em prompts complexos, apenas clarear e completar.
- *Preserve User Content*.
- *Reasoning Before Conclusions*: conclusões sempre por último. Ainda é útil em saídas estruturadas de modelos sem raciocínio e irrelevante quando o raciocínio é interno.
- Exemplos com placeholders.
- *Clarity and Conciseness*: sem instruções genéricas.
- *Constants*: rubricas e guias dentro do prompt.
- *Output Format* detalhado, com viés para JSON em dados estruturados.

A estrutura gerada tem: primeira linha com a tarefa, sem cabeçalho; detalhes; `# Steps` (opcional); `# Output Format`; `# Examples` (1–3, opcional); `# Notes` (casos de borda). Há variantes de edição que classificam a complexidade do prompt de entrada (1–5).

**OpenAI Prompt Optimizer (dashboard).** Otimiza "according to current best practices" e, idealmente, usa um dataset com anotações boas e ruins, críticas escritas e resultados de graders. A documentação avisa que o prompt otimizado pode "perform worse than your original on specific inputs" e que a eficácia depende da qualidade dos graders. A versão baseada em dataset está sendo descontinuada junto com a plataforma Evals, que fica read-only em 31/10/2026 e encerra em 30/11/2026. A OpenAI aponta o Promptfoo como caminho de migração.

**Google (Boonstra, fev/2025).** O whitepaper lista: Provide examples; Design with simplicity; Be specific about the output; Use Instructions over Constraints; Control the max token length; Use variables in prompts; Experiment with input formats and writing styles; For few-shot classification, mix up the classes; Adapt to model updates; Experiment with output formats; JSON Repair; Working with Schemas; Experiment together with other prompt engineers; CoT best practices; Document the various prompt attempts. Também descreve Automatic Prompt Engineering, em que um LLM gera candidatos que depois são pontuados.

**O que os improvers acrescentam, em síntese:**
1. Estrutura (seções e tags).
2. Formato de saída explícito.
3. Exemplos padronizados.
4. Variáveis e placeholders.
5. Notas de casos de borda.
6. Historicamente, CoT e prefill, hoje obsoletos.

O que **não** acrescentam e a skill deve acrescentar: critério de pronto, verificação, política de autonomia, escopo e contexto do projeto. Esses são justamente os temas dominantes dos guias de 2026.

**Otimização automática na pesquisa (APE, OPRO, DSPy, TextGrad).** Esses métodos otimizam prompts contra uma métrica, o que exige um dataset e um avaliador. A lição para a skill é indireta: um improver sem avaliação é uma heurística. Os métodos não foram aprofundados nesta pesquisa.

## Recommendations

### G. Recomendações concretas para a skill /prompt

**1. Estrutura do prompt gerado** (confiança alta para os elementos; média para a ordem e os rótulos exatos). Use cabeçalhos Markdown para as seções e tags XML para insumos colados:

```
<Objetivo em 1–2 frases, na primeira linha, no imperativo>

## Contexto
Por que isso importa, onde se encaixa no projeto, stack/versões relevantes.

## Insumos
<arquivos> caminhos a ler (preferir referência a colar) </arquivos>
<log>/<erro>/<trecho> só o essencial </log>

## Tarefa e escopo
O que fazer. O que está fora do escopo (e por quê).

## Restrições
Cada regra com seu motivo. Convenções do projeto que se aplicam.

## Critério de pronto e verificação
Condições observáveis; comandos de teste/build; o que NÃO fazer para "passar" (ex.: não editar testes).

## Autonomia
Pode fazer sem perguntar: ... | Pergunte antes de: ... (ações destrutivas/irreversíveis nomeadas).
Suposições assumidas: ... (o executor deve sinalizar se alguma estiver errada)

## Formato da resposta
Template específico do tipo de tarefa (seção D).
```

Omita as seções vazias. Não inclua persona longa: no máximo uma linha de papel, e só quando o tom importar. Não inclua "pense passo a passo", tags `<thinking>`, CAIXA ALTA, gorjeta nem prefill.

**2. Perguntar vs. assumir** (confiança média-alta):
- Pergunte apenas quando a resposta mudaria materialmente o resultado e não puder ser descoberta lendo o projeto. Exemplos: qual de dois comportamentos de negócio é o correto, ou se uma ação destrutiva está autorizada.
- Faça no máximo 1–3 perguntas, de uma vez, com opções sugeridas.
- No mais, assuma o default mais provável, liste as suposições na seção "Autonomia" e instrua o executor a investigar com ferramentas antes de adivinhar.
- Isso segue a orientação da Anthropic ("infer the most useful likely action… using tools to discover any missing details instead of guessing") e o comportamento documentado do GPT-6 Astra.

**3. Padronizar o formato de saída por tipo** (confiança alta):
- Classifique o pedido em um dos 9 tipos da seção D e injete o template correspondente.
- Em todo tipo, a primeira frase da resposta deve responder "o que aconteceu ou o que foi encontrado", como nos guias do Opus 5 e do Fable 5.2.
- Dê limites de comprimento concretos, que funcionam melhor do que "seja conciso".
- Para saída consumida por máquina, peça JSON ou um schema, ou use structured outputs.

**4. Contexto do projeto** (confiança alta):
- Leia o CLAUDE.md, a estrutura do repositório e o `pom.xml`/`build.gradle`/`pyproject.toml`, e referencie os arquivos por caminho em vez de colá-los (recuperação just-in-time).
- Inclua só convenções que mudam o resultado. Use o teste da Anthropic para cada linha: "Would removing this cause Claude to make mistakes?".
- Não duplique no prompt o que já está no CLAUDE.md, que já é carregado automaticamente.

**5. Tamanho ideal** (confiança média, porque não há número empírico universal):
- Proporcional à complexidade. Cerca de 5–15 linhas para tarefas simples e cerca de 30–80 linhas para tarefas agênticas longas.
- Acima disso, mova o conteúdo para arquivos referenciados.
- Prefira cortar a acrescentar: prompts enxutos foram melhores e mais baratos nos testes da OpenAI com agentes de código, e o guia de context engineering da Anthropic sustenta o mesmo princípio.

**6. Comportamento da própria skill:**
- Preserve integralmente o que o usuário escreveu (identificadores, nomes de classes, mensagens de erro). Esse é o princípio "Preserve User Content" da OpenAI.
- Mostre o prompt gerado para aprovação antes de executar, com a opção de "executar direto".
- Não acrescente instruções de "verifique tudo" nem de "use subagentes" por padrão. Calibre ao modelo.
- Mantenha um pequeno conjunto de casos de teste (pedidos reais "às pressas" e o resultado esperado) para avaliar mudanças na skill. Isso cumpre a recomendação unânime de iterar com evals.
- Idioma: gere no idioma do usuário (pt-BR) e mantenha código, identificadores e mensagens de erro no original. Não há evidência forte nas fontes revisadas de que traduzir para inglês melhore os resultados nos modelos atuais (confiança baixa).

**7. Checklist final de qualidade do prompt gerado:**
- [ ] A primeira linha diz o objetivo no imperativo.
- [ ] Um colega sem contexto conseguiria executar? (teste da Anthropic)
- [ ] Cada restrição tem o seu porquê.
- [ ] O escopo e o que fica fora estão explícitos.
- [ ] O critério de pronto é verificável, com comandos e testes.
- [ ] A política de autonomia nomeia as ações que exigem confirmação.
- [ ] As suposições estão listadas.
- [ ] O formato de saída corresponde ao tipo de tarefa e tem limite concreto.
- [ ] Os insumos estão em tags ou são referenciados por caminho, sem colagem desnecessária.
- [ ] Não há CoT forçado, CAIXA ALTA, persona inflada, gorjeta, prefill nem regras "nunca" sem motivo.
- [ ] Não há instruções que conflitem com o CLAUDE.md, as skills ou o AGENTS.md.
- [ ] O tamanho é proporcional à tarefa, sem seções vazias.

### H. Fontes principais (organização, data, link)

**Anthropic**
- Prompting best practices, página viva, consultada em nov/2026: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Prompting Claude Fable 5.2 (modelo lançado em 09/11/2026): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
- Prompting Claude Opus 5 e Opus 5.5, 2026: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 e .../prompting-claude-opus-5-5
- Effective context engineering for AI agents (Rajasekaran et al., 29/09/2025): https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Claude Code: Best practices for agentic coding, 2025: https://www.anthropic.com/research/claude-code-best-practices
- Prompt improver, anúncio de 14/11/2024: https://www.anthropic.com/news/prompt-improver
- Release notes, aposentadoria do Workbench e do improver (anúncio em 17/07/2026, efetiva em 17/08/2026): https://platform.claude.com/docs/en/release-notes/overview
- Metaprompt (cookbook, 2024): https://platform.claude.com/cookbook/misc-metaprompt

**OpenAI**
- Prompt engineering, página viva, 2026: https://developers.openai.com/api/docs/guides/prompt-engineering
- Using GPT-6, set/2026: https://developers.openai.com/api/docs/guides/latest-model
- Rethinking skills and prompts for GPT-6 Astra, set/2026: https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
- GPT-5 prompting guide (ago/2025), GPT-5.1 (nov/2025) e GPT-5.2 (fim de 2025): https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide e variantes
- Reasoning best practices, 2025: https://developers.openai.com/api/docs/guides/reasoning-best-practices
- Prompt generation (meta-prompt, out/2024): https://developers.openai.com/api/docs/guides/prompt-generation
- Prompt optimizer (em descontinuação, 2026): https://developers.openai.com/api/docs/guides/prompt-optimizer

**Google**
- Prompt design strategies, Gemini API, página viva, 2026: https://ai.google.dev/gemini-api/docs/prompting-strategies
- Gemini 3 developer guide, 2025–2026: https://ai.google.dev/gemini-api/docs/gemini-3
- Lee Boonstra, Prompt Engineering whitepaper (Google/Kaggle, fev/2025)

**Pesquisa**
- Wharton GAIL, Prompting Science Reports: 1 (04/03/2025), 2 sobre CoT (08/06/2025, arXiv 2506.07142), 3 sobre gorjeta e ameaça (01/08/2025, arXiv 2508.00614), 4 sobre personas (07/12/2025, arXiv 2512.05858)
- Schulhoff et al., The Prompt Report (arXiv 2406.06608, 2024; revisado em 2025)
- Sclar et al., sensibilidade à formatação (ICLR 2024, arXiv 2310.11324)
- Zheng et al., personas em system prompts (arXiv 2311.10054)
- Liu et al., Lost in the Middle (TACL 2024)
- Chroma, Context Rot (2025)
- Wei et al., chain-of-thought (2022)

**Frameworks**
- CO-STAR: GovTech Singapura e Sheila Teo, 2023
- Comparação 5W3H, CO-STAR e RISEN: arXiv 2603.29953, 2026

## Caveats

- **Cobertura incompleta:** Microsoft Azure, Meta Llama e Mistral não foram verificados em fonte primária. Pela cobertura da InfoQ, o guia da Azure é semelhante ao da OpenAI, com dicas de temperature e top_p. Guias de praticantes (Simon Willison, Lilian Weng, Eugene Yan, Hamel Husain) também não foram verificados nesta rodada, e os métodos APE, OPRO, DSPy, TextGrad, self-consistency e os "26 princípios" (Bsharat et al.) aparecem apenas de forma contextual.
- **Muito da evidência sobre os modelos atuais vem dos próprios fornecedores** ("in Anthropic's testing…"), com números internos não replicados. Os estudos independentes (Wharton) usam benchmarks de múltipla escolha, como GPQA e MMLU-Pro, e podem não se transferir para tarefas agênticas de código.
- **Sensibilidade e literalidade mudam a cada versão de modelo** (Opus 5 vs. Fable 5.2 vs. GPT-6 Astra). Trate as recomendações específicas por modelo como perecíveis e revalide com evals a cada migração.
- **Os números do estudo de formatação de Sclar et al. (até 76 pontos, em cenário few-shot) são de modelos open-source de 2023.** Modelos de fronteira atuais tendem a ser menos sensíveis, mas a variação por questão ainda existe (Wharton).
- **O prompt improver da Anthropic e o optimizer da OpenAI não estão mais disponíveis, ou estão em descontinuação.** As descrições deles vêm de documentação antiga e de cópias de terceiros, e foram usadas apenas para entender o desenho.

## Lista completa de fontes consultadas

- claude: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools
- innopreneur: https://www.innopreneur.io/wp-content/uploads/2025/04/22365_3_Prompt-Engineering_v7-1.pdf
- google: https://ai.google.dev/gemini-api/docs/prompting-strategies
- google: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/prompt-design-strategies
- openai: https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide
- promptessor: https://promptessor.com/blog/gemini-3-8-flash-prompting-guide
- munderdiffl: https://munderdiffl.in/blog/claude-code-best-practices/
- vercel: https://agent-master-handbook.vercel.app/en/curated/entries/anthropic-context-engineering/
- count: https://count.co/ai/how-to-optimise-a-prompt
- searchenginejournal: https://www.searchenginejournal.com/researchers-test-if-threats-improve-ai-improves-performance/552813/
- openai: https://developers.openai.com/api/docs/guides/reasoning-best-practices
- google: https://ai.google.dev/gemini-api/docs/gemini-3
- claude: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
- openai: https://developers.openai.com/cookbook/examples/realtime_prompting_guide
- arxiv: https://arxiv.org/pdf/2311.10054
- github: https://lawwu.github.io/til/posts/2024-10-11-prompt-generation-metaprompt/
- medium: https://medium.com/@aihealthybrains/openais-new-prompting-guide-how-to-get-the-best-results-from-reasoning-models-cf845a57a4eb
- claude: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
- dmarketertayeeb: https://dmarketertayeeb.com/blog/gpt-6-astra-prompting-guide/
- aicatchup: https://aicatchup.com/practices/prompting-gpt-6
- openai: https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
- claude: https://platform.claude.com/docs/en/models/fable-5-2/whats-new-fable-5-2
- openai: https://developers.openai.com/api/docs/guides/latest-model
- the-decoder: https://the-decoder.com/openai-shares-prompting-tips-for-gpt-6-astra-including-a-blocklist-of-slop-words/
- promptessor: https://promptessor.com/blog/gpt-6-astra-prompting-guide
- arxiv: https://arxiv.org/pdf/2603.29953
- equinetacademy: https://www.equinetacademy.com/blog/co-star-prompt-engineering-framework-explained-with-examples/
- parloa: https://www.parloa.com/knowledge-hub/prompt-engineering-frameworks/
- texttoolsai: https://www.texttoolsai.app/tools/prompt-generator/frameworks/ai-prompt-frameworks
- arxiv: https://arxiv.org/pdf/2506.07142
- arxiv: https://arxiv.org/pdf/2512.05858
- upenn: https://penntoday.upenn.edu/news/wharton-why-you-shouldnt-ask-chatbots-act-expert
- pith: https://pith.science/paper/2508.00614
- the-decoder: https://the-decoder.com/anthropic-adds-claude-powered-prompt-optimizer-to-its-ai-development-console/
- claude: https://platform.claude.com/docs/en/release-notes/overview
- mintlify: https://anthropic.mintlify.app/en/docs/build-with-claude/prompt-engineering/prompt-improver
- claude: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools.md
- anthropic: https://www.anthropic.com/news/prompt-improver
- taku: https://taku.ai/blog/claude-prompt-improver
- claude: https://platform.claude.com/cookbook/misc-metaprompt
- patreon: https://www.patreon.com/posts/anthropic-meta-100639122
- openai: https://developers.openai.com/api/docs/guides/prompt-generation
- openai: https://developers.openai.com/api/docs/guides/prompt-optimizer
- promptbuilder: https://promptbuilder.cc/blog/best-prompt-optimizer-tools-2026
- uhaid: https://www.uhaid.org/p/a-study-guide-for-lee-boonstras-prompt
- claude: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
- rundatarun: https://ai.rundatarun.io/AI+Development+&+Agents/claude-code-best-practices
- anthropic: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- arxiv: https://arxiv.org/html/2406.06608
- arxiv: https://arxiv.org/pdf/2311.07230
- infoq: https://www.infoq.com/news/2023/12/openai-prompt-engineering/
- upenn: https://gail.wharton.upenn.edu/research-and-insights/
