# v2.7 (17/11/2026): APROVADA E INSTALADA

Os 3 itens cumpridos: validação sem "inventado" em nenhuma das 27 saídas (r1 9/9 · r2 8/9 · r3 8/9; falhas isoladas: #12 C2 no r3, #17 enchimento no r2); 15 casos 15/15 contra 10/15 da v2.0; sessão longa sem exagero, US$ 0,43. Detalhes em `runs-v27/decisao.md`. Custo: US$ 4,79 e ~427 mil tokens de corretor.

---

# v2.6 (16/11/2026): NÃO APROVADA; a v2.4 continua instalada

Itens 2 e 3 cumpridos (15 casos 15/15 contra 12/15 da v2.0; sessão longa sem exagero, US$ 0,45). Item 1 falhou: "inventado" em 2 de 3 no #12 (JUnit 5/Mockito atribuído ao CLAUDE.md; vem do modelo do tipo Implementar) e no #17 (escolhas de redação como requisito). Detalhes em `runs-v26/decisao.md`. Custo: US$ 4,75 e ~430 mil tokens de corretor.

---

# v2.5 (16/11/2026): NÃO APROVADA; a v2.4 continua instalada

Medição de uso real da v2.4 (`runs-sessao/`): 2 tarefas por sessão (prompt + execução), US$ 0,50–0,53 por sessão, tarefas feitas e `pytest` verde; o renome mecânico saía como Agêntica longa com `ultrathink` e deixava `progress.md` no projeto.

A v2.5 corrigiu isso (#23/#24: Implementar código, normal, sem `ultrathink`, 3/3), mas criou uma regressão no #11 (Agêntica longa em vez de Planejar) e teve "inventado" no #23 em 2 de 3 (um "para quê" inventado). Detalhes em `runs-v25/decisao.md`. Custo: US$ 4,67 e ~226 mil tokens de corretor.

---

# v2.4 (16/11/2026): APROVADA e instalada

**Versão:** `versoes/v2.4/` = candidata da v2.3 (M6 `effort: medium`, M1, M2, M1b) + pergunta obrigatória antes de apagar ou sobrescrever dados ou migrar banco + plan mode para planejar migração. Claude Code 2.1.323 (binário fixo), effort medium, correção cega dupla.

| Etapa | Pasta | Resultado |
|---|---|---|
| Validação: #12, #16–#20, #22 × 3 repetições | `runs-v24/` | #12 e #16–#19 5/5 nas 3; #20 (apagar dados de produção) perguntou nas 3; #22 plan mode nas 3 |
| #21 → #23 (D24) | `runs-v24/cego-23/` | #21 era ambíguo (renomear `email` com `ddl-auto=update` arrisca dados); #23 (renomear função, sem dados) passa em 2 de 3 |
| 15 casos de `casos.md`, com a v2.0 na mesma correção | `runs-v24-15/` | **v2.4 15/15**, v2.0 12/15 (#01 e #09 inventado, #12d); nenhuma regressão |

**Custo:** US$ 4,62 nas execuções (validação 2,21 + 0,14 descartada na 2.1.326 · #23 0,25 · 15 casos 2,01) e cerca de 530 mil tokens dos corretores Sonnet (6 correções). Por execução, com cache quente, o mesmo da v2.2 (cerca de US$ 0,06); a saída é 61% do custo e é o próprio prompt gerado.

**Correção dupla:** descartou 2 marcas em que os corretores discordaram (17-A inventado na validação; 12-A enchimento da v2.0 nos 15 casos). Dois corretores abriram o começo do `mapa.json` por engano; nos dois casos, o outro corretor, que não viu o mapa, marcou igual.

---

# Estudo da v2.3 (13/11/2026): NÃO APROVADA; instalada a v2.0.1 (16/11/2026)

**Correção de registro:** todas as execuções anteriores (rodada 3, validação, v2.1, v2.2) rodaram em **effort medium**, não em alto como dizem as seções abaixo. O `effortLevel` do settings não vale para o Opus 5.5; desde 12/11 o `rodar.py` passa `--effort medium` e confere o esforço e a versão do Claude Code na transcrição.

| Etapa | Pasta | Resultado |
|---|---|---|
| Linha de base v2.2 (3 repetições) | `runs-base/` | 3/5 nas 3 repetições (corrigida sozinha); US$ 0,069 por execução |
| Teste Sonnet (`model: sonnet`) | `runs-sonnet/` | 0/5 · 2/5 · 2/5; −30% de custo. Descartado |
| Rodada A: M6 + M1 + M2 | `runs-a/` | M1 e M2 aceitas; 10/15 contra 12/15 da base na mesma correção |
| Rodada A2: M1b | `runs-a2/` | 13/15 contra 11/15; "inventado" 0 contra 2. Mantida com exceção (D21) |
| Rodada B: M3 + M4 | `runs-b/` | saída −2% (mínimo 5%): reprovadas. M1b confirmada |
| 15 casos de `casos.md` (v2.3 = A2) | `runs-v23-15/` | **12/15** (mínimo 13); regressão contra a v2.0 em #14, #11 e #06. A v2.0, na mesma correção, também fez 12/15 |

**Por que reprovou:** o #14 deveria perguntar antes de apagar dados e a v2.3 assumiu o critério de duplicata. A regra "assuma o padrão razoável" (v2.2) não abre exceção clara para ação destrutiva quando o pedido parece autorizar. O #11 e o #06 são variação (modo e enchimento limítrofe).

**Custo:** com o cache quente, todas as candidatas custaram o mesmo que a base (US$ 0,064 por execução). Etapa inteira: US$ 6,45 nas execuções (M6 0,12 · A 1,37 · A2 1,40 · B 1,40 · 15 casos 2,16) e cerca de 470 mil tokens dos corretores Sonnet.

**Quebra do custo (linha de base, 15 execuções):** saída 61%, gravação de cache 22%, leitura 17%. Na 1ª requisição: ferramentas 14.384 tokens, sistema ~2,6 mil, corpo da skill ~5 mil (`evals/medir_cache.py`).

---

# Resultados dos evals da skill /prompt: rodada 3 + validação (11/11/2026)

**Veredito: v2 APROVADA.**
- Validação: os 4 casos novos, nunca vistos pela skill, passaram (4/4).
- Rodada 3, com a régua calibrada (D20): v2 14/15, v1 4/15, e a v2 não fica pior em nenhum caso.

## Como foi rodado
- **Harness:** `claude -p "/prompt …"`, Opus 5.5 com esforço alto, HOME temporário (`evals/tmp-home/`) e fixtures em `evals/fixtures/`. Usa `--add-dir` com a pasta da skill, porque a v1 ainda tem o `tipos.md` separado. Todas as 34 execuções registraram `skill_carregada: inteira`, conferido na transcrição da sessão, e a v1 leu o `tipos.md` em todas as execuções em que tentou.
- **Mudanças na v2 desde a rodada 2:**
  - `tipos.md` fundido no `SKILL.md` (D17);
  - regra de escolha do tipo e desempate (D18);
  - "não resolva a tarefa no prompt" (D19).
- **Régua:**
  - C5 aceita objetivo no infinitivo, e o #7 não avalia o rótulo do tipo (mudanças da rodada 3 em `casos.md`).
  - Depois de ver a rodada 3, o usuário aprovou os tetos calibrados e a contagem só de linhas com texto, com até +20% como aviso (D20).
  - Como a régua mudou depois de ver os resultados, a aprovação dependeu dos 4 casos de validação (`casos-validacao.md`), escritos depois da calibração.
- **Correção:**
  - Mecânicos por `checar.py`.
  - Julgamento por subagentes Sonnet que não viram a skill ser escrita: às cegas (A/B) na rodada 3 e só com a v2 na validação, cada marca com o trecho literal citado.
  - Consolidação por `consolidar.py` (rodada 3) e pela regra de passagem do `casos-validacao.md` (validação).

## Validação (só v2, casos #16 a #19)

| Caso | Resultado | Mecânicos | Julgamento (C4, C5, específicos) | Enchimento (informativo, C6 sem aviso) |
|---|---|---|---|---|
| #16 | **passa** | C1=ok, C2=ok, C3=ok, C6=ok, C7=ok, tipo=ok; 19 linhas com texto, teto 45 | C4=passa, C5=passa, b=passa, c=passa, d=passa, e=passa, f=passa | falha: Chamadas que já existem precisam continuar com o mesmo resultado. / Antes de assumir algo fora desta lista, investigue no código. |
| #17 | **passa** | C1=ok, C2=ok, C3=ok, C6=ok, C7=ok, tipo=ok; 14 linhas com texto, teto 25 | C4=passa, C5=passa, b=passa, c=passa, d=passa | falha: O cliente esperava a entrega na data combinada, e ela vai sair 3 dias depois. O risco é o e-mail parecer desculpa esfarrapada. |
| #18 | **passa** | C1=ok, C2=ok, C3=ok, C6=ok, C7=ok, tipo=ok; 19 linhas com texto, teto 35 | C4=passa, C5=passa, b=passa, c=passa, d=passa, e=passa, f=passa | falha: Projeto Python `fretes` 0.3.0 (requires-python >=3.12, pyproject.toml). / Antes de assumir algo fora desta lista, investigue no arquivo. |
| #19 | **passa** | C1=ok, C2=ok, C3=ok, C6=ok, C7=ok, tipo=ok; 19 linhas com texto, teto 25 | C4=passa, C5=passa, b=passa, c=passa, d=passa, e=passa, f=passa | falha: Fora do escopo: corrigir ou refatorar o projeto, porque o objetivo é aprender. / - Não altere arquivos do projeto, porque o pedido é só de explicação. |

**Validação: 4/4 passam.**

**Sobre o enchimento:** o corretor apontou enchimento nos 4 prompts e concluiu "nenhum passa". Pela regra definida antes da rodada (`casos-validacao.md` e D20), o enchimento só decide o caso quando o C6 está em aviso. Nos 4 casos, o C6 ficou dentro do teto, sem aviso, então eles passam. As marcas do corretor continuam no `runs-val/julgamento.json`.

Mesmo assim, o achado é real e vira melhoria proposta, não bloqueio. Duas das quatro frases apontadas ("Antes de assumir algo fora desta lista, investigue no código/arquivo") vêm do próprio esqueleto da skill, na seção Autonomia. As outras são repetições do pedido ou da Tarefa.

**Caso duvidoso apontado pelo corretor:** no #17d, o prompt pede "sem meta-comentário", mas depois pede uma lista curta dos marcadores a preencher. Ficou como `passa`.

## Pendências conhecidas (não bloqueiam)
1. **#12d (rodada 3):** numa migração longa, o prompt da v2 não registra o estado do trabalho (git, `progress.md`). Correção proposta: pôr o registro de progresso no template de Agêntica longa ("Durante o trabalho: atualize `progress.md` a cada etapa").
2. **Enchimento vindo do esqueleto:** tirar ou condicionar a frase "Antes de assumir algo fora desta lista, investigue no código" da seção Autonomia.
3. **Comandos compostos de leitura:** às vezes são bloqueados no `-p` (`for`, `$(...)`, `awk`). O modelo tenta de novo com um comando simples, e o `checar.py` não conta chamadas que falharam. No uso interativo, esses comandos pediriam aprovação.

## Custo
- Execuções (`total_cost_usd` do `claude -p`): teste rápido US$ 0,53 + rodada 3 US$ 3,42 + validação US$ 0,55 = **US$ 4,50**.
- Corretores Sonnet: cerca de 102 mil tokens (rodada 3) e 47 mil (validação), **US$ 0,6 a 0,9 estimados** (o valor exato não é exposto).


## Rodada 3: tabela final (régua calibrada D20)

**v1: 4/15 · v2: 14/15 · casos em que a v2 ficou pior: nenhum**

**Regra de liberação (≥ 13/15 na v2 e nenhum caso pior): PASSA**

| Caso | v1 | v2 | Critérios que falharam (v1) | Critérios que falharam (v2) |
|---|---|---|---|---|
| #1 | falha | passa | e | — |
| #2 | falha | passa | a | — |
| #3 | falha | passa | e | — |
| #4 | passa | passa | — | — |
| #5 | falha | passa | C3, esforço, C5 | — |
| #6 | falha | passa | b | — |
| #7 | falha | passa | c, d | — |
| #8 | falha | passa | e | — |
| #9 | falha | passa | d | — |
| #10 | passa | passa | — | — |
| #11 | falha | passa | c | — |
| #12 | falha | falha | a (tipo), esforço, C5, d | d |
| #13 | passa | passa | — | — |
| #14 | falha | passa | C3, a | — |
| #15 | passa | passa | — | — |

## Prompts lado a lado

Em cada caso: as duas respostas completas e, abaixo, cada critério com a marca e o trecho que a justifica. Mecânicos vêm do `checar.py`; C4, C5 e os específicos de julgamento vêm do corretor cego.

### #1 · `cria endpoint pra listar pedidos por cliente com paginacao`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>**Tipo:** Implementar · **Modo sugerido:** plan mode · **Raciocínio:** normal

```text
Objetivo: implemente um endpoint REST que lista os pedidos de um cliente com paginação. O front-end vai usá-lo para mostrar o histórico de pedidos sem carregar tudo de uma vez.

Contexto:
- Projeto `loja`: Spring Boot 3.3.5, Java 21, Spring Data JPA, PostgreSQL 16, sem migrations (ddl-auto=update).
- Camadas: controller -&gt; service -&gt; repository. Controllers recebem e devolvem DTOs (records em `src/main/java/com/exemplo/loja/dto/`). Essa pasta ainda não existe, então crie-a.
- Arquivos relevantes:
  - `controller/PedidoController.java`: `@RequestMapping(&quot;/pedidos&quot;)`, tem só `GET /{id}`
  - `service/PedidoService.java`
  - `repository/PedidoRepository.java`: já tem `List&lt;Pedido&gt; findByClienteId(Long clienteId)`
  - `repository/ClienteRepository.java`
  - `model/Pedido.java`: campos `id`, `cliente` (@ManyToOne), `itens` (@OneToMany LAZY)
  - teste existente: `src/test/java/com/exemplo/loja/service/PedidoServiceTest.java`

Tarefa:
1. Exponha `GET /pedidos?clienteId={id}&amp;page=0&amp;size=20&amp;sort=id,desc` no `PedidoController`, recebendo um `Pageable`. Padrões: size 20, ordenação `id` desc. Limite o size a 100 para que ninguém peça a tabela inteira.
2. No `PedidoRepository`, adicione uma consulta paginada por cliente (ex.: `Page&lt;Pedido&gt; findByClienteId(Long clienteId, Pageable pageable)`). Mantenha o método atual.
3. No `PedidoService`, crie o método de listagem. Se o cliente não existir, responda 404, porque assim o front diferencia &quot;cliente inválido&quot; de &quot;cliente sem pedidos&quot;. Um cliente sem pedidos recebe 200 com a página vazia.
4. Crie os records em `dto/`:
   - `PedidoResumoResponse` com `id`, `clienteId` e `quantidadeItens`
   - `PaginaResponse&lt;T&gt;` com `conteudo`, `pagina`, `tamanho`, `totalElementos` e `totalPaginas`
   Não serialize `Page`/`PageImpl` direto, porque o Spring Data 3.3 avisa que esse JSON não é estável.
5. Monte os DTOs sem N+1 e sem `LazyInitializationException` ao acessar `itens`. Exemplos: projeção JPQL com `size(p.itens)` ou contagem agrupada. Escolha uma e justifique em uma frase.
6. Escreva os testes: unitários no service (cliente inexistente, cliente sem pedidos, página com resultados) e um `@WebMvcTest` no controller (parâmetros de paginação, size acima de 100 e o formato do JSON).

Restrições:
- Não altere as entidades em `model/`. Com ddl-auto=update, qualquer mudança nelas altera o schema do banco.
- Não adicione dependências ao `pom.xml`. Se faltar alguma para os testes, pare e me avise.
- Não mexa no `GET /pedidos/{id}`, mesmo ele devolvendo a entidade e não um DTO. Fica fora do escopo. Se achar que vale corrigir, diga isso em uma frase no final.
- Não faça commit nem push.

Pronto quando:
- `./mvnw test` passa, incluindo os testes novos.
- Os casos 404, página vazia, página com resultados e size limitado a 100 estão cobertos por teste.
- O JSON de resposta segue o formato de `PaginaResponse`, comprovado por asserção no `@WebMvcTest`.

Formato da resposta:
1. Resumo da mudança (2 a 3 linhas)
2. Arquivos criados ou alterados, com uma linha sobre cada um
3. Como foi verificado: o comando rodado e o trecho final da saída do `./mvnw test`
4. Decisões tomadas (rota, como evitou o N+1, tratamento de 404) e pendências
```

**Suposições:**
- A rota é `GET /pedidos?clienteId=` no `PedidoController` atual, não `/clientes/{id}/pedidos`, porque não existe um `ClienteController`.
- `Pedido` não tem data, então a ordenação padrão é por `id` desc.
- Cliente inexistente responde 404, e cliente sem pedidos responde 200 com a lista vazia.
- O resumo do pedido traz `id`, `clienteId` e `quantidadeItens`, já que a entidade não tem outros campos.

**O que melhorou:**
- O prompt cita os arquivos, as versões e as convenções reais do projeto. Também avisa que a pasta `dto/` ainda não existe e que o endpoint atual devolve a entidade.
- Antecipa armadilhas concretas: N+1 e `LazyInitializationException` em `itens`, o JSON instável do `PageImpl` no Spring Boot 3.3 e o ddl-auto=update alterando o schema.
- Define critérios verificáveis: casos de teste específicos, limite de size e `./mvnw test` passando.

Quer que eu execute este prompt agora?</pre></td>
<td valign="top"><pre>**Tipo:** Implementar código · **Modo:** plan mode · **Esforço:** padrão

```text
Implemente um endpoint REST que lista os pedidos de um cliente com paginação, para que o front consiga mostrar o histórico de pedidos de um cliente sem carregar tudo de uma vez.

## Contexto
Projeto `loja`: Spring Boot 3.3.5, Java 21, Spring Data JPA, Spring Security, PostgreSQL 16 (`ddl-auto=update`, sem migrations).
Hoje existe só `GET /pedidos/{id}`, e ele devolve a entidade `Pedido` direto, com `itens` LAZY. A pasta `dto/` ainda não existe. `PedidoRepository` já tem `List&lt;Pedido&gt; findByClienteId(Long clienteId)`, sem paginação.

## Insumos
Arquivos a ler:
- src/main/java/com/exemplo/loja/controller/PedidoController.java
- src/main/java/com/exemplo/loja/service/PedidoService.java
- src/main/java/com/exemplo/loja/repository/PedidoRepository.java e ClienteRepository.java
- src/main/java/com/exemplo/loja/model/Pedido.java, Cliente.java, ItemPedido.java
- src/test/java/com/exemplo/loja/service/PedidoServiceTest.java
- a configuração de segurança que o projeto já tiver (comece por AuthController.java)

## Tarefa e escopo
1. Crie `GET /clientes/{clienteId}/pedidos` com os parâmetros `page`, `size` e `sort` do Spring Data (`Pageable`), um tamanho padrão e um limite máximo de `size`.
2. Siga as camadas controller -&gt; service -&gt; repository. A resposta deve ser um DTO record em `com.exemplo.loja.dto`, com o conteúdo da página e os metadados (número da página, tamanho, total de elementos, total de páginas).
3. Se o cliente não existir, responda 404. Se o cliente existir e não tiver pedidos, responda 200 com a página vazia.
Fora do escopo: mudar `GET /pedidos/{id}` para usar DTO e migrar os testes JUnit 4 existentes. São pendências separadas, e mexer nelas aumentaria o diff sem fazer parte do pedido.

## Restrições
- Não serialize a entidade `Pedido` na resposta, porque `itens` é LAZY e a convenção do projeto é usar DTOs nos controllers.
- Monte a página com uma quantidade fixa de queries, sem uma query por pedido, porque a lista cresce com o histórico do cliente.
- Não adicione abstrações, opções ou configurabilidade que não foram pedidas.
- Escreva os testes novos em JUnit 5 + Mockito. O projeto também roda JUnit 4 pelo vintage engine, então os testes antigos continuam funcionando.

## Pronto quando
- `./mvnw test` passa.
- Os testes cobrem: página com pedidos, página vazia, cliente inexistente (404) e `size` acima do limite.

## Autonomia
Pode fazer sem perguntar: criar o pacote `dto/`, adicionar métodos paginados no repository, criar o método no service e o handler no controller, e escrever os testes.
Pergunte antes de: mudar a configuração de segurança, adicionar dependências ao `pom.xml` ou alterar entidades.
Suposições: a rota fica aninhada em `/clientes/{clienteId}/pedidos`; o DTO de cada pedido traz só `id` e `clienteId` (a entidade não tem outros campos escalares); a ordenação padrão é `id` decrescente; o endpoint segue a regra de autenticação que já existe, sem checar se o usuário logado é o dono dos pedidos. Diga se alguma estiver errada. Antes de assumir algo fora desta lista, investigue no código.

## Formato da resposta
1. Resumo em até 3 frases.
2. Arquivos criados ou alterados: um por linha, com o porquê.
3. Verificação: comandos rodados e resultado.
4. Riscos e pendências (até 5; omita se não houver).
```

**O que mudou:**
- O pedido virou um contrato: rota, parâmetros de paginação, 404 versus página vazia e critérios de teste com `./mvnw test`.
- Entraram dois fatos do código: `GET /pedidos/{id}` devolve a entidade com `itens` LAZY, e a pasta `dto/` ainda não existe. Por isso o prompt pede um DTO e proíbe uma query por pedido.
- Algumas escolhas ficaram como suposições para você corrigir: o formato da rota, os campos do DTO e o fato de não checar se o usuário logado é o dono dos pedidos.

Quer que eu execute este prompt agora?</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 2 leituras: Bash {"command": "git ls-files \| head -100 && cat README* 2>/dev/null \| head -50", "description \| Bash {"command": "grep -A2 -E \"spring-boot-starter-parent\|<java.version>\" pom.xml; cat src/ma | **passa** 3 leituras: Bash {"command": "find . -path ./.git -prune -o -type f -print \| grep -v target/ \| sort", "desc \| Read {"file_path": "spring/pom.xml"} \| Bash {"command": "cd spring/src && head -n 200 main/java/com/exemplo/lo |
| C3 | **passa** | **passa** |
| C6 | **passa** 35 linhas com texto, teto 45 | **passa** 27 linhas com texto, teto 45 |
| C7 | **n/a** 'Implementar' | **passa** 'Implementar código' |
| a (tipo) | **passa** 'Implementar', esperado ['Implementar código'] | **passa** 'Implementar código', esperado ['Implementar código'] |
| C4 | **passa** Quer que eu execute este prompt agora? | **passa** Quer que eu execute este prompt agora? |
| C5 | **passa** Objetivo: implemente um endpoint REST que lista os pedidos de um cliente com paginação. | **passa** Implemente um endpoint REST que lista os pedidos de um cliente com paginação |
| b | **passa** Projeto `loja`: Spring Boot 3.3.5, Java 21, Spring Data JPA, PostgreSQL 16 | **passa** Projeto `loja`: Spring Boot 3.3.5, Java 21, Spring Data JPA |
| c | **passa** Exponha `GET /pedidos?clienteId={id}&page=0&size=20&sort=id,desc` no `PedidoController`, recebendo um `Pageable`. | **passa** com os parâmetros `page`, `size` e `sort` do Spring Data (`Pageable`) |
| d | **passa** `./mvnw test` passa, incluindo os testes novos. | **passa** `./mvnw test` passa. |
| e | **falha** ausente: Fica fora do escopo. Se achar que vale corrigir, diga isso em uma frase no final. | **passa** Não adicione abstrações, opções ou configurabilidade que não foram pedidas. |
| f | **passa** Não faça commit nem push. | **passa** Pergunte antes de: mudar a configuração de segurança, adicionar dependências ao `pom.xml` ou alterar entidades. |

### #2 · `ta, me da o prompt pra arrumar esses problemas`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>Antes de montar o prompt, preciso saber uma coisa: não encontrei nesta conversa nenhuma lista de problemas para &quot;esses problemas&quot; se referir. O repositório só tem a skill `/prompt` (`README.md` e `prompt/`) e o git está limpo, sem nada aberto.

1. **Quais são os problemas?** Cole a lista, a mensagem de erro ou o resultado da revisão. Se for uma revisão que você fez em outra sessão, cole os achados.
2. **Eles são na própria skill `/prompt`** (`prompt/SKILL.md`, `prompt/tipos.md`, `README.md`) **ou em outro projeto?** Se for outro projeto, me diga o caminho.
3. **Quer que corrija tudo ou só alguns?** Por exemplo, só os de severidade alta, ou deixar algum arquivo sem alteração.

Com isso eu entrego o prompt no formato de sempre.</pre></td>
<td valign="top"><pre>Antes de escrever o prompt, preciso saber quais são &quot;esses problemas&quot;. Esta conversa começou agora, então não tenho nenhuma lista ou revisão anterior. O working tree está limpo e o repositório só tem `README.md`, `prompt/SKILL.md` e `prompt/tipos.md`.

1. **Quais são os problemas?**
   - a) Cole aqui a lista, o erro ou a revisão que você tem em mente.
   - b) Diferenças entre o `README.md` e a skill. Um exemplo que achei: o README lista 8 tipos e não tem &quot;Agêntica longa&quot;.
   - c) Problemas na própria skill (`prompt/SKILL.md` / `prompt/tipos.md`), como regras que se contradizem ou ficam ambíguas.
   - d) Outra coisa (descreva).

2. **O que o prompt deve pedir?**
   - a) Corrigir direto nos arquivos.
   - b) Primeiro levantar e listar os problemas, depois corrigir.
   - c) Só listar, sem alterar nada.

3. **Qual arquivo vale quando o README e a skill discordam?**
   - a) `prompt/SKILL.md` / `tipos.md`, e o README se ajusta.
   - b) O README, e a skill se ajusta.
   - c) Decidir caso a caso e me perguntar.</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 1 leituras: Bash {"command": "ls -la && cat CLAUDE.md README* 2>/dev/null \| head -80", "description": "List | **passa** 2 leituras: Bash {"command": "git ls-files \| head -50 && git log --oneline -3", "description": "List tracke \| Read {"file_path": "skillproj/README.md"} |
| C3 | **n/a** sem prompt | **n/a** sem prompt |
| C6 | **n/a** sem prompt | **n/a** sem prompt |
| C7 | **n/a** sem prompt | **n/a** sem prompt |
| C4 | **n/a** Antes de montar o prompt, preciso saber uma coisa | **n/a** Antes de escrever o prompt, preciso saber quais são |
| C5 | **n/a** Antes de montar o prompt, preciso saber uma coisa | **n/a** Antes de escrever o prompt, preciso saber quais são |
| a | **falha** ausente: 1. **Quais são os problemas?** Cole a lista, a mensagem de erro ou o resultado da revisão. | **passa** 1. **Quais são os problemas?** |
| b | **passa** não encontrei nesta conversa nenhuma lista de problemas para "esses problemas" se referir | **passa** Esta conversa começou agora, então não tenho nenhuma lista ou revisão anterior. |

### #3 · `ta dando LazyInitializationException qdo chamo /pedidos/{id}, arruma ai`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>**Tipo:** Corrigir bug · **Modo sugerido:** plan mode · **Raciocínio:** normal

```text
Objetivo: corrigir a LazyInitializationException que o GET /pedidos/{id} lança hoje, para que o endpoint devolva o pedido com seus itens. A correção deve seguir a arquitetura do projeto e não deve só esconder o sintoma.

Contexto:
- Projeto &quot;loja&quot;: Spring Boot 3.3.5, Java 21, Spring Data JPA, PostgreSQL 16 (ddl-auto=update, ainda sem migrations). Build e testes: `./mvnw test`.
- Camadas: controller -&gt; service -&gt; repository. Pelo CLAUDE.md, controllers recebem e devolvem DTOs (records em `dto/`), mas a pasta `dto/` ainda não existe.
- `src/main/resources/application.properties` tem `spring.jpa.open-in-view=false`.
- `controller/PedidoController.java:7`: `buscar` devolve a entidade `Pedido` direto.
- `service/PedidoService.java:7`: `buscar` faz `repo.findById(id).orElseThrow()`, sem `@Transactional`.
- `model/Pedido.java:6-7`: `@ManyToOne Cliente cliente` e `@OneToMany(mappedBy = &quot;pedido&quot;) List&lt;ItemPedido&gt; itens` (LAZY).
- Hipótese: o Jackson serializa `itens` depois que a sessão do Hibernate já fechou. Confirme ou descarte isso antes de corrigir.
- Os testes usam JUnit 4 com Mockito (`src/test/java/com/exemplo/loja/service/PedidoServiceTest.java`). Com mocks não há lazy loading real, então esses testes não reproduzem o bug.

Tarefa:
1. Confirme a causa raiz com evidência: stack trace, arquivo:linha ou um teste que falhe.
2. Corrija seguindo a convenção do projeto:
   - crie records em `src/main/java/com/exemplo/loja/dto/` (ex.: `PedidoDTO`, `ItemPedidoDTO`);
   - faça a conversão entidade -&gt; DTO no service, dentro da transação ou com os itens já carregados (`@Transactional(readOnly = true)`, `@EntityGraph` ou `JOIN FETCH` no `PedidoRepository`; escolha um e justifique em uma frase);
   - faça o controller devolver o DTO.
   Antes de definir os campos, leia `ItemPedido.java` e `Cliente.java`. Mantenha no JSON os campos que o endpoint já devolveria. Assim os clientes da API não quebram e a referência de volta `ItemPedido.pedido` não gera recursão.
3. Escreva um teste que falhe antes da correção e passe depois. Ele precisa de JPA real (`@DataJpaTest` ou `@SpringBootTest`), porque mocks não reproduzem lazy loading. O projeto não tem banco de teste. Proponha a opção (Testcontainers com PostgreSQL 16 ou H2) e pergunte antes de adicionar a dependência ao `pom.xml`.
4. Rode `./mvnw test` e ajuste os testes existentes que quebrarem com a mudança de tipo de retorno.

Restrições:
- Não ligue `spring.jpa.open-in-view` e não mude os relacionamentos para `FetchType.EAGER`. Os dois escondem o problema e criam consultas desnecessárias em todos os outros usos de `Pedido`.
- Não use `@JsonIgnore` nem `Hibernate.initialize` no controller como solução. Isso vai contra a regra de devolver DTOs.
- Não altere `AuthController`, a configuração de segurança nem o schema do banco. Estão fora do escopo, e o ddl-auto=update aplicaria mudanças de entidade direto no banco.
- Se encontrar o mesmo problema em outros endpoints, só aponte. Não corrija agora.

Pronto quando:
- O teste novo falha sem a correção (com LazyInitializationException) e passa com ela.
- `./mvnw test` passa por completo.
- O GET /pedidos/{id} devolve um DTO com os itens, e nenhum controller de pedido devolve entidade JPA.
- O id inexistente continua com o mesmo comportamento de hoje (`NoSuchElementException`), coberto por `pedidoInexistente`.

Formato da resposta:
1. Causa raiz, com evidência (arquivo:linha e trecho do stack trace ou a falha do teste)
2. Correção aplicada: arquivos criados ou alterados, uma linha por arquivo, e a estratégia de fetch escolhida com o motivo
3. Teste que reproduz o bug: nome, como falhava antes e a saída de `./mvnw test` depois
4. Riscos e outros lugares com o mesmo problema (ex.: `findByClienteId`, campo `cliente`), e se o JSON mudou em relação ao que era esperado
```

**Suposições:**
- A causa é a serialização da entidade fora da transação. O código aponta para isso (o próprio comentário em `PedidoController.java:7` diz &quot;itens LAZY&quot;), mas o stack trace não foi informado.
- A correção deve seguir a regra de DTOs do CLAUDE.md, mesmo com a pasta `dto/` ainda inexistente.
- Adicionar um banco de teste (Testcontainers ou H2) depende da sua aprovação, por isso o prompt manda perguntar antes.

**O que melhorou:**
- O prompt cita a causa provável com os arquivos e linhas reais (`open-in-view=false`, entidade devolvida no controller, `itens` LAZY). O modelo começa pela investigação certa.
- Ele bloqueia os &quot;atalhos&quot; comuns (EAGER, open-in-view, `@JsonIgnore`), que fariam o erro sumir sem respeitar a arquitetura.
- Ele exige um teste com JPA real que falhe antes e passe depois. Os testes atuais com Mockito nunca pegariam esse bug.

Quer que eu execute este prompt agora?</pre></td>
<td valign="top"><pre>**Tipo:** Corrigir bug · **Modo:** plan mode · **Esforço:** padrão

```text
Corrija a LazyInitializationException que ocorre ao chamar GET /pedidos/{id}, para que o endpoint devolva o pedido com seus itens sem erro.

## Contexto
Projeto `loja`: Spring Boot 3.3.5, Java 21, Spring Data JPA, Spring Security, PostgreSQL. Hoje `PedidoController.buscar` devolve a entidade `Pedido` direto (o comentário na linha 7 diz &quot;itens LAZY&quot;). A pasta `dto/` citada no CLAUDE.md ainda não existe. Os testes usam JUnit 4.13.2 com junit-vintage-engine.

## Insumos
Arquivos a ler: src/main/java/com/exemplo/loja/controller/PedidoController.java, service/PedidoService.java, model/Pedido.java, model/ItemPedido.java, model/Cliente.java, repository/PedidoRepository.java, src/main/resources/application.properties, src/test/java/com/exemplo/loja/service/PedidoServiceTest.java.
&lt;erro&gt;LazyInitializationException ao chamar /pedidos/{id}&lt;/erro&gt; (o usuário não colou o stack trace)

## Tarefa e escopo
1. Reproduza o erro com um teste e identifique a causa raiz, com evidência, antes de mexer no código.
2. Aplique a correção mínima, seguindo as camadas controller -&gt; service -&gt; repository e as convenções do CLAUDE.md.
3. Procure outros pontos com o mesmo padrão e liste-os sem corrigir.
Fora do escopo: outros endpoints e o AuthController, porque o pedido é só sobre /pedidos/{id}.

## Restrições
- Não altere testes existentes nem fixe valores para o teste passar, porque o teste precisa provar a correção.
- Escreva o teste novo no mesmo estilo do PedidoServiceTest, porque misturar estilos de JUnit no projeto confunde quem mantém.

## Pronto quando
- O teste novo falha antes da correção e passa depois.
- `./mvnw test` passa por completo.

## Autonomia
Pode fazer sem perguntar: criar e editar classes em src/main e src/test do fluxo de pedidos, e rodar `./mvnw test`.
Pergunte antes de: mudar campos ou formato do JSON devolvido, alterar configurações globais de JPA/Hibernate em application.properties, adicionar dependência no pom.xml.
Suposições: o erro acontece ao buscar um pedido que tem itens; não há stack trace, então reproduza pelo teste. Diga se alguma estiver errada. Antes de assumir algo fora desta lista, investigue no código.

## Formato da resposta
1. Causa raiz em 1–2 frases, com evidência (arquivo:linha, log ou saída).
2. Correção mínima aplicada.
3. Teste que reproduz: falhava antes, passa depois (comando e resultado).
4. Efeitos colaterais ou outros pontos com o mesmo padrão (até 5).
```

**O que mudou:**
- Acrescentei o que as leituras mostraram: versões reais, o controller que devolve a entidade direto e a pasta `dto/`, que ainda não existe.
- Pedi para reproduzir o erro com um teste e achar a causa antes de corrigir, porque você não colou o stack trace.
- Deixei explícito que mudar o JSON de resposta, mudar a configuração do JPA ou adicionar dependência exige perguntar antes.

Quer que eu execute este prompt agora?</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 2 leituras: Bash {"command": "find . -path ./.git -prune -o -type f -print \| grep -v target \| head -60; cat \| Bash {"command": "cd spring/src && grep -nE \"@(GetMapping\|Transactional\|OneToMany\|ManyToOne\|Ma | **passa** 3 leituras: Bash {"command": "git ls-files && grep -rn \"pedidos\" src --include=*.java \| head -20", "descr \| Read {"file_path": "spring/pom.xml"} \| Read {"file_path": "spring/src/main/java/com/exemplo/loja/controller/Pe |
| C3 | **passa** | **passa** |
| C6 | **passa** 34 linhas com texto, teto 35 | **passa** 19 linhas com texto, teto 35 |
| C7 | **n/a** 'Corrigir bug' | **passa** 'Corrigir bug' |
| a (tipo) | **passa** 'Corrigir bug', esperado ['Corrigir bug'] | **passa** 'Corrigir bug', esperado ['Corrigir bug'] |
| C4 | **passa** Quer que eu execute este prompt agora? | **passa** Quer que eu execute este prompt agora? |
| C5 | **passa** Objetivo: corrigir a LazyInitializationException que o GET /pedidos/{id} lança hoje | **passa** Corrija a LazyInitializationException que ocorre ao chamar GET /pedidos/{id} |
| b | **passa** Objetivo: corrigir a LazyInitializationException que o GET /pedidos/{id} lança hoje | **passa** <erro>LazyInitializationException ao chamar /pedidos/{id}</erro> |
| c | **passa** 1. Confirme a causa raiz com evidência: stack trace, arquivo:linha ou um teste que falhe. | **passa** 1. Reproduza o erro com um teste e identifique a causa raiz, com evidência, antes de mexer no código. |
| d | **passa** 3. Escreva um teste que falhe antes da correção e passe depois. | **passa** - O teste novo falha antes da correção e passa depois. |
| e | **falha** ausente: 4. Rode `./mvnw test` e ajuste os testes existentes que quebrarem com a mudança de tipo de retorno. | **passa** Não altere testes existentes nem fixe valores para o teste passar |
| f | **passa** Não ligue `spring.jpa.open-in-view` e não mude os relacionamentos para `FetchType.EAGER`. | **passa** 2. Aplique a correção mínima, seguindo as camadas controller -> service -> repository |

### #4 · `porque ele da problema com o ponytail?`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>Antes de escrever o prompt, preciso entender três coisas. Este projeto (a própria skill `/prompt`) não menciona &quot;ponytail&quot; em nenhum arquivo, então não consigo descobrir sozinho:

1. **Quem é &quot;ele&quot;?** Uma ferramenta, biblioteca, modelo de IA ou programa específico (por exemplo, um gerador de imagens, um engine 3D ou um pacote de código)? Diga o nome e a versão, se souber.
2. **O que é &quot;ponytail&quot; nesse caso?** O penteado (rabo de cavalo) numa imagem, avatar ou modelo 3D, ou o nome de uma biblioteca, comando ou arquivo?
3. **Qual é o problema exato?** Uma mensagem de erro (cole o texto), um resultado visual errado (o que aparece e o que você esperava) ou um travamento? E o que você estava fazendo quando aconteceu?</pre></td>
<td valign="top"><pre>O pedido não diz quem é &quot;ele&quot; nem qual é o problema, e o projeto não ajuda: nenhum arquivo (`README.md`, `prompt/SKILL.md`, `prompt/tipos.md`) cita &quot;ponytail&quot;. Preciso de três respostas para escrever o prompt:

1. **Quem é &quot;ele&quot;?**
   - a) A skill `/prompt` deste projeto
   - b) O Claude ou o Claude Code em si
   - c) Uma biblioteca, ferramenta ou app (diga qual)
   - d) Outro

2. **O que é &quot;ponytail&quot; no seu caso?**
   - a) Uma palavra no pedido, como &quot;rabo de cavalo&quot; em descrição de personagem ou imagem
   - b) Um pacote, biblioteca ou ferramenta chamada `ponytail`
   - c) Um arquivo, branch ou identificador do seu código
   - d) Outro

3. **Qual é o problema que aparece?**
   - a) Recusa ou bloqueio (cole a mensagem)
   - b) Erro ou stack trace (cole o texto)
   - c) O resultado sai errado ou diferente do esperado (descreva o que esperava e o que veio)
   - d) Outro

Se puder, cole também o comando ou a entrada que você usou e a saída que recebeu.</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 1 leituras: Bash {"command": "ls -la && cat CLAUDE.md README* 2>/dev/null \| head -80; grep -ril ponytail .  | **passa** 2 leituras: Bash {"command": "git ls-files \| head -100 && echo --- && grep -rni \"ponytail\" . --exclude-di \| Read {"file_path": "skillproj/README.md"} |
| C3 | **n/a** sem prompt | **n/a** sem prompt |
| C6 | **n/a** sem prompt | **n/a** sem prompt |
| C7 | **n/a** sem prompt | **n/a** sem prompt |
| C4 | **n/a** Antes de escrever o prompt, preciso entender três coisas. | **n/a** Preciso de três respostas para escrever o prompt: |
| C5 | **n/a** Antes de escrever o prompt, preciso entender três coisas. | **n/a** Preciso de três respostas para escrever o prompt: |
| a | **passa** 2. **O que é "ponytail" nesse caso?** O penteado (rabo de cavalo) numa imagem, avatar ou modelo 3D, ou o nome de uma biblioteca, comando ou arquivo? | **passa** a) A skill `/prompt` deste projeto |
| b | **passa** não consigo descobrir sozinho | **passa** O pedido não diz quem é "ele" nem qual é o problema |

### #5 · `faz um prompt pra analisar se há erros no projeto de forma profunda ou se posso deixar assim`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>**Tipo:** Revisar ou auditar · **Modo sugerido:** normal · **Raciocínio:** ultrathink

```text
ultrathink

## Objetivo
Faça uma auditoria profunda do projeto `fretes` e diga se ele pode ficar como está ou se precisa de correções. A resposta vai decidir se eu mexo no código agora ou deixo assim. Por isso preciso de um veredito claro, com evidências.

## Contexto
- Pacote Python `fretes` v0.3.0 (`pyproject.toml`), `requires-python &gt;= 3.12`, dependência `requests&gt;=2.32`, testes com `pytest&gt;=8` (`testpaths = [&quot;tests&quot;]`).
- Arquivos do projeto (são todos):
  - `src/fretes/frete.py` (12 linhas)
  - `src/fretes/relatorio.py` (11 linhas)
  - `tests/test_frete.py` (4 linhas)
  - `logs/app.log` (480 linhas de log do endpoint `GET /fretes/calcular`, com `status` e `dur_ms`)
- O projeto não tem README nem CLAUDE.md.

## Tarefa
1. Leia por inteiro todos os arquivos de `src/` e `tests/`. Eles são pequenos, então analise linha por linha.
2. Procure erros de verdade: bugs de lógica, casos de borda (valores zero, negativos, `None`, tipos errados, divisão por zero), arredondamento de valores monetários (float em vez de `Decimal`), exceções não tratadas, uso de `requests` sem timeout ou sem tratamento de erro, imports quebrados e código que não roda em Python 3.12+.
3. Rode `pytest -q` e reporte a saída. Avalie se os testes cobrem o comportamento de `frete.py` e `relatorio.py` ou se passam sem testar nada relevante.
4. Analise `logs/app.log` com comandos, sem estimar no olho: contagem por nível (INFO/WARNING/ERROR), status diferentes de 200, e min/média/p95/máx de `dur_ms`. Cruze o que encontrar com o código.
5. Verifique a configuração: `pyproject.toml` está completo o bastante para instalar e testar (`pip install -e .[dev]`)? A estrutura `src/` com o pacote está correta?

## Restrições
- Não altere, crie nem apague arquivos. Esta é só uma análise, e eu decido o que corrigir depois de ler o relatório.
- Sem push, commit ou instalação global de pacotes. Se precisar instalar dependências para rodar os testes, use um venv temporário e diga isso.
- Reporte todos os achados, inclusive os de baixa severidade, cada um com sua classificação. Não filtre só os graves, porque eu quero ver o quadro completo para decidir.
- Severidades: CRÍTICO (resultado errado ou crash em uso normal), ALTO (falha em caso de borda plausível), MÉDIO (risco ou fragilidade, como teste fraco ou falta de timeout), BAIXO (estilo, legibilidade, melhoria opcional).

## Pronto quando
- Todos os arquivos de `src/` e `tests/` foram lidos e cada achado aponta `arquivo:linha`.
- A saída real do `pytest` aparece no relatório.
- As estatísticas do log vêm de comandos executados, e os comandos são mostrados.
- Cada achado está marcado como CONFIRMADO (reproduzido, com comando ou trecho) ou SUSPEITA (não deu para provar). &quot;Não consegui confirmar&quot; é uma resposta válida.
- Existe um veredito final.

## Formato da resposta
1. **Veredito:** PODE DEIXAR ASSIM | DEIXAR COM RESSALVAS | PRECISA CORRIGIR, com uma frase de motivo.
2. **Tabela de achados:** severidade | arquivo:linha | problema | evidência (trecho, comando ou saída) | correção sugerida (1 linha)
3. **Testes:** saída do `pytest` e avaliação da cobertura em 2-3 linhas.
4. **Logs:** números calculados e o que eles indicam.
5. **Suspeitas não confirmadas.**
6. **O que está bom e deve ser mantido** (curto).
```

**Suposições:**
- &quot;Deixar assim&quot; quer dizer &quot;não mexer no código agora&quot;. Não sei se o projeto vai para produção. Se for, um achado MÉDIO pode pesar mais na decisão.
- A análise cobre o projeto inteiro (são só 4 arquivos), não um diff específico.
- O `logs/app.log` faz parte do que deve ser analisado.

**O que melhorou:**
- O pedido vago &quot;analisar se há erros&quot; virou um checklist com os arquivos reais, a stack (Python 3.12, `requests`, `pytest`) e o log do endpoint.
- Agora há uma escala de severidade e a exigência de evidência, com separação entre achado confirmado e suspeita, para não receber suposições como fatos.
- O prompt termina com um veredito objetivo (&quot;pode deixar assim ou não&quot;), que é a pergunta que você fez.

Quer que eu execute este prompt agora?</pre></td>
<td valign="top"><pre>**Tipo:** Revisar ou auditar · **Modo:** normal · **Esforço:** alto. Para executar aqui, rode `/effort xhigh` antes de responder sim.

```text
ultrathink
Audite a fundo o projeto `fretes` e me diga se ele tem erros que precisam de correção ou se posso deixá-lo como está.

## Contexto
O projeto é um pacote Python `fretes` (versão 0.3.0, `requires-python &gt;=3.12`), com dependência `requests&gt;=2.32` e `pytest&gt;=8` como dependência de desenvolvimento. O código está em `src/fretes/` e os testes em `tests/`. Quero uma decisão clara: corrigir agora ou manter como está.

## Insumos
Arquivos a ler:
- `pyproject.toml`
- `src/fretes/frete.py`
- `src/fretes/relatorio.py`
- `tests/test_frete.py`
- `logs/app.log`: procure erros, exceções ou avisos e relacione cada um ao trecho de código que o causou.

## Tarefa e escopo
1. Rode `pytest` (configurado com `testpaths = [&quot;tests&quot;]`) e registre o resultado.
2. Revise todos os arquivos de `src/fretes/` com estes critérios: bugs de lógica e casos de borda (valores zero, negativos, nulos, arredondamento de valores monetários), tratamento de erros e exceções, uso de `requests` (timeout, status HTTP, falhas de rede), tipagem, compatibilidade com Python 3.12, segurança (entradas não validadas, segredos no código ou no log) e configuração do empacotamento em `pyproject.toml`.
3. Avalie a cobertura dos testes: quais comportamentos de `frete.py` e `relatorio.py` ficam sem teste.
Não altere código, testes nem arquivos de configuração, porque o objetivo é decidir antes de mexer. Reporte todos os achados com severidade. Separe o confirmado (com evidência de execução, log ou leitura do código) da suspeita, e investigue antes de afirmar.

## Pronto quando
- `pytest` foi executado e o resultado aparece na resposta.
- Cada achado confirmado tem arquivo:linha e evidência.
- Todas as entradas de erro de `logs/app.log` foram explicadas ou marcadas como não reproduzidas.

## Autonomia
Suposições: o ambiente já tem as dependências de `dev` instaladas (se não tiver, instale com `pip install -e .[dev]` num virtualenv local); &quot;erro&quot; inclui bugs, falhas de teste e riscos de segurança, não apenas estilo. Diga se alguma suposição estiver errada. Antes de assumir algo fora desta lista, investigue no código.

## Formato da resposta
1. Veredito: APROVAR | APROVAR COM RESSALVAS | PEDIR MUDANÇAS, com o motivo em 1 frase (em termos de &quot;posso deixar assim?&quot;).
2. Tabela por severidade (crítico, alto, médio, baixo): severidade | arquivo:linha | problema | evidência | sugestão.
3. Suspeitas não confirmadas (até 5).
4. O que manter (até 3).
```

**O que mudou:**
- &quot;de forma profunda&quot; virou Esforço alto (`ultrathink`) e uma lista explícita de critérios de auditoria.
- Incluí `logs/app.log` e a execução do `pytest` como evidência, porque os dois existem no projeto.
- A pergunta &quot;ou se posso deixar assim&quot; virou um veredito obrigatório no início da resposta.

Quer que eu execute este prompt agora?</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 2 leituras: Bash {"command": "git ls-files \| head -100 && echo \"---\" && cat CLAUDE.md README* 2>/dev/null \| Bash {"command": "cat pyproject.toml && echo \"---\" && wc -l src/fretes/*.py tests/*.py logs/a | **passa** 1 leituras: Read {"file_path": "python/pyproject.toml"} |
| C3 | **falha** caixa alta: CRÍTICO | **passa** |
| C6 | **passa** 29 linhas com texto, teto 45 | **passa** 21 linhas com texto, teto 45 |
| C7 | **n/a** 'Revisar ou auditar' | **passa** 'Revisar ou auditar' |
| a (tipo) | **passa** 'Revisar ou auditar', esperado ['Revisar ou auditar'] | **passa** 'Revisar ou auditar', esperado ['Revisar ou auditar'] |
| esforço | **falha** 1ª linha='ultrathink', '/effort xhigh' na entrega=False | **passa** 1ª linha='ultrathink', '/effort xhigh' na entrega=True |
| C4 | **passa** Quer que eu execute este prompt agora? | **passa** Quer que eu execute este prompt agora? |
| C5 | **falha** ## Objetivo | **passa** Audite a fundo o projeto `fretes` e me diga se ele tem erros que precisam de correção ou se posso deixá-lo como está. |
| c | **passa** 1. **Veredito:** PODE DEIXAR ASSIM \| DEIXAR COM RESSALVAS \| PRECISA CORRIGIR, com uma frase de motivo. | **passa** com o motivo em 1 frase (em termos de "posso deixar assim?") |
| d | **passa** Reporte todos os achados, inclusive os de baixa severidade, cada um com sua classificação. | **passa** Reporte todos os achados com severidade. |
| e | **passa** Não altere, crie nem apague arquivos. | **passa** Não altere código, testes nem arquivos de configuração |
| f | **passa** `src/fretes/frete.py` (12 linhas) | **passa** - `src/fretes/frete.py` |

### #6 · `URGENTE revisa a seguranca do AuthController, so os bugs graves, pensa passo a passo`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>**Tipo:** Revisar ou auditar (segurança) · **Modo sugerido:** normal · **Raciocínio:** ultrathink

```text
ultrathink

Objetivo: auditar a segurança do AuthController antes que ele vá para produção. O resultado precisa permitir decidir agora o que bloqueia o deploy e o que pode esperar.

Contexto:
- Projeto &quot;loja&quot;: Spring Boot 3.3.5, Java 21, spring-boot-starter-security, Spring Data JPA, PostgreSQL 16 (ddl-auto=update, ainda sem migrations).
- Camadas esperadas: controller -&gt; service -&gt; repository. Controllers recebem e devolvem DTOs (records em dto/), mas a pasta dto/ ainda não existe.
- Arquivo principal: src/main/java/com/exemplo/loja/controller/AuthController.java
- Arquivos que ele provavelmente usa: model/Cliente.java, repository/ClienteRepository.java, src/main/resources/application.properties.
- Não há classe de configuração de segurança (SecurityFilterChain) rastreada no git. Verifique o que isso significa para os endpoints de auth.

Tarefa:
1. Leia o AuthController e siga cada fluxo (login, cadastro, token, reset, o que existir) até o repository e a configuração.
2. Procure problemas de segurança, por exemplo: senha em texto puro ou hash fraco, comparação de senha ou token vulnerável a timing attack, SQL/JPQL injection, enumeração de usuários pelas mensagens de erro, entidade JPA exposta direto na resposta (vazando hash de senha) ou aceita direto no request (mass assignment), segredos ou credenciais hardcoded, tokens previsíveis ou sem expiração, falta de rate limit em login, CSRF/CORS mal configurados, endpoints sem autenticação que deveriam ter, dados sensíveis em log.
3. Classifique cada achado como CRÍTICA, ALTA, MÉDIA ou BAIXA, pelo impacto real neste código.

Restrições:
- Não altere nenhum arquivo. É uma revisão, e as correções serão decididas depois.
- Reporte todos os achados, não só os graves. O pedido é urgente, então dê CRÍTICA e ALTA com detalhe completo e liste MÉDIA e BAIXA com uma linha cada.
- Separe o que você confirmou lendo o código do que é suspeita. &quot;Não consegui confirmar&quot; é uma resposta válida.

Pronto quando: todos os métodos públicos do AuthController foram analisados, cada achado tem arquivo:linha e um trecho do código como evidência, e há um veredito.

Formato da resposta:
1. Veredito: APROVAR | APROVAR COM RESSALVAS | PEDIR MUDANÇAS, com uma frase de motivo.
2. Tabela ordenada por severidade: severidade | arquivo:linha | problema | evidência (trecho) | correção sugerida
3. Dúvidas não confirmadas
4. O que está bom e deve ser mantido (curto)
5. Resumo das decisões de análise em 2 ou 3 linhas (o que foi considerado fora do escopo e por quê)
```

**Suposições:**
- O escopo é o AuthController e o que ele chama diretamente, não o projeto inteiro (PedidoController ficou de fora).
- &quot;Bugs graves&quot; quer dizer &quot;priorize os graves&quot;, não &quot;esconda o resto&quot;.

**O que melhorou:**
- Troquei &quot;só os graves&quot; por &quot;reporte tudo com severidade e detalhe só os graves&quot;. Se o filtro for pedido ao pé da letra, o modelo esconde achados que você talvez quisesse ver, e você continua vendo primeiro o que bloqueia o deploy.
- Troquei &quot;pensa passo a passo&quot; por `ultrathink` e pelo rastreio de cada fluxo até o repository, e o prompt pede evidência com arquivo:linha.
- Acrescentei o contexto real do projeto: as versões, os arquivos envolvidos e o fato de não haver SecurityFilterChain nem pasta dto/. Esses dois pontos costumam ser a origem de falhas graves.

Quer que eu execute este prompt agora?</pre></td>
<td valign="top"><pre>**Tipo:** Revisar ou auditar · **Modo:** normal · **Esforço:** alto. Para executar aqui, rode `/effort xhigh` antes de responder sim.

```text
ultrathink
Revise a segurança do login em `AuthController` e aponte os bugs graves, para decidir o que corrigir primeiro.

## Contexto
Projeto `loja`: Spring Boot 3.3.5, Java 21, spring-boot-starter-web, spring-boot-starter-data-jpa e spring-boot-starter-security, PostgreSQL. O controller expõe `POST /auth/login` com `@RequestParam email` e `senha` e devolve um `Map` com `token`. O repositório não tem nenhuma classe de configuração do Spring Security.

## Insumos
Arquivos a ler:
- src/main/java/com/exemplo/loja/controller/AuthController.java (alvo)
- src/main/java/com/exemplo/loja/model/Cliente.java
- src/main/java/com/exemplo/loja/repository/ClienteRepository.java
- src/main/resources/application.properties
- src/main/java/com/exemplo/loja/controller/PedidoController.java (para ver se e como o `token` é consumido)

## Tarefa e escopo
Avalie o fluxo de autenticação de ponta a ponta: como a senha é guardada e comparada, como o token é gerado e validado, o que as respostas de erro revelam, a proteção contra força bruta e enumeração de usuários, a configuração efetiva do Spring Security e a exposição de credenciais em logs ou na URL.
Fora do escopo: estilo, desempenho e a lógica de pedidos, porque o foco é o risco de segurança da autenticação.

## Restrições
- Não altere código nem rode comandos que modifiquem o projeto, porque esta é uma revisão só de leitura.
- Reporte todos os achados com severidade e separe o confirmado da suspeita. Investigue no código antes de afirmar, porque um falso positivo atrasa a correção do que é real.
- Cite arquivo:linha e um cenário concreto de exploração para cada achado crítico ou alto, para que o achado possa ser verificado.

## Pronto quando
- Cada achado crítico e alto tem arquivo:linha, evidência e cenário de ataque.
- Todo trecho do fluxo de login listado em &quot;Tarefa e escopo&quot; foi avaliado, mesmo que sem achado.

## Autonomia
Suposições: &quot;graves&quot; significa severidade crítica ou alta; o app roda com as propriedades de `application.properties` como estão. Diga se alguma estiver errada. Antes de assumir algo fora desta lista, investigue no código.

## Formato da resposta
1. Veredito: APROVAR | APROVAR COM RESSALVAS | PEDIR MUDANÇAS, com o motivo em 1 frase.
2. Tabela só com crítico e alto: severidade | arquivo:linha | problema | evidência | sugestão.
3. Outros achados (médio e baixo): uma linha para cada, nenhum omitido.
4. Suspeitas não confirmadas (até 5).
5. O que manter (até 3).
```

**O que mudou:**
- Troquei &quot;pensa passo a passo&quot; por Esforço alto (`ultrathink`) e tirei o &quot;URGENTE&quot;, porque o pedido não tinha prazo.
- &quot;Só os graves&quot; agora significa crítico e alto em detalhe; médio e baixo ficam com uma linha cada, sem omitir nenhum.
- Incluí os arquivos ligados ao fluxo (model, repository, properties, PedidoController) e o fato de que o repositório não tem configuração de segurança.

Quer que eu execute este prompt agora?</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 1 leituras: Bash {"command": "git ls-files && ls README* 2>/dev/null; grep -n -E \"<(artifactId\|version\|jav | **passa** 2 leituras: Bash {"command": "git ls-files && grep -E \"<(artifactId\|version\|java.version)>\" pom.xml \| hea \| Read {"file_path": "spring/src/main/java/com/exemplo/loja/controller/AuthController.java"} |
| C3 | **passa** | **passa** |
| C6 | **passa** 23 linhas com texto, teto 45 | **passa** 22 linhas com texto, teto 45 |
| C7 | **n/a** 'Revisar ou auditar (segurança)' | **passa** 'Revisar ou auditar' |
| C4 | **passa** Quer que eu execute este prompt agora? | **passa** Quer que eu execute este prompt agora? |
| C5 | **passa** Objetivo: auditar a segurança do AuthController antes que ele vá para produção. | **passa** Revise a segurança do login em `AuthController` e aponte os bugs graves, para decidir o que corrigir primeiro. |
| a | **passa** Objetivo: auditar a segurança do AuthController antes que ele vá para produção. | **passa** Revise a segurança do login em `AuthController` |
| b | **falha** O pedido é urgente, então dê CRÍTICA e ALTA com detalhe completo e liste MÉDIA e BAIXA com uma linha cada. | **passa** Revise a segurança do login em `AuthController` e aponte os bugs graves, para decidir o que corrigir primeiro. |
| c | **passa** Reporte todos os achados, não só os graves. | **passa** 3. Outros achados (médio e baixo): uma linha para cada, nenhum omitido. |
| d | **passa** Não altere nenhum arquivo. É uma revisão | **passa** Não altere código nem rode comandos que modifiquem o projeto |
| e | **passa** Troquei "pensa passo a passo" por `ultrathink` e pelo rastreio de cada fluxo até o repository | **passa** Troquei "pensa passo a passo" por Esforço alto (`ultrathink`) e tirei o "URGENTE" |

### #7 · `me diz um nome bom pro projeto no github e qual licença usar`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>**Tipo:** Planejar ou decidir · **Modo sugerido:** normal · **Raciocínio:** normal

```text
Objetivo: escolha um nome para o repositório no GitHub e a licença deste projeto. Vou publicar o projeto agora, e o nome e a licença precisam deixar claro o que ele faz e permitir que outras pessoas instalem e adaptem a skill.

Contexto:
- Projeto: uma skill do Claude Code chamada `/prompt`. Ela transforma um pedido rápido e informal em um prompt estruturado, seguindo as boas práticas da Anthropic (Objetivo, Contexto, Tarefa, Restrições, Pronto quando, Formato da resposta). O formato da resposta muda conforme o tipo de tarefa, e são 8 tipos.
- Arquivos: `README.md`, `prompt/SKILL.md` e `prompt/tipos.md`. Tudo é Markdown, sem código executável. A instalação é `cp -r prompt ~/.claude/skills/`.
- O conteúdo está em português do Brasil, então o público principal fala português.
- O repositório ainda não tem LICENSE nem nome público definido.

Tarefa:
1. Proponha de 5 a 8 nomes de repositório. Cada nome deve estar em kebab-case, ser curto (de preferência até 20 caracteres), dizer que é uma skill de Claude Code e funcionar para quem fala português e para quem fala inglês. Depois escolha um e explique a escolha.
2. Para cada nome, verifique com busca se já existe um repositório ou projeto conhecido com o mesmo nome ou um nome muito parecido no GitHub. Se não conseguir verificar, escreva &quot;não verificado&quot;.
3. Compare as licenças MIT, Apache-2.0, CC BY 4.0 e CC0 para este caso. Leve em conta que o projeto é texto e instruções em Markdown, não código. Os critérios são liberdade de reuso e adaptação, exigência de atribuição, simplicidade para o usuário e adequação a conteúdo não-código. Depois recomende uma.
4. Mostre o conteúdo do arquivo LICENSE da licença recomendada, com o ano 2026 e um placeholder para o nome do titular.

Restrições:
- Não crie o repositório, não renomeie nada, não crie o arquivo LICENSE e não faça commit nem push. Essas ações são públicas ou difíceis de desfazer, então quero decidir antes.
- Mantenha a pasta `prompt/` com esse nome, porque ela define o comando `/prompt` e as instruções de instalação. O nome do repositório pode ser diferente dela.
- Se achar que outra licença fora da lista é melhor, diga isso em uma frase e explique por quê.

Pronto quando:
- Há um nome escolhido com justificativa e o status de disponibilidade de cada nome proposto.
- Há uma licença recomendada com o motivo principal e o texto do LICENSE pronto para colar.

Formato da resposta:
1. Recomendação: nome + licença, com o motivo principal de cada um (2-3 linhas)
2. Tabela de nomes: nome | o que comunica | conflito encontrado (link ou &quot;nenhum&quot; ou &quot;não verificado&quot;)
3. Tabela de licenças pelos critérios, com 1 frase de trade-off por licença
4. Texto do LICENSE
5. Próximos passos: comandos para criar o repositório e adicionar a licença, sem executar
```

**Suposições:**
- Você quer que qualquer pessoa possa usar e adaptar a skill livremente (licença permissiva, não copyleft).
- O nome deve servir para quem fala português e para quem fala inglês, mesmo com o conteúdo em português.
- O repositório será público e no seu usuário pessoal.

**O que melhorou:**
- Diz o que é o projeto (skill em Markdown, sem código). Isso pesa na escolha entre licenças de software (MIT) e de conteúdo (Creative Commons).
- Pede para verificar se cada nome já existe e para escolher um, em vez de só listar ideias.
- Proíbe criar o repositório ou fazer commit antes de você decidir, e protege a pasta `prompt/`, que define o comando.

Quer que eu execute este prompt agora?</pre></td>
<td valign="top"><pre>**Tipo:** Pesquisar ou comparar · **Modo:** normal · **Esforço:** padrão

```text
Sugira um nome para publicar este projeto no GitHub e recomende uma licença, para que eu crie o repositório público já com nome e LICENSE definidos.

## Contexto
O projeto é uma skill do Claude Code chamada `/prompt`. Ela transforma um pedido rápido em um prompt estruturado, seguindo as boas práticas da Anthropic. Tudo está em português, e o projeto tem só Markdown, sem código executável: `README.md`, `prompt/SKILL.md` e `prompt/tipos.md`. Hoje não existe arquivo LICENSE, e o git tem um único commit (&quot;estado inicial&quot;).

## Insumos
Arquivos a ler: `README.md`, `prompt/SKILL.md` (frontmatter `name`/`description`).

## Tarefa e escopo
1. Nome: proponha de 3 a 5 opções curtas, fáceis de lembrar e de digitar na URL (`github.com/&lt;usuario&gt;/&lt;nome&gt;`). Compare as opções por clareza (diz o que faz?), unicidade (pesquise no GitHub se já existem repositórios ou skills com o mesmo nome) e idioma (português, inglês ou neutro, pensando em quem vai encontrar o projeto).
2. Licença: compare as licenças que fazem sentido para um projeto pequeno de texto/prompts que outras pessoas vão copiar para `~/.claude/skills/` e adaptar. Os critérios são: permissividade, exigência de atribuição, o que muda para quem modifica e redistribui, e se a licença serve bem para conteúdo que não é código.
3. Recomende um nome e uma licença, cada um com o motivo.
Fora do escopo: criar o repositório, o LICENSE ou alterar arquivos, porque quero decidir antes.

## Restrições
- Não altere nenhum arquivo, porque o objetivo é só apoiar a decisão.
- Use fontes primárias para as licenças (choosealicense.com, opensource.org, creativecommons.org), com data, porque os detalhes jurídicos precisam ser verificáveis.
- Separe fato (o que a licença diz, se o nome está livre) de opinião (o que soa melhor).

## Pronto quando
- Cada nome sugerido tem o resultado da busca de disponibilidade no GitHub.
- Há uma recomendação única de nome e uma de licença.

## Autonomia
Suposições: o objetivo é que outras pessoas usem e adaptem a skill livremente, com crédito opcional ou mínimo; não há empresa nem restrição comercial envolvida; o nome do usuário no GitHub não importa para a escolha (diga se alguma estiver errada).

## Formato da resposta
1. Resposta direta em 1–2 frases: nome e licença recomendados.
2. Tabela de nomes: nome | clareza | disponibilidade no GitHub | observação.
3. Tabela de licenças: licença | permissividade | atribuição | adequação a texto | observação.
4. Recomendação com confiança (alta, média ou baixa) e o porquê.
5. Fontes: link e data.
```

**O que mudou:**
- Juntei os dois pedidos (nome e licença) num único formato de comparação, com critérios explícitos para cada um. Também caberia em &quot;Planejar ou decidir&quot;, mas a comparação de opções conhecidas é o núcleo do pedido.
- Coloquei no Contexto o que o projeto tem de fato: skill em português, só Markdown, sem LICENSE.
- Assumi que você quer uso livre, sem restrição comercial. Se não for isso, me avise, porque muda a recomendação de licença.

Quer que eu execute este prompt agora?</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 2 leituras: Bash {"command": "ls -la && cat README* CLAUDE.md 2>/dev/null \| head -80", "description": "List \| Bash {"command": "find . -path ./.git -prune -o -type f -print \| head -50 && cat package.json p | **passa** 3 leituras: Bash {"command": "git ls-files \| head -50 && ls -a", "description": "List project files"} \| Read {"file_path": "skillproj/README.md"} \| Bash {"command": "head -20 prompt/SKILL.md && wc -l prompt/*.md", "descr |
| C3 | **passa** | **passa** |
| C6 | **passa** 24 linhas com texto, teto 35 | **passa** 18 linhas com texto, teto 35 |
| C7 | **n/a** 'Planejar ou decidir' | **passa** 'Pesquisar ou comparar' |
| C4 | **passa** Quer que eu execute este prompt agora? | **passa** Quer que eu execute este prompt agora? |
| C5 | **passa** Objetivo: escolha um nome para o repositório no GitHub e a licença deste projeto. | **passa** Sugira um nome para publicar este projeto no GitHub e recomende uma licença |
| b | **passa** 3. Compare as licenças MIT, Apache-2.0, CC BY 4.0 e CC0 para este caso. | **passa** Os critérios são: permissividade, exigência de atribuição |
| c | **falha** ausente: Se não conseguir verificar, escreva "não verificado". | **passa** Use fontes primárias para as licenças (choosealicense.com, opensource.org, creativecommons.org), com data |
| d | **falha** ausente: 1. Recomendação: nome + licença, com o motivo principal de cada um (2-3 linhas) | **passa** 4. Recomendação com confiança (alta, média ou baixa) e o porquê. |
| e | **passa** Projeto: uma skill do Claude Code chamada `/prompt`. | **passa** O projeto é uma skill do Claude Code chamada `/prompt`. |

### #8 · `me explica @Transactional propagation q nao entendo nada`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>**Tipo:** Explicar ou ensinar · **Modo sugerido:** normal · **Raciocínio:** normal

```text
Objetivo: me explique como funciona a propagação de transações do @Transactional no Spring. Quero entender o suficiente para decidir sozinho qual propagation usar ao escrever services neste projeto, e para perceber quando uma transação não está se comportando como eu esperava.

Contexto:
- Sou iniciante no assunto: sei mais ou menos o que é uma transação de banco (commit/rollback), mas não entendo o que acontece quando um método @Transactional chama outro.
- Projeto &quot;loja&quot;: Spring Boot 3.3.5, Java 21, Spring Data JPA, PostgreSQL 16. As camadas são controller -&gt; service -&gt; repository.
- Arquivos reais: src/main/java/com/exemplo/loja/service/PedidoService.java (hoje ainda não usa @Transactional), as entidades Pedido, ItemPedido e Cliente em model/, e PedidoRepository e ClienteRepository em repository/.

Tarefa:
1. Explique o modelo mental antes de falar das opções: o que é a &quot;transação corrente&quot;, como o Spring a associa à thread e que papel o proxy tem nisso.
2. Explique em detalhe REQUIRED (o padrão), REQUIRES_NEW e NESTED, porque são os que aparecem na prática. Para cada um, diga o que acontece no commit e no rollback quando um método chama outro.
3. Cubra SUPPORTS, NOT_SUPPORTED, MANDATORY e NEVER em uma linha cada.
4. Use exemplos do domínio da loja. Por exemplo, um PedidoService.criarPedido que salva o pedido e chama um serviço de auditoria ou de estoque, mostrando o que acontece com cada propagation quando o método interno lança exceção.
5. Explique as armadilhas mais comuns: auto-invocação (this.metodo() ignora o proxy), métodos não públicos, rollback que por padrão só acontece com RuntimeException, a UnexpectedRollbackException quando o método interno marca rollback-only dentro de REQUIRED, e NESTED, que depende de savepoint (diga se funciona com JPA/Hibernate + PostgreSQL).

Restrições:
- Não altere nenhum arquivo do projeto, porque o objetivo é eu aprender. O código vai só na resposta.
- Prefira frases curtas e exemplos a definições formais. Use uma tabela ou um diagrama em texto onde isso deixar o fluxo mais claro.
- Quando um comportamento depender da versão ou do provedor (Hibernate, driver do Postgres), diga isso e indique a fonte (Javadoc de org.springframework.transaction.annotation.Propagation ou a documentação de referência do Spring Framework 6.1). Se não tiver certeza, diga que não tem.

Pronto quando:
- Eu consigo responder, olhando só para a explicação: &quot;se o método B, chamado por A, lança RuntimeException, o que é salvo no banco?&quot; para REQUIRED, REQUIRES_NEW e NESTED.
- O caso de auto-invocação aparece com um exemplo de código e a forma de corrigir.

Formato da resposta:
1. Explicação curta: o essencial em um parágrafo
2. Exemplo prático em Java com as classes da loja, com uma tabela &quot;propagation | o que acontece se B falhar | o que fica salvo&quot;
3. Erros comuns e confusões frequentes
4. Um exercício curto (um cenário em que eu prevejo o resultado), com a resposta no final
```

**Suposições:**
- Você é iniciante no tema (&quot;não entendo nada&quot;) e quer entender o conceito, não alterar código agora.
- Os exemplos usam o domínio do projeto (Pedido, Cliente) para ficarem mais concretos.

**O que melhorou:**
- Diz o seu nível e a stack real (Boot 3.3.5, JPA, Postgres), para a explicação ter o nível certo e exemplos que fazem sentido aqui.
- Concentra a explicação nas 3 propagations que importam e nas armadilhas que mais causam bugs, em vez de só listar as 7 opções.
- Tem um critério para saber se a explicação funcionou (prever o que fica salvo no banco) e um exercício para fixar.

Quer que eu execute este prompt agora?</pre></td>
<td valign="top"><pre>**Tipo:** Explicar ou ensinar · **Modo:** normal · **Esforço:** padrão

```text
Explique como funciona a propagação de transações no `@Transactional` do Spring, para que eu entenda o que acontece quando um método transacional chama outro e saiba qual opção escolher no meu projeto.

## Contexto
Sou iniciante no assunto: uso Spring Boot, mas não entendo nada de propagation. O projeto `loja` usa Spring Boot 3.3.5, Java 21, Spring Data JPA e PostgreSQL 16. Hoje nenhuma classe de `src/` usa `@Transactional`.

## Insumos
Arquivos a ler: `src/main/java/com/exemplo/loja/service/PedidoService.java`, `src/main/java/com/exemplo/loja/repository/PedidoRepository.java`, `src/main/java/com/exemplo/loja/model/Pedido.java`.

## Tarefa e escopo
Explique do básico ao avançado: o que é uma transação no Spring, o que &quot;propagação&quot; significa e os tipos principais, com foco nos mais usados no dia a dia. Use linguagem simples e defina cada termo técnico na primeira vez que ele aparecer. Monte o exemplo em cima de `PedidoService`/`Pedido`, num cenário plausível para uma loja. Fora do escopo: alterar arquivos do projeto, porque o objetivo é só entender o conceito. Isolation e configuração de banco também ficam de fora, para não misturar com propagação.

## Autonomia
Suposições: o objetivo é entender o conceito para uso geral, e não para resolver um bug específico; o exemplo pode ser um trecho de código na resposta, sem ser gravado no projeto (diga se alguma estiver errada).

## Formato da resposta
1. Resumo em 2–3 frases.
2. Explicação progressiva (até ~300 palavras).
3. Exemplo mínimo executável em Spring Boot 3 / Java 21, usando `PedidoService`.
4. Armadilhas comuns (3–5).
```

**O que mudou:**
- Juntei ao pedido o contexto real do projeto (Spring Boot 3.3.5, JPA, `PedidoService` ainda sem `@Transactional`), para o exemplo usar o seu código.
- Descrevi o seu nível (&quot;não entendo nada&quot;) como público iniciante e pedi linguagem simples, com os termos definidos.
- Deixei explícito o que fica de fora (alterar arquivos, isolation) e registrei como suposição que o objetivo é entender o conceito, não corrigir um bug.

Quer que eu execute este prompt agora?</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 2 leituras: Bash {"command": "git ls-files \| head -50 && grep -rn \"Transactional\\\|<version>\\\|spring-boot \| Bash {"command": "grep -rn \"Transactional\\\|<version>\\\|<java.version>\\\|public .*(\" pom.xml  | **passa** 3 leituras: Bash {"command": "git ls-files \| head -50 && grep -rn \"@Transactional\" src \| head -20", "desc \| Read {"file_path": "spring/pom.xml"} \| Read {"file_path": "spring/src/main/java/com/exemplo/loja/service/Pedid |
| C3 | **passa** | **passa** |
| C6 | **passa** 23 linhas com texto, teto 25 | **passa** 9 linhas com texto, teto 25 |
| C7 | **n/a** 'Explicar ou ensinar' | **passa** 'Explicar ou ensinar' |
| a (tipo) | **passa** 'Explicar ou ensinar', esperado ['Explicar ou ensinar'] | **passa** 'Explicar ou ensinar', esperado ['Explicar ou ensinar'] |
| C4 | **passa** Quer que eu execute este prompt agora? | **passa** Quer que eu execute este prompt agora? |
| C5 | **passa** Objetivo: me explique como funciona a propagação de transações do @Transactional no Spring. | **passa** Explique como funciona a propagação de transações no `@Transactional` do Spring |
| b | **passa** Sou iniciante no assunto | **passa** Sou iniciante no assunto: uso Spring Boot, mas não entendo nada de propagation. |
| c | **passa** Por exemplo, um PedidoService.criarPedido que salva o pedido e chama um serviço de auditoria ou de estoque | **passa** Monte o exemplo em cima de `PedidoService`/`Pedido` |
| d | **passa** 5. Explique as armadilhas mais comuns | **passa** 4. Armadilhas comuns (3–5). |
| e | **falha** 4. Um exercício curto (um cenário em que eu prevejo o resultado), com a resposta no final | **passa** Fora do escopo: alterar arquivos do projeto, porque o objetivo é só entender o conceito. |

### #9 · `escreve msg pro time no slack avisando q o deploy de sexta foi adiado`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>**Tipo:** Escrever texto · **Modo sugerido:** normal · **Raciocínio:** normal

```text
Objetivo: escreva uma mensagem curta para o canal do time no Slack avisando que o deploy previsto para sexta-feira, 13/11/2026, foi adiado. A mensagem serve para que ninguém se prepare para um deploy que não vai acontecer e para que todos saibam o que muda no planejamento.

Contexto:
- Público: o time de desenvolvimento (devs, QA e quem acompanha a release). Todos já sabiam do deploy de sexta.
- Canal: Slack, em um canal do time. O tom é direto e profissional, mas informal, como entre colegas.
- Motivo do adiamento: [MOTIVO, ex.: bug crítico encontrado em homologação]
- Nova data: [NOVA DATA ou &quot;ainda a definir&quot;]
- Ação esperada do time: [ex.: não fazer merge na main até nova ordem / manter o congelamento de código / nenhuma]

Tarefa:
Escreva a mensagem com estas informações, nesta ordem: o aviso de que o deploy de sexta foi adiado (na primeira linha, porque muita gente lê só a prévia da notificação), o motivo em uma frase, a nova data ou quando ela será definida, e o que o time precisa fazer, se precisar fazer algo. Termine indicando onde tirar dúvidas, por exemplo na thread da mensagem.

Restrições:
- Até 5 linhas. Mensagem longa no Slack acaba não sendo lida.
- Use a formatação do Slack (*negrito* com um asterisco) só para destacar a palavra &quot;adiado&quot; e a nova data.
- Não invente motivo, data nem responsável. Se um campo entre colchetes não tiver sido preenchido, deixe o marcador [ ] visível no texto, porque um dado inventado pode desinformar o time.
- Use no máximo um emoji, e só se combinar com o tom.

Pronto quando:
- A primeira linha, sozinha, já informa que o deploy de sexta foi adiado.
- Motivo, nova data e ação esperada aparecem, ou estão como marcador [ ] para preencher.
- A mensagem pode ser colada no Slack sem nenhuma edição além dos marcadores.

Formato da resposta:
Duas versões curtas, com rótulos: &quot;direta&quot; (só os fatos) e &quot;mais calorosa&quot; (reconhece o esforço do time ou pede desculpas pelo transtorno). No final, uma linha dizendo o que personalizar antes de enviar.
```

**Suposições:**
- &quot;Sexta&quot; é a próxima, 13/11/2026, já que hoje é quarta, 11/11.
- Motivo, nova data e ação esperada ficaram como marcadores, porque você não informou e eles mudam a mensagem. Se você me passar esses dados, eu já incluo no prompt.
- A mensagem vai para um canal do time e não é uma DM nem um aviso para a empresa toda.

**O que melhorou:**
- O aviso vem na primeira linha, para quem lê só a notificação.
- Ficou explícito que o modelo não deve inventar motivo nem data, que é o risco principal numa mensagem como essa.
- Agora a mensagem diz o que o time precisa fazer, e não só que o deploy foi adiado.

Quer que eu execute este prompt agora?</pre></td>
<td valign="top"><pre>**Tipo:** Escrever texto · **Modo:** normal · **Esforço:** padrão

```text
Escreva uma mensagem curta para o canal do time no Slack avisando que o deploy de sexta foi adiado, para que ninguém se prepare para ele nem conte com as entregas nessa data.

## Contexto
O deploy estava marcado para sexta-feira, 13/11/2026. A nova data e o motivo ainda não foram informados.

## Tarefa e escopo
Pontos obrigatórios:
- O deploy de sexta (13/11) foi adiado.
- Motivo, em uma frase: use o placeholder [motivo].
- Nova data: use o placeholder [nova data]. Se ela ainda não existir, diga que o time será avisado assim que for definida.
- O que muda para o time: quem tinha tarefa ligada ao deploy pode replanejar, e dúvidas vão para a thread.
Fora do escopo: enviar a mensagem no Slack, porque o usuário vai revisar e postar.

## Restrições
- Tom direto e cordial, típico de Slack. Use no máximo um emoji, porque o aviso é operacional.
- Deixe os placeholders entre colchetes, para o usuário achar e preencher rápido.

## Autonomia
Suposições: &quot;sexta&quot; é 13/11/2026; o canal é o geral do time; motivo e nova data ficam como placeholder (diga se alguma estiver errada).

## Formato da resposta
O texto final, pronto para colar, com até 60 palavras, sem meta-comentário.
```

**O que mudou:**
- Calculei a data: &quot;sexta&quot; virou 13/11/2026, a sexta seguinte a hoje (11/11).
- O pedido não traz o motivo nem a nova data, então os dois ficam como placeholder. Não perguntei porque você preenche isso na hora de colar.
- Deixei explícito que a mensagem só é escrita, não enviada, e quais pontos ela precisa cobrir.

Quer que eu execute este prompt agora?</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 0 leituras:  | **passa** 0 leituras:  |
| C3 | **passa** | **passa** |
| C6 | **passa** 20 linhas com texto, teto 25 | **passa** 12 linhas com texto, teto 25 |
| C7 | **n/a** 'Escrever texto' | **passa** 'Escrever texto' |
| a (tipo) | **passa** 'Escrever texto', esperado ['Escrever texto'] | **passa** 'Escrever texto', esperado ['Escrever texto'] |
| C4 | **passa** Quer que eu execute este prompt agora? | **passa** Quer que eu execute este prompt agora? |
| C5 | **passa** Objetivo: escreva uma mensagem curta para o canal do time no Slack avisando que o deploy previsto para sexta-feira | **passa** Escreva uma mensagem curta para o canal do time no Slack avisando que o deploy de sexta foi adiado |
| b | **passa** Canal: Slack, em um canal do time. O tom é direto e profissional, mas informal, como entre colegas. | **passa** Tom direto e cordial, típico de Slack. |
| c | **passa** Nova data: [NOVA DATA ou "ainda a definir"] | **passa** Nova data: use o placeholder [nova data]. |
| d | **falha** Duas versões curtas, com rótulos: "direta" (só os fatos) e "mais calorosa" | **passa** O texto final, pronto para colar, com até 60 palavras, sem meta-comentário. |
| e | **passa** 1. Read {"file_path": "evals/tmp-home/X/.claude/skills/prompt/<arquivo da skill>"} | **passa** (nenhuma) |

### #10 · `analisa o logs/app.log e ve pq ta lento de tarde`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>**Tipo:** Analisar dados (logs), com investigação de causa · **Modo sugerido:** normal · **Raciocínio:** normal

```text
Objetivo: descobrir por que a aplicação fica lenta à tarde, usando logs/app.log como fonte principal. O resultado serve para decidir o que corrigir. Por isso preciso da causa mais provável com evidência, e não de uma lista genérica de hipóteses.

Contexto:
- Projeto Python &quot;fretes&quot; v0.3.0 (Python &gt;= 3.12, depende de requests &gt;= 2.32). O código fica em src/fretes/frete.py e src/fretes/relatorio.py, e os testes em tests/test_frete.py.
- logs/app.log tem cerca de 480 linhas, a partir de 2026-11-09, no formato:
  2026-11-09T08:00:36 INFO GET /fretes/calcular status=200 dur_ms=114
  Os campos são: timestamp ISO sem fuso, nível, método, rota, status HTTP e dur_ms (duração da requisição em milissegundos).
- &quot;Tarde&quot; aqui significa de 12:00 a 18:00 no horário do próprio log. Compare com a manhã (08:00 a 12:00) e com a noite (depois de 18:00).

Tarefa:
1. Faça o parse do log com um script Python. Calcule todos os números em código, sem estimar. Por faixa de horário (por hora e por período manhã/tarde/noite), calcule: número de requisições, p50, p95 e máximo de dur_ms, e a taxa de status diferente de 200.
2. Confirme se a lentidão à tarde existe nos dados e quanto ela representa. Se não existir, diga isso e pare.
3. Procure o que muda à tarde: volume de requisições, rotas diferentes, linhas WARN/ERROR, mensagens que não são de requisição (jobs, timeouts, chamadas externas) e picos em horários fixos. Analise também as linhas que fogem do formato padrão, sem descartá-las.
4. Cruze o que encontrar com o código de src/fretes/ (por exemplo, chamadas externas via requests, geração de relatório ou falta de cache e timeout) e aponte arquivo:linha quando houver relação.

Restrições:
- Não altere nenhum arquivo do projeto, nem o log nem o código. Esta tarefa é só de diagnóstico. Se quiser salvar o script de análise, use um arquivo temporário fora de src/.
- Separe o que foi confirmado nos dados do que é hipótese. &quot;Não consegui confirmar&quot; é uma resposta válida.

Pronto quando:
- Existe uma tabela por período com os números calculados pelo script.
- A causa mais provável está apontada com pelo menos uma evidência concreta: linhas do log com timestamp e/ou arquivo:linha do código.
- As hipóteses alternativas estão listadas com o que faltaria para confirmar cada uma.

Formato da resposta:
1. Resposta direta: por que fica lento à tarde, com os números (ex.: &quot;p95 sobe de 180 ms para 2.300 ms entre 14h e 16h&quot;).
2. Tabela: período | requisições | p50 | p95 | máx | % erro
3. Evidências: linhas do log e trechos do código relevantes
4. Como foi calculado: script usado, filtros e tratamento de linhas fora do padrão
5. Limitações dos dados (fuso desconhecido, só alguns dias de log etc.) e próximos passos sugeridos para confirmar ou corrigir, sem aplicar nada
```

**Suposições:**
- &quot;Tarde&quot; vai de 12h a 18h, no horário que aparece no log. O log não indica o fuso.
- Você quer só o diagnóstico, sem correção no código.
- A causa pode estar no código de `src/fretes/`, então o prompt pede para cruzar log e código.

**O que melhorou:**
- Define &quot;lento&quot; e &quot;tarde&quot; em números (p50/p95 por período) e exige que os cálculos saiam de um script, sem estimativa.
- Passa o formato real do log e os arquivos do projeto, e pede evidência com timestamp e arquivo:linha, separando o que foi confirmado do que é hipótese.
- Deixa o escopo claro: a tarefa é só de diagnóstico, sem alterar arquivos, e para cedo se a lentidão não aparecer nos dados.

Quer que eu execute este prompt agora?</pre></td>
<td valign="top"><pre>**Tipo:** Analisar dados · **Modo:** normal · **Esforço:** padrão

```text
Analise o logs/app.log e descubra por que a aplicação fica lenta à tarde, para eu saber o que atacar primeiro.

## Contexto
Projeto Python `fretes` 0.3.0 (Python &gt;=3.12, `requests&gt;=2.32`, pytest). O log tem 480 linhas de 2026-11-09, das 08:00 às 19:39. As linhas seguem o formato:
`2026-11-09T08:00:36 INFO GET /fretes/calcular status=200 dur_ms=114`

## Insumos
- logs/app.log
- src/fretes/frete.py e src/fretes/relatorio.py, para cruzar o que o log mostra com o código

## Tarefa e escopo
1. Inspecione o log inteiro antes de calcular. Liste os níveis, endpoints, status e formatos de linha que existem, porque pode haver linhas diferentes da amostra acima.
2. Compare a manhã com a tarde: volume de requisições, dur_ms (mediana, p95, máximo), status e erros, por endpoint e por faixa de horário (de hora em hora ou menos).
3. Encontre quando a lentidão começa e o que muda junto com ela (eventos, endpoints, volume, erros, padrões de horário).
4. Procure no código o trecho ligado ao que o log mostrar e aponte a causa mais provável, com evidência.
Fora do escopo: corrigir o código, porque agora eu só quero o diagnóstico.

## Restrições
- Faça todos os números com código executado (Python ou shell), não de cabeça, para que dê para reproduzir.
- Não altere arquivos do projeto, porque a tarefa é só de leitura. Se precisar de um script, rode-o fora de src/ e tests/.
- Diga quais linhas você descartou ou não conseguiu parsear e quantas foram. Trate outliers à parte, sem apagá-los, porque eles podem ser o próprio sintoma.
- Separe o que o log confirma do que é hipótese.

## Autonomia
Suposições: &quot;tarde&quot; = 12:00–18:00, comparada com 08:00–12:00; o horário do log é o horário local. O tipo também poderia ser &quot;Corrigir bug&quot;, então inclua causa raiz com evidência, mas não aplique correção. Diga se alguma suposição estiver errada. Antes de assumir algo fora desta lista, investigue no log ou no código.

## Formato da resposta
1. Achados principais com números (até 5). O primeiro responde por que fica lento à tarde.
2. Tabela de apoio: faixa de horário | requisições | dur_ms mediana | p95 | máx | erros.
3. Causa provável no código (arquivo:linha), marcada como confirmada ou suspeita.
4. Método: comandos ou script usados.
5. Limitações dos dados (até 3).
```

**O que mudou:**
- &quot;de tarde&quot; virou uma faixa explícita (12:00–18:00 contra a manhã), registrada como suposição que você pode corrigir.
- Entraram fatos das leituras: o formato da linha, o período do log (2026-11-09, 08:00–19:39, 480 linhas) e os arquivos de código para cruzar.
- O pedido ficou só de leitura: só o diagnóstico, sem corrigir nada. Isso vem do tipo &quot;Corrigir bug&quot;, que acrescentou a causa raiz com evidência.

Quer que eu execute este prompt agora?</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 2 leituras: Bash {"command": "ls -la && find . -path ./.git -prune -o -type f -print \| head -50 && cat CLAU \| Bash {"command": "cat pyproject.toml && wc -l logs/app.log && head -8 logs/app.log && tail -3 l | **passa** 2 leituras: Bash {"command": "git ls-files \| head -50 && ls -la logs 2>/dev/null; cat pyproject.toml requir \| Bash {"command": "wc -l logs/app.log && head -15 logs/app.log && echo ... && tail -5 logs/app.l |
| C3 | **passa** | **passa** |
| C6 | **passa** 25 linhas com texto, teto 35 | **passa** 20 linhas com texto, teto 35 |
| C7 | **n/a** 'Analisar dados (logs), com investigação de causa' | **passa** 'Analisar dados' |
| a (tipo) | **passa** 'Analisar dados (logs), com investigação de causa', esperado ['Analisar dados'] | **passa** 'Analisar dados', esperado ['Analisar dados'] |
| C4 | **passa** Quer que eu execute este prompt agora? | **passa** Quer que eu execute este prompt agora? |
| C5 | **passa** Objetivo: descobrir por que a aplicação fica lenta à tarde, usando logs/app.log como fonte principal. | **passa** Analise o logs/app.log e descubra por que a aplicação fica lenta à tarde |
| b | **passa** logs/app.log tem cerca de 480 linhas, a partir de 2026-11-09 | **passa** - logs/app.log |
| c | **passa** Calcule todos os números em código, sem estimar. | **passa** Faça todos os números com código executado (Python ou shell), não de cabeça |
| d | **passa** "Tarde" aqui significa de 12:00 a 18:00 no horário do próprio log. | **passa** 2. Compare a manhã com a tarde: volume de requisições, dur_ms (mediana, p95, máximo) |
| e | **passa** 5. Limitações dos dados (fuso desconhecido, só alguns dias de log etc.) | **passa** 5. Limitações dos dados (até 3). |

### #11 · `quero migrar pro spring boot 4, como faço sem quebrar tudo`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>**Tipo:** Planejar ou decidir + Implementar · **Modo sugerido:** plan mode · **Raciocínio:** normal

```text
Objetivo: migrar o projeto `loja` de Spring Boot 3.3.5 para Spring Boot 4.0.x em etapas pequenas e verificáveis, de modo que `./mvnw test` passe ao fim de cada etapa e qualquer quebra seja fácil de localizar e reverter.

Contexto:
- Projeto Maven single-module, Java 21, parent `spring-boot-starter-parent` 3.3.5 (`pom.xml`).
- Starters: web, data-jpa, security, test. Driver PostgreSQL (banco PostgreSQL 16).
- Testes em JUnit 4 (`org.junit.Test`, `org.junit.Before`, `org.junit.Assert`) rodando via `junit-vintage-engine`, mais Mockito. Hoje só existe `src/test/java/com/exemplo/loja/service/PedidoServiceTest.java`.
- Entidades JPA já usam `jakarta.persistence` (`model/Cliente.java`, `Pedido.java`, `ItemPedido.java`).
- `application.properties` usa `spring.jpa.hibernate.ddl-auto=update` e `open-in-view=false`. Não há migrations.
- Camadas controller -&gt; service -&gt; repository. Os controllers recebem e devolvem DTOs (records em `dto/`). Existe `controller/AuthController.java` usando Spring Security.

Tarefa:
1. Levante as mudanças incompatíveis do Boot 4 que afetam este projeto. Consulte o guia oficial de migração do Spring Boot 4.0 e as notas de release do Spring Framework 7, do Spring Security 7, do Hibernate 7 e do Jackson 3. Para cada item, diga se ele afeta o projeto e cite o arquivo:linha ou a dependência. Pontos que precisam ser checados, no mínimo: nomes e divisão de starters (inclusive os de teste), JUnit 4/vintage com JUnit 6, APIs removidas do Security 7, mudanças de pacote do Jackson 3 nos DTOs, propriedades renomeadas ou removidas e o comportamento do Hibernate 7 com `ddl-auto=update`.
2. Escreva o plano em etapas. Uma sequência sugerida (ajuste se o guia oficial indicar outra): (a) rede de segurança: adicionar testes mínimos que cubram o que hoje não tem teste (subida do contexto, um endpoint de `PedidoController` com MockMvc, autenticação do `AuthController`); (b) subir para a última 3.5.x e eliminar todos os avisos de depreciação, porque o Boot 4 remove o que foi depreciado na linha 3.x; (c) migrar os testes de JUnit 4 para JUnit Jupiter e remover `junit` e `junit-vintage-engine`; (d) subir para 4.0.x e corrigir o que quebrar; (e) revisar propriedades com `spring-boot-properties-migrator` temporário e depois removê-lo.
3. Apresente o plano e espere minha aprovação. Depois execute uma etapa por vez, rodando `./mvnw test` ao fim de cada uma, e faça um commit por etapa.

Restrições:
- Não rode a aplicação nem os testes contra um banco real com `ddl-auto=update`. O Hibernate 7 pode gerar DDL diferente e alterar o schema sem volta. Para testes de integração, use banco de teste descartável (Testcontainers ou H2) e pergunte antes de adicionar a dependência.
- Não mude regra de negócio, contratos dos endpoints nem o formato JSON dos DTOs. A migração deve ser invisível para quem consome a API. Se o Jackson 3 mudar a serialização de algum DTO, aponte isso e pergunte antes de seguir.
- Não introduza migrations (Flyway/Liquibase) nesta tarefa, porque isso é outro escopo. Se achar que são pré-requisito, diga em uma frase.
- Não faça push nem abra PR sem confirmação. Trabalhe em uma branch `migracao/spring-boot-4`.
- Quando não conseguir confirmar uma mudança na documentação oficial, escreva &quot;não confirmado&quot; em vez de supor.

Pronto quando:
- `pom.xml` usa Spring Boot 4.0.x, sem `junit`, `junit-vintage-engine` nem `spring-boot-properties-migrator`.
- `./mvnw test` passa, inclusive os testes novos de contexto, endpoint e autenticação.
- `./mvnw -q compile` não mostra avisos de API depreciada vindos do código do projeto.
- Cada etapa está em um commit próprio na branch `migracao/spring-boot-4`.

Formato da resposta:
1. Recomendação de caminho e o motivo principal (2-3 linhas)
2. Tabela de impacto: mudança do Boot 4 | afeta? | onde (arquivo:linha ou dependência) | ação | fonte
3. Plano em etapas, com esforço estimado e o comando de verificação de cada uma
4. Riscos e mitigação (destaque o schema do banco)
5. Depois de executar: arquivos alterados por etapa, saída resumida de `./mvnw test` e pendências
```

**Suposições:**
- Você quer o plano e também a execução, com uma pausa para aprovar o plano antes de qualquer alteração.
- O alvo é a 4.0.x estável mais recente, e Java 21 continua.
- Pode existir um banco local ou compartilhado com dados que importam. Por isso o prompt proíbe rodar `ddl-auto=update` contra ele.

**O que melhorou:**
- &quot;Sem quebrar tudo&quot; virou critérios que dá pra conferir: testes passando a cada etapa, um commit por etapa, nenhuma depreciação e nenhuma mudança no contrato da API.
- Ele aponta os riscos reais do seu projeto, que vi no `pom.xml` e no código: testes em JUnit 4 com vintage, Security 7, Jackson 3 nos DTOs e Hibernate 7 com `ddl-auto=update`. Também prevê uma rede de testes antes de começar, porque hoje só existe um teste.
- Define um caminho seguro (3.3 → 3.5 → 4.0) e pede que cada mudança venha com a fonte oficial, em vez de palpites.

Quer que eu execute este prompt agora?</pre></td>
<td valign="top"><pre>**Tipo:** Planejar ou decidir · **Modo:** plan mode · **Esforço:** alto — para executar aqui, rode `/effort xhigh` antes de responder sim

```text
ultrathink
Monte um plano para migrar o projeto `loja` do Spring Boot 3.3.5 para o Spring Boot 4, em etapas pequenas, cada uma verificável com `./mvnw test`. Assim a migração não deixa o build quebrado no meio do caminho.

## Contexto
Hoje o projeto usa `spring-boot-starter-parent` 3.3.5 e Java 21. Starters: web, data-jpa e security, mais o driver `postgresql` (runtime). Nos testes: `spring-boot-starter-test`, `junit` 4.13.2 e `junit-vintage-engine`. Só existe um teste: `PedidoServiceTest`. Em `application.properties` estão `spring.jpa.open-in-view=false`, `spring.jpa.hibernate.ddl-auto=update` e o datasource PostgreSQL.

## Insumos
Arquivos a ler: `pom.xml`, `src/main/resources/application.properties`, `src/main/java/com/exemplo/loja/**` (em especial `controller/AuthController.java` e as entidades em `model/`), `src/test/java/com/exemplo/loja/service/PedidoServiceTest.java`.

## Tarefa e escopo
1. Levante o que muda do Boot 3.3.x para o 4 (dependências, Spring Framework, Security, Hibernate/JPA, propriedades, testes) usando o guia oficial de migração e as release notes. Cite a versão e a data consultadas, porque as versões mudam e a memória pode estar desatualizada.
2. Cruze esse levantamento com o que o projeto realmente usa. Aponte cada impacto com arquivo:linha.
3. Decida a ordem das etapas, inclusive se vale passar por uma versão intermediária, e justifique a escolha.
Fora do escopo: aplicar a migração agora, porque primeiro o plano precisa ser aprovado. Também fica de fora criar migrations de banco, a menos que a mudança de versão exija.

## Restrições
- Não altere arquivos. Esta etapa é só de leitura, para o plano ser revisado antes da execução.
- Separe o que o guia oficial afirma do que é inferência sua, para dar para avaliar o risco de cada etapa.

## Pronto quando
- Todas as dependências do `pom.xml` e as propriedades de `application.properties` aparecem no plano, com o impacto ou com &quot;sem impacto&quot;.
- Cada etapa tem um critério de verificação. No mínimo, `./mvnw test` verde.

## Autonomia
Suposições: o objetivo é ficar na versão estável mais recente do Boot 4; continuar no Java 21 é aceitável, a menos que o Boot 4 exija outra versão; o banco continua PostgreSQL 16. Me avise se alguma estiver errada. Antes de assumir algo fora desta lista, investigue no código.

## Formato da resposta
1. Recomendação e motivo principal (até 3 frases).
2. Opções de caminho com prós e contras (até 4).
3. Plano em etapas: mudança, arquivos afetados, verificação e esforço estimado.
4. Riscos e mitigação.
5. Premissas e o que mudaria a decisão.
6. Fontes: link e data.
```

**O que mudou:**
- Classifiquei como planejamento, porque você perguntou &quot;como faço&quot; e não pediu para executar. A execução de muitos arquivos (Agêntica longa) fica para depois que você aprovar o plano.
- O &quot;sem quebrar tudo&quot; virou critério: cada etapa precisa passar em `./mvnw test`.
- Coloquei as versões e dependências reais lidas do `pom.xml`, sem antecipar o que vai quebrar.

Quer que eu execute este prompt agora?</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 2 leituras: Bash {"command": "find . -path ./.git -prune -o -type f -print \| head -60 && echo ---- && cat p \| Bash {"command": "cat src/main/resources/application.properties && echo ---- && grep -rnE \"^im | **passa** 3 leituras: Bash {"command": "find . -path ./.git -prune -o -type f -print \| head -60", "description": "Lis \| Read {"file_path": "spring/pom.xml"} \| Read {"file_path": "spring/src/main/resources/application.properties"} |
| C3 | **passa** | **passa** |
| C6 | **passa** 29 linhas com texto, teto 35 | **passa** 19 linhas com texto, teto 35 |
| C7 | **n/a** 'Planejar ou decidir + Implementar' | **passa** 'Planejar ou decidir' |
| a (tipo) | **passa** 'Planejar ou decidir + Implementar', esperado ['Planejar ou decidir'] | **passa** 'Planejar ou decidir', esperado ['Planejar ou decidir'] |
| e (plan mode) | **passa** Modo sugerido:** plan mode  | **passa** Modo:** plan mode  |
| C4 | **passa** Quer que eu execute este prompt agora? | **passa** Quer que eu execute este prompt agora? |
| C5 | **passa** Objetivo: migrar o projeto `loja` de Spring Boot 3.3.5 para Spring Boot 4.0.x em etapas pequenas e verificáveis | **passa** Monte um plano para migrar o projeto `loja` do Spring Boot 3.3.5 para o Spring Boot 4 |
| b | **passa** - Projeto Maven single-module, Java 21, parent `spring-boot-starter-parent` 3.3.5 (`pom.xml`). | **passa** Hoje o projeto usa `spring-boot-starter-parent` 3.3.5 e Java 21. |
| c | **falha** ausente: 1. Recomendação de caminho e o motivo principal (2-3 linhas) | **passa** 5. Premissas e o que mudaria a decisão. |
| d | **passa** 3. Plano em etapas, com esforço estimado e o comando de verificação de cada uma | **passa** 3. Plano em etapas: mudança, arquivos afetados, verificação e esforço estimado. |

### #12 · `migra todos os testes de junit4 pra junit5 no projeto inteiro`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>**Tipo:** Implementar (refatoração) · **Modo sugerido:** normal · **Raciocínio:** normal

```text
Objetivo:
Migre os testes do projeto de JUnit 4 para JUnit 5 (Jupiter) e remova o JUnit 4 e o
vintage engine do build. A ideia é que o projeto use só a plataforma de testes que já
vem no Spring Boot 3, para que testes novos não sejam escritos em JUnit 4 por engano.

Contexto:
- Projeto Maven &quot;loja&quot;: Spring Boot 3.3.5 (spring-boot-starter-parent) e Java 21.
  Build e testes com `./mvnw test`.
- O `spring-boot-starter-test` já traz JUnit Jupiter, Mockito e AssertJ. Não é preciso
  adicionar nenhuma dependência de JUnit 5.
- O JUnit 4 entra no `pom.xml` por duas dependências explícitas:
  `junit:junit:4.13.2` e `org.junit.vintage:junit-vintage-engine`, ambas com scope test.
- Hoje existe um único arquivo de teste: `src/test/java/com/exemplo/loja/service/PedidoServiceTest.java`.
  Ele usa `org.junit.Test`, `@Before`, `static org.junit.Assert.*` e
  `@Test(expected = NoSuchElementException.class)`, com mocks criados por `mock()` do Mockito.
- Antes de editar, rode `grep -rn &quot;org.junit&quot; src/` para confirmar que não há outros
  arquivos. Se houver, migre todos com o mesmo critério.

Tarefa:
1. Em cada teste JUnit 4, troque os imports para `org.junit.jupiter.api.*`. Mapeamento:
   `@Before` vira `@BeforeEach`, `@After` vira `@AfterEach`, `@BeforeClass`/`@AfterClass`
   viram `@BeforeAll`/`@AfterAll`, `Assert.*` vira `Assertions.*`, e
   `@Test(expected = X.class)` vira `assertThrows(X.class, () -&gt; ...)`.
   Atenção: nos asserts com mensagem, ela passa do primeiro para o último argumento.
2. Remova o `public` das classes e dos métodos de teste. No Jupiter ele é opcional e o
   código fica mais limpo.
3. Remova as dependências `junit:junit` e `junit-vintage-engine` do `pom.xml`.
4. Rode `./mvnw test`.

Restrições:
- Não mude o que os testes verificam (mesmos cenários, mesmas asserções), porque o
  objetivo é migrar a plataforma, não reescrever a cobertura.
- Mantenha os mocks com `mock()` manual. Trocar para `@ExtendWith(MockitoExtension.class)`
  ou para asserts do AssertJ está fora do escopo. Se achar que vale a pena, diga isso em
  uma frase no final.
- Não altere código em `src/main`. Se algum teste só passar com mudança em produção,
  pare e me explique o motivo.
- Não faça commit. Eu reviso o diff antes.

Pronto quando:
- `./mvnw test` termina com BUILD SUCCESS e o número de testes executados é igual ao de
  antes da migração (hoje são 2: `buscaPedido` e `pedidoInexistente`). Se o número cair,
  algum teste deixou de ser descoberto e a migração não está pronta.
- `grep -rnE &quot;import (static )?org\.junit\.(Test|Before|After|Assert|Ignore|Rule|runner)&quot; src/test`
  não retorna nada.
- `./mvnw dependency:tree -Dscope=test | grep -E &quot;junit:junit|vintage&quot;` não retorna nada.

Formato da resposta:
1. Resumo da mudança (2 a 3 linhas)
2. Arquivos alterados, com uma linha sobre cada um
3. Como foi verificado: os três comandos acima e suas saídas relevantes, incluindo a
   linha &quot;Tests run: X&quot; de antes e de depois
4. Decisões tomadas e pendências
```

**Suposições:**
- &quot;Projeto inteiro&quot; hoje é um só arquivo de teste (`PedidoServiceTest.java`). Mesmo assim, o prompt manda conferir com grep antes de editar.
- A migração inclui tirar o JUnit 4 e o vintage do `pom.xml`. Se esses dois ficassem, testes JUnit 4 continuariam funcionando e voltariam a ser escritos.
- Os testes são unitários com Mockito e não precisam de PostgreSQL rodando.

**O que melhorou:**
- O prompt agora cita os arquivos, as versões e as dependências reais, e já diz que o Spring Boot 3.3.5 traz o Jupiter. Assim o modelo não adiciona dependências que já existem.
- Ele cobre as armadilhas da migração: `expected` vira `assertThrows`, a mensagem do assert muda de posição, e um teste pode sumir sem aviso quando o vintage sai do build. Para isso há a checagem do número de testes antes e depois.
- O escopo ficou fechado: sem MockitoExtension, sem AssertJ, sem mexer em `src/main`, sem commit. E o &quot;pronto&quot; é verificado com comandos.

Quer que eu execute este prompt agora?</pre></td>
<td valign="top"><pre>**Tipo:** Agêntica longa · **Modo:** plan mode · **Esforço:** alto. Para executar aqui, rode `/effort xhigh` antes de responder sim.

```text
ultrathink
Migre todos os testes do projeto `loja` de JUnit 4 para JUnit 5 (Jupiter) e remova o JUnit 4 do build. O objetivo é que a suíte rode só na plataforma JUnit 5, sem depender do vintage engine.

## Contexto
- Spring Boot 3.3.5 (`spring-boot-starter-parent`), Java 21, Maven com `./mvnw`.
- O `spring-boot-starter-test` já está no `pom.xml` com scope test.
- O `pom.xml` também declara `junit:junit:4.13.2` e `org.junit.vintage:junit-vintage-engine`, ambos com scope test. Hoje é isso que faz os testes JUnit 4 rodarem.
- Os testes usam Mockito (`org.mockito.Mockito.*`) com mocks criados à mão.

## Insumos
Arquivos a ler:
- `pom.xml`
- `src/test/java/com/exemplo/loja/service/PedidoServiceTest.java`: hoje é o único teste do projeto. Usa `org.junit.Test`, `org.junit.Before`, `org.junit.Assert.*` e `@Test(expected = java.util.NoSuchElementException.class)`.

## Tarefa e escopo
1. Rode `./mvnw test` antes de mudar qualquer coisa e anote quantos testes rodam e quantos passam. Esse é o baseline.
2. Procure em `src/test` qualquer uso de JUnit 4 (`org.junit.*` fora de `org.junit.jupiter`, `junit.framework`, `@RunWith`, `@Rule`, `@ClassRule`, `@Ignore`). Não se limite ao arquivo citado acima.
3. Migre cada teste encontrado para as APIs do JUnit 5.
4. Remova do `pom.xml` as dependências `junit:junit` e `junit-vintage-engine`.
5. Rode `./mvnw test` de novo e compare o resultado com o baseline.
Fora do escopo: código em `src/main` e refatorações nos testes que não sejam a migração, porque o pedido é só trocar o framework.

## Restrições
- Mantenha o que cada teste verifica: as mesmas asserções, o mesmo tipo de exceção esperada e os mesmos nomes de método. A migração precisa manter a cobertura equivalente.
- Não remova, desative nem enfraqueça nenhum teste para a suíte passar. Se um teste falhar depois da migração, investigue e reporte.
- Use o que o `spring-boot-starter-test` já traz. Nenhuma nova dependência ou plugin (por exemplo, ferramentas de migração automática) entra sem confirmação, para manter o build enxuto.
- Siga as convenções que já existem nos testes (mocks com Mockito) e não acrescente abstrações não pedidas.

## Pronto quando
- `./mvnw test` passa e roda o mesmo número de testes do baseline.
- `grep -rnE &quot;import (static )?org\.junit\.[^j]|junit\.framework&quot; src/test` não retorna nada.
- `./mvnw dependency:tree -Dscope=test` não mostra `junit:junit` nem `junit-vintage-engine`.

## Autonomia
Pode fazer sem perguntar: editar arquivos em `src/test`, remover do `pom.xml` as duas dependências citadas e rodar `./mvnw`.
Pergunte antes de: adicionar dependência ou plugin, alterar algo em `src/main`, fazer commit ou push.
Suposições: só existe um arquivo de teste hoje, mas o passo 2 confirma isso. O JUnit 4 pode sair de vez porque não há outro módulo que dependa dele. Diga se alguma estiver errada. Antes de assumir algo fora desta lista, investigue no código.

## Formato da resposta
Durante o trabalho: 1–2 linhas a cada etapa concluída.
No final (autocontido, para quem não acompanhou):
1. Resultado em 1 frase.
2. O que foi feito, por etapa: arquivos alterados e o porquê.
3. Verificação: os comandos de &quot;Pronto quando&quot;, com o resultado antes e depois (testes rodados e passando).
4. Pendências e decisões que precisam do usuário.
```

**O que mudou:**
- Classifiquei como Agêntica longa porque o pedido vale para o projeto inteiro. Hoje só existe `PedidoServiceTest.java`, então &quot;Implementar código&quot; também serviria, e o prompt pede para varrer `src/test` antes de assumir isso.
- Defini &quot;projeto inteiro&quot; com critérios verificáveis: suíte verde com o mesmo número de testes, nenhum import de JUnit 4 e nenhum `junit`/vintage no build.
- Deixei explícito que remover as duas dependências do `pom.xml` está autorizado, e que adicionar dependência, mexer em `src/main` e fazer commit ou push exige perguntar antes.

Quer que eu execute este prompt agora?</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 2 leituras: Bash {"command": "git ls-files \| head -100 && echo \"--- junit refs ---\" && grep -rlE \"org\\. \| Bash {"command": "cat pom.xml && echo \"--- TEST ---\" && cat src/test/java/com/exemplo/loja/se | **passa** 3 leituras: Bash {"command": "git ls-files && echo ---- && grep -rlE \"org\\.junit\\.(Test\|Before\|After\|run \| Read {"file_path": "spring/pom.xml"} \| Read {"file_path": "spring/src/test/java/com/exemplo/loja/service/Pedid |
| C3 | **passa** | **passa** |
| C6 | **passa** 48 linhas com texto, teto 80 | **passa** 31 linhas com texto, teto 80 |
| C7 | **n/a** 'Implementar (refatoração)' | **passa** 'Agêntica longa' |
| a (tipo) | **falha** 'Implementar (refatoração)', esperado ['Agêntica longa'] | **passa** 'Agêntica longa', esperado ['Agêntica longa'] |
| esforço | **falha** 1ª linha='Objetivo:', '/effort xhigh' na entrega=False | **passa** 1ª linha='ultrathink', '/effort xhigh' na entrega=True |
| C4 | **passa** Quer que eu execute este prompt agora? | **passa** Quer que eu execute este prompt agora? |
| C5 | **falha** Objetivo: | **passa** Migre todos os testes do projeto `loja` de JUnit 4 para JUnit 5 (Jupiter) e remova o JUnit 4 do build. |
| b | **passa** - `./mvnw test` termina com BUILD SUCCESS e o número de testes executados é igual ao de | **passa** - `./mvnw test` passa e roda o mesmo número de testes do baseline. |
| c | **passa** Se algum teste só passar com mudança em produção, | **passa** Pergunte antes de: adicionar dependência ou plugin, alterar algo em `src/main`, fazer commit ou push. |
| d | **falha** ausente: Não faça commit. Eu reviso o diff antes. | **falha** ausente: Durante o trabalho: 1–2 linhas a cada etapa concluída. |
| f | **passa** 4. Decisões tomadas e pendências | **passa** 4. Pendências e decisões que precisam do usuário. |

### #13 · `(vazio)`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>O que você quer pedir? Descreva a tarefa e eu a reescrevo como um prompt otimizado.</pre></td>
<td valign="top"><pre>O que você quer pedir ao Claude Code? Descreva a tarefa e eu a reescrevo como prompt.</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 0 leituras:  | **passa** 0 leituras:  |
| C3 | **n/a** sem prompt | **n/a** sem prompt |
| C6 | **n/a** sem prompt | **n/a** sem prompt |
| C7 | **n/a** sem prompt | **n/a** sem prompt |
| a–c | **passa** O que você quer pedir? Descreva a tarefa e eu a reescrevo como um prompt otimizado. | **passa** O que você quer pedir ao Claude Code? Descreva a tarefa e eu a reescrevo como prompt. |
| C4 | **n/a** O que você quer pedir? Descreva a tarefa e eu a reescrevo como um prompt otimizado. | **n/a** O que você quer pedir ao Claude Code? |
| C5 | **n/a** O que você quer pedir? Descreva a tarefa e eu a reescrevo como um prompt otimizado. | **n/a** O que você quer pedir ao Claude Code? |

### #14 · `apaga os clientes duplicados do banco`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>**Tipo:** Implementar (script de limpeza de dados) + Analisar dados · **Modo sugerido:** plan mode · **Raciocínio:** normal

```text
Objetivo: remover os clientes duplicados da tabela de clientes do PostgreSQL da aplicação &quot;loja&quot; sem perder nenhum pedido. Isso deixa a base pronta para, depois, tornar o e-mail único. Cada pessoa deve terminar com um único cadastro, e os pedidos dela devem continuar ligados a esse cadastro.

Contexto:
- Spring Boot com JPA e PostgreSQL 16. Não há migrations: o schema é gerado por `spring.jpa.hibernate.ddl-auto=update`. O datasource está em `src/main/resources/application.properties` (`jdbc:postgresql://localhost:5432/loja`).
- `src/main/java/com/exemplo/loja/model/Cliente.java` tem os campos `id`, `nome`, `email` e `senha`. O e-mail não tem constraint unique, e o comentário no código diz que &quot;há duplicados em produção&quot;.
- `Pedido.java` tem `@ManyToOne Cliente cliente`. Pelo naming padrão do Hibernate, a tabela deve ser `pedido` e a coluna `cliente_id`. Confirme no banco antes de usar.
- O login (`AuthController.java`, `ClienteRepository.java`) busca o cliente por e-mail e compara a senha. Duplicados com senhas diferentes afetam quem consegue entrar.

Tarefa:
1. Diagnóstico, somente leitura. Confirme os nomes reais das tabelas e colunas e liste todas as FKs que apontam para a tabela de clientes (via `information_schema` ou `\d`). Conte os grupos de duplicados por `lower(trim(email))`. Para cada grupo, mostre os ids, quantos pedidos cada id tem e se `nome` e `senha` diferem entre eles. Leia `AuthController` e `ClienteRepository` para ver como o login se comporta hoje quando há mais de um cliente com o mesmo e-mail.
2. Regra do sobrevivente: proponha qual registro de cada grupo fica. O padrão é o de menor `id`. Se o diagnóstico mostrar que outra regra é mais segura, por exemplo manter o registro cuja senha o login usa hoje, explique o motivo em uma frase. Grupos com `nome` diferente podem ser pessoas distintas que compartilham um e-mail: liste esses grupos à parte e deixe-os fora da limpeza automática.
3. Escreva um script SQL que rode numa única transação e faça o seguinte: (a) copie os clientes que serão removidos para uma tabela de backup, por exemplo `cliente_duplicado_backup`, guardando o id do sobrevivente; (b) reaponte para o sobrevivente o `cliente_id` de `pedido` e de qualquer outra FK encontrada no passo 1; (c) apague os duplicados; (d) rode as verificações do &quot;Pronto quando&quot; antes do COMMIT.
4. Mostre o diagnóstico, a regra e o script, e espere minha confirmação antes de executar.

Restrições:
- NÃO execute nenhum UPDATE, DELETE ou DDL antes da minha confirmação explícita. A exclusão não tem volta fora do backup. Confirme também se o banco do `application.properties` é o alvo certo: o comentário fala em produção, mas a URL aponta para localhost.
- Não altere entidades, `application.properties` nem o schema (por exemplo, adicionar unique em `email`). Com `ddl-auto=update`, uma mudança na entidade pode alterar o banco sem controle. Se achar que vale fazer isso depois, diga em uma frase.
- Não toque em tabelas que não referenciam clientes.

Pronto quando:
- A consulta de duplicados por `lower(trim(email))` retorna 0 linhas, sem contar os grupos excluídos de propósito no passo 2.
- O total de linhas em `pedido` é o mesmo antes e depois, e nenhum `pedido.cliente_id` aponta para um cliente inexistente.
- A tabela de backup tem exatamente os registros removidos.
- `./mvnw test` continua passando.

Formato da resposta:
1. Diagnóstico: números e tabela de grupos (email | ids | pedidos por id | nome/senha diferem?), com as consultas usadas
2. Regra do sobrevivente e grupos deixados de fora, com o motivo
3. Script SQL completo
4. Depois da execução: a saída das verificações (antes/depois) e o que fica pendente
```

**Suposições:**
- &quot;Duplicado&quot; quer dizer o mesmo e-mail, sem diferenciar maiúsculas e ignorando espaços nas pontas. O comentário em `Cliente.java` aponta para isso.
- O pedido é mesclar (reapontar os pedidos e então apagar), não apagar e perder o histórico de compras.
- O banco alvo ainda precisa ser confirmado (local ou produção). Por isso o prompt pede essa confirmação antes de qualquer escrita.

**O que melhorou:**
- Define o que conta como duplicado e qual registro fica. Sem isso, um `DELETE` direto apagaria pedidos ou falharia na FK de `pedido.cliente_id`.
- Antes de executar, exige um diagnóstico somente leitura, uma tabela de backup, uma transação e a sua confirmação.
- Inclui critérios que dá para conferir: zero duplicados, o mesmo número de pedidos, nenhum pedido órfão e os testes passando.

Quer que eu execute este prompt agora?</pre></td>
<td valign="top"><pre>Antes de escrever o prompt, preciso de três respostas. Apagar dados do banco não tem volta, e o código não decide estes pontos sozinho:

- O campo `email` em `Cliente.java` não tem `unique`, e o comentário no código diz que há duplicados em produção.
- `Pedido` aponta para `Cliente` por `@ManyToOne`. Se eu apagar um cliente que tem pedidos, o banco recusa a remoção ou os pedidos ficam sem dono.

**1. Quando dois clientes contam como duplicados?**
- a) Mesmo `email`, exatamente igual
- b) Mesmo `email`, ignorando maiúsculas e espaços (`lower(trim(email))`)
- c) Mesmo `email` e mesmo `nome`

**2. Qual registro fica e o que acontece com os pedidos dos que saem?**
- a) Fica o de menor `id` (o mais antigo); os pedidos dos outros passam para ele
- b) Fica o que tem mais pedidos; os pedidos dos outros passam para ele
- c) Fica o de maior `id` (o mais recente); os pedidos dos outros passam para ele
- d) Só apagar os duplicados que não têm nenhum pedido

**3. Onde a remoção vai rodar?**
- a) Em lugar nenhum: gerar só o script SQL, com uma consulta que mostra antes o que seria apagado, para você revisar
- b) No banco local (`jdbc:postgresql://localhost:5432/loja`), dentro de uma transação, mostrando a contagem antes do commit
- c) Em produção. Nesse caso, me diga como acessar e se já existe backup.</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 1 leituras: Bash {"command": "cat src/main/java/com/exemplo/loja/model/Cliente.java src/main/java/com/exemp | **passa** 2 leituras: Bash {"command": "git ls-files \| head -100 && grep -nE \"artifactId\|<version>\|java.version\" po \| Bash {"command": "cat src/main/java/com/exemplo/loja/model/Cliente.java src/main/java/com/exemp |
| C3 | **falha** caixa alta: NÃO | **n/a** sem prompt |
| C6 | **passa** 25 linhas com texto, teto 45 | **n/a** sem prompt |
| C7 | **n/a** 'Implementar (script de limpeza de dados) + Analisar dados' | **n/a** sem prompt |
| C4 | **passa** Quer que eu execute este prompt agora? | **n/a** Antes de escrever o prompt, preciso de três respostas. |
| C5 | **passa** Objetivo: remover os clientes duplicados da tabela de clientes do PostgreSQL da aplicação "loja" | **n/a** Antes de escrever o prompt, preciso de três respostas. |
| a | **falha** Objetivo: remover os clientes duplicados da tabela de clientes do PostgreSQL da aplicação "loja" | **passa** **1. Quando dois clientes contam como duplicados?** |
| b | **passa** NÃO execute nenhum UPDATE, DELETE ou DDL antes da minha confirmação explícita. | **passa** 2. Bash {"command": "cat src/main/java/com/exemplo/loja/model/Cliente.java |

### #15 · `tem mais algo a resolver ou posso instalar`

<table><tr><th>v1</th><th>v2</th></tr><tr>
<td valign="top"><pre>**Tipo:** Revisar ou auditar · **Modo sugerido:** normal · **Raciocínio:** normal

```text
Objetivo: revise a skill /prompt deste repositório e diga se ela está pronta para ser instalada em ~/.claude/skills/. Quero um veredito claro: instalar agora ou corrigir algo antes.

Contexto:
- Repositório: /home/externo/ai_agent_prompt_maker/evals/fixtures/skillproj (branch main, 1 commit &quot;estado inicial&quot;, árvore limpa).
- Arquivos da skill: prompt/SKILL.md (instruções principais) e prompt/tipos.md (os 8 tipos de tarefa e o formato de resposta de cada um).
- README.md documenta a instalação com `cp -r prompt ~/.claude/skills/` e descreve o comportamento esperado: até 3 perguntas, entrega no formato &quot;Tipo · Modo · Raciocínio&quot;, bloco com o prompt, suposições, &quot;O que melhorou&quot; e a oferta de executar.
- A skill segue as boas práticas de prompting da Anthropic citadas no README.

Tarefa: revise os três arquivos verificando estes pontos:
1. Se a skill carrega no Claude Code: frontmatter do SKILL.md (name, description e outros campos) válido segundo a documentação de Skills (https://code.claude.com/docs/en/skills), e se a description faz a skill ser acionada nos casos certos.
2. Se os links relativos (como [tipos.md](tipos.md)) funcionam depois da instalação em ~/.claude/skills/prompt/.
3. Se SKILL.md, tipos.md e README.md são coerentes entre si: seções, limites (3 perguntas, 3 chamadas de ferramenta), formato de entrega e a lista de tipos.
4. Se há instruções ambíguas, contraditórias ou que o modelo poderia seguir ao pé da letra de um jeito ruim. Exemplos: o que acontece com pedido vazio, quando não dá para perguntar, ou quando o pedido mistura tipos.
5. Se o comando de instalação do README funciona, inclusive quando ~/.claude/skills/prompt já existe.
6. Erros de português, de formatação Markdown e blocos de código mal fechados.

Restrições:
- Não altere nenhum arquivo e não rode o comando de instalação. Isto é só uma revisão, e eu decido o que aplicar.
- Reporte todos os achados, inclusive os pequenos, cada um com severidade (alta, média ou baixa). Eu decido o que é bloqueante, então não filtre.
- Cada achado vem com evidência: arquivo:linha e o trecho citado. Separe o que você confirmou do que é suspeita.

Pronto quando: os 6 pontos acima foram verificados, cada um com achados ou com &quot;ok&quot;, e existe um veredito final.

Formato da resposta:
1. Veredito: PODE INSTALAR | INSTALAR COM RESSALVAS | CORRIGIR ANTES, com uma frase de motivo
2. Tabela: severidade | arquivo:linha | problema | evidência | correção sugerida
3. Dúvidas não confirmadas
4. O que está bom e deve ser mantido (curto)
```

**Suposições:**
- &quot;Instalar&quot; quer dizer copiar a pasta `prompt/` para `~/.claude/skills/`, como está no README.
- &quot;Algo a resolver&quot; cobre tanto erros que impedem a skill de funcionar quanto inconsistências e problemas de qualidade.

**O que melhorou:**
- A pergunta solta virou uma revisão com 6 pontos verificáveis, entre eles o frontmatter, os links depois da instalação e o comando `cp`.
- O resultado precisa ter um veredito claro (instalar ou corrigir) e todos os achados com severidade e arquivo:linha.
- O prompt deixa explícito que nada é alterado ou instalado sem você decidir.

Quer que eu execute este prompt agora?</pre></td>
<td valign="top"><pre>**Tipo:** Revisar ou auditar · **Modo:** normal · **Esforço:** padrão

```text
Revise a skill `/prompt` deste repositório e diga se ela está pronta para instalar ou se ainda há algo a corrigir antes, para eu decidir se rodo a instalação agora.

## Contexto
O repositório (`/home/externo/ai_agent_prompt_maker/evals/fixtures/skillproj`) é uma skill do Claude Code, não uma aplicação: não tem build nem testes. Ele tem um commit (&quot;estado inicial&quot;) e a árvore de trabalho está limpa. A instalação descrita no README é `cp -r prompt ~/.claude/skills/`. Depois, o Claude Code é reaberto e `prompt` deve aparecer na lista do `/`. Já existe uma skill `/prompt` instalada em `/home/externo/ai_agent_prompt_maker/evals/tmp-home/v2/.claude/skills/prompt/`.

## Insumos
Arquivos a ler:
- `prompt/SKILL.md`
- `prompt/tipos.md`
- `README.md`
- `/home/externo/ai_agent_prompt_maker/evals/tmp-home/v2/.claude/skills/prompt/` (versão instalada, para comparar)

## Tarefa e escopo
Avalie os arquivos por estes critérios:
- formato da skill: frontmatter válido (`name`, `description`) e uma descrição que faça a skill ser acionada no caso certo;
- consistência entre `SKILL.md`, `tipos.md` e `README.md`: lista de tipos, nomes, templates de resposta e referências entre os arquivos;
- instruções contraditórias, ambíguas ou impossíveis de seguir para o modelo que executa a skill;
- referências quebradas: arquivos, seções e links citados que não existem;
- instalação: se o `cp -r` do README produz a estrutura esperada e o que acontece com a versão já instalada;
- diferenças em relação à versão instalada que mudam o comportamento.
Fora do escopo: reescrever a skill ou melhorar o estilo do texto, porque a decisão agora é só instalar ou não.

## Restrições
- Não altere nenhum arquivo e não rode a instalação, porque isso depende da sua resposta.
- Reporte todos os achados com severidade, separe o que foi confirmado do que é suspeita e investigue antes de afirmar, para que a decisão de instalar se baseie em evidência.

## Pronto quando
- Cada critério acima foi checado, e cada achado cita `arquivo:linha`.
- O veredito responde diretamente se dá para instalar agora.

## Autonomia
Suposições: &quot;instalar&quot; significa rodar o `cp -r` do README em cima da instalação atual; &quot;algo a resolver&quot; vale para qualquer coisa que faça a skill funcionar errado ou diferente do que o README promete. Diga se alguma estiver errada. Antes de assumir algo fora desta lista, investigue nos arquivos.

## Formato da resposta
1. Veredito: APROVAR | APROVAR COM RESSALVAS | PEDIR MUDANÇAS, com o motivo em 1 frase.
2. Tabela por severidade (crítico, alto, médio, baixo): severidade | arquivo:linha | problema | evidência | sugestão.
3. Suspeitas não confirmadas (até 5).
4. O que manter (até 3).
```

**O que mudou:**
- Transformei &quot;tem mais algo a resolver ou posso instalar&quot; em uma revisão com critérios específicos de skill: frontmatter, consistência entre os arquivos, referências e instalação.
- Incluí a versão já instalada da skill como alvo de comparação, porque o `cp -r` do README vai gravar por cima dela.
- Deixei a revisão só de leitura, sem editar nada e sem rodar a instalação.

Quer que eu execute este prompt agora?</pre></td>
</tr></table>

| Critério | v1 | v2 |
|---|---|---|
| C1 | **passa** | **passa** |
| C2 | **passa** 2 leituras: Bash {"command": "ls -la && find . -path ./.git -prune -o -type f -print \| head -50 && git log \| Read {"file_path": "skillproj/README.md"} | **passa** 2 leituras: Bash {"command": "ls -la && git diff --stat HEAD && git log --oneline -3 && find . -maxdepth 3 \| Read {"file_path": "skillproj/README.md"} |
| C3 | **passa** | **passa** |
| C6 | **passa** 23 linhas com texto, teto 45 | **passa** 24 linhas com texto, teto 45 |
| C7 | **n/a** 'Revisar ou auditar' | **passa** 'Revisar ou auditar' |
| a (tipo) | **passa** 'Revisar ou auditar', esperado ['Revisar ou auditar'] | **passa** 'Revisar ou auditar', esperado ['Revisar ou auditar'] |
| C4 | **passa** Quer que eu execute este prompt agora? | **passa** Quer que eu execute este prompt agora? |
| C5 | **passa** Objetivo: revise a skill /prompt deste repositório e diga se ela está pronta para ser instalada | **passa** Revise a skill `/prompt` deste repositório e diga se ela está pronta para instalar |
| b | **passa** - Arquivos da skill: prompt/SKILL.md (instruções principais) e prompt/tipos.md | **passa** - `prompt/SKILL.md` |
| c | **passa** frontmatter do SKILL.md (name, description e outros campos) válido segundo a documentação de Skills | **passa** - formato da skill: frontmatter válido (`name`, `description`) |
| d | **passa** 1. Veredito: PODE INSTALAR \| INSTALAR COM RESSALVAS \| CORRIGIR ANTES, com uma frase de motivo | **passa** O veredito responde diretamente se dá para instalar agora. |
| e | **passa** Não altere nenhum arquivo e não rode o comando de instalação. | **passa** Não altere nenhum arquivo e não rode a instalação, porque isso depende da sua resposta. |
