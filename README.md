# cgmacros-glicose-ag-rna

Sistema de recomendação em saúde que usa uma **Rede Neural Artificial (RNA)** e um **Algoritmo Genético (AG)** para sugerir alimentação e atividade física que reduzam a glicose, a partir do dataset [CGMacros](https://physionet.org/content/cgmacros/1.0.0/) (PhysioNet, v1.0.0).

Projeto final da disciplina de Introdução à Inteligência Artificial.

## Alunas

- Larissa Vilasboas Gondim (20250017317)
- Laura Morais Tiné de Oliveira (20250017335)
- Maria Luiza Uchoa Cavalcanti (20250018118)

## A ideia

A partir de 6 dias de dados de um participante (D1 a D6), o sistema recomenda um comportamento para os 3 dias seguintes (D7 a D9) com o objetivo de reduzir a glicose no último dia.

- **RNA (simulador):** uma MLP que prevê a glicose média de um dia a partir dos dias anteriores, do comportamento daquele dia e dos dados clínicos do participante.
- **AG (recomendador):** busca o plano de alimentação e atividade para D7 a D9 que leva à menor glicose prevista no D9, sem se afastar demais dos hábitos da pessoa.

## Progresso atual

- [x] Dados baixados e organizados
- [x] **Análise exploratória (EDA)** concluída: [notebooks/01_eda.ipynb](notebooks/01_eda.ipynb) e relatório em [docs/eda_relatorio.md](docs/eda_relatorio.md)

Principais decisões da EDA:

| Decisão | Escolha |
|---|---|
| Sensor de glicose | Dexcom (~2,7× mais medições reais que o Libre) |
| Dia válido | Dexcom com valor em ≥ 90% dos minutos do dia |
| Participante válido | ≥ 9 dias válidos seguidos |
| Exclusões | 007, 018 e 026 |
| Grupo clínico | HbA1c, pelos cortes da ADA |
| Dataset final | 42 participantes (14 por grupo) e 378 dias válidos |

Principais achados: cerca de 90% da variação da glicose diária vem de quem é a pessoa, e o efeito do carboidrato se inverte quando se compara cada pessoa com ela mesma (paradoxo de Simpson). Por isso a rede precisa receber o histórico de cada participante, e a validação precisa separar participantes.

- [x] **Pré-processamento** concluído: [notebooks/02_preprocessamento.ipynb](notebooks/02_preprocessamento.ipynb), funções em [src/dados.py](src/dados.py) e relatório em [docs/preprocessamento_relatorio.md](docs/preprocessamento_relatorio.md)

| Decisão | Escolha |
|---|---|
| Entrada da rede | glicose dos dias anteriores (média, desvio, pico, % > 140) + comportamento do dia + dados do participante |
| Comportamento (genes do AG) | carboidratos, proteína, gordura, fibra, atividade e horário da última refeição |
| Dados do participante | idade, sexo, IMC, HbA1c e glicemia de jejum |
| Carboidrato acima de 500 g | limitado a 500 g (5 dias) |
| Dia sem Fitbit (participante 033) | média de atividade do próprio participante |
| Dias anteriores | duas versões, com 2 e 3 dias; a escolha fica para o treino da RNA |

Tabelas geradas em `data/processed/`: `dias.csv` (493 dias), `blocos_d1_d9.csv` (os 9 dias de cada participante), `dataset_rna_2.csv` (294 exemplos) e `dataset_rna_3.csv` (252 exemplos).

## O que falta

- [ ] **RNA:** treinar a MLP, validar por participante (GroupKFold) e comparar com os baselines (persistência e regressão linear), usando MAE em mg/dL
- [ ] **AG:** cromossomo de 18 genes (6 variáveis × 3 dias), limites em torno dos hábitos de cada participante e fitness com a glicose prevista no D9 mais penalidades
- [ ] **Avaliação:** comparar a glicose prevista no D9 nos cenários real × habitual × recomendado, por grupo clínico
- [ ] **Bônus:** usar o AG para otimizar os hiperparâmetros da RNA
- [ ] **Apresentação**

## Próximos passos

Para a RNA (`notebooks/03_rna.ipynb`):

1. Carregar as tabelas com `carregar_tabela('dataset_rna_2')` e `carregar_tabela('dataset_rna_3')`.
2. Calcular os baselines por participante (GroupKFold): persistência ("hoje = ontem", MAE de ~8 mg/dL) e regressão linear.
3. Treinar a MLP com ReLU, normalizando as entradas só com os dados de treino de cada fold.
4. Comparar as versões com 2 e 3 dias anteriores nos mesmos dias de teste.
5. Guardar, para cada participante, uma rede treinada sem os dados dele. É essa que o AG vai consultar.

## Estrutura

```
data/        dados do CGMacros (fora do git); brutos em data/raw/, tabelas prontas em data/processed/
notebooks/   01_eda.ipynb, 02_preprocessamento.ipynb
src/         código reaproveitável (dados.py)
results/     figuras e resultados
docs/        relatórios
```

## Como rodar

1. Baixe o CGMacros no PhysioNet e extraia as pastas `CGMacros-0XX` e os arquivos `bio.csv` e `DataDictionary_*.csv` em `data/raw/`.
2. Crie o ambiente e instale as dependências:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install pandas numpy matplotlib seaborn scikit-learn jupyter
   ```

3. Rode os notebooks em ordem: `01_eda.ipynb` e depois `02_preprocessamento.ipynb`, que gera as tabelas em `data/processed/`.
