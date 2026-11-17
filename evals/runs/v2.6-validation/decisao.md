# v2.6: NÃO APROVADA (16/11/2026)

Regra: a da v2.5 (`validation-cases.md`). Correção dupla em `runs/v2.6-validation/cego/` (validação) e `runs/v2.6-regression/cego/` (15 casos); sessão em `runs/v2.6-session/`.

| Item | Resultado | Cumpre? |
|---|---|---|
| 1. Validação | #16, #18–#20, #22, #24 sem falha; #23 e #24 troca mecânica 3/3; #12 Agêntica longa 3/3 e apaga `progress.md` 3/3; #22 plan 3/3. Mas #12 e #17 com "inventado" em 2 de 3, e #12/#16–#19 só com 4/5 ou mais em 1 repetição (r1 3/5 · r2 5/5 · r3 3/5) | **não** |
| 2. 15 casos | v2.6 15/15, v2.0 12/15, sem regressão; #11 voltou a Planejar | sim |
| 3. Sessão longa | renome como Implementar código, normal, padrão, sem `ultrathink`; tarefas feitas, 7 testes verdes, sem `progress.md`; US$ 0,45 (v2.4: 0,50–0,53) | sim |

**Causas do item 1:**
- #12 (novo na v2.6): "O CLAUDE.md do projeto indica JUnit 5/Mockito como convenção de testes". O CLAUDE.md da fixture não fala de testes. A origem é o modelo do tipo Implementar na skill ("convenções que mudam o resultado (Spring: camadas, DTOs, JUnit 5/Mockito; Python: tipagem, pytest)"), apresentado como convenção do projeto. A mesma origem explica o "type hints" inventado no #16 (v2.0, Sonnet).
- #17: "peça desculpas uma vez" e "assuma a responsabilidade" como requisitos firmes. As mesmas frases apareciam na v2.4 e passaram naquela correção; aqui os dois corretores reprovaram. É escolha de redação apresentada como requisito.

Custo: US$ 4,75 nas execuções (validação 2,24 · 15 casos 2,07 + #11 0,16 · sessão 0,45) e ~430 mil tokens dos corretores.
