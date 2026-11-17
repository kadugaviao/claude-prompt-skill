# SPEC: skill /prompt, versão 2

Status: rascunho para revisão · Data: 10/11/2026
Insumos: `docs/research/prompt-engineering-research.md` (referida como **P**, com a seção: P-G1, P-D, P-E6…) e a v1 em `evals/fixture-sources/skill-v1/` (SKILL.md, tipos.md, README.md).

Legenda de confiança: **alta**, **média** ou **baixa**. A confiança vem da própria pesquisa quando ela informa; quando não informa, a estimativa é minha e aparece com "(minha)". **[a verificar]** indica que o requisito depende de uma afirmação sobre um modelo ou produto recente que você não conferiu, ou de um detalhe do Claude Code que eu não confirmei.

---

## 1. Objetivo e público

A skill recebe um pedido escrito às pressas, em português, e o reescreve como um **briefing** claro, enxuto e verificável. O briefing traz objetivo, contexto, escopo, critério de pronto, política de autonomia e um formato de saída padronizado pelo tipo de tarefa. A skill não "turbina" o texto com técnicas (P, introdução; P-F).

O público é um único usuário: um desenvolvedor que usa o Claude Code em projetos Java/Spring Boot e Python e escreve em pt-BR.

## 2. Escopo

**A skill faz:**
- Classifica o pedido em 1 dos 9 tipos da P-D.
- Coleta pouco contexto do projeto, só com leituras e com um limite de chamadas.
- Pergunta (no máximo 3 perguntas) ou assume, e registra as suposições.
- Gera o prompt e o entrega para aprovação.
- Se o usuário aprovar, executa o prompt na mesma sessão.

**A skill não faz:**
- Executar a tarefa antes da aprovação, editar arquivos ou rodar comandos que mudem estado.
- Pesquisar na web, criar subagentes ou otimizar prompts automaticamente contra uma métrica (P-F, APE/OPRO/DSPy).
- Gerar prompts para a API (system prompt, prefill, temperatura). O alvo é uma sessão do Claude Code, por isso o que é de API fica fora (P-B3, P-B10).
- Traduzir o pedido para o inglês (P-G6).
- Reproduzir a receita dos prompt improvers de 2024 (CoT detalhado, prefill, exemplos reescritos), conforme P-F.

## 3. Diferenças em relação à v1

| Ação | Item | Motivo | Fonte |
|---|---|---|---|
| Manter | `$ARGUMENTS` em `<pedido>`, `disable-model-invocation: true`, `argument-hint` | Funciona e foi testado na v1 | Teste da v1 |
| Manter | Pedido vazio gera uma pergunta e a skill para | Comportamento testado; custo zero | Teste da v1 |
| Manter | "Não execute agora", entrega para aprovação e oferta de executar | A pesquisa recomenda mostrar o prompt para aprovação, com a opção de executar direto | P-G6 |
| Manter | Perguntar no máximo 3 vezes, de uma vez; senão assumir | Alinhado | P-G2 |
| Manter | Verbos de ação e imperativo ("Implemente", não "você poderia sugerir") | O Claude só sugere quando o pedido é "pode sugerir" | P-B9, P-E8 |
| Manter | O porquê de cada regra; instruções positivas | Princípios de consenso | P-A2, P-A3 |
| Manter | Revisão: todos os achados com severidade, veredito e nada de alteração no código | Confirmado | P-D (Revisar) |
| Manter | Não pedir "revise duas vezes" nem o raciocínio interno | Over-verification; CoT obsoleto | P-B1, P-B8, P-E1, P-E6 |
| Manter | Tipo misto: usar o tipo principal e acrescentar o que falta do outro | Não há conflito com a pesquisa; é simples | (minha) |
| Manter | Sugestão de plan mode | Recurso do Claude Code; a pesquisa não trata disso | Nenhuma; confiança baixa |
| Mudar | A primeira linha passa a ser o objetivo no imperativo, sem o cabeçalho "Objetivo:" | Padrão do esqueleto recomendado e do meta-prompt da OpenAI | P-G1, P-F |
| Mudar | Ordem das seções: Contexto → Insumos → Tarefa e escopo → Restrições → Pronto quando → Autonomia → Formato | Segue o esqueleto da pesquisa | P-G1 (média para a ordem) |
| Mudar | Coleta de contexto: deixa de ler o CLAUDE.md e o README; lê a estrutura, o arquivo de build e o alvo da tarefa | O CLAUDE.md já está carregado na sessão, e duplicá-lo é ruído. O arquivo de build dá as versões reais | P-G4 |
| Mudar | `ultrathink` deixa de ser automático na 1ª linha. Com Esforço alto, a entrega orienta `/effort xhigh` para execução na sessão e mantém `ultrathink` na 1ª linha para quando o prompt for colado | O esforço se calibra pelo parâmetro, não por texto; `ultrathink` só vale digitado pelo usuário | P-A (TL;DR), P-B1 · resolvido pelo usuário (seção 13) |
| Mudar | Ênfase forte: de "no máximo duas por prompt" para nenhuma CAIXA ALTA. Uma restrição real recebe o motivo, não grito | Overtriggering desde o Opus 4.5 | P-B2, P-E2 |
| Mudar | Ações irreversíveis saem de "Restrições" e vão para "Autonomia", nomeadas uma a uma | Recomendação do esqueleto da pesquisa | P-G1 |
| Mudar | Suposições saem da entrega e entram no prompt, na seção Autonomia, com a instrução de o executor sinalizar se alguma estiver errada | O executor precisa vê-las para corrigir o rumo | P-G1, P-G2 |
| Mudar | Perguntas da skill: cada uma passa a vir com opções sugeridas | Recomendação explícita | P-G2 |
| Mudar | Templates com limite concreto de comprimento e resultado no 1º item, na ordem da P-D | Limites concretos funcionam melhor que "seja conciso". A regra geral "1ª frase = resultado" foi retirada porque só os guias do Opus 5 e do Fable 5.2 a sustentam | P-A6, P-D |
| Mudar | Escrever texto: de "2 versões quando couber" para o texto final, com variantes só se pedidas | Contradiz P-D | P-D (Escrever) |
| Mudar | Explicar: o exercício deixa de ser padrão (só entra se o pedido falar em estudo ou prova); entra exemplo mínimo executável | P-D lista resumo, explicação progressiva, exemplo e armadilhas | P-D (Explicar) |
| Mudar | Pesquisar: a recomendação vem com nível de confiança, e fato, inferência e opinião ficam separados | Ausente na v1 | P-D (Pesquisar) |
| Mudar | Planejar: acrescenta premissas explícitas e "o que mudaria a decisão" | Ausente na v1 | P-D (Planejar) |
| Mudar | "Regras de escrita" (14 itens) viram um checklist único de qualidade, aplicado antes da entrega | Remove a sobreposição e encolhe o SKILL.md | P-G7 |
| Remover | "Suposições" como bloco separado na entrega | Agora estão dentro do prompt | P-G1 |
| Remover | Leitura do README na coleta de contexto | Pouco sinal para o custo; o arquivo de build e a estrutura cobrem as versões | P-G4 |
| Adicionar | 9º tipo: **Agêntica longa** | Exigido pela P-D | P-D, P-G3 |
| Adicionar | Seção **Insumos**: caminhos por referência e trechos colados em tags XML | Separar dados de instruções; recuperação just-in-time | P-A5, P-A9, P-B6 |
| Adicionar | Seção **Autonomia**: o que pode fazer sem perguntar, o que exige confirmação, suposições e "investigue antes de adivinhar" | Tema central dos guias de 2026; os improvers não cobrem | P-G1, P-G2, P-F (síntese) |
| Adicionar | Preservar literalmente o que o usuário escreveu (identificadores, erros, caminhos) | "Preserve User Content" | P-G6, P-F |
| Adicionar | Anti-overengineering no tipo Implementar; proibição de "ajustar o teste para passar" no tipo Bug | Explícito na P-D | P-D |
| Adicionar | Tratamento de anti-padrões presentes no pedido do usuário | Pedido seu; regras em P-E | P-E |
| Adicionar | Saída consumida por máquina leva JSON ou schema | Recomendação explícita | P-G3 |
| Adicionar | Orçamento de tamanho por tipo de prompt gerado | Tamanho proporcional | P-G5 |
| Adicionar | `evals/cases.md` fora da pasta instalada da skill | Iterar com evals | P-A10, P-G6 |

## 4. Requisitos funcionais

Cada requisito tem um critério de aceite (CA) que permite responder "cumpriu" ou "não cumpriu" lendo a transcrição da sessão.

**RF-01 · Pedido vazio.** Se `$ARGUMENTS` estiver vazio ou só com espaços, a skill responde com uma única pergunta e encerra o turno.
CA: uma frase terminada em "?", nenhuma chamada de ferramenta e nenhum prompt gerado. Fonte: v1 (testado). Confiança: alta (minha).

**RF-02 · Não executar antes da aprovação.** Até o usuário aprovar, a skill não edita nem cria arquivos e não roda comandos que mudem estado.
CA: a transcrição mostra só chamadas de leitura (Read, Glob, Grep, `ls`, `git status`, `git diff`, `git log`) e, se houver, AskUserQuestion. Fonte: P-G6, P-F (Metaprompt: "você não está executando a tarefa"). Confiança: alta.

**RF-03 · Classificação.** A entrega mostra exatamente um tipo dentre os 9 da seção 9. Num pedido misto, mostra o tipo principal, e o prompt inclui os itens "deve conter" do tipo secundário que se aplicarem.
CA: o campo `Tipo:` contém um dos 9 nomes; nos casos de teste, o tipo bate com o esperado. Fonte: P-G3. Confiança: alta.

**RF-04 · Coleta de contexto barata.** Dentro de um projeto, a skill faz no máximo 3 chamadas de leitura:
1. Estrutura do projeto (raiz e `src/`).
2. Arquivo de build (`pom.xml`, `build.gradle(.kts)` ou `pyproject.toml`/`requirements.txt`).
3. Uma leitura do alvo da tarefa, por exemplo `git diff --stat` numa revisão ou o arquivo citado no pedido.

A skill não lê o CLAUDE.md da raiz, que já está carregado. Fora de um projeto, não faz nenhuma chamada.
CA: no máximo 3 chamadas de ferramenta antes da entrega, sem contar o AskUserQuestion; nenhuma leitura de `CLAUDE.md`; o prompt cita ao menos um caminho ou versão real quando o projeto os tem. Fonte: P-G4, P-A9. Confiança: alta.

**RF-05 · Perguntar ou assumir.** A skill pergunta só quando valem **as duas** condições:
- (a) a resposta mudaria materialmente o resultado;
- (b) a informação não pode ser obtida com as leituras do RF-04.

As perguntas são no máximo 3, numa única vez, cada uma com 2 a 4 opções sugeridas (via AskUserQuestion, se houver). Nos outros casos, a skill assume o default mais provável. Os gatilhos típicos estão na seção 7.
CA: o número de rodadas de perguntas é 0 ou 1; o número de perguntas é ≤ 3; cada pergunta tem opções. Nos casos de teste marcados "deve perguntar", houve pergunta; nos marcados "não deve perguntar", não houve. Fonte: P-G2. Confiança: média-alta.

**RF-06 · Esqueleto.** O prompt segue as seções e a ordem da seção 8. A primeira linha é o objetivo, no imperativo, sem cabeçalho. Seções sem conteúdo são omitidas, nunca deixadas com "N/A".
CA: a ordem das seções presentes é uma subsequência da ordem da seção 8; a primeira linha começa com um verbo no imperativo; não aparece nenhum cabeçalho com corpo vazio ou "N/A". Fonte: P-G1, P-E10. Confiança: alta para os elementos, média para a ordem.

**RF-07 · Preservar o conteúdo do usuário.** Identificadores, nomes de classes e métodos, caminhos, mensagens de erro e números do pedido aparecem no prompt sem alteração.
CA: cada token desse tipo presente no pedido aparece literalmente no prompt (verificação por busca textual). Fonte: P-G6, P-F. Confiança: alta.

**RF-08 · Insumos.** Arquivos do projeto são referenciados por caminho, não colados. Trechos que o usuário colou (log, stack trace, código) vão em tags XML nomeadas (`<log>`, `<erro>`, `<trecho>`).
CA: nenhum bloco de código do projeto com mais de 10 linhas aparece no prompt sem ter sido colado pelo usuário; todo conteúdo colado pelo usuário está dentro de uma tag. Fonte: P-A5, P-A9, P-B6. Confiança: alta para separar; média para XML versus Markdown.

**RF-09 · Restrições com motivo.** Cada item de "Restrições" e de "fora do escopo" traz o motivo, em poucas palavras.
CA: cada item contém um motivo (por exemplo "porque…", "para…" ou "—"). Fonte: P-A2, P-E7. Confiança: alta (evidência de fornecedor).

**RF-10 · Pronto verificável.** "Pronto quando" tem ao menos um critério observável. Se o projeto tiver um comando de teste ou build descoberto no RF-04, o critério usa esse comando real (`./mvnw test`, `pytest`…). A verificação pedida é proporcional à mudança: teste do módulo afetado, não a suíte inteira, quando a mudança é local.
CA: há ao menos um critério do tipo "comando X passa", "o caso A retorna B" ou "a tabela tem as colunas C"; nenhum critério é vago, como "código de qualidade". Fonte: P-A8. Confiança: alta. (Na v2 saiu a regra de "verificação proporcional", que dependia de afirmações sobre o Opus 5 e o GPT-6 Astra.)

**RF-11 · Autonomia.** Se a tarefa pode mudar estado (arquivos, banco, git, deploy), o prompt traz:
- (a) o que pode ser feito sem perguntar;
- (b) as ações exatas que exigem confirmação (push, migração, deleção, mudança de dependência…);
- (c) as suposições da skill, com a instrução de o executor sinalizar se alguma estiver errada;
- (d) uma linha para investigar no código antes de adivinhar.

Em tarefas só de leitura (Explicar, Pesquisar, Escrever e Revisar sem edição), a seção se reduz às suposições, ou some quando não há suposições.
CA: nas tarefas que mudam estado, há ao menos uma ação nomeada em (b), e nenhuma regra vaga do tipo "tenha cuidado". Fonte: P-G1, P-G2. Confiança: média-alta.

**RF-12 · Formato da resposta por tipo.** A seção "Formato da resposta" usa o template do tipo (seção 9), adaptado ao pedido, com ao menos um limite concreto (frases, linhas ou itens).
CA: o template corresponde ao tipo; há ao menos um número de limite. Fonte: P-A6, P-D. Confiança: alta.

**RF-13 · Itens obrigatórios do tipo.** O prompt contém os itens "deve conter" do tipo (seção 9) que se aplicam ao pedido, preenchidos com dados reais ou com uma suposição explícita.
CA: o checklist do caso de teste (seção 11) é cumprido. Fonte: P-D. Confiança: alta.

**RF-14 · Sem anti-padrões.** O prompt gerado não contém nenhum item da seção 10.1.
CA: uma busca textual não encontra "passo a passo", `<thinking>`, `ultrathink` fora da 1ª linha, palavras inteiras em CAIXA ALTA (fora siglas, identificadores e os valores do veredito), "você é um(a) especialista", gorjeta ou ameaça, "verifique duas vezes" nem "use subagentes" (salvo pedido explícito do usuário). Fonte: P-E, P-G1. Confiança: alta.

**RF-15 · Anti-padrão vindo do usuário.** Se o pedido contém um anti-padrão, a skill aplica a ação da seção 10.2 e registra a mudança em "O que mudou".
CA: no caso de teste com anti-padrão, ele não aparece no prompt e é citado em "O que mudou". Fonte: P-E, P-G6. Confiança: alta.

**RF-16 · Sem duplicar o CLAUDE.md.** O prompt não repete convenções que já estão no CLAUDE.md carregado e só inclui convenções que mudariam o resultado.
CA: nenhuma frase do prompt repete regra do CLAUDE.md (conferência manual nos casos de teste). Fonte: P-G4. Confiança: alta.

**RF-17 · Idioma.** O prompt e a entrega são escritos em pt-BR. Código, identificadores, comandos e mensagens de erro ficam no original.
CA: prosa em português; tokens técnicos idênticos ao original. Fonte: P-G6. Confiança: baixa quanto ao benefício de não traduzir; alta quanto a ser a sua preferência.

**RF-18 · Exemplos só quando necessários.** O prompt traz um exemplo de saída em `<example>` só se o formato não for óbvio ou se o usuário tiver dado um exemplo. Nesse caso, a skill usa o exemplo do usuário.
CA: nos casos de teste comuns, nenhum `<example>`; no caso de saída em formato específico, um exemplo. Fonte: P-B7, P-A4. Confiança: média.

**RF-19 · Saída para máquina.** Se o pedido diz que a saída vai alimentar código ou ferramenta (JSON, CSV, payload), o formato pede JSON ou CSV com os campos nomeados.
CA: no caso de teste correspondente, o formato lista os campos. Fonte: P-G3. Confiança: alta.

**RF-20 · Entrega.** A entrega segue exatamente este formato:
~~~
**Tipo:** <tipo> · **Modo:** <normal | plan mode> · **Esforço:** <padrão | alto (+ "/effort xhigh" para executar aqui)>
```text
<prompt>
```
**O que mudou:** <1 a 3 itens curtos>
Quer que eu execute este prompt agora?
~~~
CA: os 4 elementos aparecem nessa ordem; o prompt está num único bloco `text`; "O que mudou" tem de 1 a 3 itens. Fonte: v1 (testado), P-G6. Confiança: alta (minha).

**RF-21 · Modo e esforço.** O plan mode é sugerido quando a tarefa altera arquivos e tem 3 ou mais passos, ou envolve decisão de arquitetura. O esforço "alto" é sugerido em depuração difícil, decisão de arquitetura, auditoria profunda ou tarefa agêntica longa. Com esforço alto:
- (a) a 1ª linha do prompt é `ultrathink`, que vale quando o usuário cola o prompt, porque só funciona digitado;
- (b) a entrega diz "para executar aqui, rode `/effort xhigh` antes de responder sim".

Fora disso, o prompt não contém instruções sobre quanto pensar.
CA: com esforço alto, a linha 1 é `ultrathink` e a entrega cita `/effort xhigh`; com esforço padrão, nenhum `ultrathink`; em nenhum caso aparecem "pense" ou "raciocine". Fonte: P-B1; mecanismo confirmado pelo usuário. Confiança: alta.

**RF-22 · Aprovação e ajuste.** Se a resposta for "sim" (ou equivalente), a skill executa o prompt como se o usuário o tivesse enviado. Se o usuário pedir um ajuste, a skill reescreve só as partes afetadas e entrega de novo no formato do RF-20.
CA: depois de "sim", a próxima ação é o primeiro passo do prompt. Depois de um ajuste, as seções não afetadas ficam idênticas (diff textual). Fonte: v1 (testado), P-G6. Confiança: alta (minha).

## 5. Requisitos não funcionais

| ID | Requisito | Meta (testável) | Fonte / confiança |
|---|---|---|---|
| RNF-01 | Tamanho da skill (arquivo único `SKILL.md`, D17) | ≤ 12 KB e ≤ 220 linhas (≈ 3 mil tokens); a v1 tem 9,7 KB em 2 arquivos | P-A9, P-G5 · média |
| RNF-02 | — | Fundido no RNF-01 (antes: limite próprio do `tipos.md`) | — |
| RNF-03 | — | Fundido no RNF-01 (antes: soma dos dois arquivos) | — |
| RNF-04 | Tamanho do prompt gerado | Linhas com texto (sem cabeçalhos e linhas em branco) até o teto da faixa da tabela abaixo; até +20% é aviso, salvo enchimento apontado pelo corretor (D20); quando passaria, o conteúdo excedente vira referência a arquivo. Ficar abaixo do piso não é falha | P-G5 · média nas pontas; baixa (minha) nas faixas intermediárias |
| RNF-05 | Custo por execução | ≤ 3 chamadas de contexto, e no máximo 1 AskUserQuestion (a skill inteira já vem carregada, sem leitura extra); zero subagentes e zero buscas na web | P-A9 · alta (minha) |
| RNF-06 | Idioma | pt-BR em toda a skill e nos prompts gerados | P-G6 · baixa (benefício), alta (preferência) |
| RNF-07 | Compatibilidade | Frontmatter válido; a skill aparece em `/` e não é invocada pelo modelo sozinha | Teste da v1 |

Faixa de tamanho do prompt gerado, contando as linhas do bloco `text`:

| Tipo | Linhas |
|---|---|
| Explicar, Escrever | 6–25 |
| Pesquisar, Analisar, Planejar | 10–35 |
| Revisar | 12–45 |
| Implementar | 15–45 |
| Corrigir bug | 15–35 |
| Agêntica longa | 30–80 |

Contagem e tolerância (D20): contam só as linhas com texto; cabeçalhos (`#`) e linhas em branco não contam. Passar do teto em até 20% gera **aviso**, não falha, a menos que o corretor aponte enchimento. Acima de 20%, é falha.

## 6. Arquitetura

```
claude-prompt-skill/
├── skills/prompt/SKILL.md   ← a skill, instalada em ~/.claude/skills/prompt/. Arquivo único: frontmatter, fluxo (seção 7),
│                              regra de escolha do tipo, esqueleto (seção 8), checklist, entrega e "Tipos de tarefa" (seção 9)
├── docs/                    ← esta especificação e a pesquisa (research/)
└── evals/                   ← casos, scripts (run.py, check.py, compare.py, session.py, cache_stats.py, make_fixtures.sh),
                               baselines/v2.0, fixture-sources/skill-v1 e runs/; roteiro em evals/README.md
```

| Arquivo | Responsabilidade | Carregado em runtime? |
|---|---|---|
| `SKILL.md` | Fluxo, regra de escolha do tipo, regra de perguntar ou assumir, esqueleto, checklist curto (P-G7) com os anti-padrões, formato de entrega e a seção "Tipos de tarefa" (itens obrigatórios, faixa de tamanho e template por tipo) | Sim, sempre e inteiro |
| ~~`tipos.md`~~ | **Removido (D17).** O conteúdo foi para o fim do `SKILL.md` | — |
| **checklist** | **Não vira arquivo.** Fica dentro do `SKILL.md`, no lugar das "Regras de escrita" da v1 | Mais uma leitura por execução, sem ganho |
| **exemplos** | **Não vira arquivo.** Nenhum exemplo completo de entrada e saída na skill | Exemplos são copiados com fidelidade, inclusive nos defeitos (P-B7), e custam tokens. Só volta se os evals mostrarem formato inconsistente |
| `evals/cases.md` | Casos de teste e resultados | Não. Fica fora de `prompt/` para não ser instalado |

**Frontmatter proposto:**
```yaml
---
name: prompt
description: Reescreve um pedido escrito às pressas como um prompt estruturado (objetivo, contexto, escopo, critério de pronto, autonomia e formato de saída por tipo de tarefa). Use digitando /prompt seguido do pedido.
argument-hint: <o que você quer pedir>
disable-model-invocation: true
---
```

Notas e dúvidas sobre o frontmatter:
- `name`, `description`, `argument-hint` e `disable-model-invocation` são os mesmos campos da v1, que funcionou. Confiança: alta.
- Não usei `allowed-tools`. `git diff`, `ls`, `cat`, `grep`, `find` e o git só de leitura não pedem permissão (confirmado pelo usuário), então o campo não traria ganho.
- Não usei `model` nem um campo de esforço no frontmatter. O esforço depende do pedido e é orientado na entrega (RF-21).
- Com `disable-model-invocation: true`, a `description` serve só para o menu `/`, não para disparo automático. Por isso ela ficou curta. **Dúvida [a verificar]:** o comportamento exato da `description` nesse modo.

## 7. Fluxo da skill

0. **Entrada.** Se `$ARGUMENTS` estiver vazio, faça uma pergunta e pare (RF-01).
1. **Classifique** com a regra de escolha e o desempate do passo 1 do `SKILL.md`. Escolha o tipo principal; se houver um secundário, cite-o em Suposições e acrescente os itens dele (RF-03).
2. **Colete contexto** com no máximo 3 leituras: estrutura, arquivo de build e alvo da tarefa (RF-04). Não comece a tarefa.
3. **Perguntar ou assumir.** Pergunte só se as duas condições abaixo forem verdadeiras:
   - (a) a resposta muda materialmente o resultado;
   - (b) as leituras do passo 2 não resolvem.

   Gatilhos típicos que satisfazem as duas condições:
   - dois comportamentos de negócio plausíveis e incompatíveis (por exemplo, o que conta como "cliente duplicado");
   - ação destrutiva ou irreversível sem autorização clara (apagar dados, push, migração em produção);
   - alvo ambíguo depois da leitura (vários candidatos e nenhum diff);
   - público ou destino de um texto que mudam o tom (cliente versus time interno).

   Não são motivo para perguntar: versão, estrutura, comando de teste (são descobertos), preferências de estilo com default razoável e tamanho de texto (vira suposição).

   Se for perguntar, faça de 1 a 3 perguntas numa única vez, com 2 a 4 opções cada, e espere a resposta. Se não for, registre as suposições para a seção Autonomia (RF-05).
4. **Monte o prompt** com o esqueleto da seção 8 e os itens do tipo (RF-06 a RF-13 e RF-16 a RF-19). Trate os anti-padrões do pedido (RF-15).
5. **Passe o checklist** abaixo. Ele é aplicado pela skill ao próprio rascunho, sem ser escrito no prompt.
   - A primeira linha está no imperativo.
   - Um colega sem contexto conseguiria executar o prompt.
   - Cada restrição tem motivo.
   - O escopo está explícito.
   - O pronto é verificável.
   - A autonomia nomeia ações.
   - O formato tem limite concreto.
   - Os insumos estão em tags ou referenciados por caminho.
   - Não há anti-padrões.
   - Não há conflito com o CLAUDE.md.
   - O tamanho está na faixa do tipo.
   - Não há seção vazia.

   Fonte: P-G7.
6. **Entregue** no formato do RF-20, com Modo e Esforço (RF-21).
7. **Aprovação:** um "sim" executa o prompt; um pedido de ajuste reescreve só o que foi pedido (RF-22).

## 8. Esqueleto do prompt gerado

Ordem fixa. Cada seção é omitida quando fica vazia. Usa cabeçalhos Markdown para as instruções e tags XML para os insumos (P-G1, P-B6).

```text
<Objetivo no imperativo, 1–2 frases, incluindo o "para quê">

## Contexto
Por que isso importa, onde se encaixa, stack e versões reais (só o que não está no CLAUDE.md).

## Insumos
Arquivos a ler: caminho/A.java, caminho/B.py
<erro>…colado pelo usuário, só o essencial…</erro>

## Tarefa e escopo
O que fazer (passos numerados só se a ordem importar). Fora do escopo: X, porque Y.

## Restrições
- Regra, porque motivo.

## Pronto quando
- Critério observável; comando real (ex.: `./mvnw test -Dtest=PedidoServiceTest` passa).
- O que não fazer para "passar" (ex.: não editar o teste).

## Autonomia
Pode fazer sem perguntar: … · Pergunte antes de: <ações nomeadas>.
Suposições: … (diga se alguma estiver errada). Antes de assumir algo fora desta lista, investigue no código.

## Formato da resposta
<template do tipo, seção 9>
```

## 9. Templates por tipo de tarefa

Os 9 tipos vêm da P-D. "Deve conter" é o que o prompt precisa trazer (RF-13). "Formato" é o que vai em "Formato da resposta" (RF-12). Os números de limite são default e podem ser ajustados ao pedido. Confiança alta para o conteúdo, que vem da P-D; os limites numéricos são meus, com confiança baixa (P-G3 recomenda que existam, não os valores).

### 9.1 Implementar código
Deve conter: comportamento esperado e critérios de aceite; arquivos ou módulos onde o código entra (por caminho); convenções que mudam o resultado (Spring: camadas, DTOs, JUnit 5/Mockito; Python: tipagem, pytest); "não adicione abstrações, opções ou configurabilidade não pedidas"; comando de teste e build.
```
1. Resumo em até 3 frases; a primeira diz o que foi entregue.
2. Arquivos criados ou alterados: um por linha, com o porquê.
3. Verificação: comandos rodados e resultado.
4. Riscos e pendências (até 5 itens; omita se não houver).
```

### 9.2 Corrigir bug
Deve conter: sintoma, com erro ou stack trace em `<erro>`; o esperado versus o obtido; como reproduzir; ambiente e versões; o que já foi tentado, se o usuário disse; pedido de causa raiz antes da correção; teste que falha antes e passa depois; "não altere o teste nem fixe valores para fazê-lo passar".
```
1. Causa raiz em 1–2 frases, com evidência (arquivo:linha, log ou saída).
2. Correção mínima aplicada (diff ou arquivos).
3. Teste que reproduz: falhava antes, passa depois (comando e resultado).
4. Efeitos colaterais ou outros pontos com o mesmo padrão (até 5).
```

### 9.3 Revisar ou auditar
Deve conter: o alvo (diff, PR, arquivos, branch); os critérios (segurança, transações, N+1, concorrência, tratamento de erros…); a escala de severidade; "não altere código"; "reporte todos os achados com severidade, separe confirmado de suspeita e investigue antes de afirmar".
```
1. Veredito: APROVAR | APROVAR COM RESSALVAS | PEDIR MUDANÇAS, com o motivo em 1 frase.
2. Tabela por severidade (crítico, alto, médio, baixo): severidade | arquivo:linha | problema | evidência | sugestão.
3. Suspeitas não confirmadas (até 5).
4. O que manter (até 3 itens).
```
Se o usuário pedir "só os graves": crítico e alto em detalhe, depois "Outros achados" com uma linha para cada. Nenhum achado é omitido (D7).

### 9.4 Pesquisar ou comparar
Deve conter: a decisão que a pesquisa apoia; os critérios, com peso quando houver; as restrições (licença, custo, compatibilidade com a stack real, por exemplo Java 21 ou Spring Boot 3); fontes primárias com data; separação entre fato, inferência e opinião.
```
1. Resposta direta em 1–2 frases.
2. Tabela comparativa pelos critérios.
3. Recomendação com nível de confiança (alta, média ou baixa) e o porquê.
4. Fontes: link e data (fato, inferência ou opinião marcados).
```

### 9.5 Explicar ou ensinar
Deve conter: o nível de quem lê e o que já sabe (descreva a audiência, não uma persona; P-B4); a profundidade e o comprimento; um exemplo no contexto do usuário (classe ou módulo real, se houver); o uso pretendido.
```
1. Resumo em 2–3 frases.
2. Explicação progressiva (até ~300 palavras).
3. Exemplo mínimo executável na stack do usuário.
4. Armadilhas comuns (3–5).
(Exercício só se o pedido mencionar estudo, prova ou entrevista.)
```

### 9.6 Escrever texto
Deve conter: a audiência e o que ela deve fazer depois de ler; o tom e o canal; o comprimento-alvo; os pontos obrigatórios; um exemplo de estilo, se o usuário der; palavras ou clichês a evitar, só se o usuário citar (a lista de "slop words" da OpenAI é para o GPT-6 e não é importada).
```
O texto final, pronto para colar, com até <N> palavras/linhas, sem meta-comentário.
Variantes só se pedidas.
```

### 9.7 Analisar dados
Deve conter: a pergunta de negócio; o caminho dos dados e o significado das colunas ou campos importantes (ou "inspecione o esquema primeiro"); calcular com código executado, não de cabeça; o tratamento de nulos e outliers.
```
1. Achados principais com números (até 5 itens; o primeiro responde à pergunta).
2. Tabela de números de apoio.
3. Método: filtros, código ou comandos usados.
4. Limitações dos dados (até 3).
```

### 9.8 Planejar ou decidir
Deve conter: o objetivo, o horizonte e o prazo; as restrições e os recursos; as alternativas já consideradas; os critérios de decisão; pedido de premissas explícitas e de uma escolha justificada, não só uma lista.
```
1. Recomendação e motivo principal (até 3 frases).
2. Opções com prós e contras (tabela, até 4 opções).
3. Plano em etapas com esforço estimado.
4. Riscos e mitigação.
5. Premissas e o que mudaria a decisão.
```

### 9.9 Agêntica longa
Deve conter: o objetivo e um critério de pronto verificável de ponta a ponta; os arquivos de estado (git, `progress.md` ou lista de testes); permissões (o que pode fazer sem perguntar e o que exige confirmação: push, migração, deleção, nova dependência); atualizações curtas de progresso. Subagentes só entram se o usuário pedir (P-E6). Na v2 saiu o bloco "terminar a tarefa", que dependia de uma afirmação sobre o Fable 5.2.
```
Durante: atualizações de 1–2 linhas a cada etapa concluída.
Final (autocontido, para quem não acompanhou):
1. Resultado na primeira frase.
2. O que foi feito, por etapa.
3. Verificação: comandos e resultados.
4. Pendências e decisões que precisam de você.
```

## 10. Anti-padrões

### 10.1 A skill nunca insere no prompt gerado

| # | Anti-padrão | Por quê | Fonte |
|---|---|---|---|
| A1 | "Pense passo a passo", tags `<thinking>`, pedir o raciocínio na resposta | Ganho marginal e custo de 20–80% a mais de tempo (OpenAI, Google, Wharton) | P-B1, P-E1 · alta |
| A2 | CAIXA ALTA, "CRITICAL", "OBRIGATÓRIO", "você DEVE" | Overtriggering | P-B2, P-E2 · alta |
| A3 | Persona ("você é um especialista sênior…") | Não aumenta a acurácia | P-B4, P-E3 · alta |
| A4 | Gorjeta, ameaça, apelo emocional ("é muito importante") | Sem efeito | P-B5, P-E4 · alta |
| A5 | Instruções herdadas: "verifique duas vezes", "sempre verifique tudo", "use subagentes", "responda sem pensar", orçamento de tokens | Anthropic e OpenAI convergem: instruções herdadas de modelos antigos causam over-verification e delegação excessiva (o detalhe por modelo foi descartado) | P-E6 · média |
| A6 | Regras "nunca" sem motivo | Dizer o que fazer e por quê funciona melhor | P-A2, P-A3 · alta |
| A7 | "Você pode sugerir…" quando o pedido é de ação | O Claude só sugere | P-E8 · alta |
| A8 | Colar arquivos do repositório ou histórico irrelevante | Degradação com contexto longo | P-A9, P-E9 · alta |
| A9 | Seções vazias, frameworks empilhados (CO-STAR + RISEN…) | Tokens sem sinal | P-C, P-E10 · média |
| A10 | Aprovação vaga ("tenha cuidado com coisas perigosas") | O esqueleto recomenda nomear as ações que exigem confirmação | P-G1 · média |
| A11 | Prefill e parâmetros de amostragem | Não se aplicam ao Claude Code; o prefill dá erro 400 na API | P-B3, P-B10 · alta |

### 10.2 Quando o pedido do usuário contém um deles

Regra geral: preserve a **intenção** e descarte a **técnica**. Registre a mudança em "O que mudou".

| No pedido | Ação |
|---|---|
| "pensa passo a passo", "raciocina bem" | Remove do prompt. Se a tarefa for difícil, sugere Esforço: alto |
| "URGENTE", "MUITO IMPORTANTE", caixa alta | Remove a ênfase. Se houver prazo real, ele vai para Contexto como fato ("precisa sair hoje") |
| "você é um especialista em X" | Converte em contexto de audiência ou escopo ("foco em desempenho de Python") ou remove |
| Gorjeta ou ameaça | Remove |
| "verifica duas vezes", "revisa a resposta" | Converte em critério em "Pronto quando" |
| "só os graves" numa revisão | Graves (crítico e alto) em detalhe; depois "Outros achados", uma linha cada. Nenhum achado é omitido (D7). Avisa em "O que mudou" |
| "pode sugerir…" quando o contexto indica ação | Imperativo, mas se a intenção for de fato "só sugerir", mantém "não altere arquivos" |
| "usa subagentes" ou outra instrução operacional explícita | **Preserva.** É um pedido real do usuário, não um tique herdado; a regra A5 vale só para inserção por padrão |
| "nunca faça X" sem motivo | Mantém a restrição e acrescenta o motivo provável como suposição |

## 11. Plano de avaliação

**Ambiente:** quatro fixtures mínimas (`spring`, `python`, `skillproj` e `vazio`). Cada caso roda com `claude -p`, numa sessão nova, num HOME temporário com só a versão testada instalada, uma vez com a v1 e outra com a v2.

**Critério:** um caso passa se todos os critérios aplicáveis, comuns e específicos, forem cumpridos. Cada marcação cita o trecho do prompt gerado que a justifica.

**Meta para liberar a v2:** pelo menos 13 de 15 casos passando e nenhum caso em que a v2 fique pior que a v1 (a v1 passa e a v2 falha, ou a v2 cumpre menos critérios).

Os 15 casos, com pedido, fixture, tipo esperado e critérios, ficam em **`evals/cases.md`**, a única fonte. Cinco deles são mensagens reais do usuário: #2, #4, #5, #7 e #15. A cobertura dos 9 tipos e os critérios comuns C1–C6 também estão lá. Os resultados, com os prompts lado a lado, ficam em `evals/results.md`.

## 12. Decisões e suposições

Nenhuma decisão exigiu pergunta: a pesquisa e a v1 resolveram tudo, ou a escolha era barata de reverter.

1. **D1: o checklist e os anti-padrões ficam dentro do `SKILL.md`**, não num arquivo separado. Uma leitura a menos por execução e menos sobreposição (RNF-03).
2. **D2: nenhum arquivo de exemplos.** O risco de cópia fiel (P-B7) e o custo superam o ganho. A decisão é revista se os evals mostrarem formato inconsistente.
3. **D3: os evals ficam fora da pasta instalada.** Rodam com `claude -p` num HOME temporário, e a conferência é binária, critério a critério, com trecho citado (`evals/results.md`). No `-p` não há resposta do usuário, então os casos de "deve perguntar" avaliam só a primeira rodada, e o RF-22 (aprovação e ajuste) não é coberto.
4. **D4: as suposições ficam dentro do prompt**, não na entrega. O executor precisa vê-las; você as vê de qualquer forma no bloco.
5. **D5: "O que mudou" foi mantido**, com 1 a 3 itens. Custa pouco e é onde aparecem os anti-padrões removidos (RF-15).
6. **D6: o plan mode foi mantido** mesmo sem respaldo na pesquisa (confiança baixa). É um recurso do Claude Code e foi útil na v1.
7. **D7 (revisada pelo usuário): "só os graves"** vira graves em detalhe e depois "Outros achados", com uma linha cada. Nunca omite achados.
8. **D8: instruções operacionais explícitas do usuário** (por exemplo, "usa subagentes") são preservadas. A proibição vale só para a inserção por padrão.
9. **D9: o CLAUDE.md não é lido pela skill.** A suposição é que ele está no contexto da sessão. CLAUDE.md de subpastas pode não estar, mas a skill não vai atrás deles (custo).
10. **D10: limites numéricos dos templates e faixas de tamanho intermediárias** são escolhas minhas, com confiança baixa, a calibrar pelos evals.
11. **D11: a lista de "slop words" da OpenAI não é importada.** Ela é específica do GPT-6, e a skill gera prompts para o Claude.
12. **D12: Markdown para as seções e XML para os insumos**, conforme P-B6. A confiança é média; não há estudo comparativo direto.
13. **Suposição S1:** você roda a skill quase sempre dentro de um repositório git. Fora de um projeto, o RF-04 faz zero chamadas.
14. **Suposição S2 (revisada):** as fixtures dos evals são projetos mínimos criados para o teste (Spring Boot 3.3.5/Java 21, Python 3.12, uma cópia do projeto da skill v1 e uma pasta vazia). Assim os testes são reproduzíveis e não tocam nos seus projetos.
15. **D13: regras específicas de modelo removidas** (pedido do usuário): ownership de código e bloco "terminar a tarefa" (Fable 5.2), regra geral "1ª frase = resultado" (guias do Opus 5 e do Fable 5.2), verificação proporcional (Opus 5 e GPT-6 Astra) e recusa `reasoning_extraction`. Ficam só os princípios que várias fontes confirmam.
16. **D14: 5 casos de eval trocados** por mensagens reais do usuário (#2, #4, #5, #7, #15), mantendo a cobertura dos 9 tipos. O caso de persona saiu.
17. **D15: tetos calibrados na rodada 2** (11/11/2026). Revisar subiu de 30 para 45 linhas e Pesquisar de 25 para 35. Nos únicos casos válidos (#15 e #7, que leram o `tipos.md`), as linhas a mais eram conteúdo. No #15, checar prontidão para instalar exige listar o que conferir em 3 arquivos. No #7, o pedido traz duas decisões (nome e licença). Os outros tetos aguardam dados válidos, porque nos demais casos o `tipos.md` não foi lido (ver seção 13).
18. **D16: limite de leituras mantido em 3.** O único caso com 4 leituras (v2-01) era uma nova tentativa depois de um comando bloqueado, sem informação nova. O `check.py` passou a não contar chamadas que falharam.
19. **D17: `tipos.md` fundido no `SKILL.md`** (rodada 3, decisão do usuário). O conteúdo é usado em toda execução, e a documentação de skills reserva arquivos de apoio para material usado "only when needed". Separado, ele custava uma leitura a mais e criava um ponto de falha de permissão: no `claude -p`, a leitura foi negada em 21 de 28 execuções, e o mesmo pode acontecer no uso real. Os limites por arquivo viraram um único: 12 KB e 220 linhas (RNF-01). Isso também resolve o ponto 9 da seção 13.
20. **D18: regra de escolha do tipo e desempate no passo 1** (rodada 3): Pesquisar = comparar opções conhecidas; "como faço X" sem pedido de execução = Planejar; projeto inteiro ou muitos arquivos = Agêntica longa. Quando dois tipos servem, vale o de formato de saída mais útil, e o outro vai para Suposições. Motivo: na rodada 2, #7, #11 e #12 foram mal classificados.
21. **D19: a skill não resolve a tarefa no prompt** (rodada 3). Ela não antecipa diagnóstico, causa, conclusão nem solução: descreve o sintoma e o objetivo. Motivo: no v2-03 (rodada 2), a causa do bug veio escrita no prompt, e o executor já não precisava investigar.
22. **D20: tetos calibrados na rodada 3 e regra de contagem** (aprovado pelo usuário em 11/11/2026). Implementar 35 → 45, Explicar 15 → 25, Escrever 15 → 25, Analisar 25 → 35, Planejar 25 → 35. Na rodada 3 (com o `tipos.md` carregado), os prompts acima do teto nesses tipos eram conteúdo, não enchimento. Os de Explicar e Escrever estouravam só pelo custo fixo do esqueleto (cabeçalhos e linhas em branco). Passam a contar só as linhas com texto. Até +20% sobre o teto é aviso, e vira falha só se o corretor apontar enchimento. Como a calibração foi feita depois de ver os resultados, a aprovação depende de 4 casos de validação nunca vistos (`evals/validation-cases.md`).
23. **D21: exceção no critério da M1b** (rodada A2 da v2.3, decisão do usuário em 13/11/2026). Pela regra gravada antes de rodar, a M1b (motivo de restrição só do pedido, das leituras ou da tarefa) não seria aceita: o 2º critério pedia enchimento do #19 em menos repetições que a base, e a base teve 0 de 3 nessa correção, então nenhum resultado o cumpriria. Os outros dois critérios cumpriram ("inventado" 0 contra 2, nenhuma regressão). A M1b foi mantida, e a exceção virou confirmação gravada antes da rodada B: se o "inventado" passar de 1 repetição na rodada B, a M1b é desfeita e a rodada B é refeita sobre `versoes/v2.3-rodada-a/` (`evals/runs/v2.3-round-a2/decisao.md`).
24. **D22: estudo da v2.3, não aprovada** (13/11/2026; regras gravadas antes de rodar em `evals/validation-cases.md`). Partiu da v2.2 com Opus em effort medium e Claude Code 2.1.323 fixos no `run.py`, correção cega com a candidata e a base na mesma passada e 3 repetições. Aceitas nas rodadas: M6 (`effort: medium` no cabeçalho, que vence o `--effort`), M1 (requisito ou fato fora do pedido vai em Suposições com "confirme:"; Escrever texto só com os pontos e a ação do leitor que o pedido traz), M2 (Agêntica longa pelo escopo do pedido, mesmo com poucos arquivos hoje) e M1b (motivo de restrição só do pedido, das leituras ou da tarefa; D21). Reprovadas: M3 e M4 (Contexto só com fatos que mudam a execução; "O que mudou" com 1 ou 2 itens): a saída caiu só 2%, contra o mínimo de 5%. Adiada: M5 (seção 13). Resultado: validação 13/15 (4/5 · 5/5 · 4/5), mas os 15 casos de `cases.md` deram 12/15, com regressão contra a v2.0 em #14 (gerou prompt em vez de perguntar antes de "apaga os clientes duplicados do banco": efeito da regra "assuma o padrão razoável" da v2.2), #11 (Modo normal em vez de plan mode) e #06 (enchimento, limítrofe). A candidata fica em `versoes/v2.3-rodada-a2/`; resultados em `evals/runs/v2.3-round-a*`, `runs/v2.3-round-b`, `runs/v2.3-regression` e `results.md`.
25. **D23: v2.0.1 instalada** (16/11/2026, decisão do usuário). É a v2.0 com `effort: medium` no cabeçalho: todas as aprovações da v2.0 foram medidas em medium (os evals nunca rodaram em high, ver `results.md`), e o padrão do usuário passou a ser high. A v2.2, reprovada, estava instalada e foi substituída.
26. **D24: o caso #21 foi trocado pelo #23 na validação da v2.4** (16/11/2026, decisão do usuário, depois de rodar). O #21 (`renomeia o campo email do Cliente pra emailContato no código todo`) era ambíguo: na fixture `spring`, `ddl-auto=update` e `Cliente.email` sem `@Column` tornam a renomeação um risco real de dados, e perguntar também é defensável. A v2.4 só falhou o item 1 da regra por esse caso (1 de 3 repetições passando em tudo: uma perguntou e outra fez 4 leituras). O #23 testa o mesmo comportamento sem efeito em dados. A skill não mudou, então os outros 7 casos continuam valendo (`evals/runs/v2.4-validation/decisao.md`).
27. **D25: v2.4 aprovada e instalada** (16/11/2026; regra gravada antes de rodar em `evals/validation-cases.md`, "Validação da v2.4"). É a candidata da v2.3 (M6, M1, M2, M1b) com duas regras novas: no passo 3, ação que apaga ou sobrescreve dados ou migra banco sempre pergunta o que será afetado, mesmo com padrão razoável (corrige a regressão do #14); e plan mode para planejar migração (estabiliza o #11). Correção cega dupla (só conta a falha marcada pelos dois corretores, `evals/grader.md`). Validação, 8 casos × 3 repetições (#21 trocado pelo #23, D24): #12 e #16–#19 5/5 nas 3, #20 perguntou nas 3, #22 plan mode nas 3, #23 2 de 3. Casos de `cases.md`: v2.4 15/15 contra 12/15 da v2.0 na mesma correção, sem regressão. O `run.py` passou a chamar o binário da versão fixada (`~/.local/share/claude/versions/2.1.323`), porque o Claude Code se atualizou para a 2.1.326 durante a rodada. Saída instalada em `~/.claude/skills/prompt/` e empacotada em `prompt-skill.zip`.
28. **D26: v2.5 não aprovada** (16/11/2026). Resolveu o exagero na troca mecânica (#23 e #24: Implementar código, modo normal, sem `ultrathink`, 3 de 3; `progress.md` apagado no fim do #12), mas reprovou: (1) regressão mecânica no #11, que virou Agêntica longa porque a regra nova cita "migrar, atualizar versão" como exemplos e puxou um "como faço" para execução; (2) "inventado" no #23 em 2 de 3, um "para quê" que o pedido não dá, provavelmente pedido pelo modelo do prompt ("Objetivo… com o 'para quê'"). A v2.4 continua instalada e volta para `skills/prompt/`; a candidata fica em `versoes/v2.5-reprovada/` (`evals/runs/v2.5-validation/decisao.md`).
29. **D27: v2.6 não aprovada** (16/11/2026). Corrigiu a regressão do #11 e manteve a troca mecânica certa (itens 2 e 3 da regra cumpridos: 15/15 contra 12/15 da v2.0, sessão longa sem exagero e US$ 0,45). Reprovou no item 1 por "inventado" em 2 de 3 no #12 (atribui ao CLAUDE.md a convenção JUnit 5/Mockito, que vem do modelo do tipo Implementar na skill) e no #17 (escolhas de redação como requisito firme). A v2.4 continua instalada; candidata em `versoes/v2.6-reprovada/` (`evals/runs/v2.6-validation/decisao.md`).
30. **D28: v2.7 aprovada e instalada** (17/11/2026; regra gravada antes de rodar em `evals/validation-cases.md`, "Validação da v2.7"). Partiu da v2.6 e tirou a fonte do "inventado": o modelo do tipo Implementar não lista mais stacks de exemplo (JUnit 5/Mockito, tipagem/pytest), só "as convenções que o CLAUDE.md ou as leituras mostram no projeto"; em Escrever texto, a estratégia de redação que o pedido não traz vai em Suposições com "confirme:". Os 3 itens cumpridos: validação sem nenhum "inventado" (r1 9/9 · r2 8/9 · r3 8/9), 15 casos 15/15 contra 10/15 da v2.0, sessão longa sem exagero e US$ 0,43. Instalada em `~/.claude/skills/prompt/`, `versoes/v2.7/` e `prompt-skill.zip` (`evals/runs/v2.7-validation/decisao.md`).
31. **D29: limpeza** (17/11/2026). Removidos do repositório as cópias de versões intermediárias e reprovadas (`evals/baselines/v2.0.1`, `v2.1`, `v2.2*`, `v2.3-rodada-a*`, `v2.5-reprovada`, `v2.6-reprovada`), os scripts da comparação v1×v2 e da v2.2 (`cegar.py`, `consolidar.py`, os subcomandos `cegar` e `consolidar` do `compare.py`), o `linha_base.py` (pedia um formato de julgamento que o fluxo atual não gera) e as rodadas de rascunho `runs-3-teste` e `runs-m6`. Ficam as rodadas citadas nas decisões, porque são a evidência delas. As referências antigas a esses caminhos nas decisões continuam valendo como registro: o conteúdo está no git (`git show 0ec0517:<caminho>`). Também apagados os HOMEs temporários (`evals/tmp/home/`, com cópias das versões antigas da skill) e as cópias de trabalho das sessões longas. Conferido antes: `make_fixtures.sh` recria as fixtures idênticas às usadas, e nenhuma execução as alterou.

32. **D30: reorganização com nomes descritivos em inglês** (17/11/2026, decisão do usuário). Nomes de pastas e arquivos em inglês e kebab-case, sem espaços; o conteúdo continua em português. As cópias `versoes/v2.4` e `versoes/v2.7` saíram (as versões ficam nas tags `v2.4` e `v2.7`) e o `prompt-skill.zip` passou a ser anexo da Release do GitHub, fora do git. As referências antigas nas decisões acima foram atualizadas; para ler um nome antigo, use a tabela:

| Antes | Depois |
|---|---|
| `v2/prompt/` | `skills/prompt/` |
| `SPEC.md`, `pesquisa-prompts.md` | `docs/spec.md`, `docs/research/prompt-engineering-research.md` |
| `research_notes/`, `reports/` | `docs/research/token-savings/`, `docs/research/token-savings-report.md` |
| `versoes/v2.0`; `v1/prompt-skill` | `evals/baselines/v2.0`; `evals/fixture-sources/skill-v1` |
| `rodar.py`, `checar.py`, `comparar_versoes.py`, `sessao.py`, `medir_cache.py`, `criar_fixtures.sh` | `run.py`, `check.py`, `compare.py`, `session.py`, `cache_stats.py`, `make_fixtures.sh` |
| `casos.md/.tsv`, `casos-validacao.md/.tsv`, `corretor.md`, `resultados.md` | `cases.md/.tsv`, `validation-cases.md/.tsv`, `grader.md`, `results.md` |
| `runs-2`, `runs-3`, `runs-val` | `runs/v1-vs-v2.0-round2`, `runs/v1-vs-v2.0-round3`, `runs/v2.0-validation` |
| `runs-v21`, `runs-v22`, `runs-base`, `runs-sonnet` | `runs/v2.1-validation`, `runs/v2.2-validation`, `runs/v2.2-baseline-opus`, `runs/v2.2-baseline-sonnet` |
| `runs-a`, `runs-a2`, `runs-b`, `runs-v23-15` | `runs/v2.3-round-a`, `-round-a2`, `-round-b`, `runs/v2.3-regression` |
| `runs-vNN`, `runs-vNN-15` (v2.4 a v2.7) | `runs/v2.N-validation`, `runs/v2.N-regression` |
| `runs-sessao/s1–s3`, `v26-s1`, `v27-s1` | `runs/v2.4-sessions/s1–s3`, `runs/v2.6-session`, `runs/v2.7-session` |
| `tmp-home/`, `tmp-sessao/` | `tmp/home/`, `tmp/session/` |

As saídas do modelo guardadas nas rodadas (respostas, transcrições, cópias cegas) não foram alteradas e podem citar os caminhos antigos.

## 13. Riscos e pontos "a verificar"

**Riscos:**

| Risco | Efeito | Mitigação |
|---|---|---|
| A v2 gera prompts maiores que a v1, por ter mais seções (Insumos, Autonomia) | Contradiz o objetivo de enxugar | RNF-04 por tipo; omitir seções vazias; Autonomia reduzida em tarefas só de leitura (RF-11) |
| Autonomia vira texto padrão repetido em todo prompt | Ruído | CA do RF-11 exige ações nomeadas; nada de frases genéricas |
| Grande parte da evidência é de fornecedor, e os estudos independentes usam múltipla escolha | As recomendações podem não valer para agentes de código | Evals próprios (seção 11); P-Caveats |
| 15 casos é uma amostra pequena; a variação por execução é alta (P-A10) | Falso passa ou falso falha | Rodar os casos que falharem 2 vezes; comparar sempre v1 e v2 |
| As regras específicas de modelo são perecíveis | A skill envelhece a cada modelo novo | Rodar os evals a cada troca de modelo (P-Caveats) |
| A skill pergunta demais ou de menos | Fricção ou erro de rumo | Casos 2, 5 e 9 (não perguntar) contra o caso 14 (perguntar) |

**Pontos "a verificar": estado em 17/11/2026**

Resolvidos pelo usuário:
1. **Esforço:** com Esforço alto, a entrega orienta `/effort xhigh` para executar na sessão e põe `ultrathink` na 1ª linha para quando o prompt for colado. `ultrathink` só funciona digitado no terminal (RF-21).
2. **Permissões:** `git diff`, `ls`, `cat`, `grep`, `find` e o git só de leitura não pedem permissão, então `allowed-tools` não é usado (seção 6).
3. **`claude -p`** invoca a skill normalmente. Os evals rodam assim (D3).
4. **Afirmações sobre o Fable 5.2 e o Opus 5:** as regras que dependiam delas foram removidas (D13).

Abertos (não bloqueiam):
5. Campo de esforço ou de modelo no frontmatter: não é usado, então não afeta a v2.
6. Os números da OpenAI sobre prompts enxutos (+10–15% de nota e −41–66% de tokens), que a própria OpenAI chama de "direcionais" e chegaram via terceiro (Count.co). Sustentam RNF-01 a RNF-04 só como direção.
7. O comportamento do GPT-6 Astra (P-B9, P-E10): é só evidência de apoio, e nenhum requisito depende dele.

**Pendente da v2.3 (13/11/2026)**
10. **M5, juntar numa só chamada as leituras independentes: descartada** (17/11/2026). Nas 42 execuções da v2.7, o modelo já junta leituras sem a regra: 93 leituras em 68 requisições, 21 delas com mais de uma leitura, e vários `cat` encadeados num só Bash. No máximo seriam 31 requisições a menos em 110 (cerca de US$ 0,01 por `/prompt`), e parte das leituras depende da anterior (a estrutura indica o arquivo a ler). Uma versão nova custa cerca de US$ 5 e ~430 mil tokens de corretor só para validar, com risco de regressão (v2.5 e v2.6 reprovaram por efeitos colaterais). Também não mudaria o C2, que conta leituras, não requisições.

**Defeito de harness achado na rodada 2 (11/11/2026)**
8. ~~Pendente~~ resolvido pela D17 (arquivo único, sem `tipos.md` para ler) e pelo `--add-dir` do `run.py`, usado em todas as rodadas desde então. No `claude -p`, a ferramenta Read negava a leitura fora do diretório do projeto. Por isso, em 21 das 28 execuções que tentaram, a skill não conseguiu ler o próprio `tipos.md`, que fica no HOME temporário. Ela seguiu sem os templates e as faixas. A correção é o `--add-dir <pasta da skill>` no `run.py`, que já está aplicado e ainda não foi testado. Isso também afeta a rodada 1.
9. ~~Pendente~~ resolvido pela D17 (arquivo único): verificar se, no uso interativo, ler o `tipos.md` também pede permissão a cada `/prompt`. Se pedir, avaliar a alternativa de juntar `tipos.md` ao `SKILL.md`, que exigiria rever o RNF-01.
