"""Junta checagem mecânica (checar.py) e julgamento cego (subagente) e escreve resultados.md.

Uso: python3 -I evals/consolidar.py <pasta-de-runs> <saida.md> [cabecalho.md]
Espera em <pasta>: checagem.json, julgamento.json, raw/mapa-cego.json e <versao>-<NN>.md.
"""
import html, json, os, re, sys

E = os.path.dirname(os.path.abspath(__file__))
pasta = os.path.join(E, sys.argv[1])
mec = json.load(open(os.path.join(pasta, 'checagem.json'), encoding='utf-8'))
jul = json.load(open(os.path.join(pasta, 'julgamento.json'), encoding='utf-8'))
mapa = json.load(open(os.path.join(pasta, 'raw', 'mapa-cego.json')))
cab = open(sys.argv[3], encoding='utf-8').read() if len(sys.argv) > 3 else ''
TIPO_NO_CASO = {'01', '03', '05', '08', '09', '10', '11', '12', '15'}  # casos com critério "a. Tipo …"
NOME_MEC = {'tipo': 'a (tipo)', 'esforco': 'esforço', 'plan': 'e (plan mode)', 'vazio': 'a–c'}
CASOS = {l.split('\t')[0]: l.rstrip('\n').split('\t')[2] for l in open(os.path.join(E, 'casos.tsv'), encoding='utf-8')}


def marcas(v, nid):
    m = {}
    for k, val in mec[f'{v}-{nid}']['resultado'].items():
        if k == 'tipo' and nid not in TIPO_NO_CASO:
            continue
        m[NOME_MEC.get(k, k)] = ('n/a' if val is None else 'passa' if val else 'falha', mec[f'{v}-{nid}']['nota'].get(k, ''))
    letra = next(l for l, vv in mapa.items() if vv == v and l.startswith(nid))
    for k, d in jul[letra].items():
        m[k] = (d['marca'], d.get('trecho', ''))
    # D20: C6 em aviso (até +20%) só falha se o corretor apontar enchimento; sozinho, "enchimento" é informativo
    if 'enchimento' in m:
        mk, tr = m['enchimento']
        if mk == 'falha' and 'AVISO' in m.get('C6', ('', ''))[1]:
            m['C6'] = ('falha', m['C6'][1] + ' + enchimento')
        m['enchimento'] = (f'info: {mk}', tr)
    return m


def falhas(m, sem_c7=False):
    return [k for k, (mk, _) in m.items() if mk == 'falha' and not (sem_c7 and k == 'C7')]


def resposta(v, nid):
    t = open(os.path.join(pasta, f'{v}-{nid}.md'), encoding='utf-8').read()
    return t.split('## Resposta final', 1)[1].strip()


linhas, pior, aprov = [], [], {'v1': 0, 'v2': 0}
for nid in sorted(CASOS):
    m1, m2 = marcas('v1', nid), marcas('v2', nid)
    f1, f2 = falhas(m1), falhas(m2)
    p1, p2 = not f1, not f2
    aprov['v1'] += p1; aprov['v2'] += p2
    # "pior": v1 passa e v2 falha, ou v2 falha em mais critérios comuns (C7 só existe na v2)
    if (p1 and not p2) or len(falhas(m2, True)) > len(falhas(m1, True)):
        pior.append(nid)
    linhas.append(f"| #{int(nid)} | {'passa' if p1 else 'falha'} | {'passa' if p2 else 'falha'} | {', '.join(f1) or '—'} | {', '.join(f2) or '—'} |")

passa = aprov['v2'] >= 13 and not pior
out = [cab, '## Tabela final', '',
       f"**v1: {aprov['v1']}/15 · v2: {aprov['v2']}/15 · casos em que a v2 ficou pior: {', '.join('#' + str(int(n)) for n in pior) or 'nenhum'}**", '',
       f"**Regra de liberação (≥ 13/15 na v2 e nenhum caso pior): {'PASSA' if passa else 'NÃO PASSA'}**", '',
       '| Caso | v1 | v2 | Critérios que falharam (v1) | Critérios que falharam (v2) |', '|---|---|---|---|---|', *linhas, '',
       '## Prompts lado a lado', '',
       'Em cada caso: as duas respostas completas e, abaixo, cada critério com a marca e o trecho que a justifica. Mecânicos vêm do `checar.py`; C4, C5 e os específicos de julgamento vêm do corretor cego.', '']
for nid in sorted(CASOS):
    out += [f'### #{int(nid)} · `{CASOS[nid] or "(vazio)"}`', '', '<table><tr><th>v1</th><th>v2</th></tr><tr>']
    out += [f'<td valign="top"><pre>{html.escape(resposta(v, nid))}</pre></td>' for v in ('v1', 'v2')]
    out += ['</tr></table>', '', '| Critério | v1 | v2 |', '|---|---|---|']
    m1, m2 = marcas('v1', nid), marcas('v2', nid)
    def cel(m, k):
        if k not in m:
            return '—'
        mk, tr = m[k]
        tr = re.sub(r'\s+', ' ', str(tr if not isinstance(tr, list) else '; '.join(map(str, tr))))[:220].replace('|', '\\|')
        return f'**{mk}** {tr}' if tr else f'**{mk}**'
    for k in dict.fromkeys([*m1, *m2]):
        out.append(f'| {k} | {cel(m1, k)} | {cel(m2, k)} |')
    out.append('')
open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(out))
print(f"v1 {aprov['v1']}/15 · v2 {aprov['v2']}/15 · pior: {pior} · liberação: {'PASSA' if passa else 'NÃO PASSA'}")
for l in linhas:
    print(l)
