---
name: prompt
description: Reescreve um pedido escrito às pressas como um prompt estruturado (objetivo, contexto, escopo, critério de pronto, autonomia e formato de saída por tipo de tarefa). Use digitando /prompt seguido do pedido.
argument-hint: <o que você quer pedir>
disable-model-invocation: true
model: sonnet
---

# Prompt

<pedido>
$ARGUMENTS
</pedido>

Reescreva esse pedido como um prompt para o Claude Code executar. Não execute o pedido agora; isso só acontece no passo 6, se o usuário aprovar. Até lá, use só leitura. Se o pedido estiver vazio, pergunte em uma frase o que o usuário quer pedir e pare.

## 1. Classifique

Escolha o tipo principal entre os 9 da seção "Tipos de tarefa", no fim deste arquivo: Implementar código, Corrigir bug, Revisar ou auditar, Pesquisar ou comparar, Explicar ou ensinar, Escrever texto, Analisar dados, Planejar ou decidir, Agêntica longa. Na linha "Tipo:", use o nome exato. Para escolher:
- **Pesquisar ou comparar:** comparar opções conhecidas (bibliotecas, licenças, nomes).
- **Planejar ou decidir:** "como faço X" sem pedido de execução; etapas, arquitetura, migração.
- **Revisar ou auditar:** julgar algo que já existe ("tá bom?", "posso instalar?").
- **Agêntica longa:** mudança no projeto inteiro ou em muitos arquivos.
- **Empate:** se dois tipos servem, escolha o que tem o formato de saída mais útil e cite o outro em Suposições. Acrescente os itens dele que se aplicarem.

## 2. Colete contexto (no máximo 3 leituras)

Dentro de um projeto, leia: a estrutura de pastas; o arquivo de build (`pom.xml`, `build.gradle*`, `pyproject.toml` ou `requirements.txt`); o alvo da tarefa (`git diff --stat`, o arquivo citado). O CLAUDE.md já está no contexto: não o leia e não repita o que ele diz. Fora de um projeto, não leia nada.

## 3. Pergunte ou assuma

Se existe um padrão razoável, inclusive em regra de negócio, assuma-o, gere o prompt e destaque a dúvida em Suposições começando com "confirme:". O usuário revisa o prompt antes de executar, então uma suposição errada custa só uma edição. Pare para perguntar só quando não há padrão razoável e as leituras não resolvem, por exemplo: um alvo ou sintoma desconhecido, ou uma ação destrutiva sem autorização clara.

Para perguntar: de 1 a 3 perguntas, de uma vez, cada uma com 2 a 4 opções. Use AskUserQuestion se existir; senão, escreva as perguntas e pare.

## 4. Escreva o prompt

Use as seções nesta ordem e omita as vazias (nunca escreva "N/A"):

```text
<Objetivo no imperativo, 1–2 frases, com o "para quê">

## Contexto
Só fatos que o pedido não diz (projeto, versões, o que existe hoje). Não repita o pedido nem invente objetivo.

## Insumos
Arquivos a ler: caminhos (sem colar o conteúdo).
<erro>, <log>, <trecho>: o que o usuário colou, só o essencial.

## Tarefa e escopo
O que fazer (passos numerados só se a ordem importar). Fora do escopo: X, porque Y.

## Restrições
- Regra, porque motivo.

## Pronto quando
- Critério observável, com o comando real do projeto.

## Autonomia
Pode fazer sem perguntar: … · Pergunte antes de: <ações nomeadas>.
Suposições: … (diga se alguma estiver errada).
[Só em Implementar, Corrigir bug, Revisar, Agêntica longa e Analisar dados com arquivos:] Antes de assumir algo fora desta lista, investigue no código.

## Formato da resposta
<template do tipo, em "Tipos de tarefa">
```

Regras:
- Não resolva a tarefa no prompt: não antecipe diagnóstico, causa, conclusão nem solução. Descreva o sintoma e o objetivo; o que as leituras mostraram entra como fato (arquivos, versões, o que existe hoje), não como resposta.
- Preserve literalmente identificadores, caminhos, mensagens de erro e números do pedido.
- Use verbos de ação ("Implemente", "Liste"). Com "você pode sugerir", o modelo só sugere.
- Dê o motivo de cada restrição e diga o que fazer, não só o que evitar.
- Em tarefa só de leitura, Autonomia fica só com as suposições.
- Exemplo de saída (`<example>`) só se o formato não for óbvio ou se o usuário der um (use o dele).
- Se a saída for para código ou ferramenta, peça JSON ou CSV com os campos nomeados.
- Tamanho: o mínimo que cobre o tipo (faixa no título do tipo). Se passar disso, referencie arquivos.
- Idioma: o do pedido. Código e identificadores no original.

Nunca insira no prompt:
- instrução de raciocínio: "pense passo a passo", "explique seu raciocínio", `<thinking>`. "Passo a passo" só fica quando vem do pedido e descreve a explicação (ex.: "me explica passo a passo"), nunca o modo de pensar;
- CAIXA ALTA de ênfase ou "OBRIGATÓRIO";
- persona ("você é um especialista");
- gorjeta, ameaça ou apelo emocional;
- "verifique duas vezes", "use subagentes" ou orçamento de tokens;
- regra "nunca" sem motivo;
- aprovação vaga ("tenha cuidado").

Se o pedido trouxer um desses itens, mantenha a intenção e descarte a técnica:
- urgência vira fato no Contexto (se houver prazo);
- persona vira audiência ou foco;
- "pensa bem" ou "pensa passo a passo" vira Esforço alto;
- "verifica duas vezes" vira critério em Pronto quando.

Instruções operacionais explícitas do usuário (por exemplo, "usa subagentes") ficam. Registre cada mudança em "O que mudou" e não cite no prompt o item removido, nem para proibi-lo.

## 5. Confira e entregue

Confira: um colega sem contexto executaria? Cada restrição tem motivo? O pronto é verificável? A Autonomia nomeia ações? Há seção vazia ou item proibido? Depois, entregue neste formato:

**Tipo:** <um dos 9 nomes, literal> · **Modo:** <normal | plan mode> · **Esforço:** <padrão | alto>

```text
<prompt>
```

**O que mudou:** <1 a 3 itens curtos>

Quer que eu execute este prompt agora?

- **Modo:** plan mode se a tarefa altera arquivos em 3 ou mais passos ou decide arquitetura; normal nos outros casos.
- **Esforço alto:** depuração difícil, arquitetura, auditoria profunda ou tarefa agêntica longa. Nesse caso, a primeira linha do prompt é `ultrathink` (vale quando o usuário cola o prompt, porque só funciona digitado), e depois de "alto" escreva: "para executar aqui, rode `/effort xhigh` antes de responder sim".

## 6. Aprovação

Se o usuário disser sim, execute o prompt como se ele tivesse acabado de enviá-lo. Se pedir ajustes, reescreva só o que mudou e entregue de novo no mesmo formato.

## Tipos de tarefa

Cada tipo traz: o que o prompt deve conter, a faixa de tamanho do prompt (linhas com texto; cabeçalhos e linhas em branco não contam) e o template de "Formato da resposta". Adapte ao pedido e não copie itens vazios.

### 1. Implementar código (15–45 linhas)
Deve conter: comportamento esperado e critérios de aceite; onde o código entra (caminhos); convenções que mudam o resultado (Spring: camadas, DTOs, JUnit 5/Mockito; Python: tipagem, pytest); "não adicione abstrações, opções ou configurabilidade não pedidas"; comando de teste e build.
```
1. Resumo em até 3 frases.
2. Arquivos criados ou alterados: um por linha, com o porquê.
3. Verificação: comandos rodados e resultado.
4. Riscos e pendências (até 5; omita se não houver).
```

### 2. Corrigir bug (15–35 linhas)
Deve conter: sintoma, com erro ou stack trace em `<erro>`; esperado versus obtido; como reproduzir; ambiente e versões; o que já foi tentado; causa raiz antes da correção; teste que falha antes e passa depois; "não altere o teste nem fixe valores para ele passar".
```
1. Causa raiz em 1–2 frases, com evidência (arquivo:linha, log ou saída).
2. Correção mínima aplicada.
3. Teste que reproduz: falhava antes, passa depois (comando e resultado).
4. Efeitos colaterais ou outros pontos com o mesmo padrão (até 5).
```

### 3. Revisar ou auditar (12–45 linhas)
Deve conter: o alvo (diff, arquivos, branch, projeto); os critérios (segurança, transações, N+1, concorrência, tratamento de erros, testes); "não altere código"; "reporte todos os achados com severidade, separe o confirmado da suspeita e investigue antes de afirmar".
```
1. Veredito: APROVAR | APROVAR COM RESSALVAS | PEDIR MUDANÇAS, com o motivo em 1 frase.
2. Tabela por severidade (crítico, alto, médio, baixo): severidade | arquivo:linha | problema | evidência | sugestão.
3. Suspeitas não confirmadas (até 5).
4. O que manter (até 3).
```
Se o usuário pedir "só os graves": crítico e alto em detalhe, depois "Outros achados" com uma linha para cada. Nenhum achado é omitido.

### 4. Pesquisar ou comparar (10–35 linhas)
Deve conter: a decisão que a pesquisa apoia; os critérios, com pesos se houver; as restrições (licença, custo, compatibilidade com a stack real); fontes primárias com data; separação entre fato, inferência e opinião.
```
1. Resposta direta em 1–2 frases.
2. Tabela comparativa pelos critérios.
3. Recomendação com confiança (alta, média ou baixa) e o porquê.
4. Fontes: link e data.
```

### 5. Explicar ou ensinar (6–25 linhas)
Deve conter: o nível de quem lê e o que já sabe (descreva a audiência, não uma persona); profundidade e comprimento; exemplo no código do usuário, se houver; para que vai usar.
```
1. Resumo em 2–3 frases.
2. Explicação progressiva (até ~300 palavras).
3. Exemplo mínimo executável na stack do usuário.
4. Armadilhas comuns (3–5).
```
Exercício só se o pedido falar em estudo, prova ou entrevista.

### 6. Escrever texto (6–25 linhas)
Deve conter: audiência e o que ela deve fazer depois de ler; tom e canal; comprimento-alvo; pontos obrigatórios; exemplo de estilo, se o usuário der; palavras a evitar, se o usuário citar.
```
O texto final, pronto para colar, com até <N> palavras, sem meta-comentário. Variantes só se pedidas.
```

### 7. Analisar dados (10–35 linhas)
Deve conter: a pergunta de negócio; o caminho dos dados e o significado dos campos importantes (ou "inspecione o esquema primeiro"); os cálculos feitos com código executado, não de cabeça; o tratamento de nulos e outliers.
```
1. Achados principais com números (até 5; o primeiro responde à pergunta).
2. Tabela de números de apoio.
3. Método: filtros, código ou comandos usados.
4. Limitações dos dados (até 3).
```

### 8. Planejar ou decidir (10–35 linhas)
Deve conter: objetivo, horizonte e prazo; restrições e recursos; alternativas já consideradas; critérios de decisão; premissas explícitas; uma escolha justificada, não só uma lista.
```
1. Recomendação e motivo principal (até 3 frases).
2. Opções com prós e contras (até 4).
3. Plano em etapas com esforço estimado.
4. Riscos e mitigação.
5. Premissas e o que mudaria a decisão.
```

### 9. Agêntica longa (30–80 linhas)
Deve conter: o objetivo e um critério de pronto verificável de ponta a ponta; o registro de progresso em `progress.md`, atualizado a cada etapa concluída para a tarefa poder ser retomada se for interrompida (criar e atualizar esse arquivo fica em "Pode fazer sem perguntar"); permissões (o que pode fazer sem perguntar e o que exige confirmação: push, migração, deleção, nova dependência).
```
Durante o trabalho: a cada etapa concluída, atualize `progress.md` (feito, próximo passo, pendências) e escreva 1–2 linhas no chat.
No final (autocontido, para quem não acompanhou):
1. Resultado em 1 frase.
2. O que foi feito, por etapa.
3. Verificação: comandos e resultados.
4. Pendências e decisões que precisam do usuário.
```
