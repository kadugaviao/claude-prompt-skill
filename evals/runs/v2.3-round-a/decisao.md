# Rodada A (M6 + M1 + M2): decisão pelas regras de validation-cases.md, "Validação da v2.3"

Correção cega mista (`runs/v2.3-round-a/cego/`, 30 saídas: candidata `v23a` e base `runs/v2.2-baseline-opus`, mesma passada). Tabelas em `runs/v2.3-round-a/cego/resumo.md`.

- **M1 aceita pela regra:** o "inventado" do #17 some em 2 de 3 repetições (falha só na r3). Ressalva: na mesma passada, a base também falha só em 1 de 3 (antes, corrigida sozinha, falhava em 3 de 3). O efeito da M1 não fica demonstrado.
- **M2 aceita:** o tipo do #12 sai certo nas 3 repetições (a base errou em 1) e nenhum outro caso muda de tipo.
- **Regressão (critério que passa em 1+ repetição da base e falha nas 3 da candidata):** nenhuma. O pior caso é o #19 enchimento, em 2 de 3 (base 0 de 3).
- **Sinal contrário:** placar total da candidata 10/15 (r1 5/5 · r2 3/5 · r3 2/5) contra 12/15 da base (4/5 nas 3). Pela regra de aprovação da v2.3, a candidata reprovaria hoje (só 1 repetição com 4/5 ou mais).
- **Padrão novo nos "inventado" da candidata:** são motivos inventados para restrições: "porque relatórios e histórico de CI dependem deles" (#12 r3), "porque eu quero revisar antes de mudar alguma coisa" (#19 r3), "porque é um e-mail para um cliente com quem já existe relação" (#17 r3).
- **Custo:** r2+r3 US$ 0,641 contra 0,636 da base (cache quente); r1 US$ 0,732 (corpo novo, cache frio). Mediana da saída por caso: #12 3265 (base 3308), #16 2199 (2274), #17 1243 (1379), #18 1844 (2044), #19 1951 (1926).
