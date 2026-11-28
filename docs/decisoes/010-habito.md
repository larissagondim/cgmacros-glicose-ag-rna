# 010 – Hábito de cada participante

- **Status:** decidida (aprovada em 27/11/2026), a confirmar com a equipe
- **Afeta:** limites do AG, cenário "habitual" e penalidades da fitness

---

## Decisão

O **hábito** de cada participante, em cada variável de comportamento,
é a **média de D1 a D6** (os dias que o sistema observa).

As variáveis são carboidrato, proteína, gordura, fibra, atividade
e horário da última refeição.

---

## Por que

- D1 a D6 são os únicos dias que o sistema pode ver. Usar D7 a D9
  seria usar dias que o AG está tentando recomendar.
- A média é simples de explicar e de calcular.
- Mudar para a mediana quase não altera o resultado: a diferença
  mediana entre as duas fica entre 1% e 7%, conforme a variável.

---

## Alternativas

**Mediana de D1 a D6**
- Prós: robusta a um dia atípico.
- Contras: com 6 dias, difere pouco da média (1% a 7%);
  menos intuitiva como "hábito".

**Média dos últimos dias (D4 a D6)**
- Prós: reflete a rotina mais recente.
- Contras: só 3 dias, então é mais ruidosa. Difere da média de 6 dias
  em 3% (atividade) a 16% (fibra).

**Média de D1 a D9**
- Prós: mais dias, menos ruído.
- Contras: usa D7 a D9, que o sistema não deve ver. Descartada.

---

## Impacto

- O hábito define o centro dos limites do AG (decisão 007).
- É o comportamento do cenário "habitual" da avaliação (decisão 006).
- Pode servir de referência para penalizar planos muito distantes do hábito
  (a decidir junto com a fitness, decisão 008).
- O hábito não é o que a pessoa fez de fato em D7 a D9: o que ela comeu
  difere da média de D1 a D6 em cerca de 5% a 16% (mediana) nas variáveis
  principais, e 29% na fibra. O cenário "habitual" é uma referência
  do modelo, não o comportamento real.

---

## Pendências

1. Dias atípicos: o teto de 500 g de carboidrato e a fibra dos
   participantes 16 e 19 (decisão 001) afetam a média.
2. Horário da última refeição: média simples (lanche depois da meia-noite
   já conta para o dia seguinte, por regra do pré-processamento).

---

## Registro da decisão

- [x] Média de D1 a D6
- [ ] Mediana de D1 a D6
- [ ] Média de D4 a D6
- [ ] Média de D1 a D9

**Data:** 27/11/2026
**Quem decidiu:** Laura
**Confirmada com a equipe:** ainda não