# 007 – Limites dos genes do AG

- **Status:** decidida (aprovada em 27/11/2026), a confirmar com a equipe
- **Afeta:** espaço de busca do AG e confiabilidade das recomendações

---

## Decisão

O limite de cada gene (variável × dia, 18 no total) é a **interseção** de:

1. **±X% do hábito** do participante (média de D1 a D6, decisão 010);
2. **faixa observada** nos dados de treino da rede;
3. **limites físicos** de cada variável.

O valor de X ainda não foi definido (ver pendências).

---

## Por que

- A rede só é confiável onde viu dados. O AG procura o melhor
  valor previsto e aproveita qualquer extrapolação errada.
- Ficar perto do hábito mantém a recomendação realista para a pessoa.
- Limites físicos impedem valores sem sentido (gramas negativas,
  horário fora do dia).
- Ajuda a reduzir o otimismo do efeito previsto (decisão 006).

---

## Dados que orientam a escolha

Variação típica de um dia em relação à média da própria pessoa
(percentis 10 a 90, 40 participantes, D1 a D9):

| Variável                   | Limite físico |     Variação diária     |
|----------------------------|---------------|-------------------------|
| Carboidrato                |     ≥ 0 g     |      −32% a +31%        |
| Proteína                   |     ≥ 0 g     |      −50% a +57%        |
| Gordura                    |     ≥ 0 g     |      −42% a +39%        |
| Fibra                      |     ≥ 0 g     |      −58% a +60%        |
| Atividade                  |    ≥ 0 kcal   |      −14% a +14%        |
| Horário da última refeição |    0 a 24 h   | −9% a +10% (dp ≈ 1,2 h) |

Faixa observada - deve ser recalculada para apenas participantes de terino - (percentis 1 a 99), para referência:

- carboidrato: 82 a 500 g (o 500 é o teto do pré-processamento)
- proteína: 35 a 226 g
- gordura: 25 a 157 g
- fibra: 4 a 45 g
- atividade: 1.532 a 4.268 kcal
- horário: 12,1 a 23,2 h

Um mesmo X para todas as variáveis não serve bem. Por exemplo, ±20% é
razoável para os macronutrientes, mas passa muito da variação típica
da atividade (±14%) e equivale a cerca de ±3,9 h no horário da refeição.

---

## Alternativas

**Só ±X% do hábito**
- Prós: simples; fácil de explicar.
- Contras: pode sair da faixa que a rede viu (hábito perto do extremo
  mais X%); um X único não serve para todas as variáveis.

**Só a faixa observada (global)**
- Prós: protege contra extrapolação.
- Contras: permite mudanças enormes para a pessoa
  (por exemplo, recomendar 82 g de carboidrato a quem come 200 g).

**Sem limites**
- Prós: dá o maior efeito previsto.
- Contras: o AG explora os erros da rede e propõe planos irreais.
  Descartada.

---

## Impacto

- Limites menores dão recomendações mais realistas e seguras,
  mas um efeito previsto menor. Limites maiores permitem mais efeito,
  mas aumentam o risco de extrapolação.
- Os limites são calculados por participante antes de rodar o AG.
- O teto de 500 g de carboidrato do pré-processamento faz com que
  o limite superior de carboidrato seja artificial.

---

## Pendências

1. Valor de X: único ou por variável. Os dados acima sugerem
   que variam muito entre variáveis.
2. Horário da última refeição em **±horas**, em vez de ±%.
3. Faixa observada: percentis 1 a 99 globais, por grupo clínico
   ou por participante.
4. Regra de coerência entre D7, D8 e D9 (cada dia livre ou um plano
   que varia pouco entre os dias).
5. A fibra usa os 40 participantes sem o 16 e o 19 (decisão 001).

---

## Registro da decisão

- [x] ±X% do hábito ∩ faixa observada ∩ limites físicos (X a definir)
- [ ] Só ±X% do hábito
- [ ] Só a faixa observada
- [ ] Sem limites

**Data:** 27/11/2026
**Quem decidiu:** Laura
**Confirmada com a equipe:** ainda não