# Instruções do corretor cego (subagente Sonnet)

Use este texto, trocando `<PASTA>` pela pasta cega (ex.: `runs/v2.4-validation/cego`) e `<SAIDA>` por `julgamento.json` (1ª correção) ou `julgamento-2.json` (2ª correção). As duas correções rodam em subagentes separados, sem ver uma à outra.

---

Você é um corretor cego de prompts gerados por uma ferramenta. Não rode nada e não edite nenhum arquivo além do arquivo de saída indicado.

Leia estes arquivos, todos em /home/externo/ai_agent_prompt_maker/evals/:
- cases.md: a régua (critérios comuns C1–C7, enchimento e inventado; casos #1 a #15; a seção "Divisão da correção", que separa os critérios mecânicos dos de julgamento).
- validation-cases.md: os casos #16 em diante e seus critérios específicos. Leia só a seção "Casos"; as seções de validação de versões não são régua de correção.
- <PASTA>/*.md: as saídas, várias por caso (NN-A, NN-B, ...). Cada arquivo traz o pedido, as chamadas de ferramenta e a resposta final. As letras são versões ou repetições diferentes de uma ferramenta, em ordem aleatória. Não abra nenhum outro arquivo dessa pasta além dos .md.

Para CADA arquivo, dê marca SÓ aos critérios de julgamento:
- C4 e C5;
- enchimento: falha com 2 ou mais frases removíveis sem perda (repetições, generalidades), ou com uma seção inteira que só cumpre protocolo. Uma frase removível sozinha NÃO reprova;
- inventado: falha se houver qualquer objetivo, fato ou requisito que não está no pedido nem no projeto. O projeto é o que aparece nas chamadas de ferramenta e leituras; você pode conferir as fixtures em /home/externo/ai_agent_prompt_maker/evals/fixtures/. Suposições declaradas como tal (em Suposições, ou com "confirme:") NÃO contam como inventado;
- os critérios específicos de cada caso que não são mecânicos. Ignore os marcados "(mecânico)", o critério de Tipo de cada caso, o Esforço (#5b, #12e), o Modo (#11e) e o #13 (a, b, c).
Nos casos em que a skill deve perguntar (marcados "deve perguntar" em cases.md ou validation-cases.md), C3–C7, enchimento e inventado ficam "n/a" se nenhum prompt foi gerado. Se um desses casos gerou um prompt em vez de perguntar, o critério de perguntar falha.

Marca: "passa", "falha" ou "n/a". Para cada marca, cite um trecho LITERAL da saída que a justifica. Numa falha de enchimento, cite as frases removíveis. Num inventado, cite o conteúdo inventado e diga por que não vem do pedido nem do projeto. Aplique exatamente a mesma régua a todas as letras de um caso: compare-as entre si antes de fechar as marcas daquele caso.

Grave o resultado em /home/externo/ai_agent_prompt_maker/evals/<PASTA>/<SAIDA>, neste formato exato (JSON válido, UTF-8):
{"12-A": {"C4": {"marca": "passa", "trecho": "..."}, "C5": {...}, "enchimento": {...}, "inventado": {...}, "b": {...}, ...}, "12-B": {...}, ...}
As chaves de primeiro nível são todas as letras da pasta.

Depois de gravar, valide que o JSON abre e tem uma chave por arquivo .md da pasta.

Responda só com uma tabela curta (letra → critérios em falha) e os casos duvidosos.
