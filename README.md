# claude-prompt-skill

Skill `/prompt` para o Claude Code: transforma um pedido escrito às pressas num prompt estruturado (objetivo, contexto, escopo, restrições, critério de pronto, autonomia e formato da resposta), conforme o tipo de tarefa. Não executa nada antes de você aprovar o prompt.

```
/prompt adiciona paginação no endpoint de pedidos do cliente
```

## Instalar

```bash
mkdir -p ~/.claude/skills/prompt
cp v2/prompt/SKILL.md ~/.claude/skills/prompt/SKILL.md
```

Também dá para usar o pacote `prompt-skill.zip`, que traz o mesmo `SKILL.md` e um README curto.

## O que a skill faz
- Classifica o pedido em 9 tipos (Implementar código, Corrigir bug, Revisar, Pesquisar, Explicar, Escrever texto, Analisar dados, Planejar, Agêntica longa) e usa o modelo de prompt do tipo.
- Lê no máximo 3 arquivos de contexto do projeto e não altera nada antes da aprovação.
- Assume o padrão razoável e marca a dúvida em Suposições com "confirme:". Pergunta sempre antes de apagar ou sobrescrever dados ou de migrar banco.
- Não inventa requisitos, motivos nem convenções: o que não está no pedido nem no projeto vai para Suposições.
- Sugere o modo (normal ou plan mode) e o esforço. Uma troca mecânica (renomear, trocar um import) é tarefa comum, sem plan mode nem esforço alto.

## Versões

| Versão | Situação |
|---|---|
| **v2.7** | instalada. 15/15 nos casos de regressão (v2.0: 10/15), validação com 9 casos × 3 repetições sem requisito inventado, sessão longa real |
| v2.4 | aprovada anterior, em `versoes/v2.4` para voltar |
| v2.0 | base de comparação dos casos de regressão |

As tags `v2.0`, `v2.0.1`, `v2.4` e `v2.7` marcam os commits de cada versão aprovada ou instalada. O histórico das decisões está no `SPEC.md` (seção 12) e em `evals/resultados.md`.

## Estrutura

```
v2/prompt/SKILL.md   a skill (arquivo único)
versoes/             cópias das versões v2.0, v2.4 e v2.7
evals/               casos, scripts de avaliação e saídas de cada rodada (roteiro em evals/README.md)
v1/                  a primeira versão, usada para montar um dos projetos de teste
SPEC.md              requisitos, arquitetura e decisões
pesquisa-prompts.md, research_notes/, reports/   pesquisa que embasou a v2
```

## Como uma versão nova é aprovada

A regra de aprovação é escrita em `evals/casos-validacao.md` antes de rodar. Cada versão roda os casos com `claude -p` num HOME isolado, com esforço e versão do Claude Code fixos. Os critérios mecânicos são conferidos por script. Os critérios de julgamento passam por correção cega dupla (dois corretores independentes, e só conta a falha marcada pelos dois), com a versão base na mesma correção. Os passos estão em `evals/README.md`.

## Licença

MIT. Veja `LICENSE`.
