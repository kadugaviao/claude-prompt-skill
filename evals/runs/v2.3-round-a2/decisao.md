# Rodada A2 (M1b): aplicação da regra de validation-cases.md

Correção cega mista (`runs/v2.3-round-a2/cego/`, 30 saídas: candidata `v23b` = rodada A + M1b; base `runs/v2.3-round-a`). Tabelas em `runs/v2.3-round-a2/cego/resumo.md`.

| Critério da M1b | A2 | base (A) | Resultado |
|---|---|---|---|
| Repetições com "inventado" (5 casos) menos que a base | 0 | 2 (#17 r1, r3) | cumpre |
| Enchimento do #19 em menos repetições que a base | 1/3 | 0/3 | **não cumpre** |
| Nenhuma regressão (critério que passa em 1+ da base e falha nas 3) | nenhuma | — | cumpre |

**Pela regra, a M1b não é aceita.** O 2º critério supunha que a base repetiria o enchimento do #19 da rodada A (2 de 3). Nesta passada a base teve 0 de 3, e nenhum resultado venceria esse número.

Outros números da mesma passada (informativos, fora da regra da M1b):
- Placar: A2 13/15 (r1 4/5 · r2 5/5 · r3 4/5); A 11/15 (4/5 · 3/5 · 4/5).
- Pela regra de aprovação da v2.3, a A2 passaria no item 1 (4/5 ou mais em 3 de 3, nenhum "inventado", #18 passa nas 3). A versão A reprovaria: tem "inventado" no #17 em 2 repetições.
- O corretor varia entre passadas. Para a mesma versão A: #19 enchimento 2/3 na rodada A e 0/3 aqui; #17 inventado 1/3 lá e 2/3 aqui.
- Custo: r2+r3 US$ 0,640 (A: 0,641). Mediana da saída: #12 3061 (A 3265), #16 2188 (2199), #17 1804 (1243), #18 1793 (1844), #19 2086 (1951). Soma das medianas +4%.

**Decisão (usuário, 13/11/2026):** M1b mantida com exceção registrada (D21). Confirmação na rodada B: "inventado" em no máximo 1 repetição, somando os 5 casos.
