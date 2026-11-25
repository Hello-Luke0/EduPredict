# Estatísticas da EDA

Gerado por `src/eda.py`. Apenas análise descritiva, sem transformação de dados.

## Estrutura e qualidade

- Dimensão: 4424 linhas × 37 colunas.
- Atributos usados na EDA: 33 (3 indicadores macro excluídos).
- Valores ausentes: 0.
- Linhas duplicadas: 0.

- 1º semestre: `approved > enrolled` em 0 de 4424 linhas.
- 2º semestre: `approved > enrolled` em 0 de 4424 linhas.
- `Admission grade`: mínimo 95.00, máximo 190.00.
- `Previous qualification (grade)`: mínimo 95.00, máximo 190.00.
- `Curricular units 1st sem (grade)`: mínimo 0.00, máximo 18.88.
- `Curricular units 2nd sem (grade)`: mínimo 0.00, máximo 18.57.
- `Age at enrollment`: mínimo 17, máximo 70, acima de 40 anos: 225 linhas.
- `Daytime/evening attendance`: valores observados [0, 1].
- `Displaced`: valores observados [0, 1].
- `Educational special needs`: valores observados [0, 1].
- `Debtor`: valores observados [0, 1].
- `Tuition fees up to date`: valores observados [0, 1].
- `Gender`: valores observados [0, 1].
- `Scholarship holder`: valores observados [0, 1].
- `International`: valores observados [0, 1].

## Distribuição do alvo

| Classe | n | % |
|---|---|---|
| Dropout | 1421 | 32.12 |
| Enrolled | 794 | 17.95 |
| Graduate | 2209 | 49.93 |

## Estatísticas numéricas

| Variavel | min | 25% | 50% | 75% | max | mean | std |
|---|---|---|---|---|---|---|---|
| Age at enrollment | 17.00 | 19.00 | 20.00 | 25.00 | 70.00 | 23.27 | 7.59 |
| Admission grade | 95.00 | 117.90 | 126.10 | 134.80 | 190.00 | 126.98 | 14.48 |
| Previous qualification (grade) | 95.00 | 125.00 | 133.10 | 140.00 | 190.00 | 132.61 | 13.19 |
| Curricular units 1st sem (enrolled) | 0.00 | 5.00 | 6.00 | 7.00 | 26.00 | 6.27 | 2.48 |
| Curricular units 1st sem (approved) | 0.00 | 3.00 | 5.00 | 6.00 | 26.00 | 4.71 | 3.09 |
| Curricular units 1st sem (grade) | 0.00 | 11.00 | 12.29 | 13.40 | 18.88 | 10.64 | 4.84 |
| Curricular units 2nd sem (enrolled) | 0.00 | 5.00 | 6.00 | 7.00 | 23.00 | 6.23 | 2.20 |
| Curricular units 2nd sem (approved) | 0.00 | 2.00 | 5.00 | 6.00 | 20.00 | 4.44 | 3.01 |
| Curricular units 2nd sem (grade) | 0.00 | 10.75 | 12.20 | 13.33 | 18.57 | 10.23 | 5.21 |

## Médias por classe

| Target | Age at enrollment | Admission grade | Previous qualification (grade) | Curricular units 1st sem (enrolled) | Curricular units 1st sem (approved) | Curricular units 1st sem (grade) | Curricular units 2nd sem (enrolled) | Curricular units 2nd sem (approved) | Curricular units 2nd sem (grade) |
|---|---|---|---|---|---|---|---|---|---|
| Dropout | 26.07 | 124.96 | 131.11 | 5.82 | 2.55 | 7.26 | 5.78 | 1.94 | 5.90 |
| Enrolled | 22.37 | 125.53 | 131.21 | 5.96 | 4.32 | 11.13 | 5.94 | 4.06 | 11.12 |
| Graduate | 21.78 | 128.79 | 134.08 | 6.67 | 6.23 | 12.64 | 6.63 | 6.18 | 12.70 |

## Medianas por classe

| Target | Age at enrollment | Admission grade | Previous qualification (grade) | Curricular units 1st sem (enrolled) | Curricular units 1st sem (approved) | Curricular units 1st sem (grade) | Curricular units 2nd sem (enrolled) | Curricular units 2nd sem (approved) | Curricular units 2nd sem (grade) |
|---|---|---|---|---|---|---|---|---|---|
| Dropout | 23.00 | 123.60 | 133.10 | 6.00 | 2.00 | 10.93 | 6.00 | 0.00 | 0.00 |
| Enrolled | 20.00 | 124.10 | 130.00 | 6.00 | 5.00 | 12.00 | 6.00 | 4.00 | 12.00 |
| Graduate | 19.00 | 127.40 | 133.10 | 6.00 | 6.00 | 13.00 | 6.00 | 6.00 | 13.00 |

## Fatores binários

| Fator | Valor | n | % Dropout | % Enrolled | % Graduate |
|---|---|---|---|---|---|
| Daytime/evening attendance | 0 | 483 | 42.86 | 15.53 | 41.61 |
| Daytime/evening attendance | 1 | 3941 | 30.80 | 18.24 | 50.95 |
| Displaced | 0 | 1998 | 37.64 | 18.07 | 44.29 |
| Displaced | 1 | 2426 | 27.58 | 17.85 | 54.58 |
| Educational special needs | 0 | 4373 | 32.11 | 17.91 | 49.99 |
| Educational special needs | 1 | 51 | 33.33 | 21.57 | 45.10 |
| Debtor | 0 | 3921 | 28.28 | 17.95 | 53.76 |
| Debtor | 1 | 503 | 62.03 | 17.89 | 20.08 |
| Tuition fees up to date | 0 | 528 | 86.55 | 7.95 | 5.49 |
| Tuition fees up to date | 1 | 3896 | 24.74 | 19.30 | 55.95 |
| Gender | 0 | 2868 | 25.10 | 16.98 | 57.91 |
| Gender | 1 | 1556 | 45.05 | 19.73 | 35.22 |
| Scholarship holder | 0 | 3325 | 38.71 | 19.97 | 41.32 |
| Scholarship holder | 1 | 1099 | 12.19 | 11.83 | 75.98 |
| International | 0 | 4314 | 32.20 | 17.85 | 49.95 |
| International | 1 | 110 | 29.09 | 21.82 | 49.09 |

## Cursos mais frequentes

| Course | n | % Dropout | % Enrolled | % Graduate |
|---|---|---|---|---|
| 9500.00 | 766.00 | 15.40 | 13.05 | 71.54 |
| 9147.00 | 380.00 | 35.26 | 28.42 | 36.32 |
| 9238.00 | 355.00 | 18.31 | 11.83 | 69.86 |
| 9085.00 | 337.00 | 26.71 | 22.26 | 51.04 |
| 9773.00 | 331.00 | 30.51 | 10.27 | 59.21 |
| 9991.00 | 268.00 | 50.75 | 20.15 | 29.10 |
| 9670.00 | 268.00 | 35.45 | 17.91 | 46.64 |
| 9254.00 | 252.00 | 38.10 | 16.27 | 45.63 |

## Modos de candidatura mais frequentes

| Application mode | n | % Dropout | % Enrolled | % Graduate |
|---|---|---|---|---|
| 1.00 | 1708.00 | 20.20 | 17.56 | 62.24 |
| 17.00 | 872.00 | 29.36 | 18.23 | 52.41 |
| 39.00 | 785.00 | 55.41 | 15.41 | 29.17 |
| 43.00 | 312.00 | 36.86 | 24.04 | 39.10 |
| 44.00 | 213.00 | 29.58 | 26.29 | 44.13 |
| 7.00 | 139.00 | 61.15 | 5.04 | 33.81 |
| 18.00 | 124.00 | 36.29 | 12.90 | 50.81 |
| 42.00 | 77.00 | 44.16 | 14.29 | 41.56 |

## Maiores correlações (Pearson)

| Variavel 1 | Variavel 2 | Correlacao |
|---|---|---|
| Curricular units 1st sem (enrolled) | Curricular units 2nd sem (enrolled) | 0.94 |
| Curricular units 1st sem (approved) | Curricular units 2nd sem (approved) | 0.90 |
| Curricular units 1st sem (grade) | Curricular units 2nd sem (grade) | 0.84 |
| Curricular units 1st sem (evaluations) | Curricular units 2nd sem (evaluations) | 0.78 |
| Curricular units 1st sem (enrolled) | Curricular units 1st sem (approved) | 0.77 |
| Curricular units 2nd sem (approved) | Curricular units 2nd sem (grade) | 0.76 |
| Curricular units 1st sem (approved) | Curricular units 2nd sem (enrolled) | 0.73 |
| Curricular units 2nd sem (enrolled) | Curricular units 2nd sem (approved) | 0.70 |
| Curricular units 1st sem (approved) | Curricular units 1st sem (grade) | 0.70 |
| Curricular units 1st sem (approved) | Curricular units 2nd sem (grade) | 0.69 |

## Figuras

- `reports/figures/eda_01_target_distribution.png`
- `reports/figures/eda_02_approved_2nd_sem_por_target.png`
- `reports/figures/eda_03_grade_2nd_sem_por_target.png`
- `reports/figures/eda_04_correlation_heatmap.png`
- `reports/figures/eda_05_taxas_binarias_por_target.png`
