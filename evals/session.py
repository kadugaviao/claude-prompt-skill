"""Mede a skill numa sessão longa, como no uso real: vários turnos na mesma conversa, incluindo a execução depois do "sim".

Uso: python3 -I evals/session.py <saida> <pasta-da-skill> [--effort high]
Ex.: python3 -I evals/session.py runs/v2.8-session ../skills/prompt

Cada turno é um `claude -p` com `--resume` na mesma sessão, numa cópia descartável da fixture `python`
(evals/tmp/session/<nome>/), com o `claude` do PATH (a versão que o usuário usa) e um venv com pytest.
Permissões: aceita edições e só libera leitura, git de leitura e pytest; o resto é negado e fica registrado.
shortcut: `-p --resume` aproxima a sessão interativa (mesmo contexto e cache), mas não a interface; para medir
a interface, só com uma sessão manual.
"""
import glob, json, os, shutil, subprocess, sys, uuid

E = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
saida, skill = os.path.join(E, args[0]), os.path.join(E, args[1])
effort = args[args.index('--effort') + 1] if '--effort' in args else 'high'  # padrão salvo do usuário
nome = os.path.basename(saida.rstrip('/'))
TURNOS = ['/prompt bota um parametro de desconto percentual no calcula_frete sem quebrar os testes', 'sim',
          '/prompt renomeia a função calcula_frete pra calcular_frete no projeto todo', 'sim']
PERMITIDOS = ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash(pytest:*)', 'Bash(python -m pytest:*)', 'Bash(python3 -m pytest:*)',
              'Bash(PYTHONPATH=src pytest:*)', 'Bash(PYTHONPATH=src python -m pytest:*)', 'Bash(PYTHONPATH=src python3 -m pytest:*)',
              'Bash(git diff:*)', 'Bash(git status:*)', 'Bash(git log:*)', 'Bash(git grep:*)', 'Bash(git ls-files:*)',
              'Bash(grep:*)', 'Bash(ls:*)', 'Bash(cat:*)', 'Bash(find:*)', 'Bash(head:*)', 'Bash(sed -n:*)', 'Bash(wc:*)']
LIMPAR = ['CLAUDECODE', 'CLAUDE_CODE_ENTRYPOINT', 'CLAUDE_CODE_SESSION_ID', 'CLAUDE_CODE_CHILD_SESSION',
          'CLAUDE_CODE_MESSAGING_SOCKET', 'CLAUDE_CODE_MESSAGING_TOKEN', 'CLAUDE_PID', 'CLAUDE_EFFORT',
          'CLAUDE_CODE_SESSION_ATTENDED']  # o mesmo ambiente de run.py

home = os.path.join(E, 'tmp/home', f'sessao-{nome}')
dest = os.path.join(home, '.claude', 'skills', 'prompt')
shutil.rmtree(dest, ignore_errors=True)
shutil.copytree(skill, dest)
json.dump({'model': 'opus'}, open(os.path.join(home, '.claude', 'settings.json'), 'w'))
trab = os.path.join(E, 'tmp/session', nome)
shutil.rmtree(trab, ignore_errors=True)
shutil.copytree(os.path.join(E, 'fixtures', 'python'), trab)  # inclui o .git da fixture
os.makedirs(os.path.join(saida, 'raw'), exist_ok=True)

with open(os.path.expanduser('~/.claude/.credentials.json')) as f:
    tok = json.load(f)['claudeAiOauth']['accessToken']
env = {k: v for k, v in os.environ.items() if k not in LIMPAR}
venv = os.path.join(E, 'tmp/session', 'venv', 'bin')
# PYTHONPATH=src faz o papel do pacote instalado no venv, como num projeto real (a fixture não instala `fretes`)
env.update(HOME=home, CLAUDE_CODE_OAUTH_TOKEN=tok, PATH=venv + os.pathsep + env['PATH'], PYTHONPATH=os.path.join(trab, 'src'))
sid = str(uuid.uuid4())


def transcricao():
    arqs = glob.glob(os.path.join(home, '.claude', 'projects', '*', f'{sid}.jsonl'))
    return [json.loads(l) for l in open(arqs[0], encoding='utf-8')] if arqs else []


turnos, vistos, acumulado = [], 0, 0.0  # total_cost_usd vem acumulado na sessão com --resume
for i, msg in enumerate(TURNOS, 1):
    cmd = ['claude', '-p', msg, '--output-format', 'stream-json', '--verbose', '--effort', effort,
           '--permission-mode', 'acceptEdits', '--allowedTools', *PERMITIDOS, '--add-dir', dest]
    cmd += ['--session-id', sid] if i == 1 else ['--resume', sid]
    raw = os.path.join(saida, 'raw', f't{i}.jsonl')
    with open(raw, 'w') as out:
        subprocess.run(cmd, cwd=trab, env=env, stdout=out, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, timeout=1800)
    reqs, ferr, negadas, res = {}, [], 0, {}
    for l in open(raw, encoding='utf-8'):
        d = json.loads(l)
        m = d.get('message') if isinstance(d.get('message'), dict) else {}
        cont = m.get('content') if isinstance(m.get('content'), list) else []
        if d.get('type') == 'assistant':
            reqs[m['id']] = m['usage']
            ferr += [c['name'] for c in cont if c.get('type') == 'tool_use']
        negadas += sum(1 for c in cont if c.get('type') == 'tool_result' and c.get('is_error')
                       and any(t in json.dumps(c.get('content', '')).lower() for t in ('permission', 'requires approval')))
        if d.get('type') == 'result':
            res = d
    tr = transcricao()
    novos = [x for x in tr if x.get('type') == 'assistant'][vistos:]
    vistos += len(novos)
    u = res.get('usage', {})
    custo = res.get('total_cost_usd', 0) - acumulado
    acumulado = res.get('total_cost_usd', 0)
    turnos.append({'turno': i, 'mensagem': msg, 'custo': round(custo, 4), 'requisicoes': len(reqs),
                   'gravacao': u.get('cache_creation_input_tokens', 0), 'leitura': u.get('cache_read_input_tokens', 0),
                   'saida': u.get('output_tokens', 0),
                   'thinking': (u.get('output_tokens_details') or {}).get('thinking_tokens', 0),
                   'esforco': sorted({str(x.get('effort')) for x in novos}),
                   'versao': sorted({str(x.get('version')) for x in novos}),
                   'ferramentas': len(ferr), 'negadas': negadas,
                   'edicoes': sum(1 for n in ferr if n in ('Edit', 'Write', 'MultiEdit')),
                   'erro': res.get('is_error', True), 'resposta': (res.get('result') or '')[:300],
                   'cabecalho': (res.get('result') or '').split('\n')[0][:160],
                   'ultrathink': 'ultrathink' in (res.get('result') or '')})
    print(json.dumps({k: v for k, v in turnos[-1].items() if k != 'resposta'}, ensure_ascii=False), flush=True)

teste = subprocess.run([os.path.join(venv, 'pytest'), '-q', '-p', 'no:cacheprovider'], cwd=trab, capture_output=True, text=True, env=env)
fim = {'progress_md': os.path.exists(os.path.join(trab, 'progress.md')), 'pytest_rc': teste.returncode, 'pytest': teste.stdout.strip().splitlines()[-1:] or [teste.stderr[-200:]],
       'diff': subprocess.run(['git', 'diff', '--stat'], cwd=trab, capture_output=True, text=True).stdout.strip(),
       'restos_calcula_frete': subprocess.run(['git', 'grep', '-n', r'calcula_frete\b'], cwd=trab,
                                              capture_output=True, text=True).stdout.strip(),
       'desconto': subprocess.run(['git', 'grep', '-n', '-i', 'desconto'], cwd=trab,
                                  capture_output=True, text=True).stdout.strip()[:600]}
json.dump({'sessao': sid, 'effort_sessao': effort, 'turnos': turnos, 'fim': fim},
          open(os.path.join(saida, 'resumo.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps(fim, ensure_ascii=False, indent=1))
