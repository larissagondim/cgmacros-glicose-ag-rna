# Decisões do projeto

Registro das decisões do recomendador de glicose (RNA + AG) com o CGMacros.
Cada decisão tem um arquivo próprio, com alternativas, prós e contras.

- **Branch:** `feat/decisoes-recomendacao`
- **Data:** 28/11/2026

---

## Índice

| Nº                                   | Título                                  |  Status  |
|--------------------------------------|-----------------------------------------|----------|
| [001](001-tratamento-fibra.md)       | Fibra dos participantes 16 e 19         | proposta |
| [002](002-modelo-rna.md)             | Modelo da RNA: MLPRegressor em conjunto | decidida |
| [003](003-alvo-D9.md)                | Alvo do D9: glicose média               | decidida |
| [004](004-validacao-normalizacao.md) | Validação e normalização                | decidida |
| [005](005-baselines-metricas.md)     | Baselines e métricas                    | decidida |
| [006](006-avaliacao-final.md)        | Avaliação final: efeito previsto        | decidida |
| [007](007-limites-ag.md)             | Limites dos genes do AG                 | decidida |
| [008](008-estrutura-ag.md)           | Estrutura do AG                         | decidida |
| [009](009-reprodutibilidade.md)      | Reprodutibilidade                       | decidida |
| [010](010-habito.md)                 | Hábito de cada participante             | decidida |
| [011](011-encadeamento.md)           | Encadeamento D7 → D8 → D9               |  aberta  |
| [012](012-dias-anteriores.md)        | Dias anteriores: 1, 2 ou 3              |  aberta  |

---

## Como ler o status

- **proposta:** documentada, mas não aplicada. A decisão final é da equipe.
- **decidida:** aprovada em 27/11/2026, a confirmar com a equipe.
- **aberta:** depende de um teste, que será feito ao construir a RNA.

---

## Formato dos documentos

Decisão, por que, alternativas (prós e contras), impacto,
riscos, pendências e registro (opção escolhida, data e quem decidiu).

---

## Pendências sem documento próprio

Serão decididas ao construir o algoritmo. Cada uma aparece
na seção "Pendências" do documento de origem.

- Valor de X dos limites, horário em ±horas e faixa observada (007)
- Coerência entre D7, D8 e D9 (007)
- Penalidades da fitness (008)
- Parâmetros do AG e execuções por participante (008, 009)
- Critério de sucesso da RNA e regressão linear simples ou Ridge (005)
- Avaliação do plano com uma rede que o AG não usou (006)
- Hiperparâmetros e alvo da rede, valor ou diferença (002, 004)
- Dias atípicos e valores fora das faixas do dicionário (001, 010)