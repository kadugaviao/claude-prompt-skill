"""Roda os casos de evals/casos.tsv com `claude -p "/prompt <pedido>"`.

Uso: python3 -I evals/rodar.py <saida> <versao=pasta-da-skill> [...] [--casos 01,02] [--paralelo 5] [--so-md] [--tsv casos.tsv]
Ex.: python3 -I evals/rodar.py runs-2 v1=../v1/prompt-skill/prompt v2=../v2/prompt

Cada versão ganha um HOME próprio em evals/tmp-home/<versao>/ com só aquela skill instalada.
O token OAuth vai por variável de ambiente (CLAUDE_CODE_OAUTH_TOKEN); nenhum arquivo de credencial é copiado.
"""
import glob, json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

E = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
COM_VALOR = ('--casos', '--paralelo', '--tsv')
# effortLevel no settings não vale para o Opus 5.5 (docs model-config); --effort vale para a sessão.
# Um `effort` no frontmatter da skill passa por cima, e a checagem pós-execução acusa.
ESFORCO = 'medium'
opts = {a: args[i + 1] for i, a in enumerate(args) if a in COM_VALOR}
pos = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or args[i - 1] not in COM_VALOR)]
saida = os.path.join(E, pos[0])
versoes = dict(p.split('=', 1) for p in pos[1:])
casos = [l.rstrip('\n').split('\t') for l in open(os.path.join(E, opts.get('--tsv', 'casos.tsv')), encoding='utf-8')]
if '--casos' in opts:
    casos = [c for c in casos if c[0] in opts['--casos'].split(',')]
os.makedirs(os.path.join(saida, 'raw'), exist_ok=True)

LIMPAR = ['CLAUDECODE', 'CLAUDE_CODE_ENTRYPOINT', 'CLAUDE_CODE_SESSION_ID', 'CLAUDE_CODE_CHILD_SESSION',
          'CLAUDE_CODE_MESSAGING_SOCKET', 'CLAUDE_CODE_MESSAGING_TOKEN', 'CLAUDE_PID', 'CLAUDE_EFFORT',
          'CLAUDE_CODE_SESSION_ATTENDED']

for v, src in versoes.items():
    home = os.path.join(E, 'tmp-home', v)
    skill = os.path.join(home, '.claude', 'skills', 'prompt')
    if os.path.isdir(skill):
        shutil.rmtree(skill)  # só a pasta da skill dentro do HOME temporário
    shutil.copytree(os.path.join(E, src), skill)
    json.dump({'model': 'opus'}, open(os.path.join(home, '.claude', 'settings.json'), 'w'))


def token():
    with open(os.path.expanduser('~/.claude/.credentials.json')) as f:
        return json.load(f)['claudeAiOauth']['accessToken']


def rel(s):
    return s.replace(os.path.join(E, 'fixtures') + '/', '').replace(E + '/', 'evals/')


def roda(job):
    v, (nid, fx, ped) = job
    env = {k: val for k, val in os.environ.items() if k not in LIMPAR}
    env.update(HOME=os.path.join(E, 'tmp-home', v), CLAUDE_CODE_OAUTH_TOKEN=token())
    raw = os.path.join(saida, 'raw', f'{v}-{nid}.jsonl')
    with open(raw, 'w') as out, open(raw + '.err', 'w') as err:
        skill_dir = os.path.join(E, 'tmp-home', v, '.claude', 'skills', 'prompt')
        r = subprocess.run(['claude', '-p', f'/prompt {ped}'.rstrip(), '--output-format', 'stream-json', '--verbose',
                            '--add-dir', skill_dir, '--effort', ESFORCO],
                           cwd=os.path.join(E, 'fixtures', fx), env=env, stdout=out, stderr=err,
                           stdin=subprocess.DEVNULL, timeout=900)
    return gera_md(v, nid, fx, ped, raw, r.returncode)


def textos(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for val in x.values():
            yield from textos(val)
    elif isinstance(x, list):
        for val in x:
            yield from textos(val)


def skill_carregada(v, sid):
    """Procura na transcrição da sessão (HOME temporário) a 1ª e a última linha do SKILL.md instalado."""
    if not sid:
        return 'sem session_id'
    corpo = open(os.path.join(E, 'tmp-home', v, '.claude', 'skills', 'prompt', 'SKILL.md'), encoding='utf-8').read()
    corpo = corpo.split('---', 2)[2]  # o frontmatter não é injetado
    linhas = [l.strip() for l in corpo.split('\n') if l.strip()]
    primeira, ultima = linhas[0], linhas[-1]
    for proj in glob.glob(os.path.join(E, 'tmp-home', v, '.claude', 'projects', '*', f'{sid}.jsonl')):
        tudo = '\n'.join(t for l in open(proj, encoding='utf-8') for t in textos(json.loads(l)))
        return {(True, True): 'inteira', (True, False): 'PARCIAL (sem a última linha)',
                (False, True): 'PARCIAL (sem a 1ª linha)', (False, False): 'NÃO'}[(primeira in tudo, ultima in tudo)]
    return 'transcrição não encontrada'


def esforcos(v, sid):
    """Valores de \"effort\" gravados nas mensagens do assistente na transcrição da sessão."""
    vals = set()
    for proj in glob.glob(os.path.join(E, 'tmp-home', v, '.claude', 'projects', '*', f'{sid}.jsonl')) if sid else []:
        for l in open(proj, encoding='utf-8'):
            d = json.loads(l)
            if d.get('type') == 'assistant':
                vals.add(d.get('effort'))
    return vals


def gera_md(v, nid, fx, ped, raw, code):
    tools, erros, res, cost, dur, model, sid = [], set(), '', 0.0, 0, [], ''
    for l in open(raw, encoding='utf-8'):
        try:
            d = json.loads(l)
        except ValueError:
            continue
        sid = sid or d.get('session_id') or ''
        m = d.get('message')
        conteudo = m.get('content') if isinstance(m, dict) and isinstance(m.get('content'), list) else []
        if d.get('type') == 'assistant':
            tools += [(c['id'], c['name'], c['input']) for c in conteudo if c.get('type') == 'tool_use']
        erros |= {c['tool_use_id'] for c in conteudo if isinstance(c, dict) and c.get('type') == 'tool_result' and c.get('is_error')}
        if d.get('type') == 'result':
            res, cost, dur = d.get('result') or '', d.get('total_cost_usd') or 0.0, d.get('duration_ms') or 0
            model = list((d.get('modelUsage') or {}).keys())
    ef = esforcos(v, sid)
    ok = ef == {ESFORCO}
    md = [f'# {v}-{nid}', '', f'- pedido: `{ped}`', f'- fixture: {fx}',
          f'- exit: {code} · custo_usd: {cost:.4f} · duracao_s: {dur / 1000:.0f} · modelo: {", ".join(model)}'
          f' · esforco: {", ".join(sorted(map(str, ef))) or "não achado"}',
          f'- skill_carregada: {skill_carregada(v, sid)}',
          '', '## Chamadas de ferramenta', '']
    md += [f'{i}. {n} {rel(json.dumps(inp, ensure_ascii=False))[:300]}' + (' (erro)' if tid in erros else '')
           for i, (tid, n, inp) in enumerate(tools, 1)] or ['(nenhuma)']
    md += ['', '## Resposta final', '', res, '']
    open(os.path.join(saida, f'{v}-{nid}.md'), 'w', encoding='utf-8').write('\n'.join(md))
    return f'{v}-{nid} exit={code} ${cost:.3f}' + ('' if ok else f' ESFORÇO ERRADO: {sorted(map(str, ef))}, esperado {ESFORCO}'), ok


if '--so-md' in args:
    for v in versoes:
        for nid, fx, ped in casos:
            print(gera_md(v, nid, fx, ped, os.path.join(saida, 'raw', f'{v}-{nid}.jsonl'), 0)[0])
    sys.exit()
jobs = [(v, c) for v in versoes for c in casos]
with ThreadPoolExecutor(int(opts.get('--paralelo', 5))) as ex:
    erros = 0
    for linha, ok in ex.map(roda, jobs):
        print(linha, flush=True)
        erros += not ok
print('FIM')
if erros:
    sys.exit(f'{erros} execução(ões) com esforço diferente de {ESFORCO}')
