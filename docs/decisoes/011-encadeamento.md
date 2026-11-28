# 011 – Encadeamento D7 → D8 → D9

- **Status:** aberta (a decidir com um teste, ao construir a RNA)
- **Data do registro:** 28/11/2026
- **Afeta:** entradas da rede, tabelas da RNA e o simulador do AG

---

## A pergunta

Que informação dos dias anteriores a rede recebe,
sabendo que para D7 e D8 só existe a **média prevista**?

---

## O problema

- Hoje a rede recebe, de cada dia anterior, quatro medidas de glicose:
  média, desvio, pico e % do tempo > 140 mg/dL.
- A rede prevê **só a média** do dia (decisão 003).
- O AG precisa prever D7, depois D8 (que usa D7), depois D9 (que usa D8).
- Para D7 e D8 não existem desvio, pico e % > 140. Só a média prevista.

Exemplo com 2 dias anteriores:

- D7 usa D5 e D6 (observados): as 4 medidas existem.
- D8 usa D6 (observado) e D7 (previsto): faltam 3 medidas de D7.
- D9 usa D7 e D8 (previstos): faltam 3 medidas de cada um.

---

## Opções

**a) Só a média dos dias anteriores**
- Prós: o encadeamento é direto, sem inventar nada; menos entradas
  para cerca de 290 exemplos.
- Contras: perde desvio, pico e % > 140, que podem ajudar a prever.

**b) Manter as quatro medidas e fixar as três que faltam**
- Prós: mantém a informação nos dias observados.
- Contras: o valor fixo (por exemplo, o hábito de D1 a D6) é inventado
  e incoerente com a média prevista; o AG não consegue mudá-lo.

**c) Rede com várias saídas (as quatro medidas)**
- Prós: mantém toda a informação e permite mostrar o efeito
  também no pico e na % > 140 (pendência da decisão 003).
- Contras: mais saídas para ajustar com pouco dado; o erro de quatro
  saídas se acumula em 2 ou 3 passos; avaliação mais complexa.

Número de entradas da rede:

| Opção                   | 2 dias | 3 dias |
|-------------------------|--------|--------|
| a) só a média           |   13   |   14   |
| b) ou c) quatro medidas |   19   |   23   |

---

## Como decidir

Com a validação de um participante por vez (decisão 004) e as mesmas
linhas de teste:

1. **Teste de um passo:** MAE da média do dia com as quatro medidas
   (tabelas atuais) e só com a média. Se a diferença ficar dentro do desvio
   entre sementes, escolher **a**.
2. **Teste do encadeamento:** usar D1 a D6 observados e o comportamento
   real de D7 a D9, encadear as previsões e comparar o D9 previsto
   com o D9 real. Isso mede o erro que o AG vai enfrentar.
   Comparar com o baseline "D9 = D6".
3. Se a versão completa for claramente melhor, testar a opção **c**.

---

## O que muda no código

- **a)** escolher só as colunas `glic_media_ant*` das tabelas atuais.
  Não precisa reprocessar.
- **b)** nada nas tabelas; o simulador do AG precisa preencher as medidas.
- **c)** a tabela precisa trazer as quatro saídas
  (pequena mudança em `montar_dataset_rna`).

---

## Riscos

- O erro cresce a cada passo do encadeamento (D7, D8, D9).
- O AG aproveita erros da rede (decisões 006 e 007).
- A conclusão depende da decisão 012 (2 ou 3 dias anteriores).

---

## Registro da decisão

- [ ] a) Só a média
- [ ] b) Quatro medidas, três fixas
- [ ] c) Várias saídas

**Data:**
**Quem decidiu:**
**Resultado do teste:**