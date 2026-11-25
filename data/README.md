# Dados

Este diretório documenta a origem, a licença e o uso dos dados do projeto.

> **Status:** Fase 1 concluída. Dois candidatos do UCI foram baixados e inspecionados; o dataset **ID 697** foi escolhido e a tarefa de classificação está definida abaixo, com evidências do arquivo real em [`reports/dataset_overview.md`](../reports/dataset_overview.md). O candidato descartado está documentado na seção final deste arquivo.

## Dataset escolhido

- **Nome:** Predict Students' Dropout and Academic Success
- **ID UCI:** 697
- **Autoria:** Valentim Realinho, Mónica Vieira Martins, Jorge Machado e Luís Baptista — Instituto Politécnico de Portalegre
- **URL:** https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success
- **DOI:** [10.24432/C5MC89](https://doi.org/10.24432/C5MC89)
- **Versão:** doação de 12/12/2021 (versão corrente do repositório UCI)
- **Data de acesso:** 2026-11-25
- **Licença:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/legalcode)
- **Redistribuição permitida?** Sim, com atribuição adequada. Por isso o arquivo `data.csv` é versionado no repositório.

### Arquivos e integridade

| Arquivo | Tamanho | SHA-256 |
|---------|---------|---------|
| `data/raw/dropout_academic_success.zip` (não versionado) | 533.344 bytes | `E90E55FD65EC462AE283EBEB2CCA409319E3460ED898D8754F62FB35CC83A65D` |
| `data/raw/dropout_academic_success/data.csv` (versionado) | 533.230 bytes | `3EF126DE5CEFFF26EB11FBB4237F1A1401CB64B488E2F1D598C23CEDEB4C45AE` |

### Formato

- Separador `;`, codificação UTF-8 com BOM.
- 4.424 linhas × 37 colunas (36 atributos + `Target`).
- Sem valores ausentes e sem linhas duplicadas (verificado).
- Um nome de coluna chega com espaço em branco (`Daytime/evening attendance<tab>`); será normalizado com `str.strip()` no carregamento.

## Problema de classificação

**Pergunta:** atributos conhecidos até o fim do 2º semestre permitem classificar o desfecho acadêmico de um estudante do ensino superior em *Dropout*, *Enrolled* ou *Graduate*?

- **Variável-alvo:** `Target` (categórica, 3 classes).
- **Classes observadas:**

  | Classe | Contagem | % |
  |--------|----------|---|
  | `Dropout` | 1.421 | 32,12% |
  | `Enrolled` | 794 | 17,95% |
  | `Graduate` | 2.209 | 49,93% |

- **Momento da previsão:** **fim do 2º semestre**. Nesse ponto, os dados de matrícula, do 1º e do 2º semestre são passado. O desfecho (`Target`) só é conhecido ao fim da duração normal do curso — portanto os atributos **precedem** o alvo e não há vazamento temporal.
- **Por que manter 3 classes:** é a formulação original do dataset, preserva a distinção entre `Enrolled` (ainda cursando) e `Graduate`, e permite discutir métricas macro/weighted (Fases 4–6). O desbalanceamento (49,9% / 32,1% / 18,0%) é real e será tratado na avaliação.

**Limitação a registrar:** `Enrolled` é um estado intermediário que pode se tornar `Graduate` ou `Dropout` depois; o rótulo é um retrato no momento da coleta.

## Atributos (33 selecionados)

Disponibilidade relativa ao momento da previsão (fim do 2º semestre).

### Perfil e candidatura — disponíveis na matrícula (21)

| # | Atributo | Tipo | Observação |
|---|----------|------|------------|
| 1 | Marital status | categórica (código) | estado civil |
| 2 | Application mode | categórica (código) | via de ingresso |
| 3 | Application order | ordinal | ordem de preferência (0 = 1ª opção) |
| 4 | Course | categórica (código) | curso |
| 5 | Daytime/evening attendance | binária | turno |
| 6 | Previous qualification | categórica (código) | qualificação anterior |
| 7 | Previous qualification (grade) | contínua | nota da qualificação anterior (0–200) |
| 8 | Nacionality | categórica (código) | nacionalidade |
| 9 | Mother's qualification | categórica (código) | escolaridade da mãe |
| 10 | Father's qualification | categórica (código) | escolaridade do pai |
| 11 | Mother's occupation | categórica (código) | ocupação da mãe |
| 12 | Father's occupation | categórica (código) | ocupação do pai |
| 13 | Admission grade | contínua | nota de admissão (0–200) |
| 14 | Displaced | binária | deslocado |
| 15 | Educational special needs | binária | necessidades educativas especiais |
| 16 | Debtor | binária | devedor |
| 17 | Tuition fees up to date | binária | mensalidades em dia |
| 18 | Gender | binária | gênero |
| 19 | Scholarship holder | binária | bolsista |
| 20 | Age at enrollment | inteira | idade na matrícula |
| 21 | International | binária | internacional |

### 1º semestre — disponíveis ao fim do 1º semestre (6)

| # | Atributo | Tipo |
|---|----------|------|
| 22 | Curricular units 1st sem (credited) | inteira |
| 23 | Curricular units 1st sem (enrolled) | inteira |
| 24 | Curricular units 1st sem (evaluations) | inteira |
| 25 | Curricular units 1st sem (approved) | inteira |
| 26 | Curricular units 1st sem (grade) | contínua |
| 27 | Curricular units 1st sem (without evaluations) | inteira |

### 2º semestre — disponíveis ao fim do 2º semestre (6)

| # | Atributo | Tipo |
|---|----------|------|
| 28 | Curricular units 2nd sem (credited) | inteira |
| 29 | Curricular units 2nd sem (enrolled) | inteira |
| 30 | Curricular units 2nd sem (evaluations) | inteira |
| 31 | Curricular units 2nd sem (approved) | inteira |
| 32 | Curricular units 2nd sem (grade) | contínua |
| 33 | Curricular units 2nd sem (without evaluations) | inteira |

### Atributos excluídos (3)

| Atributo | Motivo da exclusão |
|----------|--------------------|
| Unemployment rate | Indicador macroeconômico anual; publicação pode ser posterior ao fim do 2º semestre, o que violaria a disponibilidade temporal. |
| Inflation rate | Idem. |
| GDP | Idem. |

Não há coluna de identificador pessoal no arquivo. Nenhum atributo é cópia direta do alvo. Caso o momento de previsão fosse outro (ex.: após a divulgação dos indicadores), os três atributos macro poderiam ser reavaliados.

## Alternativa descartada — ID 320 (Student Performance)

| Critério | Evidência inspecionada |
|----------|------------------------|
| Tamanho | 395 linhas (matemática) e 649 (português), 33 colunas |
| Alvo | `G3` (nota final 0–20) |
| Problema | `G1`/`G2` são as notas dos períodos anteriores e altamente correlacionadas com `G3` (alerta do próprio UCI); sem elas o sinal preditivo é fraco e o resultado pouco informativo |
| Sobreposição | 382 estudantes aparecem nos dois arquivos, exigindo cuidado extra |
| Conclusão | Válido, porém menor e com maior risco de vazamento/proxy e de resultados triviais |

Registro de integridade: `student-mat.csv` = `E47F9EE225E1EE6E69B7564E6DAC7123E80B8486677FE111F351964CEF5DEC80`; `student-por.csv` = `A7594A11D7771C0EFE1A740824E0E833DA9C4CAD07C39A9766A874575563FB3F`.

## Como obter novamente

```powershell
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri "https://archive.ics.uci.edu/static/public/697/predict+students+dropout+and+academic+success.zip" -OutFile "data/raw/dropout_academic_success.zip"
Expand-Archive -LiteralPath "data/raw/dropout_academic_success.zip" -DestinationPath "data/raw/dropout_academic_success" -Force
Get-FileHash -Algorithm SHA256 -LiteralPath "data/raw/dropout_academic_success/data.csv"
```

Alternativa descartada (ID 320):

```powershell
Invoke-WebRequest -Uri "https://archive.ics.uci.edu/static/public/320/student+performance.zip" -OutFile "data/raw/student_performance.zip"
Expand-Archive -LiteralPath "data/raw/student_performance.zip" -DestinationPath "data/raw/student_performance" -Force
Expand-Archive -LiteralPath "data/raw/student_performance/student.zip" -DestinationPath "data/raw/student_performance/files" -Force
```

## Estrutura local

```text
data/
├── raw/
│   ├── dropout_academic_success/
│   │   └── data.csv          # dataset escolhido (versionado, CC BY 4.0)
│   └── student_performance/  # inspeção do candidato descartado (não versionado)
└── README.md
```

Apenas o arquivo do dataset escolhido é versionado. ZIPs e os arquivos do ID 320 permanecem locais e ignorados pelo Git.

## Citação

Realinho, V., Vieira Martins, M., Machado, J., & Baptista, L. (2021). *Predict Students' Dropout and Academic Success* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89
