# Evals da skill /prompt

Como medir uma versão nova da skill de ponta a ponta. A régua está em `casos.md` (15 casos de regressão) e `casos-validacao.md` (casos #16 a #24 e a regra de aprovação de cada versão). O histórico está em `resultados.md` e as decisões no `../SPEC.md`.

## Antes de rodar
- `./criar_fixtures.sh` recria os projetos de teste em `fixtures/`, que ficam fora do git. O script recusa rodar se `fixtures/` já existir.
- O `rodar.py` fixa o esforço (`ESFORCO = 'medium'`) e a versão do Claude Code (`VERSAO`). Ele para com erro se a transcrição registrar outra coisa. Se o Claude Code atualizar, mude `VERSAO` e rode de novo a v2.0 (`versoes/v2.0`) nos 15 casos, senão a comparação mistura duas versões.
- Escreva a regra de aprovação em `casos-validacao.md` antes de rodar, para a régua não mudar depois de ver o resultado.
- Custo de referência (Opus 5.5, preço de tabela): de US$ 0,03 a 0,20 por execução, cerca de US$ 5 numa validação completa. A 1ª repetição de uma versão nova custa mais, porque o corpo novo da skill regrava o cache. O custo de cada execução sai no `rodadas.log`.

## Validação completa de uma versão nova (a regra da v2.5 em diante)
Os comandos rodam de `evals/`. A versão em teste fica em `../v2/prompt` e ganha um nome curto (ex.: `v28`). Rode primeiro um caso só: se a resposta for a mensagem de limite de uso, pare e espere a janela de 5 horas.

```bash
# 1. Validação: 9 casos × 3 repetições
for r in r1 r2 r3; do
  python3 -I rodar.py runs-v28/$r v28=../v2/prompt --casos 12 | tee -a runs-v28/rodadas.log
  python3 -I rodar.py runs-v28/$r v28=../v2/prompt --tsv casos-validacao.tsv --casos 16,17,18,19,20,22,23,24 | tee -a runs-v28/rodadas.log
  python3 -I checar.py runs-v28/$r --json runs-v28/$r/checagem-12.json
  python3 -I checar.py runs-v28/$r --tsv casos-validacao.tsv --json runs-v28/$r/checagem-val.json
done
# 2. Os 15 casos de casos.md, 1 execução cada
python3 -I rodar.py runs-v28-15 v28=../v2/prompt | tee -a runs-v28-15/rodadas.log
python3 -I checar.py runs-v28-15 --json runs-v28-15/checagem.json
# 3. Sessão longa (prompt + execução depois do "sim", 2 tarefas)
python3 -I sessao.py runs-sessao/v28-s1 ../v2/prompt
# 4. Correção cega dupla
python3 -I comparar_versoes.py cegar-reps runs-v28/cego v28=runs-v28:v28
python3 -I comparar_versoes.py cegar-reps runs-v28-15/cego v28=runs-v28-15:v28 v20=runs-3:v2   # a v2.0 na mesma correção
# corretor: 4 subagentes Sonnet independentes, com o texto de corretor.md, gravam
# julgamento.json e julgamento-2.json em cada pasta cego/; um critério só falha se falhou nos dois
python3 -I comparar_versoes.py consolidar-reps runs-v28/cego
python3 -I comparar_versoes.py consolidar-reps runs-v28-15/cego
```

Para procurar falhas mecânicas, use `checar.py ... | grep FALHA`. Um filtro que esconda as linhas com "ok" também esconde uma falha que esteja na mesma linha de um "ok".

## Outras ferramentas
- `medir_cache.py calibrar <versao>` e `medir_cache.py quebrar <pastas>` separam a gravação de cache por origem (ferramentas, sistema, skill, resto).

## Cuidados
- O corretor varia: a mesma saída pode passar numa correção e falhar na outra. Compare sempre a versão nova e a base **na mesma correção cega**, e confie só em diferenças que aparecem em 2 de 3 repetições ou que um script confere (tipo, esforço, modo).
- O `consolidar-reps` precisa da checagem mecânica (`checagem*.json`) em cada pasta de repetição, e conta a correção dupla sozinho quando existe `julgamento-2.json`.
- `tmp-home/` (HOME temporário de cada versão) e `tmp-sessao/` (cópias de trabalho da sessão longa) ficam fora do git e podem ser apagados depois de uma rodada. Só o `tmp-sessao/venv`, com o pytest da sessão longa, precisa ficar.
