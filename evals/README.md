# Evals da skill /prompt

Como medir uma versão nova da skill de ponta a ponta. A régua está em `cases.md` (15 casos de regressão) e `validation-cases.md` (casos #16 a #24 e a regra de aprovação de cada versão). O histórico está em `results.md` e as decisões no `../docs/spec.md`.

## Pastas
- `cases.md` / `cases.tsv`: os 15 casos de regressão. `validation-cases.md` / `.tsv`: os casos #16 a #24 e a regra de aprovação de cada versão. `grader.md`: as instruções do corretor. `results.md`: o histórico.
- `baselines/v2.0/`: a v2.0, base de comparação dos casos de regressão.
- `fixture-sources/skill-v1/`: a primeira versão da skill. Não é usada como skill: o `make_fixtures.sh` a copia para o projeto de teste `skillproj` do caso #15 ("melhore esta skill").
- `runs/<versão>-<conjunto>/`: as saídas de cada rodada (`validation`, `regression`, `session`; as mais antigas têm `round-a`, `baseline-opus` etc.). Cada pasta de aprovação tem um `decisao.md`.
- `fixtures/` e `tmp/`: gerados, fora do git.

## Antes de rodar
- `./make_fixtures.sh` recria os projetos de teste em `fixtures/`, que ficam fora do git. O script recusa rodar se `fixtures/` já existir.
- O `run.py` fixa o esforço (`ESFORCO = 'medium'`) e a versão do Claude Code (`VERSAO`). Ele para com erro se a transcrição registrar outra coisa. Se o Claude Code atualizar, mude `VERSAO` e rode de novo a v2.0 (`baselines/v2.0`) nos 15 casos, senão a comparação mistura duas versões.
- A sessão longa usa um venv com pytest: `python3 -m venv tmp/session/venv && tmp/session/venv/bin/pip install pytest`.
- Escreva a regra de aprovação em `validation-cases.md` antes de rodar, para a régua não mudar depois de ver o resultado.
- Custo de referência (Opus 5.5, preço de tabela): de US$ 0,03 a 0,20 por execução, cerca de US$ 5 numa validação completa. A 1ª repetição de uma versão nova custa mais, porque o corpo novo da skill regrava o cache. O custo de cada execução sai no `rodadas.log`.

## Validação completa de uma versão nova (a regra da v2.5 em diante)
Os comandos rodam de `evals/`. A versão em teste fica em `../skills/prompt` e ganha um nome curto (ex.: `v28`). Cada rodada fica em `runs/<versão>-<conjunto>` (`validation`, `regression`, `session`). Rode primeiro um caso só: se a resposta for a mensagem de limite de uso, pare e espere a janela de 5 horas.

```bash
V=v2.8; N=v28   # versão em teste e o nome curto que vai nos arquivos
# 1. Validação: 9 casos × 3 repetições
mkdir -p runs/$V-validation runs/$V-regression
for r in r1 r2 r3; do
  python3 -I run.py runs/$V-validation/$r $N=../skills/prompt --casos 12 | tee -a runs/$V-validation/rodadas.log
  python3 -I run.py runs/$V-validation/$r $N=../skills/prompt --tsv validation-cases.tsv --casos 16,17,18,19,20,22,23,24 | tee -a runs/$V-validation/rodadas.log
  python3 -I check.py runs/$V-validation/$r --json runs/$V-validation/$r/checagem-12.json
  python3 -I check.py runs/$V-validation/$r --tsv validation-cases.tsv --json runs/$V-validation/$r/checagem-val.json
done
# 2. Os 15 casos de regressão (cases.md), 1 execução cada
python3 -I run.py runs/$V-regression $N=../skills/prompt | tee -a runs/$V-regression/rodadas.log
python3 -I check.py runs/$V-regression --json runs/$V-regression/checagem.json
# 3. Sessão longa (prompt + execução depois do "sim", 2 tarefas)
python3 -I session.py runs/$V-session ../skills/prompt
# 4. Correção cega dupla, com a v2.0 na mesma correção dos 15 casos
python3 -I compare.py cegar-reps runs/$V-validation/cego $N=runs/$V-validation:$N
python3 -I compare.py cegar-reps runs/$V-regression/cego $N=runs/$V-regression:$N v20=runs/v1-vs-v2.0-round3:v2
# corretor: 4 subagentes Sonnet independentes, com o texto de grader.md, gravam
# julgamento.json e julgamento-2.json em cada pasta cego/; um critério só falha se falhou nos dois
python3 -I compare.py consolidar-reps runs/$V-validation/cego
python3 -I compare.py consolidar-reps runs/$V-regression/cego
```

Para procurar falhas mecânicas, use `check.py ... | grep FALHA`. Um filtro que esconda as linhas com "ok" também esconde uma falha que esteja na mesma linha de um "ok".

## Outras ferramentas
- `cache_stats.py calibrar <versao>` e `cache_stats.py quebrar <pastas>` separam a gravação de cache por origem (ferramentas, sistema, skill, resto).

## Cuidados
- O corretor varia: a mesma saída pode passar numa correção e falhar na outra. Compare sempre a versão nova e a base **na mesma correção cega**, e confie só em diferenças que aparecem em 2 de 3 repetições ou que um script confere (tipo, esforço, modo).
- O `consolidar-reps` precisa da checagem mecânica (`checagem*.json`) em cada pasta de repetição, e conta a correção dupla sozinho quando existe `julgamento-2.json`.
- `tmp/home/` (HOME temporário de cada versão) e `tmp/session/` (cópias de trabalho da sessão longa) ficam fora do git e podem ser apagados depois de uma rodada. Se apagar o `tmp/session/venv`, recrie-o antes da próxima sessão longa.
