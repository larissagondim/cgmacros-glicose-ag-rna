# Pré-processamento – CGMacros: o que fizemos e por quê

## 1. Objetivo

Esta etapa transforma os arquivos minuto a minuto do CGMacros nas tabelas que a rede neural (RNA) e o algoritmo genético (AG) vão usar. As regras são as da EDA (`docs/eda_relatorio.md`), ou seja, glicose do Dexcom, dia válido com cobertura de pelo menos 90% e participante válido com pelo menos 9 dias válidos seguidos. O resultado é uma tabela com um dia por linha, os exemplos de treino da rede e os 9 dias de cada participante que o AG vai usar.

## 2. Organização do código

As funções ficam em `src/dados.py`, e o notebook `notebooks/02_preprocessamento.ipynb` só as chama, mostra os resultados e explica as decisões. Separamos assim porque os notebooks da RNA e do AG vão precisar das mesmas funções, e com o código num lugar só uma correção vale para todos. As listas de colunas que entram na rede (`GLICOSE`, `COMPORTAMENTO` e `BIO`) também estão no `dados.py`, e a lista `COMPORTAMENTO` é a mesma que o AG vai usar como genes.

## 3. Do minuto ao dia

A função `resumo_dia` transforma os minutos de um participante em uma linha por dia. O dia é a data do calendário, da meia-noite às 23h59, e para cada um calculamos:

- **glicose (Dexcom):** cobertura (fração dos 1440 minutos com valor), média, desvio padrão, pico e porcentagem do tempo acima de 140 mg/dL;
- **comportamento:** carboidratos, proteína, gordura e fibra somados nas refeições, atividade (soma de `Calories (Activity)`) e horário da última refeição em horas decimais (20,8 = 20h48);
- **número de refeições registradas.**

A função também completa o calendário. Uma data sem nenhuma linha no arquivo entra com cobertura 0, e assim a contagem de dias seguidos não pula o buraco, o erro silencioso que a primeira versão da análise cometeu na EDA. Na atividade, a soma usa `min_count=1`. Sem isso, o pandas transforma um dia em que o Fitbit não registrou nada em 0 caloria, quando o certo é dizer que o valor não existe. O `Amount Consumed` foi ignorado, como decidido na EDA, e os macronutrientes entram como foram registrados.

No participante 001, os 14.730 minutos viram 11 linhas. Os dois dias da ponta têm cobertura de 0,51 e 0,40 e também somas menores (o último tem uma única refeição e 73 g de carboidrato), e ficam de fora pela regra dos 90%.

## 4. Participantes válidos

Aplicando a `resumo_dia` aos 45 participantes, as regras da EDA dão o mesmo resultado: o 007, o 018 e o 026 não têm 9 dias bons seguidos e saem. Ficam 42 participantes, com 493 dias no calendário, dos quais 378 são bons. São exatamente 9 dias bons por participante, um detalhe que pesa nas decisões das seções 6 e 8.

## 5. Dados do participante

A EDA mostrou que cerca de 90% da variação da glicose diária vem de quem é a pessoa, e que sem essa informação a rede aprenderia que mais carboidrato baixa a glicose. Por isso, cada dia recebe os dados do `bio.csv` do participante, pela função `carregar_bio`. Escolhemos cinco medidas ligadas à glicose: idade, sexo (1 = masculino, 0 = feminino), IMC, HbA1c e glicemia de jejum. Insulina, colesterol e as medidas por picada no dedo ficaram de fora, porque, com só 42 participantes, cada coluna a mais é um número a mais para a rede ajustar com poucos exemplos.

O grupo clínico também é criado aqui, pelos cortes de HbA1c da ADA, mas só para analisar os resultados. Ele não entra na rede, já que a própria HbA1c entra. Depois da junção, os 42 participantes ficam divididos em 14 por grupo, e a glicose média dos dias bons é de 121, 137 e 167 mg/dL, os mesmos valores da EDA.

## 6. Valores estranhos

Com só 9 dias bons por pessoa, apagar qualquer um deles tira o participante do projeto. Por isso corrigimos os valores em vez de remover dias.

Cinco dias têm mais de 500 g de carboidrato (a mediana é 188 g), nos participantes 004, 021 e 036, provavelmente por erro de registro ou refeição duplicada. Nesses dias, o carboidrato foi limitado a 500 g.

No participante 033, o Fitbit parou de registrar em 25/04, o último dos 9 dias bons dele. A atividade desse dia foi preenchida com a média dos outros dias bons do próprio 033 (2585 kcal), que fica dentro da faixa normal dele, de cerca de 2000 a 3000 kcal.

Os 9 dias com pico de 400 mg/dL ficaram como estão, porque esse é o limite do sensor e não há como saber o valor real. Depois desses ajustes, nenhum dia bom tem valor vazio.

## 7. Tabela da rede

Cada exemplo de treino é um dia bom *d*. A entrada tem a glicose dos dias anteriores (média, desvio, pico e % acima de 140), o comportamento de *d* e os dados do participante; o alvo é a glicose média de *d*. A glicose do próprio dia *d* nunca entra na entrada, senão a rede estaria vendo a resposta. Um dia só vira exemplo se ele e todos os dias anteriores usados forem bons.

Não sabíamos se a rede precisaria de 2 ou 3 dias de histórico, então montamos as duas versões:

| | 2 dias anteriores | 3 dias anteriores |
|---|---|---|
| exemplos | 294 (7 por participante) | 252 (6 por participante) |
| variáveis de entrada | 19 | 23 |
| exemplos por grupo | 98 | 84 |

Com 3 dias a rede tem mais histórico, mas cada participante perde um exemplo a mais no começo. A escolha fica para o treino da rede, comparando o erro só nos dias que existem nas duas versões.

## 8. Bloco D1 a D9

O AG e a avaliação final trabalham com 9 dias seguidos de cada participante. De D1 a D6 o comportamento é observado, e de D7 a D9 é o AG que o propõe. A função `montar_blocos` pega os primeiros 9 dias bons seguidos de cada pessoa e os numera de 1 a 9. Aqui ela acaba pegando todos os dias bons, mas foi escrita para o caso geral, caso a regra de dia bom mude. São 42 blocos em datas seguidas e sem valores vazios.

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

- Um lanche depois da meia-noite conta para o dia seguinte, então o horário da última refeição pode subestimar o quanto a pessoa comeu tarde. Aceitamos isso para que o dia da refeição seja o mesmo dia da glicose.
- O teto de 500 g e a atividade preenchida do 033 são estimativas, e não valores medidos.
- Como o `Amount Consumed` foi ignorado, uma refeição comida pela metade conta como inteira.
- Os dados do participante vêm de um único exame, feito no início do estudo.

Os dias D7 a D9 de cada participante também aparecem como exemplos de treino da rede. Quando o AG for recomendar algo para uma pessoa, a rede que ele consulta tem que ter sido treinada sem os dados dela, senão já "conhece" a glicose real do D9 e o resultado sai otimista. A validação por participante (GroupKFold) resolve isso, desde que seja usada também nessa hora.
