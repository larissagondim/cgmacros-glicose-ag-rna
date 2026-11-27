# 004 – Validação e normalização

- **Status:** decidida (aprovada em 27/11/2026), a confirmar com a equipe
- **Afeta:** treino da RNA, medida do erro e redes consultadas pelo AG

---

## Decisão

1. **Validação:** deixar **um participante de fora por vez**
   (`LeaveOneGroupOut`, agrupando por `pid`).
2. **Normalização:** `StandardScaler` ajustado **só com os dados de treino**
   de cada rodada, dentro de um `Pipeline` com a rede.

Cada participante tem assim um conjunto de redes treinado sem os dados dele.
É esse conjunto que o AG consulta para recomendar para aquele participante.

---

## Por que

- A EDA mostrou que cerca de 90% da variação da glicose vem de quem é a pessoa.
  Com dias do mesmo participante no treino e no teste, a rede acertaria
  só por reconhecê-lo, e o erro pareceria menor do que é.
- Um mesmo procedimento serve para medir o erro e para gerar
  as redes do AG, sem treino extra.
- Com cerca de 290 exemplos, cada treino leva segundos.
- O `Pipeline` garante que a média e o desvio do teste nunca entram
  no cálculo da normalização.

---

## Alternativas

**GroupKFold com 5 grupos**
- Prós: bem mais barato (5 treinos por semente em vez de 40 ou 42).
  Cada participante também fica sem os próprios dados no modelo do seu grupo.
- Contras: cada rede treina com cerca de 80% dos participantes, e não com
  todos menos um; a estimativa do erro fica um pouco pessimista.

**Validação comum por linhas (KFold)**
- Prós: a mais simples.
- Contras: mistura dias do mesmo participante no treino e no teste.
  Vaza informação e mascara o erro real. Descartada.

**Separação fixa (por exemplo, 8 participantes de teste)**
- Prós: a mais rápida.
- Contras: o resultado depende de quem caiu no teste;
  com 40 a 42 participantes, a variação é grande.

**Normalizar com todos os dados**
- Prós: uma linha de código a menos.
- Contras: usa informação do teste. Descartada.

**Normalizar dentro de cada participante**
- Prós: remove diferenças de escala entre pessoas.
- Contras: apaga justamente o que a rede precisa para saber
  de quem está falando (a EDA).

---

## Impacto

|           Validação          | Treinos (× 5 sementes) |
|------------------------------|------------------------|
| Um por vez, 42 participantes |          210           |
| Um por vez, 40 participantes |          200           |
| GroupKFold com 5 grupos      |           25           |

- O número de participantes depende da decisão 001 (fibra).
- O erro (MAE) é calculado por participante e por grupo clínico,
  com média e desvio entre as sementes (decisão 009).
- Os baselines usam a mesma validação e as mesmas linhas de teste.
- Saem 40 a 42 conjuntos de redes para guardar (por exemplo, com `joblib`).

---

## Riscos

- Se os hiperparâmetros forem ajustados nas mesmas rodadas usadas para
  reportar o erro, o resultado fica otimista.
- Cada participante de teste tem poucas linhas (6 ou 7), então o erro
  de um só participante é ruidoso. O resumo confiável é o do conjunto.

---

## Pendências

1. Como ajustar os hiperparâmetros sem vazar o participante de teste:
   grade mínima fixada antes, busca aninhada ou busca à parte
   (a decidir, ligada à decisão 002).
2. Confirmar o número de participantes (decisão 001).

---

## Registro da decisão

- [x] Um participante por vez + normalização só no treino
- [ ] GroupKFold com 5 grupos
- [ ] Separação fixa

**Data:** 27/11/2026
**Quem decidiu:** Laura
**Confirmada com a equipe:** ainda não