# Pré-processamento

Gerado por `src/preprocessing.py`. Nenhum modelo foi treinado nesta fase.

## Decisões

- Alvo `Target` mantido como texto, em 3 classes, sem recodificação.
- 33 atributos selecionados na Fase 1; 3 indicadores macroeconômicos excluídos.
- 24 atributos numéricos padronizados com `StandardScaler`.
- 9 atributos nominais codificados com `OneHotEncoder(handle_unknown="ignore")`.
- Sem imputação: o dataset não tem valores ausentes.
- Sem reamostragem ou balanceamento nesta fase.
- Pré-processador compartilhado pelos dois modelos, garantindo comparação justa.

## Atributos numéricos

**Numéricos padronizados (24)**

| # | Atributo |
|---|----------|
| 1 | `Daytime/evening attendance` |
| 2 | `Displaced` |
| 3 | `Educational special needs` |
| 4 | `Debtor` |
| 5 | `Tuition fees up to date` |
| 6 | `Gender` |
| 7 | `Scholarship holder` |
| 8 | `International` |
| 9 | `Application order` |
| 10 | `Previous qualification (grade)` |
| 11 | `Admission grade` |
| 12 | `Age at enrollment` |
| 13 | `Curricular units 1st sem (credited)` |
| 14 | `Curricular units 1st sem (enrolled)` |
| 15 | `Curricular units 1st sem (evaluations)` |
| 16 | `Curricular units 1st sem (approved)` |
| 17 | `Curricular units 1st sem (grade)` |
| 18 | `Curricular units 1st sem (without evaluations)` |
| 19 | `Curricular units 2nd sem (credited)` |
| 20 | `Curricular units 2nd sem (enrolled)` |
| 21 | `Curricular units 2nd sem (evaluations)` |
| 22 | `Curricular units 2nd sem (approved)` |
| 23 | `Curricular units 2nd sem (grade)` |
| 24 | `Curricular units 2nd sem (without evaluations)` |

## Atributos nominais

**Nominais codificados com one-hot (9)**

| # | Atributo |
|---|----------|
| 1 | `Marital status` |
| 2 | `Application mode` |
| 3 | `Course` |
| 4 | `Previous qualification` |
| 5 | `Nacionality` |
| 6 | `Mother's qualification` |
| 7 | `Father's qualification` |
| 8 | `Mother's occupation` |
| 9 | `Father's occupation` |

## Atributos excluídos

| Atributo | Motivo |
|----------|--------|
| `Unemployment rate` | Indicador macroeconômico com disponibilidade temporal incerta no momento da previsão. |
| `Inflation rate` | Indicador macroeconômico com disponibilidade temporal incerta no momento da previsão. |
| `GDP` | Indicador macroeconômico com disponibilidade temporal incerta no momento da previsão. |

## Divisão treino/teste

- `test_size` = 20%; `random_state` = 42; `stratify=y`.
- Treino: 3539 linhas; teste: 885 linhas.
- Sobreposição de índices entre treino e teste: 0.
- Desvio máximo das proporções de classe (treino vs. base): 0.0075 p.p.

**Treino**

| Classe | n | % |
|--------|---|---|
| `Dropout` | 1137 | 32.13 |
| `Enrolled` | 635 | 17.94 |
| `Graduate` | 1767 | 49.93 |

**Teste**

| Classe | n | % |
|--------|---|---|
| `Dropout` | 284 | 32.09 |
| `Enrolled` | 159 | 17.97 |
| `Graduate` | 442 | 49.94 |

## Dimensões após o pré-processamento

- Colunas numéricas: 24.
- Colunas geradas pelo one-hot: 209.
- Dimensão final: 233 colunas.
- Matriz de treino: 3539 × 233.
- Matriz de teste: 885 × 233.
- Valores NaN após transformação: 0.

## Controle de vazamento

- O split ocorre antes de qualquer ajuste de codificador ou escalonador.
- `fit_transform` é aplicado somente em `X_train`; `X_test` recebe apenas `transform`.
- Categorias ausentes no treino são ignoradas por `handle_unknown="ignore"`.
- Nenhum atributo derivado do alvo e nenhuma informação do teste é usada no ajuste.
- Nenhuma reamostragem foi aplicada.
