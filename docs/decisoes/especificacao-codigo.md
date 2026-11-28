# Especificação para o código

- **Data:** 28/11/2026
- **Para:** quem for gerar o código da RNA, do AG e da avaliação
- **Base:** decisões 001 a 012 (`docs/decisoes/`)

---

## 1. Como usar este documento

- **Fixado:** decisões 002 a 010, aprovadas. Seguir como está.
- **Provisório:** valor sugerido só para destravar o código.
  Nada da seção 5 foi aprovado. Deixar tudo como constante no topo do código.
- **Aberto:** 001, 011 e 012. O código deve funcionar com todas as opções
  mudando só constantes.

---

## 2. Dados

Tabelas em `data/processed/`, lidas com `carregar_tabela(nome)` (`src/dados.py`).

|     Tabela      | Linhas |             Conteúdo               |
|-----------------|--------|------------------------------------|
| `dias`          |  493   | um dia por linha, 42 participantes |
| `blocos_d1_d9`  |  378   | D1 a D9 de cada participante       |
| `dataset_rna_2` |  294   | treino da rede, 2 dias anteriores  |
| `dataset_rna_3` |  252   | treino da rede, 3 dias anteriores  |

Colunas (nomes exatos):

- **Identificação:** `pid`, `data`, `dia` (só em `blocos`, de 1 a 9),
  `grupo` (saudável, pré-diabetes, DM2). O `grupo` nunca é entrada.
- **Glicose do dia (`GLICOSE`):** `glic_media`, `glic_dp`, `glic_pico`, `pct_140`.
- **Comportamento (`COMPORTAMENTO`, nesta ordem):** `carbs`, `proteina`,
  `gordura`, `fibra`, `atividade`, `hora_ultima_refeicao`.
- **Participante (`BIO`):** `idade`, `sexo_masc`, `imc`, `hba1c`, `glicemia_jejum`.
- **Outras em `dias` e `blocos`:** `cobertura`, `n_refeicoes`, `bom`.
- **Em `dataset_rna_N`:** `glic_media_ant1` é o dia d−1, `ant2` é d−2, e assim
  por diante (também `glic_dp_ant*`, `glic_pico_ant*`, `pct_140_ant*`).
  `alvo` é a `glic_media` do dia d.
- **Ordem das entradas da rede:** glicose dos dias anteriores (`ant1` primeiro),
  depois `COMPORTAMENTO`, depois `BIO`.
- **Unidades:** glicose em mg/dL; macronutrientes em g; `atividade` em kcal;
  horário em horas decimais (20,8 = 20h48).

Os números de linhas valem para 42 participantes. Com 40 (sem 16 e 19):
`dias` 470, `blocos` 360, `dataset_rna_2` 280, `dataset_rna_3` 240.

---

## 3. Constantes (nomes sugeridos, em `src/dados.py`)

|    Constante      |   Valor inicial   | Observação                            |
|-------------------|-------------------|---------------------------------------|
| `EXCLUIR_FIBRA`   |        `[]`       | decisão 001; testar também `[16, 19]` |
| `SEMENTES`        | `[0, 1, 2, 3, 4]` | decisões 002 e 009                    |
| `N_ANTERIORES`    |        `2`        | decisão 012                           |
| `ENTRADA_GLICOSE` | `['glic_media']`  | decisão 011, opção a)                 |

- Todo o código filtra `pid` com `EXCLUIR_FIBRA` logo depois de carregar.
  Filtrar as linhas dá o mesmo resultado de reprocessar sem esses participantes.
- `ENTRADA_GLICOSE` escolhe as colunas `<medida>_ant*` usadas como entrada.

---

## 4. Decisões fixadas

|         Item            |                    Valor                      | Decisão  |
|-------------------------|-----------------------------------------------|----------|
| Alvo                    | `glic_media` do dia                           |   003    |
| Modelo                  | `MLPRegressor` em conjunto de sementes        |   002    |
| Validação               | `LeaveOneGroupOut` por `pid`                  |   004    |
| Normalização            | `StandardScaler` no `Pipeline`, só treino     |   004    |
| Baselines               | persistência e regressão linear               |   005    |
| Métricas                | MAE (principal), RMSE                         |   005    |
| Comparação 1, 2, 3 dias | linhas D4 a D9                                | 005, 012 |
| Efeito do plano         | previsto recomendado − previsto habitual      |   006    |
| Hábito                  | média de D1 a D6 de cada variável             |   010    |
| Genes                   | 18 reais: `COMPORTAMENTO` × D7 a D9           |   008    |
| Operadores do AG        | torneio, elitismo, aritmético, gaussiana      |   008    |
| Fitness                 | **minimizar** o D9 previsto, mais penalidades | 003, 008 |
| Limites                 | ±X% do hábito ∩ faixa observada ∩ física      |   007    |
| Sementes                | fixas, várias, média ± desvio                 |   009    |

---

## 5. Valores provisórios (a confirmar)

|       Parâmetro      |              Valor provisório                        | Pendência |
|----------------------|------------------------------------------------------|-----------|
| Rede                 | 1 camada oculta de 16, ReLU                          |    002    |
| Treino               | `alpha=0.01`, `early_stopping=True`, `max_iter=1000` | 002, 004  |
| Alvo da rede         | valor direto (não a diferença)                       |    002    |
| Regressão linear     | simples (`LinearRegression`)                         |    005    |
| Critério de sucesso  | MAE menor que o da persistência                      |    005    |
| Faixa observada      | percentis 1 e 99, só dados de treino                 |    007    |
| Coerência D7 a D9    | dias independentes                                   |    007    |
| Penalidades          | nenhuma na primeira versão                           |    008    |
| População e gerações | 100 e 200                                            |    008    |
| Torneio e elitismo   | tamanho 3 e 2 indivíduos                             |    008    |
| Cruzamento e mutação | 0,8 e 0,1 por gene (desvio de 10% da amplitude)      |    008    |
| Parada               | número fixo de gerações                              |    008    |
| Execuções do AG      | 1 por semente de `SEMENTES`                          |    009    |
| Checagem do otimismo | regressão linear sem o participante                  |    006    |
| Dias atípicos        | manter o teto de 500 g de carboidrato                | 001, 010  |

X dos limites, por variável (provisório, baseado na variação diária típica):

|       Variável         |              X              |
|------------------------|-----------------------------|
| `carbs`                |             30%             |
| `proteina`             |             50%             |
| `gordura`              |             40%             |
| `fibra`                |             60%             |
| `atividade`            |             15%             |
| `hora_ultima_refeicao` | ±1,2 h (em horas, não em %) |

Limites físicos: gramas e kcal ≥ 0; horário entre 0 e 24 h.
Caso a tratar: hábito fora da faixa observada (interseção vazia).

---

## 6. Fluxo do código

### 6.1 RNA (`notebooks/03_rna.ipynb`)

1. Carregar `dataset_rna_{N_ANTERIORES}` e filtrar `EXCLUIR_FIBRA`.
2. Para cada `pid` (um por vez), treinar o conjunto de `SEMENTES` redes
   com as linhas dos outros participantes.
3. Prever as linhas do `pid` pela média das redes. Guardar o conjunto.
4. Calcular MAE e RMSE geral e por `grupo`, com média ± desvio entre sementes.
5. Calcular os baselines com a mesma validação e as mesmas linhas.
6. Comparar 1, 2 e 3 dias nas linhas D4 a D9 (cruzar por `pid` e `data`).

### 6.2 Simulador do D9 (`src/ag.py`)

Entrada: `pid`, glicose observada dos últimos dias de D1 a D6 e um plano
(3 dias × 6 variáveis). Exemplo com 2 dias anteriores e só a média:

- **D7:** `ant1` = D6, `ant2` = D5 (observados); comportamento do plano em D7.
- **D8:** `ant1` = previsto D7, `ant2` = D6 observado.
- **D9:** `ant1` = previsto D8, `ant2` = previsto D7. A saída é o D9 previsto.

Usar o conjunto treinado **sem** esse `pid`. A previsão é a média das redes.
Avaliar a população inteira de uma vez (matriz), um dia por vez.

### 6.3 AG (`notebooks/04_ag.ipynb`)

1. Calcular o hábito (média de D1 a D6) e os limites de cada gene.
2. Evoluir 18 genes na ordem (dia, variável), cortando nos limites.
3. Repetir por semente de `SEMENTES`. Guardar o melhor plano de cada execução.

### 6.4 Avaliação (`notebooks/05_avaliacao.ipynb`)

- Cenário **habitual:** plano = hábito nos três dias.
- Efeito = D9 previsto (plano do AG) − D9 previsto (habitual).
- Reportar média ± desvio entre execuções, por `pid` e por `grupo`.
- Referência: D9 real (`blocos`, `dia` = 9) e o erro do habitual previsto.
- Checagem do otimismo: avaliar o plano com a regressão linear.
- Informar quantos genes terminam nos limites.

---

## 7. Arquivos (provisório)

```
src/dados.py                    constantes e leitura (existente)
src/rna.py                      pipeline, treino do conjunto, validação, baselines
src/ag.py                       limites, simulador do D9, fitness, evolução
notebooks/03_rna.ipynb
notebooks/04_ag.ipynb
notebooks/05_avaliacao.ipynb
results/modelos/                um conjunto por participante (joblib)
results/tabelas/                MAE, RMSE e efeitos em csv
results/figures/
```

---

## 8. Cuidados

- Nunca usar `grupo` nem a glicose do próprio dia como entrada.
- O `Pipeline` ajusta a normalização só no treino.
- As linhas do `pid` de teste, inclusive D7 a D9, ficam fora do treino
  do conjunto dele.
- Faixa observada e percentis: calcular só com os participantes de treino.
- O hábito usa só D1 a D6. Nunca D7 a D9.
- Usar a mesma ordem de colunas no treino e na previsão.
- Fixar `random_state` em redes e AG. Registrar as versões do scikit-learn e do numpy.
- O AG tende a empurrar os genes para os limites: relatar.
- O efeito é previsto, não causal. Esperar uma redução pequena (poucos mg/dL).