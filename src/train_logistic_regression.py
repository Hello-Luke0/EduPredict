"""Treino e avaliação do Modelo 1 (Logistic Regression).

Uso:
    python src/train_logistic_regression.py

Usa a divisão e o pré-processador definidos em ``src/preprocessing.py``.
Ajusta o pipeline apenas no treino, avalia no teste e grava relatório,
métricas em JSON e a matriz de confusão.
"""

from __future__ import annotations

import platform
import warnings
from pathlib import Path

import numpy as np
import sklearn
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
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
FIG_PATH = ROOT / "reports" / "figures" / "model1_logreg_confusion_matrix.png"
REPORT_PATH = ROOT / "reports" / "model1_logistic_regression.md"
METRICS_PATH = ROOT / "reports" / "model1_metrics.json"

MODEL_NAME = "Logistic Regression"
CONFIG = {
    "C": 1.0,
    "solver": "lbfgs",
    "max_iter": 2000,
    "class_weight": None,
    "random_state": RANDOM_STATE,
}


def build_pipeline() -> Pipeline:
    """Monta o pipeline com o pré-processador compartilhado e o classificador."""
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("classifier", LogisticRegression(**CONFIG)),
        ]
    )


def main() -> None:
    """Executa treino, avaliação e geração dos artefatos."""
    frame = load_dataset()
    X_train, X_test, y_train, y_test = split_dataset(frame)

    pipeline = build_pipeline()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        pipeline.fit(X_train, y_train)

    convergence_warnings = [
        str(item.message)
        for item in caught
        if issubclass(item.category, ConvergenceWarning)
    ]
    classifier = pipeline.named_steps["classifier"]
    n_iter = int(np.ravel(classifier.n_iter_)[0])
    converged = not convergence_warnings and n_iter < CONFIG["max_iter"]

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
        extra_metrics={
            "convergence": {
                "converged": converged,
                "n_iter": n_iter,
                "warnings": convergence_warnings,
            }
        },
    )

    save_confusion_matrix(metrics, f"Matriz de confusão — {MODEL_NAME}", FIG_PATH)
    write_metrics_json(metrics, METRICS_PATH)

    convergence_section = [
        "## Convergência",
        "",
        f"- Iterações até parar: {n_iter} de {CONFIG['max_iter']}.",
        f"- Convergiu sem aviso: {'sim' if converged else 'não'}.",
    ]
    if convergence_warnings:
        convergence_section.extend(
            ["", "Avisos de convergência:", "", *[f"- {item}" for item in convergence_warnings]]
        )
    convergence_section.append("")

    config_lines = [
        f"- Algoritmo: {MODEL_NAME}.",
        f"- Hiperparâmetros: `C={CONFIG['C']}`, `solver='{CONFIG['solver']}'`, "
        f"`max_iter={CONFIG['max_iter']}`, `class_weight={CONFIG['class_weight']}`, "
        f"`random_state={CONFIG['random_state']}`.",
        "- Observação: `penalty` não é passado (depreciado no scikit-learn 1.8+); o padrão é L2.",
        "- Pré-processamento: o mesmo `ColumnTransformer` da Fase 3, ajustado somente no treino.",
        f"- Divisão: {len(X_train)} treino / {len(X_test)} teste (estratificada, seed {RANDOM_STATE}).",
        f"- Ambiente: Python {platform.python_version()}, scikit-learn {sklearn.__version__}.",
    ]

    report = render_report(
        model_name=MODEL_NAME,
        phase_label="Modelo 1",
        intro="Gerado por `src/train_logistic_regression.py`. Resultados reais no conjunto de teste.",
        config_lines=config_lines,
        extra_sections=convergence_section,
        metrics=metrics,
        figure_name=FIG_PATH.name,
        metrics_path=METRICS_PATH.relative_to(ROOT).as_posix(),
        limitations=[
            "Modelo de referência, sem ajuste de hiperparâmetros nem reamostragem.",
            "Desbalanceamento real pode reduzir o recall das classes minoritárias.",
            "Coeficientes não devem ser interpretados como efeito causal.",
            "Não deve ser usado para decisões reais sobre estudantes.",
        ],
    )
    REPORT_PATH.write_text(report, encoding="utf-8")

    print(f"Acurácia: {metrics['accuracy']:.4f}")
    print(f"Macro F1: {metrics['macro']['f1']:.4f} | Weighted F1: {metrics['weighted']['f1']:.4f}")
    print(f"Convergiu: {converged} (n_iter={n_iter})")
    print(f"Relatório: {REPORT_PATH.relative_to(ROOT).as_posix()}")
    print(f"Matriz: {FIG_PATH.relative_to(ROOT).as_posix()}")
    print(f"Métricas: {METRICS_PATH.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
