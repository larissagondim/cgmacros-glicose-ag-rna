# 005 – Baselines e métricas da RNA

- **Status:** decidida (aprovada em 27/11/2026), a confirmar com a equipe
- **Afeta:** avaliação da RNA e escolha entre 2 e 3 dias anteriores

---

## Decisão

1. **Baselines:** comparar a RNA com dois palpites simples.
   - **Persistência:** "a glicose de hoje é igual à de ontem".
   - **Regressão linear:** mesmas entradas e mesma normalização da rede.
2. **Métrica principal:** **MAE em mg/dL**. **RMSE** como métrica secundária.
3. **Mesmas linhas de teste** para os três modelos (validação da decisão 004).

---

## Por que

- A EDA mostrou que a persistência já erra só cerca de 8 mg/dL.
  Comparar com a média geral faria qualquer modelo parecer bom.
- O MAE é fácil de ler (mg/dL) e comparável direto com o baseline.
- O RMSE pune mais os erros grandes e mostra se a rede falha em dias atípicos.
- A regressão linear mostra se a rede aprende algo além de relações simples.

---

## O baseline a superar

Erro da persistência (MAE, mg/dL):

|           Linhas          | Persistência |
|---------------------------|--------------|
| D3 a D9, 42 participantes |     8,25     |
| D3 a D9, 40 participantes |     8,43     |
| D4 a D9, 42 participantes |     7,85     |
| D4 a D9, 40 participantes |     8,04     |

- D3 a D9 são as linhas da versão com 2 dias anteriores;
  D4 a D9, as da versão com 3 dias (e as comuns às duas).
- Os "40 participantes" valem se a decisão 001 excluir o 16 e o 19.

---

## Alternativas

**Comparar só com a média geral**
- Prós: simples.
- Contras: quase toda a variação vem de quem é a pessoa, então
  qualquer modelo ganha. Descartada.

**Usar R² como métrica**
- Prós: conhecido e sem unidade.
- Contras: enganoso aqui. Cerca de 90% da variação é entre pessoas,
  então o R² sai alto só por reconhecer o participante.

**Só MAE, sem RMSE**
- Prós: um número só.
- Contras: não mostra se a rede erra feio em poucos dias.

**Sem o baseline de regressão linear**
- Prós: menos trabalho.
- Contras: não dá para dizer se a rede traz algo além de um modelo simples.

---

## Impacto

- **2 ou 3 dias anteriores:** o erro é comparado só nas linhas D4 a D9,
  que existem nas duas versões.
- **Resultado reportado:** MAE e RMSE de cada modelo, geral e por grupo clínico
  (saudável, pré-diabetes e DM2), com média e desvio entre sementes (decisão 009).
- **Por participante:** em quantos participantes a rede erra menos
  que a persistência.
- **Expectativa realista (EDA):** o ganho sobre a persistência deve ser modesto.

---

## Riscos

- Cada participante tem poucas linhas, então o erro individual é ruidoso.
  O resumo confiável é o do conjunto.
- Uma diferença pequena entre 2 e 3 dias pode estar dentro da variação
  entre sementes.

---

## Pendências

1. Critério de sucesso: por quanto a rede precisa vencer a persistência
   para ser considerada útil.
2. Usar a regressão linear simples ou uma versão regularizada (Ridge),
   já que há 19 a 23 entradas para cerca de 290 linhas.
3. Como apresentar os resultados por grupo clínico.

---

## Registro da decisão

- [x] Persistência + regressão linear; MAE (principal) e RMSE (secundário)
- [ ] Comparar só com a média geral
- [ ] Usar R²
- [ ] Só MAE

**Data:** 27/11/2026
**Quem decidiu:** Laura
**Confirmada com a equipe:** ainda não