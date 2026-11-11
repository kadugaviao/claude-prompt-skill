---
name: prompt
description: Transforma um pedido escrito às pressas em um prompt estruturado e completo, seguindo as boas práticas da Anthropic, para tirar o melhor resultado do Claude. Usar quando o usuário digitar /prompt seguido do pedido.
argument-hint: <o que você quer pedir>
disable-model-invocation: true
---

# Prompt

Pedido do usuário:

<pedido>
$ARGUMENTS
</pedido>

Sua tarefa é reescrever esse pedido como um prompt que extraia o melhor resultado possível de um modelo Claude. Não execute o pedido agora. Isso só acontece no passo 4, se o usuário aceitar.

Se o pedido estiver vazio, pergunte em uma frase o que o usuário quer pedir e pare.

## 1. Entenda o pedido

- Classifique o tipo da tarefa com a lista de [tipos.md](tipos.md). Leia esse arquivo agora, porque ele define o que incluir e o formato de resposta de cada tipo.
- Se a sessão estiver dentro de um projeto, colete contexto barato, com no máximo 3 chamadas de ferramenta: `CLAUDE.md`, `README` e a estrutura de pastas. Assim o prompt cita arquivos, comandos e versões reais. Não comece a fazer a tarefa.
- Identifique lacunas. Pergunte só o que mudaria o resultado de forma importante e que você não consegue descobrir sozinho: objetivo, público, escopo ou formato. Faça no máximo 3 perguntas curtas, todas de uma vez (use AskUserQuestion se estiver disponível). Se não houver lacunas assim, ou se não for possível perguntar, assuma a interpretação mais razoável e liste as suposições na entrega.

## 2. Escreva o prompt

Use estas seções, nesta ordem. Omita as que não se aplicam ao pedido.

1. **Objetivo:** o que deve ser feito e para quê, em 1 ou 2 frases. O "para quê" faz o modelo tomar decisões melhores nos casos que o prompt não cobre.
2. **Contexto:** só o que o modelo não sabe. Projeto, stack e versões, decisões já tomadas, caminhos reais dos arquivos relevantes, público do resultado.
3. **Tarefa:** o que precisa ser feito. Use passos numerados só quando a ordem importa.
4. **Restrições:** o que fica fora do escopo e o que não deve ser alterado, cada item com o motivo em poucas palavras. Ações difíceis de desfazer (apagar, publicar, push, migrar dados) exigem confirmação antes.
5. **Pronto quando:** critérios verificáveis. Por exemplo: os testes passam, um comando específico retorna um resultado específico, os casos A e B estão cobertos.
6. **Formato da resposta:** use o modelo do tipo, em [tipos.md](tipos.md), adaptado ao pedido.

### Regras de escrita

- **Verbos de ação.** "Implemente", "Revise e liste", "Compare". Evite "você poderia sugerir", que tende a gerar só sugestões.
- **Dê o porquê das regras importantes.** O modelo generaliza a partir do motivo e acerta casos que a regra não cobre.
- **Diga o que fazer, não só o que evitar.** "Responda em parágrafos corridos" funciona melhor que "não use listas".
- **Tom normal.** Modelos atuais seguem instruções de perto e reagem demais a gritos. Use ênfase forte (NÃO, OBRIGATÓRIO) só em restrições reais, no máximo duas por prompt.
- **Seja específico.** Use nomes reais de arquivos, comandos, versões e números. Troque o vago ("melhore", "otimize") por um critério ("reduza o tempo de resposta do endpoint X para menos de 200 ms").
- **Controle o escopo.** Peça para entregar o que foi pedido. Se o modelo achar uma abordagem melhor, ele diz isso em uma frase e segue com o pedido.
- **Peça evidência.** Afirmações importantes vêm com a fonte, a saída de um comando ou o trecho do arquivo. "Não consegui confirmar" é uma resposta válida.
- **Revisões e auditorias:** peça para reportar tudo, cada achado com severidade, e não "só o grave". O modelo segue esse tipo de filtro ao pé da letra e esconde achados. Inclua um veredito como critério de parada.
- **Exemplo de saída:** se o formato for crítico, inclua um exemplo curto da resposta esperada.
- **Não peça para "revisar a resposta duas vezes".** Os modelos atuais já verificam o próprio trabalho, e isso só gasta tempo. O critério de "Pronto quando" faz esse papel.
- **Não peça o raciocínio interno.** Peça um resumo das decisões tomadas.
- **Tamanho:** o mínimo que cobre o necessário. Um prompt longo dilui o que importa.
- **Idioma:** o mesmo do pedido.

## 3. Entregue neste formato

**Tipo:** <tipo> · **Modo sugerido:** <normal | plan mode> · **Raciocínio:** <normal | ultrathink>

```text
<o prompt completo>
```

**Suposições:** <lista curta; omita se não houver>

**O que melhorou:** <de 2 a 3 itens curtos, comparando com o pedido original>

Como escolher o modo e o raciocínio:
- **Plan mode:** quando a tarefa altera arquivos e tem 3 ou mais passos, ou envolve uma decisão de arquitetura.
- **ultrathink:** quando exige raciocínio difícil, como depurar um bug obscuro, decidir uma arquitetura ou fazer uma auditoria profunda. Se usar, a palavra `ultrathink` deve ser a primeira linha do prompt.
- **Normal:** nos outros casos.

## 4. Ofereça executar

Termine com: "Quer que eu execute este prompt agora?" Se o usuário disser que sim, execute o prompt como se ele tivesse acabado de enviá-lo. Se ele pedir ajustes, reescreva só o que mudou e entregue de novo no mesmo formato.
