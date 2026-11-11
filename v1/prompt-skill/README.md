# Skill /prompt

Transforma um pedido rápido, do jeito que vier na cabeça, em um prompt estruturado seguindo as boas práticas da Anthropic. O resultado sai sempre no mesmo formato.

```
/prompt revisa meu codigo ve se ta bom
```

vira um prompt com:
- **Objetivo**
- **Contexto** (com arquivos e versões reais do projeto)
- **Tarefa**
- **Restrições**
- **Pronto quando**
- **Formato da resposta**, que muda conforme o tipo de tarefa

## Instalar

```zsh
cp -r prompt ~/.claude/skills/
```

Abra o Claude Code de novo. Digite `/` e confira se `prompt` aparece na lista.

## Usar

1. Digite `/prompt` seguido do pedido.
2. Se faltar algo que muda o resultado, ele pergunta (no máximo 3 perguntas). Senão, assume e lista as suposições.
3. Ele entrega o prompt num bloco de código, com o modo sugerido (plan mode ou não) e se vale usar `ultrathink`.
4. No final, pergunta se você quer executar o prompt. Responda "sim" ou peça ajustes.

## Tipos de tarefa

Cada tipo tem o seu formato de resposta padrão. Eles estão definidos em `prompt/tipos.md`:

| Tipo | Formato da resposta |
|---|---|
| Implementar | resumo, arquivos alterados, como foi verificado |
| Corrigir bug | causa raiz, correção, teste que reproduz |
| Revisar ou auditar | veredito, tabela de achados com severidade |
| Pesquisar ou comparar | recomendação, tabela comparativa, fontes |
| Explicar ou ensinar | essencial, exemplo, erros comuns, exercício |
| Escrever texto | texto pronto (ou 2 versões) |
| Analisar dados | resposta com números, método, limitações |
| Planejar ou decidir | recomendação, plano em etapas, riscos |

Para mudar um formato, edite o `tipos.md`.

## Boas práticas aplicadas

Baseadas na documentação da Anthropic para os modelos atuais:
- verbos de ação;
- o porquê de cada regra;
- instruções positivas;
- tom normal, porque modelos atuais reagem demais a "OBRIGATÓRIO";
- escopo explícito;
- pedido de evidência;
- em revisões, todos os achados com severidade, porque um filtro "só o grave" é seguido ao pé da letra;
- critério de pronto, em vez de "revise duas vezes".

Fontes:
- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Skills – Claude Code](https://code.claude.com/docs/en/skills)
