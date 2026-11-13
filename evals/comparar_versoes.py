"""Compara versões da skill nos mesmos casos, com correção cega e a regra de aprovação da v2.2.

Uso:
  python3 -I evals/comparar_versoes.py cegar      -> runs-v22/cego/NN-{A,B,C}.md + runs-v22/raw/mapa-cego.json
  python3 -I evals/comparar_versoes.py consolidar -> imprime a tabela e grava runs-v22/resumo.md
Regra (casos-validacao.md, "Validação da v2.2"): a v2.2 passa em >= 4/5, nenhum "inventado" em falha
e nenhum caso em que a v2.0 passa e a v2.2 falha.
"""
import json, os, random, re, sys

E = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(E, 'runs-v22')
CASOS = ['12', '16', '17', '18', '19']
# versão -> (caminho do .md por caso, checagem mecânica por caso)
FONTES = {
    'v2.0': (lambda n: f'runs-3/v2-{n}.md' if n == '12' else f'runs-val/v2-{n}.md',
             lambda n: ('runs-3/checagem.json' if n == '12' else 'runs-val/checagem.json', f'v2-{n}')),
    'v2.1': (lambda n: f'runs-v21/v21-{n}.md',
             lambda n: ('runs-v21/checagem-12.json' if n == '12' else 'runs-v21/checagem-val.json', f'v21-{n}')),
    'v2.2': (lambda n: f'runs-v22/v22-{n}.md',
             lambda n: ('runs-v22/checagem-12.json' if n == '12' else 'runs-v22/checagem-val.json', f'v22-{n}')),
}


def cegar():
    random.seed('v22-cego')
    os.makedirs(os.path.join(OUT, 'cego'), exist_ok=True)
    mapa = {}
    for n in CASOS:
        vs = list(FONTES); random.shuffle(vs)
        for letra, v in zip('ABC', vs):
            t = open(os.path.join(E, FONTES[v][0](n)), encoding='utf-8').read()
            t = re.sub(r'^# v\d+-\d\d', f'# caso {n}-{letra}', t, flags=re.M)
            t = re.sub(r'tmp-home/v\d+', 'tmp-home/X', t)
            t = re.sub(r'^- (exit|skill_carregada):.*\n', '', t, flags=re.M)
            open(os.path.join(OUT, 'cego', f'{n}-{letra}.md'), 'w', encoding='utf-8').write(t)
            mapa[f'{n}-{letra}'] = v
    json.dump(mapa, open(os.path.join(OUT, 'raw', 'mapa-cego.json'), 'w'), indent=1)
    print(len(mapa), 'arquivos cegos')


def falhas(mec, jul_caso):
    """Critérios em falha de um caso: mecânicos (checar.py) + julgamento, na régua da v2.2."""
    f = [k for k, val in mec['resultado'].items() if val is False]
    aviso = 'AVISO' in str(mec['nota'].get('C6', ''))
    for k, d in jul_caso.items():
        if d['marca'] != 'falha':
            continue
        if k == 'enchimento' and not aviso:
            f.append('enchimento')  # régua v2.2: enchimento real reprova sempre
        elif k == 'enchimento':
            f.append('C6+enchimento')
        else:
            f.append(k)
    return f


def consolidar():
    mapa = json.load(open(os.path.join(OUT, 'raw', 'mapa-cego.json')))
    jul = json.load(open(os.path.join(OUT, 'julgamento.json'), encoding='utf-8'))
    res = {}
    for letra, v in mapa.items():
        n = letra[:2]
        arq, chave = FONTES[v][1](n)
        mec = json.load(open(os.path.join(E, arq), encoding='utf-8'))[chave]
        res[(v, n)] = falhas(mec, jul[letra])
    linhas = ['| Caso | v2.0 | v2.1 | v2.2 |', '|---|---|---|---|']
    for n in CASOS:
        cel = [('passa' if not res[(v, n)] else 'falha: ' + ', '.join(res[(v, n)])) for v in FONTES]
        linhas.append(f'| #{n} | ' + ' | '.join(cel) + ' |')
    ok22 = sum(not res[('v2.2', n)] for n in CASOS)
    inventado = [n for n in CASOS if 'inventado' in res[('v2.2', n)]]
    pior = [n for n in CASOS if not res[('v2.0', n)] and res[('v2.2', n)]]
    aprov = ok22 >= 4 and not inventado and not pior
    tot = {v: sum(not res[(v, n)] for n in CASOS) for v in FONTES}
    linhas += ['', f"Placar: v2.0 {tot['v2.0']}/5 · v2.1 {tot['v2.1']}/5 · v2.2 {tot['v2.2']}/5",
               f"Regra: v2.2 >= 4/5 ({ok22}/5) · sem inventado ({'ok' if not inventado else 'falha em ' + ', '.join(inventado)})"
               f" · não pior que a v2.0 ({'ok' if not pior else 'pior em ' + ', '.join(pior)})",
               f"**Resultado: {'APROVADA' if aprov else 'NÃO APROVADA'}**"]
    open(os.path.join(OUT, 'resumo.md'), 'w', encoding='utf-8').write('\n'.join(linhas) + '\n')
    print('\n'.join(linhas))


if __name__ == '__main__':
    {'cegar': cegar, 'consolidar': consolidar}[sys.argv[1]]()
