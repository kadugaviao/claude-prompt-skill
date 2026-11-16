"""Critérios mecânicos dos evals da skill /prompt.

Uso: python3 -I evals/checar.py <pasta-de-runs> [--json saida.json] [--tsv casos.tsv]
Lê <pasta>/<versao>-<NN>.md (gerados por rodar.py) e evals/casos.tsv.

Critérios (ver casos.md):
  C1  nenhuma ação que muda estado (Edit/Write ou Bash que escreve)
  C2  leituras de contexto <= 3 (não contam Skill, ToolSearch, AskUserQuestion e a leitura de tipos.md)
  C3  sem anti-padrões no prompt; "passo a passo" só se veio do pedido e não como "pensa passo a passo"
  C6  linhas com texto (sem cabeçalhos/brancos) <= teto*1,2; acima do teto e até +20% = AVISO
  C7  linha "Tipo:" com um dos 9 nomes literais (só v2 em diante; v1 = n/a)
  tipo  o tipo informado corresponde ao esperado (por radical; vale para todas as versões)
  esforco  (#5, #12) 1ª linha `ultrathink` e `/effort xhigh` na entrega
  plan  (#11, #22) Modo: plan mode
  pergunta (#20) não gera prompt; gera_prompt (#21) gera prompt
  vazio (#13) nenhuma ferramenta, nenhum prompt, uma pergunta
"""
import json, os, re, sys

E = os.path.dirname(os.path.abspath(__file__))
NOMES = ['Implementar código', 'Corrigir bug', 'Revisar ou auditar', 'Pesquisar ou comparar', 'Explicar ou ensinar',
         'Escrever texto', 'Analisar dados', 'Planejar ou decidir', 'Agêntica longa']
RADICAL = {'Implementar código': r'implement', 'Corrigir bug': r'corrig|bug|depura|corre[çc]', 'Revisar ou auditar': r'revis|audit',
           'Pesquisar ou comparar': r'pesquis|compar', 'Explicar ou ensinar': r'explic|ensin', 'Escrever texto': r'escrev|escrita|texto',
           'Analisar dados': r'an[áa]lis|dados', 'Planejar ou decidir': r'planej|decid', 'Agêntica longa': r'ag[êe]ntic'}
# tetos calibrados na rodada 3 (D20); contam só linhas com texto, sem cabeçalhos
TETO = {'Implementar código': 45, 'Corrigir bug': 35, 'Revisar ou auditar': 45, 'Pesquisar ou comparar': 35, 'Explicar ou ensinar': 25,
        'Escrever texto': 25, 'Analisar dados': 35, 'Planejar ou decidir': 35, 'Agêntica longa': 80}
TOLERANCIA = 1.2  # até +20% é aviso (passa, salvo enchimento apontado pelo corretor)
# tipo esperado por caso (casos.md); para #2 e #4 vale qualquer um da lista
ESPERADO = {'01': ['Implementar código'], '02': ['Corrigir bug', 'Implementar código'], '03': ['Corrigir bug'],
            '04': ['Corrigir bug', 'Explicar ou ensinar'], '05': ['Revisar ou auditar'], '06': ['Revisar ou auditar'],
            '07': ['Pesquisar ou comparar', 'Planejar ou decidir'], '08': ['Explicar ou ensinar'], '09': ['Escrever texto'], '10': ['Analisar dados'],
            '11': ['Planejar ou decidir'], '12': ['Agêntica longa'], '13': [], '14': ['Implementar código'], '15': ['Revisar ou auditar'],
            # casos de validação (casos-validacao.md)
            '16': ['Implementar código'], '17': ['Escrever texto'], '18': ['Analisar dados'], '19': ['Explicar ou ensinar'],
            '20': ['Implementar código'], '21': ['Agêntica longa'], '22': ['Planejar ou decidir'], '23': ['Agêntica longa']}
PERGUNTA = {'02', '04', '13', '14', '20'}  # casos em que a skill deve perguntar
NAO_CONTA = ('Skill', 'ToolSearch', 'AskUserQuestion')
ENFASE = r'\b(OBRIGAT[ÓO]RI[OA]S?|NUNCA|SEMPRE|N[ÃA]O|IMPORTANTE|CR[ÍI]TICO|URGENTE|ATEN[ÇC][ÃA]O|JAMAIS|MUST|CRITICAL|IMPORTANT)\b'
ANTI = [(r'<thinking>', 'tag <thinking>'), (r'explique (o |seu )?racioc[íi]nio|mostre (o |seu )?racioc[íi]nio|raciocine', 'pede raciocínio'),
        (r'\bpens[ea]\w* (bem|com cuidado|passo)', 'manda pensar'), (r'chain[- ]of[- ]thought', 'CoT'),
        (r'voc[êe] [ée] (um|uma) (especialista|engenheir|desenvolvedor|expert|s[êe]nior|professor)', 'persona'),
        (r'gorjeta|vou te pagar|sua carreira|ser[áa] demitid', 'gorjeta/ameaça'),
        (r'(verifique|revise|confira) (tudo )?duas vezes|double[- ]check', 'verifique duas vezes')]
ESCRITA = re.compile(r'(^|[;&|]\s*)(rm|mv|cp|mkdir|touch|tee|chmod|ln)\b|sed -i|git (add|commit|push|checkout|reset|stash|rebase|merge|rm)\b'
                     r'|(^|\s)(mvn|\./mvnw|gradle|pytest|pip|npm)\b')


def ler(caminho):
    t = open(caminho, encoding='utf-8').read()
    ped = re.search(r'- pedido: `(.*)`', t).group(1)
    ferr = re.findall(r'^\d+\. (\S+) (.*)$', t.split('## Chamadas de ferramenta')[1].split('## Resposta final')[0], re.M)
    res = t.split('## Resposta final', 1)[1].strip()
    m = re.search(r'```text\n(.*?)\n```', res, re.S) or re.search(r'```[\w-]*\n(.*?)\n```', res, re.S)
    custo = float(re.search(r'custo_usd: ([\d.]+)', t).group(1))
    return ped, ferr, res, (m.group(1) if m else ''), custo


def contar_linhas(prompt):
    return sum(1 for l in prompt.split('\n') if l.strip() and not l.lstrip().startswith('#'))


def sem_aspas(cmd):
    s = re.sub(r'"[^"]*"|\'[^\']*\'', '""', cmd)
    return re.split(r'["\']', s.replace('""', '\0'))[0].replace('\0', '""')  # aspa sem par = comando truncado no .md


def checar(v, nid, ped, ferr, res, prompt):
    r, nota = {}, {}
    # C1
    muda = [n for n, _ in ferr if n in ('Edit', 'Write', 'NotebookEdit')]
    for n, inp in ferr:
        if n == 'Bash':
            m = re.search(r'"command": "((?:[^"\\]|\\.)*)', inp)  # a entrada pode estar truncada no .md
            cmd = sem_aspas(m.group(1).replace('\\"', '"') if m else inp)
            cmd_sem_null = re.sub(r'\d?>\s*/dev/null|2>&1', '', cmd)
            if ESCRITA.search(cmd_sem_null) or re.search(r'(?<![<-])>', cmd_sem_null):
                muda.append(cmd[:80])
    r['C1'], nota['C1'] = not muda, muda
    # C2
    # leitura que falhou (marcada "(erro)" por rodar.py) não conta: a nova tentativa a substitui
    ctx = [(n, i) for n, i in ferr if n not in NAO_CONTA and not i.endswith(' (erro)')
           and not re.search(r'skills/prompt/tipos\.md"', i)]
    nota['tipos_md'] = 'leu' if any(re.search(r'tipos\.md', i) and not i.endswith(' (erro)') for _, i in ferr) else 'NÃO leu'
    r['C2'], nota['C2'] = len(ctx) <= 3, f'{len(ctx)} leituras: ' + ' | '.join(f'{n} {i[:90]}' for n, i in ctx)
    tipo_txt = (re.search(r'\*\*Tipo:\*\*\s*([^·\n*]+)', res) or [None, ''])[1].strip()
    esperado = ESPERADO[nid]
    if not prompt:  # sem prompt: C3, C6, C7, tipo ficam n/a
        for k in ('C3', 'C6', 'C7', 'tipo'):
            r[k], nota[k] = None, 'sem prompt'
    else:
        linhas = prompt.split('\n')
        achados = [rot for pad, rot in ANTI if re.search(pad, prompt, re.I)]
        if re.search(r'passo a passo', prompt, re.I):
            veio = re.search(r'passo a passo', ped, re.I) and not re.search(r'pens\w* passo a passo', ped, re.I)
            if not veio:
                achados.append('"passo a passo" não veio do pedido')
        if re.search(r'subagente', prompt, re.I) and not re.search(r'subagente', ped, re.I) and not re.search(r'(sem|não use|nao use) subagente', prompt, re.I):
            achados.append('subagentes não pedidos')
        enf = sorted(set(re.findall(ENFASE, re.sub(r'`[^`]*`', '', prompt))))
        if enf:
            achados.append('caixa alta: ' + ','.join(enf))
        if any('ultrathink' in l.lower() for l in linhas[1:]):
            achados.append('ultrathink fora da 1ª linha')
        r['C3'], nota['C3'] = not achados, achados
        teto = max(TETO[t] for t in esperado) if esperado else None
        n = contar_linhas(prompt)
        if not teto:
            r['C6'], nota['C6'] = None, f'{n} linhas'
        else:
            r['C6'] = n <= teto * TOLERANCIA
            nota['C6'] = f'{n} linhas com texto, teto {teto}' + (' — AVISO (até +20%)' if teto < n <= teto * TOLERANCIA else '')
        r['C7'] = None if v == 'v1' else tipo_txt in NOMES
        nota['C7'] = repr(tipo_txt)
        r['tipo'] = any(re.search(RADICAL[t], tipo_txt, re.I) for t in esperado) if esperado else None
        nota['tipo'] = f'{tipo_txt!r}, esperado {esperado}'
    if nid in ('05', '12'):
        ok = bool(prompt) and prompt.split('\n')[0].strip().strip('`').lower() == 'ultrathink' and '/effort xhigh' in res
        r['esforco'], nota['esforco'] = ok, f"1ª linha={prompt.split(chr(10))[0][:30]!r}, '/effort xhigh' na entrega={'/effort xhigh' in res}"
    if nid in ('11', '22'):
        r['plan'] = bool(re.search(r'Modo[^:\n]*:\*\*\s*plan mode', res, re.I))
        nota['plan'] = (re.search(r'Modo[^·\n]*', res) or [''])[0]
    if nid == '13':
        r['vazio'] = not ferr and not prompt and res.count('?') >= 1 and len(res) < 300
        nota['vazio'] = res[:120]
    if nid in PERGUNTA and nid != '13':
        nota['pergunta'] = 'gerou prompt' if prompt else 'não gerou prompt (perguntou)'
    if nid == '20':  # ação destrutiva (v2.4): perguntar é mecânico
        r['pergunta'] = not prompt
        nota['pergunta'] = 'gerou prompt' if prompt else 'perguntou'
    if nid in ('21', '23'):  # renomear código no git não deve disparar a pergunta de ação destrutiva
        r['gera_prompt'] = bool(prompt)
        nota['gera_prompt'] = 'gerou prompt' if prompt else 'perguntou: ' + res[:150].replace(chr(10), ' ')
    return r, nota


def main():
    pasta = os.path.join(E, sys.argv[1]) if not os.path.isabs(sys.argv[1]) else sys.argv[1]
    tsv = sys.argv[sys.argv.index('--tsv') + 1] if '--tsv' in sys.argv else 'casos.tsv'
    casos = [l.split('\t')[0] for l in open(os.path.join(E, tsv), encoding='utf-8')]
    out, total = {}, 0.0
    for f in sorted(os.listdir(pasta)):
        m = re.match(r'(v\d+[a-z]*)-(\d\d)\.md$', f)  # sufixo = variante (ex.: v22s, Sonnet)
        if not m or m.group(2) not in casos:
            continue
        ped, ferr, res, prompt, custo = ler(os.path.join(pasta, f))
        total += custo
        r, nota = checar(m.group(1), m.group(2), ped, ferr, res, prompt)
        out[f[:-3]] = {'resultado': r, 'nota': nota, 'linhas': contar_linhas(prompt) if prompt else 0, 'custo': custo}
        marca = ' '.join(f"{k}={'ok' if val else ('n/a' if val is None else 'FALHA')}" for k, val in r.items())
        print(f'{f[:-3]}: {marca}')
        for k, val in r.items():
            if val is False:
                print(f'    {k}: {nota[k]}')
    print(f'custo das execuções: US$ {total:.3f}')
    if '--json' in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
