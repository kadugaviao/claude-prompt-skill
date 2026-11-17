# v2.5: NÃO APROVADA (16/11/2026)

Regra: `validation-cases.md`, "Validação da v2.5". Correção dupla (`runs/v2.5-validation/cego/`); 15 casos em `runs/v2.5-regression/`.

**O que a v2.5 resolveu:** o exagero na troca mecânica. #23 e #24 saíram Implementar código, Modo normal e sem `ultrathink` nas 3 repetições (antes: Agêntica longa + plan mode + `ultrathink`). O #12 continua Agêntica longa e manda apagar o `progress.md` no fim nas 3. #20 perguntou nas 3; #22 plan mode nas 3.

**Por que reprovou:**
1. Item 2 (15 casos): regressão em critério mecânico no #11 (`quero migrar pro spring boot 4, como faço sem quebrar tudo`): saiu Agêntica longa em vez de Planejar ou decidir. A frase nova da Agêntica longa cita "migrar, atualizar versão" como exemplos, e isso puxou um "como faço" (pedido de plano) para execução. A v2.0 passa nesse critério.
2. Item 1 (validação): #23 com "inventado" em 2 de 3 repetições, marcado pelas duas correções ("para que o nome siga a forma verbal no infinitivo", "para padronizar o nome no infinitivo"). Causa provável: o modelo do prompt pede "Objetivo no imperativo, 1–2 frases, com o 'para quê'", e o pedido não dá o porquê. O mesmo apareceu no #23 da v2.4 (1 de 3).

A correção dupla dos 15 casos e a sessão longa não foram rodadas: com a regressão mecânica, o resultado já estava decidido.

Placar da validação: r1 6/9 · r2 8/9 · r3 8/9 (4 marcas de enchimento descartadas por discordância). Custo: US$ 4,67 nas execuções (validação 2,18 + 0,47 que bateram no limite de uso · 15 casos 2,02) e ~226 mil tokens dos corretores.
