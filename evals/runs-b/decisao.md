# Rodada B (M3 + M4 sobre a A2): aplicação da regra de casos-validacao.md

Correção cega mista (`runs-b/cego/`, 30 saídas: candidata `v23c` = A2 + M3 + M4; base `runs-a2`). Tabelas em `runs-b/cego/resumo.md`.

| Critério | Rodada B | Base (A2) | Resultado |
|---|---|---|---|
| Mediana da saída cai em 3+ dos 5 casos | 4 de 5 | — | cumpre |
| Soma das medianas cai 5% ou mais | −2,0% (10.710 contra 10.932) | — | **não cumpre** |
| Enchimento menor ou igual ao da base | 0 repetições | 2 | cumpre |
| Nenhuma regressão | nenhuma | — | cumpre |
| Confirmação da M1b: "inventado" em no máximo 1 repetição | 1 (#17 r1) | 0 | cumpre |

**Decisão:** M3 e M4 não são aceitas (ganho de tokens abaixo do mínimo) e foram desfeitas. A M1b fica confirmada. A v2.3 candidata é a versão da rodada A2 (`versoes/v2.3-rodada-a2/`).

Placar nesta passada: rodada B 13/15 (4/5 · 5/5 · 4/5), A2 13/15 (4/5 · 5/5 · 4/5). Custo r2+r3: B US$ 0,657, A2 US$ 0,640.
O corretor abriu as primeiras linhas do `mapa.json` por engano (só a letra 12-A); o #12 passou nas 6 letras.
