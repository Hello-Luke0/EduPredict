"""Pré-processamento reproduzível do EduPredict (UCI ID 697).

Uso:
    python src/preprocessing.py

Define a tipagem dos atributos, o split treino/teste estratificado e o
``ColumnTransformer`` compartilhado. Ajusta o pré-processador apenas no
conjunto de treino, valida o resultado e grava ``reports/preprocessing.md``.
Não treina modelos.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "raw" / "dropout_academic_success" / "data.csv"
REPORT_PATH = ROOT / "reports" / "preprocessing.md"

TARGET = "Target"
CLASSES = ["Dropout", "Enrolled", "Graduate"]
EXCLUDED_FEATURES = ["Unemployment rate", "Inflation rate", "GDP"]

NUMERIC_FEATURES = [
    "Daytime/evening attendance",
    "Displaced",
    "Educational special needs",
    "Debtor",
    "Tuition fees up to date",
    "Gender",
    "Scholarship holder",
    "International",
    "Application order",
    "Previous qualification (grade)",
    "Admission grade",
    "Age at enrollment",
    "Curricular units 1st sem (credited)",
    "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (evaluations)",
    "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)",
    "Curricular units 1st sem (without evaluations)",
    "Curricular units 2nd sem (credited)",
    "Curricular units 2nd sem (enrolled)",
    "Curricular units 2nd sem (evaluations)",
    "Curricular units 2nd sem (approved)",
    "Curricular units 2nd sem (grade)",
    "Curricular units 2nd sem (without evaluations)",
]

CATEGORICAL_FEATURES = [
    "Marital status",
    "Application mode",
    "Course",
    "Previous qualification",
    "Nacionality",
    "Mother's qualification",
    "Father's qualification",
    "Mother's occupation",
    "Father's occupation",
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
RANDOM_STATE = 42
TEST_SIZE = 0.2


def load_dataset() -> pd.DataFrame:
    """Carrega a base bruta normalizando apenas os nomes das colunas."""
    frame = pd.read_csv(DATA_PATH, sep=";", encoding="utf-8-sig")
    frame.columns = [str(column).strip() for column in frame.columns]
    return frame


def build_preprocessor() -> ColumnTransformer:
    """Monta o pré-processador compartilhado pelos dois modelos."""
    numeric_pipeline = Pipeline(steps=[("scaler", StandardScaler())])
    categorical_pipeline = Pipeline(
        steps=[
            (
                "onehot",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            )
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )


def split_dataset(
    frame: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Divide em treino/teste antes de qualquer ajuste de pré-processamento."""
    features = frame[FEATURES]
    target = frame[TARGET]
    return train_test_split(
        features,
        target,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=target,
    )


def class_table(target: pd.Series, name: str) -> list[str]:
    """Tabela Markdown com contagem e percentual por classe."""
    counts = target.value_counts().reindex(CLASSES, fill_value=0)
    shares = counts / counts.sum() * 100
    lines = [
        f"**{name}**",
        "",
        "| Classe | n | % |",
        "|--------|---|---|",
    ]
    for label in CLASSES:
        lines.append(f"| `{label}` | {int(counts[label])} | {shares[label]:.2f} |")
    lines.append("")
    return lines


def feature_table(names: list[str], description: str) -> list[str]:
    """Tabela Markdown de atributos."""
    lines = [
        f"**{description} ({len(names)})**",
        "",
        "| # | Atributo |",
        "|---|----------|",
    ]
    for position, name in enumerate(names, start=1):
        lines.append(f"| {position} | `{name}` |")
    lines.append("")
    return lines


def main() -> None:
    """Executa a divisão, ajusta o pré-processador no treino e valida."""
    frame = load_dataset()
    missing_columns = set(FEATURES) - set(frame.columns)
    extra_columns = set(frame.columns) - set(FEATURES) - {TARGET} - set(EXCLUDED_FEATURES)
    if missing_columns:
        raise ValueError(f"Colunas ausentes na base: {sorted(missing_columns)}")
    if extra_columns:
        raise ValueError(f"Colunas não classificadas: {sorted(extra_columns)}")

    X_train, X_test, y_train, y_test = split_dataset(frame)

    preprocessor = build_preprocessor()
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    train_index = set(X_train.index)
    test_index = set(X_test.index)
    overlap = train_index & test_index
    if overlap:
        raise ValueError(f"Índices em comum entre treino e teste: {len(overlap)}")

    if np.isnan(X_train_transformed).any() or np.isnan(X_test_transformed).any():
        raise ValueError("Valores NaN encontrados após o pré-processamento.")

    if X_train_transformed.shape[0] != len(X_train):
        raise ValueError("Número de linhas transformadas difere do treino.")
    if X_test_transformed.shape[0] != len(X_test):
        raise ValueError("Número de linhas transformadas difere do teste.")
    if X_train_transformed.shape[1] != X_test_transformed.shape[1]:
        raise ValueError("Treino e teste têm dimensões transformadas diferentes.")

    full_shares = frame[TARGET].value_counts(normalize=True).reindex(CLASSES) * 100
    train_shares = y_train.value_counts(normalize=True).reindex(CLASSES) * 100
    test_shares = y_test.value_counts(normalize=True).reindex(CLASSES) * 100
    max_deviation = float((train_shares - full_shares).abs().max())
    if max_deviation > 0.5:
        raise ValueError(
            f"Desvio de proporção de classe acima do tolerado: {max_deviation:.2f} p.p."
        )

    encoder = preprocessor.named_transformers_["categorical"].named_steps["onehot"]
    onehot_names = encoder.get_feature_names_out(CATEGORICAL_FEATURES)

    sections = [
        "# Pré-processamento",
        "",
        "Gerado por `src/preprocessing.py`. Nenhum modelo foi treinado nesta fase.",
        "",
        "## Decisões",
        "",
        "- Alvo `Target` mantido como texto, em 3 classes, sem recodificação.",
        "- 33 atributos selecionados na Fase 1; 3 indicadores macroeconômicos excluídos.",
        "- 24 atributos numéricos padronizados com `StandardScaler`.",
        "- 9 atributos nominais codificados com `OneHotEncoder(handle_unknown=\"ignore\")`.",
        "- Sem imputação: o dataset não tem valores ausentes.",
        "- Sem reamostragem ou balanceamento nesta fase.",
        "- Pré-processador compartilhado pelos dois modelos, garantindo comparação justa.",
        "",
        "## Atributos numéricos",
        "",
        *feature_table(NUMERIC_FEATURES, "Numéricos padronizados"),
        "## Atributos nominais",
        "",
        *feature_table(CATEGORICAL_FEATURES, "Nominais codificados com one-hot"),
        "## Atributos excluídos",
        "",
        "| Atributo | Motivo |",
        "|----------|--------|",
        *[
            f"| `{name}` | Indicador macroeconômico com disponibilidade temporal incerta no momento da previsão. |"
            for name in EXCLUDED_FEATURES
        ],
        "",
        "## Divisão treino/teste",
        "",
        f"- `test_size` = {TEST_SIZE:.0%}; `random_state` = {RANDOM_STATE}; `stratify=y`.",
        f"- Treino: {len(X_train)} linhas; teste: {len(X_test)} linhas.",
        f"- Sobreposição de índices entre treino e teste: {len(overlap)}.",
        f"- Desvio máximo das proporções de classe (treino vs. base): {max_deviation:.4f} p.p.",
        "",
        *class_table(y_train, "Treino"),
        *class_table(y_test, "Teste"),
        "## Dimensões após o pré-processamento",
        "",
        f"- Colunas numéricas: {len(NUMERIC_FEATURES)}.",
        f"- Colunas geradas pelo one-hot: {len(onehot_names)}.",
        f"- Dimensão final: {X_train_transformed.shape[1]} colunas.",
        f"- Matriz de treino: {X_train_transformed.shape[0]} × {X_train_transformed.shape[1]}.",
        f"- Matriz de teste: {X_test_transformed.shape[0]} × {X_test_transformed.shape[1]}.",
        f"- Valores NaN após transformação: {int(np.isnan(X_train_transformed).sum() + np.isnan(X_test_transformed).sum())}.",
        "",
        "## Controle de vazamento",
        "",
        "- O split ocorre antes de qualquer ajuste de codificador ou escalonador.",
        "- `fit_transform` é aplicado somente em `X_train`; `X_test` recebe apenas `transform`.",
        "- Categorias ausentes no treino são ignoradas por `handle_unknown=\"ignore\"`.",
        "- Nenhum atributo derivado do alvo e nenhuma informação do teste é usada no ajuste.",
        "- Nenhuma reamostragem foi aplicada.",
        "",
    ]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Treino: {X_train.shape} | Teste: {X_test.shape}")
    print(f"Treino por classe: {y_train.value_counts().reindex(CLASSES).to_dict()}")
    print(f"Teste por classe: {y_test.value_counts().reindex(CLASSES).to_dict()}")
    print(f"Dimensao transformada: {X_train_transformed.shape[1]}")
    print(f"Relatorio: {REPORT_PATH.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
