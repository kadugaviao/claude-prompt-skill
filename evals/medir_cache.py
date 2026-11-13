"""Quebra a gravação de cache das execuções por origem: ferramentas, prompt de sistema, corpo da skill, resto.

Uso:
  python3 -I evals/medir_cache.py calibrar <versao>         -> runs-base/calibracao.json (7 execuções mínimas, "responda só ok")
  python3 -I evals/medir_cache.py quebrar <pasta> [...]      -> imprime a tabela e grava <1ª pasta>/../cache.json

Modelo: a API monta o prefixo na ordem ferramentas -> sistema -> mensagens. Na 1ª requisição de uma execução:
  T = ferramentas (B - B com --tools ""), S = sistema da fixture (B - B com --system-prompt "."),
  M = resto da 1ª mensagem (B - T - S: CLAUDE.md, lembretes), K = corpo da skill + pedido (N1 - B).
Cada requisição grava [cache_read, total); a gravação é atribuída aos blocos que esse intervalo cobre.
Tudo depois da 1ª requisição (respostas, resultados de ferramenta) é "resto".
shortcut: T e S medidos com flags que podem mudar outras seções do system prompt; erro de algumas centenas
de tokens, que vai para "resto". Para exatidão, só com count_tokens (exige API key).
"""
import glob, json, os, subprocess, sys

E = os.path.dirname(os.path.abspath(__file__))
FIXTURES = {'12': 'spring', '16': 'python', '17': 'vazio', '18': 'python', '19': 'spring'}
LIMPAR = ['CLAUDECODE', 'CLAUDE_CODE_ENTRYPOINT', 'CLAUDE_CODE_SESSION_ID', 'CLAUDE_CODE_CHILD_SESSION',
          'CLAUDE_CODE_MESSAGING_SOCKET', 'CLAUDE_CODE_MESSAGING_TOKEN', 'CLAUDE_PID', 'CLAUDE_EFFORT',
          'CLAUDE_CODE_SESSION_ATTENDED']  # o mesmo ambiente de rodar.py
PRECO_GRAVA_1H = 8.0  # US$/M tokens, Opus 5.5 (ajuste em resultados locais)


def requisicoes(raw):
    """[(lidos, gravados, sem_cache)] por requisição, na ordem, sem repetir o id da mensagem."""
    vis = {}
    for l in open(raw, encoding='utf-8'):
        d = json.loads(l)
        if d.get('type') == 'assistant':
            u = d['message']['usage']
            vis[d['message']['id']] = (u['cache_read_input_tokens'], u['cache_creation_input_tokens'], u['input_tokens'])
    return list(vis.values())


def calibrar(v):
    with open(os.path.expanduser('~/.claude/.credentials.json')) as f:
        tok = json.load(f)['claudeAiOauth']['accessToken']
    env = {k: val for k, val in os.environ.items() if k not in LIMPAR}
    env.update(HOME=os.path.join(E, 'tmp-home', v), CLAUDE_CODE_OAUTH_TOKEN=tok)
    jobs = [(fx, var) for fx in sorted(set(FIXTURES.values())) for var in ('B', 'sem_sistema')] + [('spring', 'sem_ferramentas')]
    extra = {'B': [], 'sem_sistema': ['--system-prompt', '.'], 'sem_ferramentas': ['--tools', '']}
    out = {}
    for fx, var in jobs:
        r = subprocess.run(['claude', '-p', 'responda só: ok', '--output-format', 'stream-json', '--verbose',
                            '--max-turns', '1', '--effort', 'medium', *extra[var]],
                           cwd=os.path.join(E, 'fixtures', fx), env=env, capture_output=True, text=True, timeout=300)
        reqs = [l for l in r.stdout.splitlines() if l.startswith('{')]
        tmp = os.path.join(E, 'runs-base', 'raw', f'calib-{fx}-{var}.jsonl')
        os.makedirs(os.path.dirname(tmp), exist_ok=True)
        open(tmp, 'w').write('\n'.join(reqs) + '\n')
        out[f'{fx}/{var}'] = sum(requisicoes(tmp)[0])
        print(fx, var, out[f'{fx}/{var}'], flush=True)
    json.dump(out, open(os.path.join(E, 'runs-base', 'calibracao.json'), 'w'), indent=1)


def quebra_execucao(raw, cal, fx):
    reqs = requisicoes(raw)
    B = cal[f'{fx}/B']
    T = cal['spring/B'] - cal['spring/sem_ferramentas']  # ferramentas não dependem da fixture
    S = B - cal[f'{fx}/sem_sistema']
    N1 = sum(reqs[0])
    blocos = [('ferramentas', 0, T), ('sistema', T, T + S), ('resto', T + S, B), ('skill', B, N1)]
    grav = dict.fromkeys(['ferramentas', 'sistema', 'skill', 'resto'], 0)
    for lido, gravado, _ in reqs:
        ini, fim = lido, lido + gravado
        coberto = 0
        for nome, a, b in blocos:
            n = max(0, min(fim, b) - max(ini, a))
            grav[nome] += n
            coberto += n
        grav['resto'] += gravado - coberto  # o que passa de N1: respostas e resultados de ferramenta
    assert sum(grav.values()) == sum(g for _, g, _ in reqs)
    return {'blocos': {'ferramentas': T, 'sistema': S, 'skill': N1 - B, 'resto_1a': B - T - S}, 'gravacao': grav}


def quebrar(pastas):
    cal = json.load(open(os.path.join(E, 'runs-base', 'calibracao.json')))
    res, linhas = {}, ['| execução | ferramentas | sistema | skill | resto | total gravado | US$ gravação |', '|---|---|---|---|---|---|---|']
    for p in pastas:
        for raw in sorted(glob.glob(os.path.join(E, p, 'raw', '*-[0-9][0-9].jsonl'))):
            nid = raw[-8:-6]
            q = quebra_execucao(raw, cal, FIXTURES[nid])
            chave = f'{os.path.basename(p.rstrip("/"))}-{nid}'
            res[chave] = q
            g = q['gravacao']; tot = sum(g.values())
            linhas.append(f'| {chave} | {g["ferramentas"]} | {g["sistema"]} | {g["skill"]} | {g["resto"]} | {tot} | {tot * PRECO_GRAVA_1H / 1e6:.3f} |')
    soma = {k: sum(q['gravacao'][k] for q in res.values()) for k in ('ferramentas', 'sistema', 'skill', 'resto')}
    tot = sum(soma.values()) or 1
    linhas.append(f'| **soma** | ' + ' | '.join(f'{soma[k]} ({soma[k] / tot:.0%})' for k in soma) + f' | {tot} | {tot * PRECO_GRAVA_1H / 1e6:.3f} |')
    b = next(iter(res.values()))['blocos']
    linhas.append(f'\nTamanho dos blocos na 1ª requisição (tokens, 1ª execução): {b}')
    json.dump(res, open(os.path.join(E, os.path.dirname(pastas[0].rstrip('/')), 'cache.json'), 'w'), indent=1)
    print('\n'.join(linhas))


if __name__ == '__main__':
    {'calibrar': lambda: calibrar(sys.argv[2]), 'quebrar': lambda: quebrar(sys.argv[2:])}[sys.argv[1]]()
