# Comparação e seleção de modelo

Gerado por `src/compare_models.py` a partir das métricas reais dos treinos, **sem retreinar**. Ambos os modelos usam o mesmo conjunto de teste.

## Método

- Conjunto de teste: 885 exemplos (split 80/20, `random_state=42`, estratificado).
- Métrica principal: **F1 macro**; secundárias: recall por classe e F1 weighted.
- Acurácia é reportada, mas não decide a escolha (classes desbalanceadas).
- Diferenças (Δ) em pontos percentuais, calculadas como Logistic Regression − Random Forest.

## Métricas agregadas

| Métrica | Logistic Regression | Random Forest | Δ (p.p.) |
|---|---|---|---|
| Acurácia | 0.7661 | 0.7616 | +0.45 |
| Precisão macro | 0.7086 | 0.6981 | +1.05 |
| Recall macro | 0.6803 | 0.6557 | +2.46 |
| F1 macro | 0.6882 | 0.6603 | +2.80 |
| Precisão weighted | 0.7507 | 0.7383 | +1.25 |
| Recall weighted | 0.7661 | 0.7616 | +0.45 |
| F1 weighted | 0.7539 | 0.7388 | +1.52 |

Erros totais: Logistic Regression = 207; Random Forest = 211 (de 885 exemplos de teste).

Referência: classe majoritária (`Graduate`) acertaria 49.94% dos casos.

## Métricas por classe

| Classe | Suporte | Logistic Regression P | Logistic Regression R | Logistic Regression F1 | Random Forest P | Random Forest R | Random Forest F1 | Δ F1 (p.p.) |
|---|---|---|---|---|---|---|---|---|
| `Dropout` | 284 | 0.7810 | 0.7535 | 0.7670 | 0.7834 | 0.7641 | 0.7736 | -0.66 |
| `Enrolled` | 159 | 0.5364 | 0.3711 | 0.4387 | 0.5250 | 0.2642 | 0.3515 | +8.72 |
| `Graduate` | 442 | 0.8084 | 0.9163 | 0.8590 | 0.7860 | 0.9389 | 0.8557 | +0.33 |

## Impacto dos erros (FP/FN)

| Classe | Logistic Regression FN | Random Forest FN | Logistic Regression FP | Random Forest FP |
|---|---|---|---|---|
| `Dropout` | 70 | 67 | 60 | 60 |
| `Enrolled` | 100 | 117 | 51 | 38 |
| `Graduate` | 37 | 27 | 96 | 113 |

Leitura orientada ao contexto educacional: um **falso negativo de `Dropout`** significa não sinalizar um estudante que acabou evadindo — tende a ser o erro mais custoso. Já `Enrolled` é uma classe intermediária ambígua, e o colapso dela em `Graduate`/`Dropout` também reduz a utilidade do modelo para apoio preventivo.

- Logistic Regression: 70 falsos negativos e 60 falsos positivos para `Dropout`.
- Random Forest: 67 falsos negativos e 60 falsos positivos para `Dropout`.

## Métrica principal

A escolha do **F1 macro** se justifica porque as classes são desbalanceadas (`Graduate` ≈ 50%) e a acurácia é dominada por essa classe. O F1 macro dá peso igual às três classes e combina precisão e recall, penalizando o desempenho fraco em `Enrolled`. Acurácia e F1 weighted são mantidos como contexto, não como critério único.

## Seleção

**Modelo selecionado para este estudo: Logistic Regression.**

- F1 macro: 0.6882 vs 0.6603 (Δ de 2.80 p.p.).
- Erros totais no teste: 207 vs 211.
- Vantagem modesta: a diferença equivale a poucas decisões no conjunto de teste; não há alegação de superioridade universal.

Desempenho por classe:

- `Dropout`: melhor F1 com **Random Forest** (0.7736 vs 0.7670).
- `Enrolled`: melhor F1 com **Logistic Regression** (0.4387 vs 0.3515).
- `Graduate`: melhor F1 com **Logistic Regression** (0.8590 vs 0.8557).

Trade-off: Random Forest pode ser preferível se o objetivo for outro critério de custo ou uma métrica específica; para o critério definido aqui, o modelo selecionado é Logistic Regression.

## Limitações

- Um único split 80/20; não há intervalos de confiança nem repetição.
- Ambos são modelos de referência, sem tuning de hiperparâmetros.
- `Enrolled` tem desempenho fraco nos dois modelos (classe intermediária ambígua).
- Dados observacionais de uma instituição; sem validação externa.
- Resultados não devem orientar decisões reais sobre estudantes e não implicam causalidade.

## Possíveis melhorias (não executadas)

- Validação cruzada/repetida para estimar variabilidade.
- Ajuste de hiperparâmetros apenas no treino.
- `class_weight` ou custos assimétricos, se o objetivo for priorizar `Dropout`.
- Calibração de probabilidades e análise de custo dos erros.

## Artefatos

- `reports/model1_metrics.json`
- `reports/model2_metrics.json`
- `reports/figures/model_comparison_f1_por_classe.png`

