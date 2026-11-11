# Casos de validação da skill /prompt (depois da calibração D20)

**Por que existem:** os tetos de tamanho e a regra de contagem foram calibrados depois de ver a rodada 3 (D20). Para confirmar a v2 sem mover a trave, estes 4 pedidos foram escritos depois da calibração. A skill não os viu e eles não foram usados para ajustar nada.

**Como rodam:** só a v2, com `rodar.py --tsv casos-validacao.tsv`, nas mesmas fixtures de `casos.md` (`spring`, `python`, `vazio`). A correção é a mesma da rodada 3:
- `checar.py --tsv casos-validacao.tsv` para os critérios mecânicos;
- um subagente Sonnet que não viu a skill ser escrita para os de julgamento, citando trechos.

**Liberação:** a v2 só fica APROVADA se os 4 casos passarem. Um caso passa quando nenhum critério aplicável falha. C6 em "aviso" (até +20% do teto) passa, salvo se o critério "enchimento" falhar.

## Critérios comuns
São os mesmos de `casos.md`: C1–C7, com C5 e C6 na redação da rodada 3. A eles se soma:

| ID | Critério | Quem corrige |
|---|---|---|
| enchimento | O prompt não tem enchimento, ou seja, frases que não mudariam o resultado se fossem removidas (repetições, generalidades, seções protocolares). Só decide o caso quando o C6 está em aviso | corretor |

## Casos

### #16 · Implementar código · python
`bota um parametro de desconto percentual no calcula_frete sem quebrar os testes`
- a. Tipo Implementar código (mecânico).
- b. `calcula_frete` e `src/fretes/frete.py` aparecem literalmente, por caminho.
- c. Define o comportamento esperado do desconto: faixa válida (por exemplo, 0–100) ou o que fazer com valor inválido, como critério ou como suposição.
- d. "Pronto quando" usa `pytest` e exige que os testes existentes (`tests/test_frete.py`) continuem passando.
- e. Tem uma linha contra overengineering ou abstrações não pedidas.
- f. Não traz a implementação pronta: nada de código da solução nem a fórmula final imposta como resposta (D19).

### #17 · Escrever texto · vazio
`faz um email pro cliente explicando q a entrega atrasou 3 dias, sem parecer desculpa esfarrapada`
- a. Tipo Escrever texto (mecânico).
- b. Canal e-mail, audiência cliente externo, tom profissional e direto que não soe como desculpa.
- c. "3 dias" aparece literalmente. O que falta (nome do cliente, pedido, motivo, nova data) vira placeholder ou suposição, e nada é inventado.
- d. Pede uma versão só, pronta para usar e sem meta-comentário.
- e. Nenhuma chamada de contexto (mecânico, pela lista de ferramentas).

### #18 · Analisar dados · python
`quantos % das requisicoes do app.log passam de 1 segundo? quero por hora`
- a. Tipo Analisar dados (mecânico).
- b. `logs/app.log` aparece por caminho, sem conteúdo colado.
- c. O limiar de 1 segundo vira um critério calculável sobre `dur_ms` (> 1000 ms ou ≥ 1000 ms, explícito).
- d. Pede o percentual por hora, numa tabela ou lista.
- e. Pede que os cálculos sejam feitos com código executado.
- f. Pede as limitações dos dados, ou o tratamento de linhas fora do padrão.

### #19 · Explicar ou ensinar · spring
`explica o que é N+1 no JPA usando meu projeto, nunca entendi direito`
- a. Tipo Explicar ou ensinar (mecânico).
- b. Declara o nível de quem lê (não entendeu direito, iniciante ou intermediário).
- c. Pede um exemplo com classes reais do projeto (`Pedido` com `itens`, `PedidoRepository` ou `PedidoService`).
- d. Pede armadilhas comuns, ou como detectar ou evitar o problema.
- e. Não inclui exercício.
- f. Não altera arquivos: a explicação é só de leitura (restrição ou fora do escopo).
