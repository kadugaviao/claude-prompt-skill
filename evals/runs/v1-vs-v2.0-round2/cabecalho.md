# Resultados dos evals da skill /prompt: rodada 2 (11/11/2026)

**Veredito: NÃO APROVADA.** A v2 passou em 5 de 15 casos; o mínimo é 13 de 15. Ela fica pior que a v1 nos casos #3, #7 e #12.

> **Atenção, defeito do harness:** no `claude -p`, a ferramenta Read nega a leitura fora do diretório do projeto. Por isso, 21 das 28 execuções que tentaram ler o `tipos.md` da skill (no HOME temporário) não conseguiram. Só v1-04, v1-07, v1-15, v2-02, v2-04, v2-07 e v2-15 leram o arquivo. As outras geraram o prompt **sem os templates, sem os itens "deve conter" e sem as faixas de tamanho**, nas duas versões. Os critérios que dependem do `tipos.md` (C6 e boa parte dos específicos) não medem a skill como ela foi desenhada. A correção, `--add-dir` com a pasta da skill, já está no `run.py`, mas ainda não foi testada.

**Como foi rodado:**
- `evals/run.py`: `claude -p "/prompt <pedido>"`, Opus 5.5 com esforço alto, HOME temporário em `evals/tmp/home/<versão>/` e fixtures em `evals/fixtures/`, recriáveis com `make_fixtures.sh`.
- Saídas em `evals/runs/v1-vs-v2.0-round2/<versão>-<NN>.md` e brutas em `runs/v1-vs-v2.0-round2/raw/`.

**Correção:**
- Critérios mecânicos: `evals/check.py`, gerando `runs/v1-vs-v2.0-round2/checagem.json`.
- Critérios de julgamento (C4, C5 e os específicos): subagente Sonnet que não viu a escrita da skill, corrigindo às cegas cópias anonimizadas A/B (`runs/v1-vs-v2.0-round2/cego/`; o mapa está em `runs/v1-vs-v2.0-round2/raw/mapa-cego.json`). Resultado em `runs/v1-vs-v2.0-round2/julgamento.json`. Ele conferiu por script que cada trecho citado existe no arquivo.
- Consolidação: `evals/consolidar.py`.
- Um caso passa quando nenhum critério aplicável falha. "Pior" quer dizer que a v1 passa e a v2 falha, ou que a v2 falha em mais critérios comuns (sem contar o C7, que só existe na v2).

**Decisões tomadas nesta rodada:**
- **Leituras de contexto: limite de 3 mantido.** O único caso com 4 leituras (v2-01) era uma nova tentativa depois de um comando bloqueado ("A variable in this command can't be checked before it runs"), sem informação nova. O `check.py` agora não conta chamadas que falharam, e a 4ª não mudou o prompt.
- **Tamanho: só calibrei onde havia dado válido**, nos casos que leram o `tipos.md`:
  - v2-15 (43 linhas, teto 30) era conteúdo: checar prontidão para instalar em 3 arquivos exige a lista de verificações. O teto de Revisar subiu para 45.
  - v2-07 (31 linhas, teto 25) era conteúdo: o pedido traz duas decisões, nome e licença. O teto de Pesquisar subiu para 35.
  - Os outros 7 estouros (#1, #3, #5, #8, #9, #10, #11) aconteceram sem o `tipos.md` carregado e ficam sem decisão até uma rodada válida.

**Custo:**
- Execuções da rodada 2: US$ 3,76 (30 casos) + US$ 0,08 do teste com 1 caso. O valor vem de `total_cost_usd` do `claude -p`; na assinatura, conta para o limite de uso.
- Corretor Sonnet: cerca de 111 mil tokens, US$ 0,4 a 0,6 estimados (o valor exato não é exposto).

