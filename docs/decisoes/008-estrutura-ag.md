# 008 – Estrutura do AG

- **Status:** decidida (aprovada em 27/11/2026), a confirmar com a equipe
- **Afeta:** implementação do recomendador (notebook do AG)

---

## Decisão

| Componente | Escolha                                                                   |
|------------|---------------------------------------------------------------------------|
| Genes      | 18 reais (6 variáveis × D7 a D9)                                          |
| Seleção    | Torneio                                                                   |
| Elitismo   | Sim                                                                       |
| Cruzamento | Aritmético                                                                |
| Mutação    | Gaussiana                                                                 |
| Limites    | Decisão 007 (valores cortados nos limites)                                |
| Fitness    | Menor glicose prevista no D9, mais penalidades (a definir) - o AG minimza |

- As 6 variáveis são as de `COMPORTAMENTO`: carboidrato, proteína,
  gordura, fibra, atividade e horário da última refeição.
- Uma execução do AG **por participante**, usando o conjunto de redes
  treinado sem os dados dele (decisão 004).

---

## Por que

- Os genes são números contínuos, então a codificação real é a mais natural.
- O torneio não depende da escala da fitness. Aqui as diferenças entre
  planos são de poucos mg/dL numa glicose de cerca de 130 mg/dL.
- O elitismo garante que o melhor plano encontrado não se perde.
- O cruzamento aritmético faz uma mistura dos pais, e a mistura
  de dois valores dentro dos limites continua dentro dos limites.
- A mutação gaussiana faz ajustes pequenos e frequentes ao redor
  do valor atual.

---

## Alternativas

**Codificação binária**
- Prós: operadores clássicos e simples.
- Contras: precisão limitada pelo número de bits; convergência mais lenta
  para 18 variáveis contínuas.

**Seleção por roleta**
- Prós: clássica.
- Contras: com diferenças pequenas de fitness, fica quase aleatória
  e exige reescalar a fitness.

**Cruzamento uniforme**
- Prós: troca genes inteiros entre os pais.
- Contras: não cria valores intermediários, então o ajuste fino
  depende só da mutação.

**Mutação não uniforme**
- Prós: o passo diminui ao longo das gerações, o que ajuda no ajuste fino.
- Contras: mais um parâmetro. Pode entrar depois, se a gaussiana não bastar.

**Sem elitismo**
- Prós: um parâmetro a menos.
- Contras: pode perder o melhor plano de uma geração para a outra.

---

## Impacto

- São 40 a 42 execuções (uma por participante), repetidas com várias
  sementes (decisão 009). O resultado é a média e o desvio do efeito.
- Avaliar a população inteira de uma vez na rede, encadeando D7, D8 e D9,
  deve manter cada execução rápida. O tempo exato fica por medir.
- A fitness usa a glicose média prevista no D9 (decisão 003).

---

## Riscos

- Como a rede costuma responder de forma simples, o AG tende a empurrar
  os genes para os limites. Isso é esperado e deve ser relatado.
- Convergência prematura com população pequena.
- O AG explora os erros da rede (ver decisões 006 e 007).

---

## Pendências

1. Tamanho da população e número de gerações.
2. Taxas de cruzamento e de mutação, e o desvio da mutação gaussiana.
3. Tamanho do torneio e quantos indivíduos o elitismo preserva.
4. Critério de parada (gerações fixas ou estagnação).
5. Penalidades da fitness: por exemplo, por distância ao hábito
   e por discordância entre as redes (decisão 002).
6. Encadeamento D7 → D8 → D9 (teste ainda a fazer).

---

## Registro da decisão

- [x] Genes reais, torneio, elitismo, cruzamento aritmético, mutação gaussiana
- [ ] Codificação binária
- [ ] Seleção por roleta
- [ ] Cruzamento uniforme

**Data:** 27/11/2026
**Quem decidiu:** Laura
**Confirmada com a equipe:** ainda não