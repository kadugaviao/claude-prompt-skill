"""Cria cópias anonimizadas A/B das saídas para o corretor cego.

Uso: python3 -I evals/cegar.py <pasta-de-runs> [semente]
Gera <pasta>/cego/NN-A.md e NN-B.md e o mapa em <pasta>/raw/mapa-cego.json.
"""
import json, os, random, re, sys

E = os.path.dirname(os.path.abspath(__file__))
pasta = os.path.join(E, sys.argv[1])
random.seed(sys.argv[2] if len(sys.argv) > 2 else pasta)
os.makedirs(os.path.join(pasta, 'cego'), exist_ok=True)
mapa = {}
for n in range(1, 16):
    nid = f'{n:02d}'; vs = ['v1', 'v2']; random.shuffle(vs)
    for letra, v in zip('AB', vs):
        t = open(os.path.join(pasta, f'{v}-{nid}.md'), encoding='utf-8').read()
        t = re.sub(r'^# v\d+-\d\d', f'# caso {nid}-{letra}', t, flags=re.M)
        t = re.sub(r'tmp-home/v\d+', 'tmp-home/X', t)
        t = re.sub(r'^- (exit|skill_carregada):.*\n', '', t, flags=re.M)  # custo e metadados podem denunciar a versão
        t = re.sub(r'skills/prompt/tipos\.md', 'skills/prompt/<arquivo da skill>', t)  # só a v1 tem tipos.md
        open(os.path.join(pasta, 'cego', f'{nid}-{letra}.md'), 'w', encoding='utf-8').write(t)
        mapa[f'{nid}-{letra}'] = v
json.dump(mapa, open(os.path.join(pasta, 'raw', 'mapa-cego.json'), 'w'), indent=1)
print(len(mapa), 'arquivos cegos')
