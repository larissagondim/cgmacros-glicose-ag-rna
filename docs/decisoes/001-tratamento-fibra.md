# 001 – Fibra dos participantes 16 e 19

- **Status:** proposta documentada, não aplicada (decisão final com a equipe)
- **Data:** 27/11/2026
- **Afeta:** pré-processamento (`src/dados.py` e notebook 02), depois RNA e AG

---

## Decisão proposta

Excluir os participantes **16** e **19** (opção A).
Resultado: 40 participantes e 360 dias bons.

---

## O problema

A fibra de `snack` e `dinner` desses dois participantes tem valores impossíveis.

|                            | 16 e 19 | Demais |
|----------------------------|---------|--------|
| Maior fibra numa refeição  | 2.830 g |  53 g  |
| Maior fibra num dia        | 3.321 g |  58 g  |
| Refeições com mais de 60 g |   25    |   0    |

- O dicionário do dataset documenta fibra de **0 a 176 g** por refeição.
- São 17 dias bons com mais de 100 g, todos nesses dois (16: 8 dias, 19: 9 dias).
- Café da manhã e almoço deles estão normais. O erro está em `snack` e `dinner`.

### Outros sinais nos mesmos dois participantes

- `Amount Consumed` vale 1 a 5 (nos demais, cerca de 100; dicionário: 0 a 100).
- Uma refeição do 16 tem 508 g de gordura (dicionário: 0 a 176 g).
- Não é erro de unidade: dividir a fibra por 1.000 não dá valores plausíveis.
- A causa do erro é desconhecida.

---

## Por que excluir

1. A fibra não parece ser o único campo comprometido nesses dois.
2. O AG aproveita qualquer erro: um hábito falso vira uma recomendação falsa.
3. O custo é pequeno (ver impacto abaixo).
4. Nenhum valor estimado entra no projeto.

---

## Impacto: com e sem a exclusão

### Tamanho dos dados

|                   |   Com    |    Sem   |
|-------------------|----------|----------|
| Participantes     |   42     |    40    |
| Dias bons         |   378    |    360   |
| Exemplos (2 dias) |   294    |    280   |
| Exemplos (3 dias) |   252    |    240   |
| Grupos*           | 14/14/14 | 13/13/14 |

\*saudável / pré-diabetes / DM2

### Fibra como entrada da rede

|                |  Com  | Sem  |
|----------------|-------|------|
| Média (g/dia)  | 77,7  | 16,4 |
| Desvio padrão  | 338,6 |  9,1 |
| Máximo (g/dia) | 3.321 |  58  |

- 96,9% da variação da fibra vem desses dois participantes.
- Com eles, a fibra dos outros 40 fica quase constante depois de normalizada.
  A rede não consegue aproveitar a variável.

### Relações com a glicose (dentro da mesma pessoa)

|             |  Com   |  Sem   |
|-------------|--------|--------|
| Fibra       | 0,013  | 0,076  |
| Carboidrato | 0,163  | 0,165  |
| Atividade   | −0,254 | −0,256 |

- A exclusão não muda os achados de carboidrato e atividade.
- A fibra tem relação fraca com a glicose nos dois cenários.

### Outros efeitos

- **Baseline** ("hoje = ontem"): MAE de 8,25 para 8,43 mg/dL (2 dias)
  e de 7,85 para 8,04 mg/dL (3 dias). Os dois são fáceis de prever,
  então tirá-los deixa a comparação um pouco mais exigente.
- **Representatividade:** os dois são mulheres com IMC alto (45,9 e 36,4).
  Ainda restam 10 participantes com IMC de 35 ou mais.

---

## Alternativas

**0. Manter como está**
- Prós: não altera o pipeline.
- Contras: a fibra fica dominada por dois participantes; o AG propõe
  mudanças sobre um hábito falso.

**B. Excluir só os dias com fibra ruim**
- Inviável: o 19 perderia os 9 dias e o 16 ficaria com 1,
  o que na prática equivale à opção A.

**C. Tirar a fibra do modelo**
- Prós: mantém os 42 participantes; muda uma linha em `COMPORTAMENTO`;
  a fibra já tem pouco efeito linear.
- Contras: perde a fibra confiável dos outros 40; o AG passa de 18 para 15 genes.

**D. Corrigir o total do dia (teto ou imputação)**
- Prós: mantém todos os participantes e variáveis.
- Contras: valor inventado em 17 dias; no 19, todos os dias.

**F1. Descartar a fibra das refeições fora de 0 a 176 g**
- Prós: regra objetiva; mantém os 42 participantes.
- Contras: fibra subestimada; sobra um dia do 19 com 187 g;
  outros campos continuam sem verificação.

**F2. Usar só café da manhã e almoço desses dois**
- Prós: usa só o registro que parece confiável.
- Contras: fibra baixa demais (mediana de 4 g no 16); regra arbitrária.

---

## Riscos

- A causa do erro é desconhecida.
- Os outros macronutrientes desses dois não foram verificados.
- É uma exclusão por qualidade do registro, não por cobertura do Dexcom.
  Deve aparecer no relatório como critério adicional.
- Os números acima vêm das tabelas atuais, sem a RNA treinada.

---

## Pendências

1. Teste de sensibilidade, depois da RNA: treinar com e sem os dois.
2. Conferir outros campos fora das faixas do dicionário
   (ex.: refeição de 472 g de carboidrato no participante 21).
3. Alinhar com a equipe.
4. Atualizar `README.md` (raiz do projeto) e o relatório de pré-processamento (citam 42 participantes).

---

## Onde conferir

- `data/raw/CGMacros-016/CGMacros-016.csv` e `CGMacros-019.csv`, coluna `Fiber`
- `data/processed/blocos_d1_d9.csv`, coluna `fibra`
- `data/raw/DataDictionary_CGMacros-00X.csv`

---

## Como aplicar (se a opção A for aprovada)

Em `src/dados.py`:

```python
EXCLUIR_FIBRA = [16, 19]  # decisão 001
```

No notebook 02, depois de calcular `validos`:

```python
validos = [p for p in validos if p not in EXCLUIR_FIBRA]
```

Depois, rodar o notebook inteiro e conferir os números da tabela de tamanho.
As tabelas ficam fora do git: regenerar ou repassar para a equipe.

---

## Registro da decisão

- [ ] A – excluir 16 e 19
- [ ] C – tirar a fibra
- [ ] F1 – descartar refeições fora da faixa
- [ ] F2 – só café da manhã e almoço
- [ ] 0 – manter como está

**Data:**
**Quem decidiu:**
**Justificativa final:**