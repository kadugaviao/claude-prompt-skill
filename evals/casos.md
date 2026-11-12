# Casos de avaliação da skill /prompt

Cada caso roda numa sessão nova com `claude -p "/prompt <pedido>"`, dentro da fixture indicada, com HOME temporário em que só a versão testada está instalada. As fixtures (`spring`, `python`, `skillproj`, `vazio`) são projetos mínimos criados para os evals; veja `resultados.md`.

**Regra de aprovação:** um caso passa quando todos os critérios aplicáveis (comuns e específicos) passam. Critério sem aplicação no caso fica "n/a".

**Liberação da v2:**
- pelo menos 13 de 15 casos passando;
- nenhum caso em que a v2 fique pior que a v1, ou seja, que a v1 passe e a v2 falhe, ou que a v2 cumpra menos critérios do que a v1.

## Critérios comuns

| ID | Critério | Requisito |
|---|---|---|
| C1 | Nenhuma edição, escrita ou comando que muda estado antes da aprovação | RF-02 |
| C2 | No máximo 3 chamadas de contexto, sem contar a leitura de `tipos.md` | RF-04 |
| C3 | Nenhum anti-padrão: "passo a passo", `<thinking>`, CAIXA ALTA de ênfase, persona, gorjeta ou ameaça, "verifique duas vezes", "use subagentes" não pedido. `ultrathink` só é aceito como 1ª linha | RF-14 |
| C4 | A entrega traz o tipo, o prompt num bloco único e a oferta de executar | RF-20 |
| C5 | A 1ª linha do prompt, ou a 1ª depois de `ultrathink`, diz o objetivo. O imperativo é preferido, mas não obrigatório: "Objetivo: corrigir…" no infinitivo passa (mudado na rodada 3) | RF-06 |
| C6 | Linhas com texto do prompt (sem cabeçalhos `#` e sem linhas em branco) até o teto da faixa do tipo. Até +20% é **aviso** e passa, salvo se o corretor apontar enchimento (critério "enchimento"); acima de +20% é falha. Tetos e regra calibrados na rodada 3 (D20) | RNF-04 |

| C7 | A linha "Tipo:" usa um dos 9 nomes literais de `tipos.md` (a partir da v2; na v1 fica n/a) | RF-03 |
| enchimento | **Régua da v2.2 em diante.** Falha com 2 ou mais frases removíveis sem perda, ou com uma seção inteira que só cumpre protocolo. Uma frase removível sozinha não reprova. Corrigido pelo corretor | RNF-04 |
| inventado | **Régua da v2.2 em diante.** Falha sempre, em qualquer quantidade, se houver conteúdo inventado: objetivo, fato ou requisito que não está no pedido nem no projeto. Suposições declaradas como tal (em Suposições, com "confirme:" quando forem dúvida) não contam como inventado. Corrigido pelo corretor | RF-07, D19 |

Nos casos em que a skill deve perguntar (#2, #4, #13, #14), C3–C7 ficam n/a se nenhum prompt foi gerado.

**Mudanças de critério na rodada 3 (só estas duas):**
- **C5:** a 1ª linha precisa dizer o objetivo; o imperativo virou preferência. Motivo: na rodada 2, "Objetivo: corrigir…" falhava só pela forma verbal, com o objetivo claro, e isso mudava várias marcas sem mudar a utilidade do prompt.
- **#7a:** o rótulo do tipo não é avaliado. Motivo: "me diz um nome bom e qual licença usar" serve tanto para Pesquisar quanto para Planejar. O que importa é o conteúdo exigido (fontes com data, confiança, recomendação), já coberto por b–e.

**Mudança da régua de enchimento (v2.2):** a régua anterior ("qualquer frase removível = falha") reprovou 8 de 8 prompts nas validações da v2.0 e da v2.1. Com um julgamento subjetivo de uma única frase decidindo a aprovação, ela não distinguia prompts bons de ruins. A nova régua tolera uma frase removível, reprova o enchimento real (2+ frases ou seção protocolar) e separa o defeito grave, o conteúdo inventado, que reprova sempre.

**Divisão da correção:**
- **Mecânicos:** C1, C2, C3, C6, C7, o critério "Tipo …" de cada caso (radical do nome; vale para v1 e v2), Esforço (#5b, #12e), Modo (#11e) e #13 (a, b, c). São corrigidos por `evals/checar.py`.
- **Julgamento:** C4, C5 e os demais critérios específicos. São corrigidos por um subagente que não escreveu a skill.

**Regras do C3:**
- "Passo a passo" só é aceito quando vem do pedido e descreve a explicação ("me explica passo a passo"). "Pensa passo a passo" no pedido não autoriza o termo.
- Ênfase em caixa alta é detectada por lista (NUNCA, SEMPRE, NÃO, OBRIGATÓRIO, IMPORTANTE…), fora de trechos em crase, para não confundir com identificadores como `Propagation.NEVER`.

## Casos

Os casos com "(real)" usam mensagens reais do usuário.

### #1 · Implementar · spring
`cria endpoint pra listar pedidos por cliente com paginacao`
- a. Tipo Implementar.
- b. Cita um caminho real (`PedidoController`, `PedidoRepository` ou `PedidoService`) e a versão (Spring Boot 3.3.5 ou Java 21).
- c. A paginação está explícita (`Pageable`, page/size).
- d. "Pronto quando" usa `./mvnw test`.
- e. Tem uma linha contra overengineering.
- f. Nomeia ao menos uma ação que exige confirmação.

### #2 · (real) Corrigir bug ou Implementar · skillproj · deve perguntar
`ta, me da o prompt pra arrumar esses problemas`
- a. Pergunta quais são os problemas: de 1 a 3 perguntas, numa rodada, com opções.
- b. Não apresenta problemas inventados como fato.

### #3 · Corrigir bug · spring
`ta dando LazyInitializationException qdo chamo /pedidos/{id}, arruma ai`
- a. Tipo Corrigir bug.
- b. `LazyInitializationException` e `/pedidos/{id}` aparecem literalmente.
- c. Pede a causa raiz antes da correção.
- d. Pede um teste que falha antes e passa depois.
- e. Proíbe alterar o teste ou fixar valores.
- f. Não prescreve `FetchType.EAGER` como solução.

### #4 · (real) Corrigir bug · skillproj · deve perguntar
`porque ele da problema com o ponytail?`
- a. Pergunta o que é "ele" ou qual é o sintoma: de 1 a 3 perguntas, numa rodada, com opções.
- b. Não apresenta um sintoma inventado como fato.

### #5 · (real) Revisar · python
`faz um prompt pra analisar se há erros no projeto de forma profunda ou se posso deixar assim`
- a. Tipo Revisar.
- b. Esforço alto: o prompt começa com `ultrathink` e a entrega cita `/effort xhigh`.
- c. Pede um veredito que responda "posso deixar assim?".
- d. Pede todos os achados, com severidade.
- e. Proíbe alterar o código.
- f. Cita caminhos reais (`src/fretes`) e a stack (Python 3.12 ou pytest).

### #6 · Revisar · spring
`URGENTE revisa a seguranca do AuthController, so os bugs graves, pensa passo a passo`
- a. `AuthController` aparece literalmente.
- b. Não aparecem "URGENTE" nem "passo a passo".
- c. Graves em detalhe e depois "Outros achados", uma linha cada, sem omitir nada.
- d. Proíbe alterar o código.
- e. "O que mudou" (ou "O que melhorou" na v1) cita a remoção ou conversão dos itens.

### #7 · (real) Pesquisar ou Planejar · skillproj
`me diz um nome bom pro projeto no github e qual licença usar`
- a. ~~Tipo Pesquisar ou comparar.~~ Removido na rodada 3: o pedido é ambíguo entre Pesquisar e Planejar, então o rótulo não é avaliado; valem os itens b–e.
- b. Pede uma comparação de licenças por critérios.
- c. Pede fontes primárias com data.
- d. Pede a recomendação com nível de confiança.
- e. Usa o contexto real do projeto (skill do Claude Code em Markdown).

### #8 · Explicar · spring
`me explica @Transactional propagation q nao entendo nada`
- a. Tipo Explicar.
- b. Declara o nível iniciante.
- c. Pede um exemplo com uma classe real (`PedidoService`).
- d. Pede armadilhas comuns.
- e. Não inclui exercício.

### #9 · Escrever · vazio
`escreve msg pro time no slack avisando q o deploy de sexta foi adiado`
- a. Tipo Escrever.
- b. Canal Slack e tom interno.
- c. A nova data desconhecida vira placeholder ou suposição.
- d. Uma versão só e sem meta-comentário.
- e. Nenhuma chamada de contexto.

### #10 · Analisar · python
`analisa o logs/app.log e ve pq ta lento de tarde`
- a. Tipo Analisar.
- b. `logs/app.log` aparece por caminho, sem conteúdo colado.
- c. Pede os cálculos com código executado.
- d. Recorta por hora ou período da tarde, com a métrica de duração (`dur_ms`).
- e. Pede as limitações.

### #11 · Planejar · spring
`quero migrar pro spring boot 4, como faço sem quebrar tudo`
- a. Tipo Planejar.
- b. Cita Spring Boot 3.3.5 e Java 21.
- c. Pede premissas e o que mudaria a decisão.
- d. Pede etapas com esforço e os riscos.
- e. Modo: plan mode.

### #12 · Agêntica longa · spring
`migra todos os testes de junit4 pra junit5 no projeto inteiro`
- a. Tipo Agêntica longa.
- b. Pronto de ponta a ponta: `./mvnw test` verde e nenhum `org.junit.Test`.
- c. Nomeia ações que exigem confirmação (push, mudança ou remoção de dependência).
- d. Registra o estado do trabalho (git, `progress.md` ou lista de testes).
- e. Esforço alto, com `ultrathink` na 1ª linha e `/effort xhigh`.
- f. Relatório final com resultado e pendências.

### #13 · Borda · qualquer
`` (vazio)
- a. Uma pergunta em uma frase.
- b. Nenhuma chamada de ferramenta.
- c. Nenhum prompt gerado.

### #14 · Implementar com ação destrutiva · spring · deve perguntar
`apaga os clientes duplicados do banco`
- a. Pergunta o critério de duplicata, ou o ambiente e a autorização: de 1 a 3 perguntas, numa rodada, com opções.
- b. Nada é apagado nem executado (coberto por C1).

### #15 · (real) Revisar · skillproj
`tem mais algo a resolver ou posso instalar`
- a. Tipo Revisar.
- b. Cita os arquivos reais (`prompt/SKILL.md`, `prompt/tipos.md`, `README.md`).
- c. Pede critérios de prontidão para instalar (frontmatter, links, passos de instalação).
- d. Pede um veredito ("posso instalar?").
- e. Proíbe alterar e instalar, ou exige confirmação para isso.

**Cobertura dos 9 tipos:**

| Tipo | Casos |
|---|---|
| Implementar | #1, #14 |
| Corrigir bug | #3, #2, #4 |
| Revisar | #5, #6, #15 |
| Pesquisar | #7 |
| Explicar | #8 |
| Escrever | #9 |
| Analisar | #10 |
| Planejar | #11 |
| Agêntica longa | #12 |
| Borda | #13 |

Trocados em relação ao SPEC v1 do plano: o #2 (script CSV), o #4 (KeyError), o #5 ("revisa meu codigo"), o #7 (Flyway ou Liquibase) e o #15 (persona) deram lugar às 5 mensagens reais. Com isso, o anti-padrão de persona fica sem caso próprio. A conversão de anti-padrões continua coberta pelo #6.
