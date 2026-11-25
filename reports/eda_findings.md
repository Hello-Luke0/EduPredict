# Achados da análise exploratória (EDA)

**Dataset:** Predict Students' Dropout and Academic Success (UCI ID 697) — 4.424 estudantes × 36 atributos.
**Alvo:** `Target` (`Dropout`, `Enrolled`, `Graduate`).
**Escopo:** análise descritiva; sem transformação de dados, testes de hipótese ou treinamento.

Tabelas completas: [`eda_stats.md`](eda_stats.md). Figuras: [`figures/`](figures/).

## Qualidade e estrutura

- 0 valores ausentes e 0 linhas duplicadas.
- 33 atributos analisados (3 indicadores macroeconômicos omitidos por disponibilidade temporal incerta).
- `approved ≤ enrolled` em todas as 4.424 linhas, nos dois semestres.
- Notas dentro das faixas esperadas (`Admission grade` e `Previous qualification (grade)`: 95–190; notas semestrais: 0–18,88).
- `Age at enrollment`: 17 a 70 anos; 225 estudantes acima de 40 anos.
- Fatores binários com domínio {0, 1} consistente.

## Achados

### 1. As três classes são desbalanceadas

**Observação:** `Graduate` = 2.209 (49,93%), `Dropout` = 1.421 (32,12%), `Enrolled` = 794 (17,95%). Um classificador que sempre prevê a classe majoritária acertaria ~49,9%.
**Hipótese:** acurácia isolada pode mascarar desempenho ruim nas classes minoritárias; a avaliação deve incluir precisão, recall e F1 com média macro e/ou weighted.
**Figura:** `figures/eda_01_target_distribution.png`.

### 2. Aprovações no 2º semestre separam fortemente as classes

**Observação:** unidades aprovadas no 2º semestre — mediana 0 (`Dropout`), 4 (`Enrolled`) e 6 (`Graduate`); médias 1,94 / 4,06 / 6,18.
**Hipótese:** o desempenho no semestre corrente concentra informação sobre o desfecho; é o sinal mais forte entre os analisados, mas mede o mesmo período da previsão e não estabelece causalidade.
**Figura:** `figures/eda_02_approved_2nd_sem_por_target.png`.

### 3. A nota do 2º semestre acompanha a mesma separação

**Observação:** nota média do 2º semestre — mediana 0,00 (`Dropout`), 12,00 (`Enrolled`) e 13,00 (`Graduate`); médias 5,90 / 11,12 / 12,70.
**Hipótese:** notas baixas no semestre corrente estão associadas ao desfecho de evasão; a mediana 0,00 em `Dropout` sugere estudantes sem avaliação aprovada no período.
**Figura:** `figures/eda_03_grade_2nd_sem_por_target.png`.

### 4. Fatores financeiros e administrativos apresentam associações marcantes

**Observação (taxa de `Dropout` / `Graduate`):**

| Fator | Valor 0 | Valor 1 |
|-------|---------|---------|
| `Tuition fees up to date` | 86,55% / 5,49% | 24,74% / 55,95% |
| `Debtor` | 28,28% / 53,76% | 62,03% / 20,08% |
| `Scholarship holder` | 38,71% / 41,32% | 12,19% / 75,98% |

**Hipótese:** situação financeira (mensalidades em atraso e dívida) e apoio financeiro (bolsa) estão associados ao desfecho. A direção não pode ser interpretada como causa: o débito pode ser consequência, e não origem, do abandono.
**Figura:** `figures/eda_05_taxas_binarias_por_target.png`.

### 5. Perfil demográfico e turno também se associam ao desfecho

**Observação (taxa de `Dropout` / `Graduate`):** `Gender = 1` (masculino) 45,05% / 35,22% vs `Gender = 0` (feminino) 25,10% / 57,91%; turno noturno (0) 42,86% / 41,61% vs diurno (1) 30,80% / 50,95%.
**Hipótese:** estudantes do sexo masculino e do turno noturno evadem mais neste recorte. Diferenças de composição entre cursos e turnos podem explicar parte do padrão; requer análise controlada (fora do escopo descritivo).
**Figura:** `figures/eda_05_taxas_binarias_por_target.png`.

### 6. As variáveis semestrais são altamente redundantes

**Observação:** correlações de Pearson entre 1º e 2º semestre — `enrolled` 0,94, `approved` 0,90, `grade` 0,84, `evaluations` 0,78. `Admission grade` e `Previous qualification (grade)` correlacionam 0,60.
**Hipótese:** há forte colinearidade entre os pares de semestre; modelos lineares podem ter coeficientes instáveis. Isso deve orientar o pré-processamento (Fase 3), sem remoção automática nesta etapa.
**Figura:** `figures/eda_04_correlation_heatmap.png`.

## Observações vs hipóteses

Os números acima são **observações** dos dados. As **hipóteses** são interpretações plausíveis e não foram testadas. Nenhuma relação deve ser lida como causal.

## Limitações

- Dados observacionais de uma única instituição; não generalizáveis sem validação externa.
- `Enrolled` é um estado intermediário que pode mudar depois da coleta.
- Associações podem refletir variáveis de confusão não observadas (ex.: curso, turno, condição socioeconômica).
- A EDA é descritiva; não há testes de significância nesta fase.

## Implicações para a Fase 3

- Definir estratégia para o desbalanceamento na avaliação (macro/weighted), não necessariamente reamostragem.
- Tratar categóricas codificadas como categóricas (não como números contínuos) e padronizar apenas onde o algoritmo exigir.
- Considerar a colinearidade entre variáveis semestrais ao interpretar coeficientes.
- Manter a divisão treino/teste antes de qualquer ajuste de imputação/escala (não há ausentes, mas a regra permanece).
