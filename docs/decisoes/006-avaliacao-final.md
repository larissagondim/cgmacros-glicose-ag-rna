# 006 – Avaliação final: efeito previsto do plano

- **Status:** decidida (aprovada em 27/11/2026), a confirmar com a equipe
- **Afeta:** avaliação do AG e relatório final

---

## Decisão

O efeito do plano recomendado é a diferença entre duas **previsões da mesma rede**
para a glicose média do D9:

> efeito = D9 previsto com o plano do AG − D9 previsto com o comportamento habitual

Valor negativo significa redução. A rede usada é a treinada sem os dados
do participante (decisão 004). O D9 real entra só como referência.

Resultados por grupo clínico (saudável, pré-diabetes e DM2).

---

## Os três cenários

| Cenário                       | O que é                                            |
|-------------------------------|----------------------------------------------------|
| Real                          | D9 observado nos dados                             |
| Habitual                      | D9 previsto, com D7 a D9 no hábito do participante |
| Recomendado                   | D9 previsto, com D7 a D9 do plano do AG            |

- O hábito é a média de D1 a D6 de cada variável (decisão 010).
- Em todos, D1 a D6 são os dias observados.

---

## Por que

- As duas previsões saem da mesma rede, então o erro da rede
  não se mistura com o efeito.
- O erro típico da rede (cerca de 8 mg/dL) é maior que a redução esperada
  (alguns mg/dL, segundo a EDA). Comparar com o D9 real esconderia o efeito.
- Comparar "habitual previsto" com o "real" mostra se a rede
  está bem calibrada.

---

## Alternativas

**Comparar o plano recomendado com o D9 real**
- Prós: usa um número observado.
- Contras: mistura o efeito com o erro da rede, que é maior que o efeito.

**Reportar só o D9 previsto do plano, sem o habitual**
- Prós: um cenário a menos.
- Contras: sem ponto de comparação, o número não diz se houve melhora.

**Testar o plano na prática**
- Prós: seria a prova real.
- Contras: impossível aqui, pois são dados observacionais.

---

## Impacto

- Para cada participante: glicose prevista habitual, recomendada e a diferença.
- Por grupo: redução média em mg/dL e em quantos participantes houve redução.
- O relatório declara que o efeito é **previsto**, aprendido de dados
  observacionais, e não prova que o plano causaria a queda (EDA).

---

## Riscos

- **Otimismo:** o AG procura o plano que a rede prevê como melhor.
  Parte da redução pode vir de erros da rede que o AG explorou.
  Avaliar com a mesma rede que guiou a busca tende a superestimar o efeito.
- A redução esperada é pequena e pode ficar dentro do erro da rede.
- Os limites do AG (decisão 007) reduzem o risco, mas não o eliminam.

---

## Pendências

1. Como montar o cenário habitual em D7 a D9
   (ligada à decisão 010 e ao teste do encadeamento).
2. Avaliar o plano com uma rede que o AG não usou na busca
   (por exemplo, sementes separadas, ou a regressão linear) para checar o otimismo.
3. Como mostrar a incerteza (desvio entre as redes do conjunto).

---

## Registro da decisão

- [x] Efeito = previsto recomendado − previsto habitual (mesma rede)
- [ ] Recomendado × D9 real
- [ ] Só o D9 previsto do plano

**Data:** 27/11/2026
**Quem decidiu:** Laura
**Confirmada com a equipe:** ainda não