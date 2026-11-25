"""Utilitários compartilhados de avaliação dos modelos do EduPredict.

Concentra cálculo de métricas, matriz de confusão, JSON e relatório em
Markdown, para que os scripts de treino não dupliquem código. Não ajusta
modelos nem acessa os dados além dos rótulos e previsões recebidos.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)


def markdown_table(rows: list[list[str]], headers: list[str]) -> list[str]:
    """Tabela Markdown simples."""
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join(["---"] * len(headers)) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def compute_metrics(
    *,
    y_true,
    y_pred,
    labels: list[str],
    model_name: str,
    config: dict,
    environment: dict,
    split: dict,
    extra_metrics: dict | None = None,
) -> dict:
    """Calcula acurácia, macro/weighted, por classe e matriz de confusão."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true e y_pred têm tamanhos diferentes.")

    accuracy = float(accuracy_score(y_true, y_pred))
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, average="macro", zero_division=0
    )
    weighted_p, weighted_r, weighted_f1, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, average="weighted", zero_division=0
    )
    report_dict = classification_report(
        y_true,
        y_pred,
        labels=labels,
        target_names=labels,
        output_dict=True,
        zero_division=0,
    )
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    cm_normalized = cm / cm.sum(axis=1, keepdims=True) * 100

    majority_label = y_true.mode()[0]
    majority_accuracy = float((y_true == majority_label).mean() * 100)

    metrics: dict = {
        "model": model_name,
        "config": config,
        "environment": environment,
        "split": split,
    }
    if extra_metrics:
        metrics.update(extra_metrics)
    metrics.update(
        {
            "accuracy": accuracy,
            "macro": {
                "precision": float(macro_p),
                "recall": float(macro_r),
                "f1": float(macro_f1),
            },
            "weighted": {
                "precision": float(weighted_p),
                "recall": float(weighted_r),
                "f1": float(weighted_f1),
            },
            "per_class": {
                label: {
                    "precision": float(report_dict[label]["precision"]),
                    "recall": float(report_dict[label]["recall"]),
                    "f1": float(report_dict[label]["f1-score"]),
                    "support": int(report_dict[label]["support"]),
                }
                for label in labels
            },
            "confusion_matrix": {
                "labels": list(labels),
                "counts": cm.tolist(),
                "row_percent": cm_normalized.tolist(),
            },
            "majority_baseline": {
                "class": str(majority_label),
                "accuracy": majority_accuracy,
            },
        }
    )
    return metrics


def save_confusion_matrix(metrics: dict, title: str, path: Path) -> None:
    """Salva a matriz de confusão com contagens e percentual por linha."""
    labels = metrics["confusion_matrix"]["labels"]
    cm = np.asarray(metrics["confusion_matrix"]["counts"])
    shares = np.asarray(metrics["confusion_matrix"]["row_percent"])

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    image = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Previsto")
    ax.set_ylabel("Real")
    ax.set_title(title)
    for i in range(len(labels)):
        for j in range(len(labels)):
            count = int(cm[i, j])
            color = "white" if count > cm.max() / 2 else "black"
            ax.text(
                j,
                i,
                f"{count}\n({shares[i, j]:.1f}%)",
                ha="center",
                va="center",
                color=color,
                fontsize=9,
            )
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def write_metrics_json(metrics: dict, path: Path) -> None:
    """Grava as métricas em JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")


def render_report(
    *,
    model_name: str,
    phase_label: str,
    intro: str,
    config_lines: list[str],
    extra_sections: list[str],
    metrics: dict,
    figure_name: str,
    metrics_path: str,
    limitations: list[str],
) -> str:
    """Monta o relatório Markdown de um modelo a partir das métricas."""
    labels = metrics["confusion_matrix"]["labels"]
    per_class_rows = [
        [
            f"`{label}`",
            f"{metrics['per_class'][label]['precision']:.4f}",
            f"{metrics['per_class'][label]['recall']:.4f}",
            f"{metrics['per_class'][label]['f1']:.4f}",
            str(metrics["per_class"][label]["support"]),
        ]
        for label in labels
    ]
    cm_rows = [
        [
            f"`{label}`",
            *[
                f"{metrics['confusion_matrix']['counts'][i][j]} "
                f"({metrics['confusion_matrix']['row_percent'][i][j]:.1f}%)"
                for j in range(len(labels))
            ],
        ]
        for i, label in enumerate(labels)
    ]
    accuracy = metrics["accuracy"]
    macro = metrics["macro"]
    weighted = metrics["weighted"]
    baseline = metrics["majority_baseline"]

    lines = [
        f"# {model_name} — {phase_label}",
        "",
        intro,
        "",
        "## Configuração",
        "",
        *config_lines,
        "",
        *extra_sections,
        "## Métricas no conjunto de teste",
        "",
        *markdown_table(
            [
                ["Acurácia", f"{accuracy:.4f}"],
                [
                    "Macro",
                    f"precisão {macro['precision']:.4f} · recall {macro['recall']:.4f} · "
                    f"F1 {macro['f1']:.4f}",
                ],
                [
                    "Weighted",
                    f"precisão {weighted['precision']:.4f} · recall {weighted['recall']:.4f} · "
                    f"F1 {weighted['f1']:.4f}",
                ],
            ],
            ["Métrica", "Valor"],
        ),
        "",
        "A média **macro** trata as classes com peso igual; a **weighted** pondera pelo "
        "suporte de cada classe. Ambas são registradas para não depender apenas da acurácia.",
        "",
        f"Referência: um classificador que sempre prevê a classe majoritária "
        f"(`{baseline['class']}`) obteria acurácia de {baseline['accuracy']:.2f}% no teste.",
        "",
        "## Métricas por classe",
        "",
        *markdown_table(per_class_rows, ["Classe", "Precisão", "Recall", "F1", "Suporte"]),
        "",
        "## Matriz de confusão",
        "",
        "Contagens com percentual em relação ao total da linha (classe real):",
        "",
        *markdown_table(cm_rows, ["Real \\ Previsto", *labels]),
        "",
        f"![Matriz de confusão](figures/{figure_name})",
        "",
        "## Limitações",
        "",
        *[f"- {item}" for item in limitations],
        "",
        f"Métricas em JSON: `{metrics_path}`.",
    ]
    return "\n".join(lines) + "\n"
