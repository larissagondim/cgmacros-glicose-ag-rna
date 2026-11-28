# 012 – Dias anteriores: 1, 2 ou 3

- **Status:** aberta (a decidir com um teste, ao construir a RNA)
- **Data do registro:** 28/11/2026
- **Afeta:** tabela de exemplos, entradas da rede e o encadeamento do AG

---

## A pergunta

Quantos dias anteriores de glicose a rede deve ver para prever o dia atual?

---

## O dilema

- **Mais dias:** mais histórico para a rede.
- **Menos dias:** mais exemplos, porque cada dia a mais custa
  um exemplo por participante (cerca de 12% a 14% da tabela).

O pré-processamento já gerou as versões de 2 e 3 dias.
A de 1 dia pode ser gerada na hora, com `montar_dataset_rna(dias, 1)`.

| Dias anteriores | Exemplos (42 / 40) | Entradas (4 medidas / só média) |
|-----------------|--------------------|---------------------------------|
|        1        |     336 / 320      |             15 / 12             |
|        2        |     294 / 280      |             19 / 13             |
|        3        |     252 / 240      |             23 / 14             |

- Os dois números de exemplos tanto em exemplos como em entradas valem sem e com a exclusão dos
  participantes 16 e 19 (decisão 001).
- "Só média" vale se a decisão 011 escolher a opção a).

---

## Opções

**1 dia**
- Prós: o maior número de exemplos (8 por participante); é o mesmo
  dia que a persistência usa.
- Contras: a rede não vê nenhuma tendência. No D9, a entrada seria só
  um valor previsto (o D8).

**2 dias**
- Prós: equilíbrio entre histórico e exemplos (7 por participante).
- Contras: no D9, as duas entradas de glicose são previstas (D7 e D8).

**3 dias**
- Prós: mais histórico; no D9, uma das três entradas é observada (D6),
  o que ancora a previsão.
- Contras: o menor número de exemplos (6 por participante) e mais entradas
  para ajustar.

---

## Como decidir

Com a validação de um participante por vez (decisão 004):

1. Comparar o erro (MAE e RMSE) nas **mesmas linhas de teste**, D4 a D9,
   que existem nas três versões.
2. O baseline nessas linhas é a persistência: **7,85 mg/dL** com
   42 participantes e **8,04** com 40 (decisão 005).
3. Usar média e desvio entre sementes (decisão 009).
4. Critério sugerido: ficar com o **menor número de dias** cujo erro
   não seja pior que o melhor por mais que o desvio entre sementes.
5. Repetir o teste do encadeamento (decisão 011) em cada versão,
   porque o erro acumulado no D9 muda com o número de dias.

---

## O que muda no código

- 2 e 3 dias: as tabelas `dataset_rna_2` e `dataset_rna_3` já existem.
- 1 dia: gerar com `montar_dataset_rna(dias, 1)`. Não precisa reprocessar.
- Com a opção a) da decisão 011, escolher só as colunas
  `glic_media_ant*`.

---

## Riscos

- A diferença entre as versões pode ficar dentro do ruído entre sementes.
- Cada participante tem poucas linhas de teste (6 a 8).
- O melhor resultado em um passo pode não ser o melhor no encadeamento.

---

## Registro da decisão

- [ ] 1 dia
- [ ] 2 dias
- [ ] 3 dias

**Data:**
**Quem decidiu:**
**Resultado do teste:**