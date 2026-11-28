# 009 – Reprodutibilidade: sementes fixas e várias repetições

- **Status:** decidida (aprovada em 27/11/2026), a confirmar com a equipe
- **Afeta:** treino da RNA, execuções do AG e forma de reportar os resultados

---

## Decisão

1. **Sementes fixas** (`random_state`) em tudo que é aleatório:
   redes, divisão interna do `early_stopping`, AG e qualquer sorteio.
2. **Várias sementes** nos resultados, reportados como **média ± desvio**.
3. As sementes ficam registradas no código, para qualquer pessoa
   da equipe repetir os mesmos números.

---

## Por que

- Com cerca de 290 exemplos, uma rede treinada com uma única semente
  pode parecer melhor ou pior do que é.
- O AG também é aleatório: duas execuções do mesmo participante
  podem recomendar planos diferentes.
- Sementes fixas permitem repetir o resultado do relatório.
- Várias sementes mostram se uma diferença (por exemplo, entre 2 e 3 dias
  anteriores) é real ou só ruído.

---

## Como as sementes se encaixam

- **Redes:** o conjunto de cerca de 5 sementes (decisão 002) faz parte
  do modelo, e a previsão é a média delas.
- **Erro da RNA:** reportar o MAE do conjunto e o MAE médio ± desvio
  de cada rede individual.
- **AG:** várias execuções por participante, com sementes diferentes.
  O efeito de cada participante é a média ± desvio entre elas.

---

## Alternativas

**Uma semente só**
- Prós: o mais rápido.
- Contras: o resultado pode depender da sorte da semente.

**Sementes aleatórias, sem registrar**
- Prós: nenhum trabalho extra.
- Contras: ninguém consegue repetir os números do relatório.

**Repetir o conjunto inteiro com vários conjuntos de sementes**
- Prós: mostra a variação do conjunto em si, não só das redes.
- Contras: multiplica os treinos (de 210 para cerca de 630 com 3 conjuntos).
  Pode ficar como verificação extra, se sobrar tempo.

---

## Impacto

- Todo número do relatório sai com média e desvio, ou com a semente indicada.
- As sementes ficam numa constante do código (por exemplo, `SEMENTES`),
  usada nos notebooks da RNA e do AG.
- O custo de tempo é pequeno com a rede pequena e poucos dados.

---

## Pendências

1. Número de execuções do AG por participante.
2. Onde registrar as sementes (constante em `dados.py` ou arquivo de configuração).
3. Registrar as versões do scikit-learn e do numpy, porque o resultado
   da rede pode mudar entre versões.

---

## Registro da decisão

- [x] Sementes fixas, várias repetições, média ± desvio
- [ ] Uma semente só
- [ ] Sementes aleatórias sem registro

**Data:** 27/11/2026
**Quem decidiu:** Laura
**Confirmada com a equipe:** ainda não