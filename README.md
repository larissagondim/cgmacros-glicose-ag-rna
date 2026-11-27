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

## O que falta

- [ ] **Pré-processamento:** tabela final com uma linha por pessoa-dia (glicose, macronutrientes, horário da última refeição, atividade e dados do `bio.csv`)
- [ ] **RNA:** treinar a MLP, validar por participante (GroupKFold) e comparar com os baselines (persistência e regressão linear), usando MAE em mg/dL
- [ ] **AG:** cromossomo de 18 genes (6 variáveis × 3 dias), limites em torno dos hábitos de cada participante e fitness com a glicose prevista no D9 mais penalidades
- [ ] **Avaliação:** comparar a glicose prevista no D9 nos cenários real × habitual × recomendado, por grupo clínico
- [ ] **Bônus:** usar o AG para otimizar os hiperparâmetros da RNA
- [ ] **Apresentação**

## Próximos passos

Pendências que a EDA deixou para o pré-processamento:

1. Padronizar os tipos de refeição (`dinner`/`Dinner`, `snack`/`Snacks`/`snack 1`).
2. Decidir o que fazer com `Amount Consumed`, que tem valores acima de 100% e falta nos participantes 028 e 029.
3. Tratar valores estranhos: 5 dias com mais de 500 g de carboidrato, 1 dia sem dados do Fitbit e picos de glicose cortados em 400 mg/dL (limite do sensor).
4. Escolher quais 9 dias seguidos de cada participante usar como D1 a D9.
5. Mover as funções de carga e agregação do notebook para `src/`, para reaproveitar nas próximas etapas.

## Estrutura

```
data/        dados do CGMacros (fora do git; os CSVs ficam em data/raw/)
notebooks/   análises (01_eda.ipynb)
src/         código reaproveitável
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

3. Abra `notebooks/01_eda.ipynb` e rode todas as células.
