# v2.7: APROVADA E INSTALADA (17/11/2026)

Regra: a da v2.5 (`validation-cases.md`, seção "Validação da v2.7"). Correção dupla em `runs/v2.7-validation/cego/` (validação) e `runs/v2.7-regression/cego/` (15 casos); sessão em `runs/v2.7-session/`.

| Item | Resultado | Cumpre? |
|---|---|---|
| 1. Validação | nenhum "inventado" nas 27 saídas (v2.6: #12 e #17 em 2 de 3). #12 Agêntica longa 3/3 e apaga `progress.md` 3/3 (r3 falha só em C2, 4 leituras); #16–#19 5/5 nas 3; #17 enchimento só no r2; #20 perguntou 3/3; #22 plan 3/3; #23 e #24 Implementar código, normal, sem `ultrathink` 3/3. Placar r1 9/9 · r2 8/9 · r3 8/9 | sim |
| 2. 15 casos | v2.7 15/15, v2.0 10/15 na mesma correção dupla (falhas da v2.0: #01, #07, #09, #15 inventado; #12 d); sem regressão no #14 nem em critério mecânico; #11 Planejar ou decidir | sim |
| 3. Sessão longa | renome como Implementar código, normal, padrão, sem `ultrathink`; tarefas feitas, 6 testes verdes, sem `progress.md`; US$ 0,43 | sim |

**O que mudou da v2.6:** (1) Implementar código pede as convenções "que o CLAUDE.md ou as leituras mostram no projeto", sem a lista de stacks; (2) em Escrever texto, a estratégia de redação que o pedido não traz vai em Suposições com "confirme:". No #17, desculpas e responsabilidade foram para Suposições nas 3 repetições.

**Discordâncias entre as correções (não contam):** validação 19-A, 19-C e 22-A enchimento; 15 casos 06-B, 08-B e 10-A inventado (todas da v2.0).

**Observação:** o 15-B (v2.0, `runs/v1-vs-v2.0-round3/`) cita a skill instalada no HOME temporário do ambiente de teste; não afeta a v2.7.

Custo: US$ 4,79 nas execuções (validação 2,22 · 15 casos 2,14 · sessão 0,43) e ~427 mil tokens dos corretores.
