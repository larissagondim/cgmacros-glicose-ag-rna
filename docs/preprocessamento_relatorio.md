# Pré-processamento – CGMacros: o que fizemos e por quê

## 1. Objetivo

O pré-processamento transforma os arquivos minuto a minuto do CGMacros nas tabelas que a rede neural (RNA) e o algoritmo genético (AG) vão usar. As regras vêm da EDA (`docs/eda_relatorio.md`): glicose do Dexcom, dia válido com cobertura de pelo menos 90% e participante válido com pelo menos 9 dias válidos seguidos.

No fim, saem três tipos de tabela: uma com um dia por linha, outra com os exemplos de treino da rede e uma terceira com os 9 dias de cada participante que o AG vai usar.

## 2. Organização do código

As funções ficam em `src/dados.py`, e o notebook `notebooks/02_preprocessamento.ipynb` só as chama, mostra os resultados e explica as decisões. Separamos assim porque os notebooks da RNA e do AG vão precisar das mesmas funções: com o código num lugar só, uma correção vale para todos. As listas de colunas que entram na rede (`GLICOSE`, `COMPORTAMENTO` e `BIO`) também estão no `dados.py`, e a lista `COMPORTAMENTO` é a mesma que o AG vai usar como genes.

## 3. Do minuto ao dia

A função `resumo_dia` transforma os minutos de um participante em uma linha por dia. O dia é a data do calendário, da meia-noite às 23h59, e para cada um calculamos:

- **glicose (Dexcom):** cobertura (fração dos 1440 minutos com valor), média, desvio padrão, pico e porcentagem do tempo acima de 140 mg/dL;
- **comportamento:** carboidratos, proteína, gordura e fibra somados nas refeições, atividade (soma de `Calories (Activity)`) e horário da última refeição em horas decimais (20,8 = 20h48);
- **número de refeições registradas.**

Três detalhes merecem nota. A função completa o calendário: uma data sem nenhuma linha no arquivo entra com cobertura 0, para que a contagem de dias seguidos não pule o buraco (foi esse o erro silencioso da primeira versão da análise na EDA). Na atividade, a soma usa `min_count=1`, porque por padrão o pandas transforma um dia sem nenhum registro do Fitbit em 0 caloria, quando o certo é dizer que o valor não existe. E o `Amount Consumed` foi ignorado, como decidido na EDA: os macronutrientes são usados como foram registrados.

No participante 001, os 14.730 minutos viram 11 linhas. Os dois dias da ponta têm cobertura de 0,51 e 0,40 e também somas menores (o último tem uma única refeição e 73 g de carboidrato), e ficam de fora pela regra dos 90%.

## 4. Participantes válidos

Aplicando a `resumo_dia` aos 45 participantes, as regras da EDA dão o mesmo resultado: o 007, o 018 e o 026 não têm 9 dias bons seguidos e saem. Ficam 42 participantes, com 493 dias no calendário, dos quais 378 são bons. A conta fecha de um jeito curioso: cada participante válido tem exatamente 9 dias bons.

## 5. Dados do participante

A EDA mostrou que cerca de 90% da variação da glicose diária vem de quem é a pessoa, e que sem essa informação a rede aprenderia que mais carboidrato baixa a glicose. Por isso, cada dia recebe os dados do `bio.csv` do participante, pela função `carregar_bio`. Escolhemos cinco medidas ligadas à glicose: idade, sexo (1 = masculino, 0 = feminino), IMC, HbA1c e glicemia de jejum. Insulina, colesterol e as medidas por picada no dedo ficaram de fora, porque, com só 42 participantes, cada coluna a mais é um número a mais para a rede ajustar com poucos exemplos.

O grupo clínico também é criado aqui, pelos cortes de HbA1c da ADA, mas só para analisar os resultados. Ele não entra na rede, já que a própria HbA1c entra. Depois da junção, os 42 participantes ficam divididos em 14 por grupo, e a glicose média dos dias bons é de 121, 137 e 167 mg/dL, os mesmos valores da EDA.

## 6. Valores estranhos

Como todo participante válido tem exatamente 9 dias bons, remover qualquer dia bom tiraria a pessoa do projeto. Isso orientou as duas decisões desta etapa.

Cinco dias têm mais de 500 g de carboidrato (a mediana é 188 g), nos participantes 004, 021 e 036, provavelmente por erro de registro ou refeição duplicada. Em vez de remover esses dias, limitamos o valor a 500 g.

O participante 033 tem um dia bom sem atividade: em 25/04, o Fitbit parou de registrar. É justamente o 9º dos 9 dias bons dele. A atividade desse dia foi preenchida com a média dos outros dias bons do próprio participante (2585 kcal), um valor dentro da faixa normal dele, entre cerca de 2000 e 3000 kcal.

Os 9 dias com pico de 400 mg/dL ficaram como estão. Esse é o limite do sensor, então registramos apenas que o pico real pode ter sido maior. Depois desses tratamentos, nenhum dia bom tem valor vazio.

## 7. Tabela da rede

Cada exemplo de treino é um dia bom *d*. A entrada tem a glicose dos dias anteriores (média, desvio, pico e % acima de 140), o comportamento de *d* e os dados do participante; o alvo é a glicose média de *d*. A glicose do próprio dia *d* nunca entra na entrada, senão a rede estaria vendo a resposta. Um dia só vira exemplo se ele e todos os dias anteriores usados forem bons.

Não sabíamos se a rede precisaria de 2 ou 3 dias de histórico, então montamos as duas versões:

| | 2 dias anteriores | 3 dias anteriores |
|---|---|---|
| exemplos | 294 (7 por participante) | 252 (6 por participante) |
| variáveis de entrada | 19 | 23 |
| exemplos por grupo | 98 | 84 |

Com 3 dias, a rede tem mais histórico, mas cada participante perde um exemplo a mais no começo. A escolha vai ser feita no treino da rede. Como as duas versões não têm os mesmos dias, a comparação precisa ser feita nos dias que existem nas duas.

## 8. Bloco D1 a D9

O AG e a avaliação final trabalham com 9 dias seguidos de cada participante: D1 a D6 são observados e, de D7 a D9, o AG propõe o comportamento. A função `montar_blocos` pega os primeiros 9 dias bons seguidos de cada participante e os numera de 1 a 9. São 42 blocos, todos com dias bons, em datas seguidas e sem valores vazios. Como cada participante tem exatamente 9 dias bons, o bloco são os próprios dias bons dele.

## 9. Tabelas geradas

As tabelas ficam em `data/processed/`, fora do git junto com os dados brutos, e são lidas com `carregar_tabela(nome)`, que devolve a data e o grupo nos tipos certos.

| Arquivo | Linhas | Conteúdo |
|---|---|---|
| `dias.csv` | 493 | todos os dias dos 42 participantes válidos, com a coluna `bom` |
| `blocos_d1_d9.csv` | 378 | os 9 dias de cada participante, para o AG e a avaliação |
| `dataset_rna_2.csv` | 294 | exemplos da rede com 2 dias anteriores |
| `dataset_rna_3.csv` | 252 | exemplos da rede com 3 dias anteriores |

Testamos a gravação e a leitura das quatro tabelas, e todas voltam idênticas.

## 10. Limites e cuidados para as próximas etapas

Alguns limites vêm desta etapa:

- um lanche depois da meia-noite conta para o dia seguinte, então o horário da última refeição pode subestimar o quanto a pessoa comeu tarde. Aceitamos isso para que o dia da refeição seja o mesmo dia da glicose;
- o teto de 500 g e o preenchimento da atividade do 033 são estimativas, e não valores medidos;
- o `Amount Consumed` foi ignorado, então uma refeição comida pela metade conta como inteira;
- os dados do participante vêm de um único exame, feito no início do estudo.

Um cuidado para a etapa da rede: os dias D7 a D9 de cada participante também aparecem como exemplos de treino. Na avaliação da recomendação, a rede consultada para um participante precisa ter sido treinada sem os dados dele. Caso contrário, ela já "conhece" a glicose real do D9, e o resultado fica otimista. A validação por participante (GroupKFold) resolve isso, desde que seja usada também nessa etapa.
