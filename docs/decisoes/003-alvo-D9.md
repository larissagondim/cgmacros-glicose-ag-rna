# 003 – Alvo do D9: glicose média do dia

- **Status:** decidida (aprovada em 27/11/2026), a confirmar com a equipe
- **Afeta:** saída da RNA, fitness do AG e avaliação final

---

## Decisão

"Reduzir a glicose no D9" significa **reduzir a glicose média do D9**
(Dexcom, mg/dL). É o alvo que já está nas tabelas `dataset_rna_2` e `dataset_rna_3`.

---

## Por que a média

- Tem o menor erro do "hoje = ontem" em relação à sua variação (tabela abaixo).
  O baseline de 8,1 mg/dL da EDA foi calculado para ela.
- É uma saída só, o que simplifica a rede, a fitness do AG e o encadeamento.
- Não satura: o pico bate em 400 mg/dL em 9 dias e a % > 140
  chega a 0% ou 100% em muitos dias.
- Não obriga a refazer as tabelas da colega.

Quanto menor o número, mais previsível é a medida de um dia para o outro:

|       Candidato      | Erro de "hoje = ontem" ÷ desvio |
|----------------------|---------------------------------|
| Média do dia         |             0,27                |
| % do tempo > 140     |             0,31                |
| Pico do dia          |             0,49                |
| Desvio padrão do dia |             0,55                |

---

## Alternativas

**% do tempo acima de 140 mg/dL**
- Prós: medida clínica comum; quase tão previsível quanto a média (0,31).
- Contras: depende do sensor (a EDA avisa); satura em 0% em 10% dos dias
  de saudáveis e em 99% ou mais em 13% dos dias de DM2.

**Pico do dia**
- Prós: capta os picos depois das refeições.
- Contras: depende de um único ponto, então é bem mais ruidoso (0,49);
  o sensor trava em 400 mg/dL em 9 dias.

**Desvio padrão do dia (variabilidade)**
- Prós: mede o quanto a glicose oscila.
- Contras: a menos previsível das quatro (0,55); o enunciado fala
  em reduzir a glicose, não a variabilidade.

**Várias saídas ao mesmo tempo**
- Prós: guarda mais informação do dia e permite relatar o efeito
  também no pico e na % > 140.
- Contras: mais saídas para ajustar com pouco dado; o erro se acumula
  ao encadear D7, D8 e D9.

---

## Impacto

- Nenhuma mudança nas tabelas nem no código da colega.
- A fitness do AG é a glicose média prevista no D9, mais as penalidades.
- A rede prevê só a média. **Pico e % > 140 só podem ser mostrados
  para o D9 real**, por grupo clínico, e não para o plano recomendado.
- Os valores absolutos mudam com o sensor (Dexcom). O efeito é comparado
  dentro do mesmo sensor.

---

## Pendências

1. Alinhar com a equipe.
2. Decidir se vale uma saída extra (por exemplo, a % > 140) na rede.
   Isso se liga ao teste do encadeamento D7 → D8 → D9.

---

## Registro da decisão

- [x] Glicose média do dia
- [ ] % do tempo acima de 140 mg/dL
- [ ] Pico do dia
- [ ] Desvio padrão do dia
- [ ] Várias saídas

**Data:** 27/11/2026
**Quem decidiu:** Laura
**Confirmada com a equipe:** ainda não