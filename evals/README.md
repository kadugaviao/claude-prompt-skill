# Evals da skill /prompt

Como medir uma versão nova da skill de ponta a ponta. A régua está em `casos.md` (15 casos) e `casos-validacao.md` (4 casos novos e as regras de aprovação de cada versão). O histórico está em `resultados.md` e as decisões no `../SPEC.md`.

## Antes de rodar
- `./criar_fixtures.sh` recria os projetos de teste em `fixtures/` (ficam fora do git).
- O `rodar.py` fixa o esforço (`ESFORCO = 'medium'`) e a versão do Claude Code (`VERSAO`). Ele para com erro se a transcrição registrar outra coisa. Se o Claude Code atualizar, mude `VERSAO` e rode a linha de base de novo (cerca de US$ 1), senão a comparação mistura duas versões.
- Escreva a regra de aprovação em `casos-validacao.md` antes de rodar, para a régua não mudar depois de ver o resultado.
- Custo de referência (Opus 5.5, preço de tabela): de US$ 0,03 a 0,20 por execução. A 1ª repetição de uma versão nova custa mais, porque o corpo novo da skill regrava o cache.

## Uma rodada (versão nova contra uma base), com 3 repetições
Os comandos rodam de `evals/`. A versão em teste fica numa pasta (ex.: `../v2/prompt`) e ganha um nome curto (ex.: `v24`). A base é uma rodada já salva (ex.: `runs-base`, nome `v22`).

```bash
for r in r1 r2 r3; do
  python3 -I rodar.py runs-x/$r v24=../v2/prompt --casos 12                        # caso de casos.tsv
  python3 -I rodar.py runs-x/$r v24=../v2/prompt --tsv casos-validacao.tsv          # #16 a #19
  python3 -I checar.py runs-x/$r --json runs-x/$r/checagem-12.json                  # critérios mecânicos
  python3 -I checar.py runs-x/$r --tsv casos-validacao.tsv --json runs-x/$r/checagem-val.json
done
python3 -I comparar_versoes.py cegar-reps runs-x/cego base=runs-base:v22 nova=runs-x:v24
# corretor: dois subagentes Sonnet independentes, com o texto de corretor.md, gravam
# runs-x/cego/julgamento.json e runs-x/cego/julgamento-2.json; um critério só falha se falhou nos dois
python3 -I comparar_versoes.py consolidar-reps runs-x/cego    # -> runs-x/cego/resumo.md e falhas.json
python3 -I linha_base.py runs-x v24                           # custo e tokens (pede runs-x/julgamento.json com chaves rN-NN)
```

Rode primeiro um caso só: se a resposta for a mensagem de limite de uso, pare e espere a janela de 5 horas.

## Outras ferramentas
- `medir_cache.py calibrar <versao>` e `medir_cache.py quebrar <pastas>`: quebram a gravação de cache por origem (ferramentas, sistema, skill, resto).
- `comparar_versoes.py cegar` e `consolidar`: a comparação original da v2.2 (v2.0 × v2.1 × v2.2, 1 execução).

## Cuidados
- O corretor varia: a mesma saída pode passar numa passada e falhar na outra. Compare sempre a versão nova e a base **na mesma correção cega** e confie só em diferenças que aparecem em 2 de 3 repetições ou que um script confere (tipo, esforço, modo).
- A partir da v2.4, corrija cada lote duas vezes e conte só a falha marcada nas duas (decisão de 13/11/2026). O `consolidar-reps` faz isso sozinho quando existe `julgamento-2.json` e lista as marcas em que as correções discordaram.
- `tmp-home/` guarda o HOME temporário de cada versão e as transcrições; fica fora do git.
