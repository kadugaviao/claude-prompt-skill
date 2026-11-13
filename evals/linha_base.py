"""Custo, tokens e nota de cada execução de uma série de repetições (r1, r2, ...), com média e variação.

Uso: python3 -I evals/linha_base.py <pasta> <versao>   ex.: linha_base.py runs-base v22
Espera <pasta>/rN/{checagem-12.json,checagem-val.json,raw/<versao>-NN.jsonl} e <pasta>/julgamento.json
com chaves "rN-NN". Grava <pasta>/resumo.md. A régua de aprovação é a de comparar_versoes.falhas.
"""
import glob, json, os, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I tira a pasta do script do path
from comparar_versoes import E, falhas

pasta, v = os.path.join(E, sys.argv[1]), sys.argv[2]
jul = json.load(open(os.path.join(pasta, 'julgamento.json'), encoding='utf-8'))
reps = sorted(os.path.basename(r) for r in glob.glob(os.path.join(pasta, 'r[0-9]*')) if os.path.isdir(r))
casos = ['12', '16', '17', '18', '19']


def uso(raw):
    for l in open(raw, encoding='utf-8'):
        d = json.loads(l)
        if d.get('type') == 'result':
            u = d['usage']
            return (d['total_cost_usd'], u['cache_creation_input_tokens'], u['cache_read_input_tokens'],
                    u['output_tokens'], (u.get('output_tokens_details') or {}).get('thinking_tokens', 0))
    raise SystemExit(f'sem evento "result" em {raw}')


linhas = ['| execução | custo US$ | gravação | leitura | saída | thinking | resultado |', '|---|---|---|---|---|---|---|']
por_rep = {r: [] for r in reps}
custos = []
for r in reps:
    for n in casos:
        mec = json.load(open(os.path.join(pasta, r, 'checagem-12.json' if n == '12' else 'checagem-val.json'),
                             encoding='utf-8'))[f'{v}-{n}']
        f = falhas(mec, jul[f'{r}-{n}'])
        c, g, l, s, t = uso(os.path.join(pasta, r, 'raw', f'{v}-{n}.jsonl'))
        custos.append(c)
        por_rep[r].append(not f)
        linhas.append(f'| {r}-{n} | {c:.3f} | {g} | {l} | {s} | {t} | {"passa" if not f else "falha: " + ", ".join(f)} |')
linhas += ['', 'Placar por repetição: ' + ' · '.join(f'{r} {sum(p)}/5' for r, p in por_rep.items()),
           f'Casos que passaram em todas as repetições: ' +
           (', '.join('#' + n for i, n in enumerate(casos) if all(p[i] for p in por_rep.values())) or 'nenhum'),
           f'Custo por execução: média US$ {statistics.mean(custos):.3f}, desvio {statistics.pstdev(custos):.3f}, '
           f'mín {min(custos):.3f}, máx {max(custos):.3f}; por repetição (5 casos): '
           + ' · '.join(f'{r} US$ {sum(custos[i * 5:i * 5 + 5]):.3f}' for i, r in enumerate(reps))]
open(os.path.join(pasta, 'resumo.md'), 'w', encoding='utf-8').write('\n'.join(linhas) + '\n')
print('\n'.join(linhas))
