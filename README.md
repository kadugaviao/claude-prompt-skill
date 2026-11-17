# claude-prompt-skill

Skill `/prompt` para o Claude Code: transforma um pedido escrito às pressas num prompt estruturado (objetivo, contexto, escopo, restrições, critério de pronto, autonomia e formato da resposta), conforme o tipo de tarefa. Não executa nada antes de você aprovar o prompt.

```
/prompt adiciona paginação no endpoint de pedidos do cliente
```

## Instalar

Baixe o `claude-prompt-skill-v2.7.zip` da [Release v2.7](https://github.com/kadugaviao/claude-prompt-skill/releases/tag/v2.7) e copie a pasta `prompt/` para `~/.claude/skills/`. Ou, com o repositório clonado:

```bash
mkdir -p ~/.claude/skills/prompt
cp skills/prompt/SKILL.md ~/.claude/skills/prompt/SKILL.md
```

## O que a skill faz
- Classifica o pedido em 9 tipos (Implementar código, Corrigir bug, Revisar, Pesquisar, Explicar, Escrever texto, Analisar dados, Planejar, Agêntica longa) e usa o modelo de prompt do tipo.
- Lê no máximo 3 arquivos de contexto do projeto e não altera nada antes da aprovação.
- Assume o padrão razoável e marca a dúvida em Suposições com "confirme:". Pergunta sempre antes de apagar ou sobrescrever dados ou de migrar banco.
- Não inventa requisitos, motivos nem convenções: o que não está no pedido nem no projeto vai para Suposições.
- Sugere o modo (normal ou plan mode) e o esforço. Uma troca mecânica (renomear, trocar um import) é tarefa comum, sem plan mode nem esforço alto.

## Versões

Cada versão aprovada ou instalada tem uma tag. O conteúdo de uma versão antiga sai com `git show <tag>:<caminho do SKILL.md naquela tag>`.

| Tag | Situação |
|---|---|
| **v2.7** | instalada. 15/15 nos casos de regressão (v2.0: 10/15), validação com 9 casos × 3 repetições sem requisito inventado, sessão longa real |
| v2.4 | aprovada anterior |
| v2.0.1 | v2.0 com esforço médio fixo, instalada entre a v2.3 e a v2.4 |
| v2.0 | primeira versão aprovada da v2; base de comparação dos casos de regressão (`evals/baselines/v2.0`) |

O histórico das decisões está em `docs/spec.md` (seção 12) e em `evals/results.md`.

## Estrutura

```
skills/prompt/SKILL.md   a skill (arquivo único)
docs/spec.md             requisitos, arquitetura e decisões
docs/research/           pesquisa que embasou a v2
evals/                   casos, scripts de avaliação e saídas de cada rodada (roteiro em evals/README.md)
```

A primeira versão da skill (v1) fica em `evals/fixture-sources/skill-v1/`: hoje ela só serve de projeto de teste para um dos casos.

## Como uma versão nova é aprovada

A regra de aprovação é escrita em `evals/validation-cases.md` antes de rodar. Cada versão roda os casos com `claude -p` num HOME isolado, com esforço e versão do Claude Code fixos. Os critérios mecânicos são conferidos por script. Os critérios de julgamento passam por correção cega dupla (dois corretores independentes, e só conta a falha marcada pelos dois), com a versão base na mesma correção. Os passos estão em `evals/README.md`.

## Licença

MIT. Veja `LICENSE`.
