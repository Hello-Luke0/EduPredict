"""Treino e avaliação do Modelo 2 (Random Forest Classifier).

Uso:
    python src/train_random_forest.py

Usa a mesma divisão, os mesmos atributos e o mesmo pré-processador do
Modelo 1. Ajusta o pipeline apenas no treino, avalia no teste e grava
relatório, métricas em JSON e a matriz de confusão.
"""

from __future__ import annotations

import platform
from pathlib import Path

import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from evaluation import (
    compute_metrics,
    render_report,
    save_confusion_matrix,
    write_metrics_json,
)
from preprocessing import (
    CLASSES,
    RANDOM_STATE,
    TEST_SIZE,
    build_preprocessor,
    load_dataset,
    split_dataset,
)

ROOT = Path(__file__).resolve().parent.parent
FIG_PATH = ROOT / "reports" / "figures" / "model2_rf_confusion_matrix.png"
REPORT_PATH = ROOT / "reports" / "model2_random_forest.md"
METRICS_PATH = ROOT / "reports" / "model2_metrics.json"

MODEL_NAME = "Random Forest"
CONFIG = {
    "n_estimators": 100,
    "criterion": "gini",
    "max_depth": None,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "max_features": "sqrt",
    "bootstrap": True,
    "class_weight": None,
    "random_state": RANDOM_STATE,
    "n_jobs": -1,
}


def build_pipeline() -> Pipeline:
    """Monta o pipeline com o pré-processador compartilhado e o classificador."""
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("classifier", RandomForestClassifier(**CONFIG)),
        ]
    )


def main() -> None:
    """Executa treino, avaliação e geração dos artefatos."""
    frame = load_dataset()
    X_train, X_test, y_train, y_test = split_dataset(frame)

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    metrics = compute_metrics(
        y_true=y_test,
        y_pred=y_pred,
        labels=CLASSES,
        model_name=MODEL_NAME,
        config=CONFIG,
        environment={
            "python": platform.python_version(),
            "scikit_learn": sklearn.__version__,
        },
        split={
            "test_size": TEST_SIZE,
            "random_state": RANDOM_STATE,
            "n_train": int(len(X_train)),
            "n_test": int(len(X_test)),
        },
    )

    save_confusion_matrix(metrics, f"Matriz de confusão — {MODEL_NAME}", FIG_PATH)
    write_metrics_json(metrics, METRICS_PATH)

    config_lines = [
        f"- Algoritmo: {MODEL_NAME} Classifier.",
        "- Hiperparâmetros: "
        + ", ".join(f"`{key}={value}`" for key, value in CONFIG.items())
        + ".",
        "- Pré-processamento: o mesmo `ColumnTransformer` da Fase 3, ajustado somente no treino.",
        f"- Divisão: {len(X_train)} treino / {len(X_test)} teste (estratificada, seed {RANDOM_STATE}).",
        f"- Ambiente: Python {platform.python_version()}, scikit-learn {sklearn.__version__}.",
    ]

    extra_sections = [
        "## Observações",
        "",
        "- Baseline sem ajuste de hiperparâmetros, para comparação justa com o Modelo 1.",
        "- Mesma divisão e mesmos 33 atributos do Modelo 1.",
        "- `StandardScaler` mantido por uniformidade; árvores não dependem de escala.",
        "",
    ]

    report = render_report(
        model_name=f"{MODEL_NAME} Classifier",
        phase_label="Modelo 2",
        intro="Gerado por `src/train_random_forest.py`. Resultados reais no conjunto de teste.",
        config_lines=config_lines,
        extra_sections=extra_sections,
        metrics=metrics,
        figure_name=FIG_PATH.name,
        metrics_path=METRICS_PATH.relative_to(ROOT).as_posix(),
        limitations=[
            "Modelo de referência, sem ajuste de hiperparâmetros nem reamostragem.",
            "Árvores podem sobreajustar o treino; o erro de treino não é medido nesta fase.",
            "Desbalanceamento real pode reduzir o recall das classes minoritárias.",
            "Importância de variáveis não é analisada nesta fase.",
            "Não deve ser usado para decisões reais sobre estudantes.",
        ],
    )
    REPORT_PATH.write_text(report, encoding="utf-8")

    print(f"Acurácia: {metrics['accuracy']:.4f}")
    print(f"Macro F1: {metrics['macro']['f1']:.4f} | Weighted F1: {metrics['weighted']['f1']:.4f}")
    print(f"Relatório: {REPORT_PATH.relative_to(ROOT).as_posix()}")
    print(f"Matriz: {FIG_PATH.relative_to(ROOT).as_posix()}")
    print(f"Métricas: {METRICS_PATH.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
