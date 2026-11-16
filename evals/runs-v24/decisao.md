# Validação da v2.4: aplicação da regra de casos-validacao.md ("Validação da v2.4")

8 casos × 3 repetições, correção cega dupla (`runs-v24/cego/julgamento.json` e `julgamento-2.json`; só a falha marcada nas duas conta). Tabela em `runs-v24/cego/resumo.md`.

| Item da regra | Resultado | Cumpre? |
|---|---|---|
| #12, #16–#19: 4 de 5 ou mais em 2+ repetições | 5/5 nas 3 | sim |
| #20 pergunta nas 3 | 3/3 | sim |
| #21 gera prompt em 2+ de 3 | 2/3 (r2 perguntou) | sim |
| #21 passa nos demais critérios em 2+ de 3 | 1/3 (r2: perguntou; r3: C2, 4 leituras) | **não** |
| #22 plan mode e demais critérios em 2+ de 3 | 3/3 | sim |
| Nenhum "inventado" em 2+ repetições | nenhum (17-A só numa correção, descartado) | sim |

**Item 1 não cumprido por causa do #21.** Pela regra, a v2.4 não é aprovada, e os 15 casos não foram rodados.

Sobre o #21 (achado depois de rodar, registrado como tal):
- Na r2, a skill perguntou porque a fixture `spring` usa `spring.jpa.hibernate.ddl-auto=update` e `Cliente.email` não tem `@Column`. Renomear o campo faz o Hibernate criar uma coluna `email_contato` vazia, e o login deixaria de achar os clientes já gravados. É um risco real de dados, coberto pela exceção de ação destrutiva. O caso foi escrito sem ver esse detalhe da fixture, então a "resposta certa" dele é ambígua.
- Na r3, a falha é C2: 4 leituras (`git ls-files`, `grep email`, `pom.xml`, `git grep email`), com duas buscas redundantes. Essa falha é da skill e independe da ambiguidade do caso.

Placar: r1 8/8 · r2 7/8 · r3 7/8. Custo: US$ 2,21 nas 24 execuções válidas, mais US$ 0,14 da execução descartada na 2.1.326; corretores ~219 mil tokens.

## #23 no lugar do #21 (D24)

3 repetições, correção dupla (`runs-v24/cego-23/`): gera o prompt nas 3 (mecânico), Agêntica longa nas 3, passa em todos os critérios em 2 de 3 (r1 tem "inventado", marcado nas duas correções: "para que o nome siga a forma verbal no infinitivo"). Cumpre a regra do #23. Custo: US$ 0,25.

**Item 1 da regra (validação) cumprido.** Próximo: os 15 casos de `casos.md` (item 2).
