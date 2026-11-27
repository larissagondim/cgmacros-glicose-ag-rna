# 002 – Modelo da RNA: MLPRegressor em conjunto

- **Status:** decidida (opção B), a confirmar com a equipe
- **Data:** 27/11/2026
- **Afeta:** notebook `03_rna`, modelos consultados pelo AG

---

## Decisão

Usar o **`MLPRegressor`** do scikit-learn em **conjunto de cerca de 5 sementes**,
com **rede pequena** e **`early_stopping`**. A previsão final é a média das redes.

A escolha do `MLPRegressor` (em vez de implementar a rede à mão)
foi feita por causa do prazo de 4 dias.

---

## Por que o conjunto, e não uma rede só

- Com cerca de 290 exemplos, o resultado de uma rede muda bastante
  de uma semente para outra.
- A média de várias redes é mais estável e dá uma superfície mais suave para o AG.
- O AG aproveita qualquer erro da rede. A discordância entre as redes
  pode indicar onde a previsão é menos confiável.
- Reforça a decisão 009 (várias sementes).

---

## Alternativas

**A. MLPRegressor simples (uma rede)**
- Prós: o caminho mais rápido; funciona com `Pipeline` e com a validação
  deixando uma pessoa de fora.
- Contras: resultado instável com tão pouco dado; o AG pode explorar
  os pontos onde a rede erra.

**C. Gradient boosting (árvores)**
- Prós: costuma ir bem em dados tabulares pequenos.
- Contras: foge do escopo "rede neural + AG"; as previsões em degraus
  são ruins para o AG explorar.

**D. Rede em PyTorch ou Keras**
- Prós: mais controle (dropout, perda própria); mostra melhor
  a backpropagation.
- Contras: custa tempo que o prazo não permite; não é necessário
  para o resultado.

**Rede implementada à mão**
- Descartada pelo prazo.
- Contra aceito: mostra menos o entendimento de backpropagation,
  que o professor avalia. O relatório pode compensar explicando
  como a rede treina.

---

## Impacto

Com a validação deixando um participante de fora (decisão 004):

|            Cenário            | Treinos |
|-------------------------------|---------|
| 42 participantes × 5 sementes |   210   |
| 40 participantes × 5 sementes |   200   |

- Cada treino é rápido (cerca de 290 linhas), então o custo total é de minutos.
- O número de participantes depende da decisão 001 (fibra).
- A explicação no relatório fica um pouco mais longa
  (rede + conjunto de sementes).

---

## Riscos

- O `early_stopping` do scikit-learn separa uma parte do treino por linhas,
  não por participante. Isso só afeta o ponto de parada,
  não o teste, que continua sendo de participantes deixados de fora.
- Com poucos dados, uma rede grande tende a decorar. Por isso a rede é pequena.

---

## Pendências

1. Arquitetura exata (camadas e neurônios) e hiperparâmetros,
   por uma busca pequena.
2. Número de sementes (cerca de 5, a confirmar).
3. Teste: prever a diferença em relação ao dia anterior (hoje menos ontem)
   em vez do valor direto. O alvo final continua sendo a glicose média.
4. Decidir, junto com as penalidades do AG, se a discordância
   entre as redes entra na fitness.

---

## Registro da decisão

- [x] B – MLPRegressor em conjunto de sementes
- [ ] A – MLPRegressor simples
- [ ] C – Gradient boosting
- [ ] D – PyTorch ou Keras

**Data:** 27/11/2026
**Quem decidiu:** Laura
**Confirmada com a equipe:** ainda não