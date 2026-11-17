# Tipos de tarefa

Conteúdo: 1. Implementar · 2. Corrigir bug · 3. Revisar ou auditar · 4. Pesquisar ou comparar · 5. Explicar ou ensinar · 6. Escrever texto · 7. Analisar dados · 8. Planejar ou decidir

Para cada tipo há o que o prompt precisa incluir e um modelo de "Formato da resposta". Adapte o modelo ao pedido; não copie seções vazias. Se o pedido misturar tipos, use o tipo principal e acrescente o que faltar do outro.

## 1. Implementar (feature, refatoração, script, integração)

Incluir:
- Comportamento esperado, com entradas e saídas ou um exemplo de uso.
- Onde o código entra: arquivos, módulo, camada.
- Convenções do projeto a seguir e dependências que podem ou não ser adicionadas.
- Testes que devem existir ou passar.

Formato da resposta:
```
1. Resumo da mudança (2-3 linhas)
2. Arquivos criados ou alterados, com uma linha sobre cada um
3. Como foi verificado: comando rodado e resultado
4. Decisões tomadas e pendências
```

## 2. Corrigir bug

Incluir:
- Sintoma exato: mensagem de erro, stack trace ou comportamento observado versus o esperado.
- Como reproduzir e desde quando acontece, se souber.
- Pedir a causa raiz antes da correção, e um teste que falha antes e passa depois.

Formato da resposta:
```
1. Causa raiz, com evidência (arquivo:linha, log, saída)
2. Correção aplicada
3. Teste que reproduz o bug: falhava antes, passa depois
4. Riscos ou outros lugares com o mesmo problema
```

## 3. Revisar ou auditar (código, texto, configuração, segurança)

Incluir:
- O que revisar (diff, arquivos, branch) e o critério: o que conta como problema.
- Pedir para reportar todos os achados com severidade e evidência. Não filtrar só os graves.
- Separar o que foi confirmado das suspeitas.
- Não alterar nada durante a revisão.

Formato da resposta:
```
1. Veredito: APROVAR | APROVAR COM RESSALVAS | PEDIR MUDANÇAS (com uma frase de motivo)
2. Tabela: severidade | arquivo:linha | problema | evidência | correção sugerida
3. Dúvidas não confirmadas
4. O que está bom e deve ser mantido (curto)
```

## 4. Pesquisar ou comparar (tecnologias, ferramentas, opções, mercado)

Incluir:
- A decisão que a pesquisa vai apoiar e os critérios que importam (custo, desempenho, curva de aprendizado...).
- Restrições: orçamento, stack atual, prazo, região.
- Pedir fontes atuais com data e a distinção entre fato e opinião.

Formato da resposta:
```
1. Recomendação em 1-2 frases
2. Tabela comparativa pelos critérios
3. Trade-offs principais de cada opção
4. Fontes, com link e data
```

## 5. Explicar ou ensinar (conceito, código, tecnologia)

Incluir:
- O nível de quem vai aprender e o que já sabe.
- Para que vai usar o conhecimento: prova, projeto, entrevista.
- Pedir exemplos concretos, de preferência na stack de quem pergunta.

Formato da resposta:
```
1. Explicação curta (o essencial em um parágrafo)
2. Exemplo prático, com código se couber
3. Erros comuns ou confusões frequentes
4. Exercício ou próximo passo para fixar
```

## 6. Escrever texto (e-mail, post, documentação, README, mensagem)

Incluir:
- Público, objetivo do texto e o que o leitor deve fazer depois de ler.
- Tom e canal: LinkedIn, e-mail formal, Slack, README técnico.
- Tamanho aproximado e pontos obrigatórios.
- Um exemplo de texto no estilo desejado, se houver.

Formato da resposta:
```
O texto pronto para usar. Se o objetivo admitir abordagens diferentes, 2 versões
curtas com rótulos (ex.: "direta" e "mais calorosa"). No final, uma linha sobre o que
personalizar.
```

## 7. Analisar dados (planilha, CSV, logs, métricas)

Incluir:
- A pergunta que a análise responde.
- Onde estão os dados e o que significam as colunas ou os campos importantes.
- Pedir que os cálculos sejam feitos em código, não estimados, e que limitações dos dados sejam apontadas.

Formato da resposta:
```
1. Resposta direta à pergunta, com os números
2. Tabela ou gráfico de apoio
3. Como foi calculado (método, filtros)
4. Limitações e próximos cortes sugeridos
```

## 8. Planejar ou decidir (arquitetura, projeto, estudo, carreira)

Incluir:
- O objetivo, o prazo e os recursos disponíveis.
- As opções já consideradas e por que estão em dúvida.
- Pedir uma escolha justificada, não só uma lista de opções.

Formato da resposta:
```
1. Recomendação e o motivo principal
2. Plano em etapas, com prazo ou esforço estimado por etapa
3. Riscos e como mitigá-los
4. O que decidir ou validar primeiro
```
