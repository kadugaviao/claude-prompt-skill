# Resultados dos evals da skill /prompt: rodada 3 + validação (11/11/2026)

**Veredito: v2 APROVADA.**
- Validação: os 4 casos novos, nunca vistos pela skill, passaram (4/4).
- Rodada 3, com a régua calibrada (D20): v2 14/15, v1 4/15, e a v2 não fica pior em nenhum caso.

## Como foi rodado
- **Harness:** `claude -p "/prompt …"`, Opus 5.5 com esforço alto, HOME temporário (`evals/tmp/home/`) e fixtures em `evals/fixtures/`. Usa `--add-dir` com a pasta da skill, porque a v1 ainda tem o `tipos.md` separado. Todas as 34 execuções registraram `skill_carregada: inteira`, conferido na transcrição da sessão, e a v1 leu o `tipos.md` em todas as execuções em que tentou.
- **Mudanças na v2 desde a rodada 2:**
  - `tipos.md` fundido no `SKILL.md` (D17);
  - regra de escolha do tipo e desempate (D18);
  - "não resolva a tarefa no prompt" (D19).
- **Régua:**
  - C5 aceita objetivo no infinitivo, e o #7 não avalia o rótulo do tipo (mudanças da rodada 3 em `cases.md`).
  - Depois de ver a rodada 3, o usuário aprovou os tetos calibrados e a contagem só de linhas com texto, com até +20% como aviso (D20).
  - Como a régua mudou depois de ver os resultados, a aprovação dependeu dos 4 casos de validação (`validation-cases.md`), escritos depois da calibração.
- **Correção:**
  - Mecânicos por `check.py`.
  - Julgamento por subagentes Sonnet que não viram a skill ser escrita: às cegas (A/B) na rodada 3 e só com a v2 na validação, cada marca com o trecho literal citado.
  - Consolidação por `consolidar.py` (rodada 3) e pela regra de passagem do `validation-cases.md` (validação).

## Validação (só v2, casos #16 a #19)

| Caso | Resultado | Mecânicos | Julgamento (C4, C5, específicos) | Enchimento (informativo, C6 sem aviso) |
|---|---|---|---|---|
| #16 | **passa** | C1=ok, C2=ok, C3=ok, C6=ok, C7=ok, tipo=ok; 19 linhas com texto, teto 45 | C4=passa, C5=passa, b=passa, c=passa, d=passa, e=passa, f=passa | falha: Chamadas que já existem precisam continuar com o mesmo resultado. / Antes de assumir algo fora desta lista, investigue no código. |
| #17 | **passa** | C1=ok, C2=ok, C3=ok, C6=ok, C7=ok, tipo=ok; 14 linhas com texto, teto 25 | C4=passa, C5=passa, b=passa, c=passa, d=passa | falha: O cliente esperava a entrega na data combinada, e ela vai sair 3 dias depois. O risco é o e-mail parecer desculpa esfarrapada. |
| #18 | **passa** | C1=ok, C2=ok, C3=ok, C6=ok, C7=ok, tipo=ok; 19 linhas com texto, teto 35 | C4=passa, C5=passa, b=passa, c=passa, d=passa, e=passa, f=passa | falha: Projeto Python `fretes` 0.3.0 (requires-python >=3.12, pyproject.toml). / Antes de assumir algo fora desta lista, investigue no arquivo. |
| #19 | **passa** | C1=ok, C2=ok, C3=ok, C6=ok, C7=ok, tipo=ok; 19 linhas com texto, teto 25 | C4=passa, C5=passa, b=passa, c=passa, d=passa, e=passa, f=passa | falha: Fora do escopo: corrigir ou refatorar o projeto, porque o objetivo é aprender. / - Não altere arquivos do projeto, porque o pedido é só de explicação. |

**Validação: 4/4 passam.**

**Sobre o enchimento:** o corretor apontou enchimento nos 4 prompts e concluiu "nenhum passa". Pela regra definida antes da rodada (`validation-cases.md` e D20), o enchimento só decide o caso quando o C6 está em aviso. Nos 4 casos, o C6 ficou dentro do teto, sem aviso, então eles passam. As marcas do corretor continuam no `runs/v2.0-validation/julgamento.json`.

Mesmo assim, o achado é real e vira melhoria proposta, não bloqueio. Duas das quatro frases apontadas ("Antes de assumir algo fora desta lista, investigue no código/arquivo") vêm do próprio esqueleto da skill, na seção Autonomia. As outras são repetições do pedido ou da Tarefa.

**Caso duvidoso apontado pelo corretor:** no #17d, o prompt pede "sem meta-comentário", mas depois pede uma lista curta dos marcadores a preencher. Ficou como `passa`.

## Pendências conhecidas (não bloqueiam)
1. **#12d (rodada 3):** numa migração longa, o prompt da v2 não registra o estado do trabalho (git, `progress.md`). Correção proposta: pôr o registro de progresso no template de Agêntica longa ("Durante o trabalho: atualize `progress.md` a cada etapa").
2. **Enchimento vindo do esqueleto:** tirar ou condicionar a frase "Antes de assumir algo fora desta lista, investigue no código" da seção Autonomia.
3. **Comandos compostos de leitura:** às vezes são bloqueados no `-p` (`for`, `$(...)`, `awk`). O modelo tenta de novo com um comando simples, e o `check.py` não conta chamadas que falharam. No uso interativo, esses comandos pediriam aprovação.

## Custo
- Execuções (`total_cost_usd` do `claude -p`): teste rápido US$ 0,53 + rodada 3 US$ 3,42 + validação US$ 0,55 = **US$ 4,50**.
- Corretores Sonnet: cerca de 102 mil tokens (rodada 3) e 47 mil (validação), **US$ 0,6 a 0,9 estimados** (o valor exato não é exposto).

