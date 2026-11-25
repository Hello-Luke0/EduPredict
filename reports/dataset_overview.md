# Visão geral do dataset escolhido

Gerado por `src/inspect_dataset.py`. Dados reais, sem transformação de modelagem.

## ID 697 — Predict Students' Dropout and Academic Success

- Arquivo: `data/raw/dropout_academic_success/data.csv`
- Dimensão: 4424 linhas × 37 colunas
- Alvo inspecionado: `Target`
- Valores ausentes (total): 0
- Linhas duplicadas: 0

### Colunas

| # | Coluna | Tipo | Únicos | Ausentes |
|---|--------|------|--------|----------|
| 1 | `Marital status` | int64 | 6 | 0 |
| 2 | `Application mode` | int64 | 18 | 0 |
| 3 | `Application order` | int64 | 8 | 0 |
| 4 | `Course` | int64 | 17 | 0 |
| 5 | `Daytime/evening attendance` | int64 | 2 | 0 |
| 6 | `Previous qualification` | int64 | 17 | 0 |
| 7 | `Previous qualification (grade)` | float64 | 101 | 0 |
| 8 | `Nacionality` | int64 | 21 | 0 |
| 9 | `Mother's qualification` | int64 | 29 | 0 |
| 10 | `Father's qualification` | int64 | 34 | 0 |
| 11 | `Mother's occupation` | int64 | 32 | 0 |
| 12 | `Father's occupation` | int64 | 46 | 0 |
| 13 | `Admission grade` | float64 | 620 | 0 |
| 14 | `Displaced` | int64 | 2 | 0 |
| 15 | `Educational special needs` | int64 | 2 | 0 |
| 16 | `Debtor` | int64 | 2 | 0 |
| 17 | `Tuition fees up to date` | int64 | 2 | 0 |
| 18 | `Gender` | int64 | 2 | 0 |
| 19 | `Scholarship holder` | int64 | 2 | 0 |
| 20 | `Age at enrollment` | int64 | 46 | 0 |
| 21 | `International` | int64 | 2 | 0 |
| 22 | `Curricular units 1st sem (credited)` | int64 | 21 | 0 |
| 23 | `Curricular units 1st sem (enrolled)` | int64 | 23 | 0 |
| 24 | `Curricular units 1st sem (evaluations)` | int64 | 35 | 0 |
| 25 | `Curricular units 1st sem (approved)` | int64 | 23 | 0 |
| 26 | `Curricular units 1st sem (grade)` | float64 | 805 | 0 |
| 27 | `Curricular units 1st sem (without evaluations)` | int64 | 11 | 0 |
| 28 | `Curricular units 2nd sem (credited)` | int64 | 19 | 0 |
| 29 | `Curricular units 2nd sem (enrolled)` | int64 | 22 | 0 |
| 30 | `Curricular units 2nd sem (evaluations)` | int64 | 30 | 0 |
| 31 | `Curricular units 2nd sem (approved)` | int64 | 20 | 0 |
| 32 | `Curricular units 2nd sem (grade)` | float64 | 786 | 0 |
| 33 | `Curricular units 2nd sem (without evaluations)` | int64 | 10 | 0 |
| 34 | `Unemployment rate` | float64 | 10 | 0 |
| 35 | `Inflation rate` | float64 | 9 | 0 |
| 36 | `GDP` | float64 | 10 | 0 |
| 37 | `Target` | str | 3 | 0 |

### Distribuição do alvo

| Valor | Contagem | % |
|-------|----------|---|
| `Dropout` | 1421 | 32.12 |
| `Enrolled` | 794 | 17.95 |
| `Graduate` | 2209 | 49.93 |

### Estatísticas das colunas numéricas

| Coluna | Mín | 25% | Mediana | 75% | Máx | Média | Desvio |
|--------|-----|-----|---------|-----|-----|-------|--------|
| `Marital status` | 1.00 | 1.00 | 1.00 | 1.00 | 6.00 | 1.18 | 0.61 |
| `Application mode` | 1.00 | 1.00 | 17.00 | 39.00 | 57.00 | 18.67 | 17.48 |
| `Application order` | 0.00 | 1.00 | 1.00 | 2.00 | 9.00 | 1.73 | 1.31 |
| `Course` | 33.00 | 9085.00 | 9238.00 | 9556.00 | 9991.00 | 8856.64 | 2063.57 |
| `Daytime/evening attendance` | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.89 | 0.31 |
| `Previous qualification` | 1.00 | 1.00 | 1.00 | 1.00 | 43.00 | 4.58 | 10.22 |
| `Previous qualification (grade)` | 95.00 | 125.00 | 133.10 | 140.00 | 190.00 | 132.61 | 13.19 |
| `Nacionality` | 1.00 | 1.00 | 1.00 | 1.00 | 109.00 | 1.87 | 6.91 |
| `Mother's qualification` | 1.00 | 2.00 | 19.00 | 37.00 | 44.00 | 19.56 | 15.60 |
| `Father's qualification` | 1.00 | 3.00 | 19.00 | 37.00 | 44.00 | 22.28 | 15.34 |
| `Mother's occupation` | 0.00 | 4.00 | 5.00 | 9.00 | 194.00 | 10.96 | 26.42 |
| `Father's occupation` | 0.00 | 4.00 | 7.00 | 9.00 | 195.00 | 11.03 | 25.26 |
| `Admission grade` | 95.00 | 117.90 | 126.10 | 134.80 | 190.00 | 126.98 | 14.48 |
| `Displaced` | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.55 | 0.50 |
| `Educational special needs` | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.01 | 0.11 |
| `Debtor` | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.11 | 0.32 |
| `Tuition fees up to date` | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.88 | 0.32 |
| `Gender` | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 0.35 | 0.48 |
| `Scholarship holder` | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.25 | 0.43 |
| `Age at enrollment` | 17.00 | 19.00 | 20.00 | 25.00 | 70.00 | 23.27 | 7.59 |
| `International` | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.02 | 0.16 |
| `Curricular units 1st sem (credited)` | 0.00 | 0.00 | 0.00 | 0.00 | 20.00 | 0.71 | 2.36 |
| `Curricular units 1st sem (enrolled)` | 0.00 | 5.00 | 6.00 | 7.00 | 26.00 | 6.27 | 2.48 |
| `Curricular units 1st sem (evaluations)` | 0.00 | 6.00 | 8.00 | 10.00 | 45.00 | 8.30 | 4.18 |
| `Curricular units 1st sem (approved)` | 0.00 | 3.00 | 5.00 | 6.00 | 26.00 | 4.71 | 3.09 |
| `Curricular units 1st sem (grade)` | 0.00 | 11.00 | 12.29 | 13.40 | 18.88 | 10.64 | 4.84 |
| `Curricular units 1st sem (without evaluations)` | 0.00 | 0.00 | 0.00 | 0.00 | 12.00 | 0.14 | 0.69 |
| `Curricular units 2nd sem (credited)` | 0.00 | 0.00 | 0.00 | 0.00 | 19.00 | 0.54 | 1.92 |
| `Curricular units 2nd sem (enrolled)` | 0.00 | 5.00 | 6.00 | 7.00 | 23.00 | 6.23 | 2.20 |
| `Curricular units 2nd sem (evaluations)` | 0.00 | 6.00 | 8.00 | 10.00 | 33.00 | 8.06 | 3.95 |
| `Curricular units 2nd sem (approved)` | 0.00 | 2.00 | 5.00 | 6.00 | 20.00 | 4.44 | 3.01 |
| `Curricular units 2nd sem (grade)` | 0.00 | 10.75 | 12.20 | 13.33 | 18.57 | 10.23 | 5.21 |
| `Curricular units 2nd sem (without evaluations)` | 0.00 | 0.00 | 0.00 | 0.00 | 12.00 | 0.15 | 0.75 |
| `Unemployment rate` | 7.60 | 9.40 | 11.10 | 13.90 | 16.20 | 11.57 | 2.66 |
| `Inflation rate` | -0.80 | 0.30 | 1.40 | 2.60 | 3.70 | 1.23 | 1.38 |
| `GDP` | -4.06 | -1.70 | 0.32 | 1.79 | 3.51 | 0.00 | 2.27 |
