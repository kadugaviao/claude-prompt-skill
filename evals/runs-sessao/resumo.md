# Uso real: sessão longa com a v2.4 (16/11/2026)

`sessao.py`: 4 turnos na mesma conversa (`claude -p --resume`), cópia da fixture `python`, Claude Code 2.1.326 (o do usuário), sessão em effort high (o padrão do usuário), edições aceitas e só leitura, git e pytest liberados.
Turnos: (1) `/prompt` desconto em `calcula_frete` · (2) "sim" · (3) `/prompt` renomear `calcula_frete` → `calcular_frete` no projeto todo · (4) "sim".
s1 descartada (defeito de harness: pytest com prefixo `PYTHONPATH=src` negado; custo por turno lido como acumulado). Válidas: s2 e s3.

| Turno | Esforço gravado | Custo s2 | Custo s3 | Requisições | Saída (tokens) |
|---|---|---|---|---|---|
| 1 `/prompt` desconto | medium | 0,158 | 0,149 | 3 | 1.900–2.350 |
| 2 "sim" (executa) | high | 0,088 | 0,105 | 3–6 | ~2.000 |
| 3 `/prompt` renome | medium | 0,116 | 0,113 | 2 | ~2.300 |
| 4 "sim" (executa) | high | 0,171 | 0,137 | 6–7 | 2.400–3.050 |
| **Sessão** | | **0,532** | **0,504** | | |

**Resultado final:** nas 2 sessões, desconto implementado com validação de faixa, renome completo (nenhum `calcula_frete` restante) e `pytest` verde (7 testes).

**Achados:**
1. O `effort: medium` do cabeçalho vale só no turno do `/prompt`; a execução depois do "sim" roda no nível do usuário (high). Comportamento previsto pela M6, confirmado.
2. A execução funciona: nas 2 sessões, as duas tarefas foram feitas e verificadas com pytest dentro da sessão.
3. **Exagero na tarefa mecânica:** o renome (8 linhas em 2 arquivos) saiu, nas 3 sessões, como Agêntica longa + plan mode + esforço alto + `ultrathink` + sugestão de `/effort xhigh` + `progress.md`, e o `progress.md` ficou no projeto do usuário depois da tarefa. É efeito da M2 (Agêntica longa pelo escopo do pedido) somado à regra "esforço alto em tarefa agêntica longa".
4. O `/prompt` custa tanto quanto a execução em tarefas pequenas (US$ 0,11–0,16 contra 0,09–0,17). O 2º `/prompt` da sessão é ~25% mais barato que o 1º (prefixo já em cache).
5. O corpo da skill fica no contexto pelo resto da sessão (~5 mil tokens), relido do cache a cada requisição: ~US$ 0,001 por requisição, cerca de 2–3% da sessão.
6. Atrito de permissão: o executor usa comandos compostos (`&&`, `;`, pipes, `sed -i`), que pedem aprovação mesmo com o pytest liberado. Em sessão interativa isso vira pedidos de permissão; não é defeito da skill.
7. M5 (juntar leituras): os turnos de `/prompt` fizeram 1–2 leituras (2–3 requisições). Juntar pouparia ~1 requisição, cerca de US$ 0,005–0,01 por `/prompt` (4–6%). Confirma que o ganho é pequeno.
