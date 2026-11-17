"""Compara versões da skill nos mesmos casos, com correção cega e repetições.

Uso:
  python3 -I evals/comparar_versoes.py cegar-reps <pasta-cego> <rotulo>=<pasta>:<versao> [...] [--casos 12,16]
     <pasta> com subpastas rN/ (uma por repetição) ou plana (1 execução); arquivos <versao>-NN.md
     -> <pasta-cego>/NN-<letra>.md + <pasta-cego>/mapa.json; o corretor grava <pasta-cego>/julgamento.json
  python3 -I evals/comparar_versoes.py consolidar-reps <pasta-cego>
     -> <pasta-cego>/resumo.md: falhas por fonte, repetição e caso, e quantas repetições falham por critério
     Com <pasta-cego>/julgamento-2.json (2ª correção independente), um critério só falha se falhou nas duas.
Pede a checagem do checar.py em cada pasta de repetição (checagem.json, checagem-12.json ou checagem-val.json).
"""
import json, os, random, re, sys

E = os.path.dirname(os.path.abspath(__file__))


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


def anonimiza(t, rotulo):
    t = re.sub(r'^# v[\w.]+-\d\d', f'# caso {rotulo}', t, flags=re.M)
    t = re.sub(r'tmp-home/v[\w.]+', 'tmp-home/X', t)
    return re.sub(r'^- (exit|skill_carregada):.*\n', '', t, flags=re.M)


def execucoes(spec):
    """'rotulo=pasta:versao' -> (rotulo, [(rep, caminho da pasta da repetição)], versao)."""
    rot, resto = spec.split('=', 1)
    pasta, v = resto.rsplit(':', 1)
    reps = sorted(d for d in os.listdir(os.path.join(E, pasta)) if re.fullmatch(r'r\d+', d))
    return rot, [(r, os.path.join(pasta, r)) for r in reps] or [('r1', pasta)], v


def cegar_reps(saida, specs, casos):
    fontes = [execucoes(sp) for sp in specs]
    if not casos:
        rot, reps, v = fontes[0]
        casos = sorted(f[-5:-3] for f in os.listdir(os.path.join(E, reps[0][1])) if re.fullmatch(rf'{v}-\d\d\.md', f))
    random.seed(saida)
    os.makedirs(os.path.join(E, saida), exist_ok=True)
    mapa = {}
    for n in casos:
        itens = [(rot, r, d, v) for rot, reps, v in fontes for r, d in reps]
        random.shuffle(itens)
        assert len(itens) <= 26
        for letra, (rot, r, d, v) in zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', itens):
            t = open(os.path.join(E, d, f'{v}-{n}.md'), encoding='utf-8').read()
            open(os.path.join(E, saida, f'{n}-{letra}.md'), 'w', encoding='utf-8').write(anonimiza(t, f'{n}-{letra}'))
            mapa[f'{n}-{letra}'] = {'fonte': rot, 'rep': r, 'pasta': d, 'versao': v}
    json.dump(mapa, open(os.path.join(E, saida, 'mapa.json'), 'w'), indent=1)
    print(len(mapa), 'arquivos cegos em', saida)


def mecanica(pasta, chave):
    """Checagem do checar.py, procurando nos nomes usados até aqui (checagem.json, -12, -val)."""
    for nome in ('checagem.json', 'checagem-12.json', 'checagem-val.json'):
        arq = os.path.join(E, pasta, nome)
        if os.path.exists(arq):
            d = json.load(open(arq, encoding='utf-8'))
            if chave in d:
                return d[chave]
    raise SystemExit(f'sem checagem de {chave} em {pasta}')


def juntar(j1, j2):
    """Correção dupla: um critério de julgamento só falha se falhou nas duas correções independentes."""
    assert j1.keys() == j2.keys(), 'as duas correções precisam cobrir as mesmas letras'
    out, discord = {}, []
    for letra in j1:
        out[letra] = {}
        for k in j1[letra].keys() | j2[letra].keys():
            m1, m2 = j1[letra].get(k, {}).get('marca'), j2[letra].get(k, {}).get('marca')
            if (m1 == 'falha') != (m2 == 'falha'):
                discord.append(f'{letra}/{k}')
            outra = next((m for m in (m1, m2) if m and m != 'falha'), 'passa')
            out[letra][k] = {'marca': 'falha' if m1 == m2 == 'falha' else outra,
                             'trecho': j1[letra].get(k, j2[letra].get(k))['trecho']}
    return out, discord


def consolidar_reps(saida):
    mapa = json.load(open(os.path.join(E, saida, 'mapa.json')))
    jul = json.load(open(os.path.join(E, saida, 'julgamento.json'), encoding='utf-8'))
    discord = None
    if os.path.exists(os.path.join(E, saida, 'julgamento-2.json')):  # correção dupla (v2.4 em diante)
        jul, discord = juntar(jul, json.load(open(os.path.join(E, saida, 'julgamento-2.json'), encoding='utf-8')))
    res = {}  # (fonte, rep, caso) -> falhas
    for letra, m in mapa.items():
        n = letra[:2]
        res[(m['fonte'], m['rep'], n)] = falhas(mecanica(m['pasta'], f"{m['versao']}-{n}"), jul[letra])
    fontes = sorted({k[0] for k in res}, key=lambda f: list(dict.fromkeys(m['fonte'] for m in mapa.values())).index(f))
    casos = sorted({k[2] for k in res})
    linhas = []
    for f in fontes:
        reps = sorted({k[1] for k in res if k[0] == f})
        linhas += [f'## {f}', '', '| caso | ' + ' | '.join(reps) + ' |', '|---' * (len(reps) + 1) + '|']
        for n in casos:
            linhas.append(f'| #{n} | ' + ' | '.join('passa' if not res[(f, r, n)] else ', '.join(res[(f, r, n)]) for r in reps) + ' |')
        linhas += ['', 'Placar por repetição: ' + ' · '.join(f'{r} {sum(not res[(f, r, n)] for n in casos)}/{len(casos)}' for r in reps), '']
    linhas += ['## Repetições em falha por caso e critério', '', '| caso | critério | ' + ' | '.join(fontes) + ' |', '|---|---|' + '---|' * len(fontes)]
    for n in casos:
        crits = sorted({c for (f, r, m), fl in res.items() if m == n for c in fl})
        for c in crits:
            cel = []
            for f in fontes:
                reps = [r for (ff, r, m) in res if ff == f and m == n]
                cel.append(f'{sum(c in res[(f, r, n)] for r in reps)}/{len(reps)}')
            linhas.append(f'| #{n} | {c} | ' + ' | '.join(cel) + ' |')
    if discord is not None:
        linhas += ['', f'Correção dupla: {len(discord)} marcas em que as duas correções discordaram (só a falha nas duas conta): '
                   + (', '.join(sorted(discord)) or 'nenhuma')]
    json.dump({f'{f}|{r}|{n}': v for (f, r, n), v in res.items()}, open(os.path.join(E, saida, 'falhas.json'), 'w'), indent=1)
    open(os.path.join(E, saida, 'resumo.md'), 'w', encoding='utf-8').write('\n'.join(linhas) + '\n')
    print('\n'.join(linhas))


if __name__ == '__main__':
    a = sys.argv[2:]
    cs = a[a.index('--casos') + 1].split(',') if '--casos' in a else None
    a = [x for i, x in enumerate(a) if x != '--casos' and (i == 0 or a[i - 1] != '--casos')]
    {'cegar-reps': lambda: cegar_reps(a[0], a[1:], cs),
     'consolidar-reps': lambda: consolidar_reps(a[0])}[sys.argv[1]]()
