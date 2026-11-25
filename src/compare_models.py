"""Comparação dos dois modelos e seleção justificada (Fase 6).

Uso:
    python src/compare_models.py

Lê as métricas reais já gravadas pelos treinos (sem retreinar), valida que
ambos usam o mesmo conjunto de teste e gera a figura comparativa e
``reports/comparison.md``. A métrica principal é o F1 macro.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from evaluation import markdown_table

ROOT = Path(__file__).resolve().parent.parent
FIG_PATH = ROOT / "reports" / "figures" / "model_comparison_f1_por_classe.png"
REPORT_PATH = ROOT / "reports" / "comparison.md"

METRICS_FILES = {
    "Logistic Regression": ROOT / "reports" / "model1_metrics.json",
    "Random Forest": ROOT / "reports" / "model2_metrics.json",
}
PRIMARY_METRIC = "macro_f1"
PRIMARY_LABEL = "F1 macro"
COLORS = {"Logistic Regression": "#4c72b0", "Random Forest": "#55a868"}


def load_metrics() -> dict[str, dict]:
    """Carrega as métricas dos dois modelos."""
    models = {}
    for name, path in METRICS_FILES.items():
        if not path.exists():
            raise FileNotFoundError(f"Métricas não encontradas: {path}")
        models[name] = json.loads(path.read_text(encoding="utf-8"))
    return models


def validate_same_test(models: dict[str, dict]) -> tuple[list[str], int]:
    """Garante comparação justa: mesmo split, mesmos rótulos e mesmo teste."""
    first_name, first = next(iter(models.items()))
    for name, metrics in models.items():
        if metrics["split"] != first["split"]:
            raise ValueError(f"Split diferente entre {first_name} e {name}.")
        if metrics["confusion_matrix"]["labels"] != first["confusion_matrix"]["labels"]:
            raise ValueError(f"Rótulos diferentes entre {first_name} e {name}.")
        counts = np.asarray(metrics["confusion_matrix"]["counts"])
        if counts.sum() != first["split"]["n_test"]:
            raise ValueError(f"Matriz de {name} não corresponde ao n_test do split.")
    labels = list(first["confusion_matrix"]["labels"])
    return labels, int(first["split"]["n_test"])


def error_counts(metrics: dict, labels: list[str]) -> dict[str, dict[str, int]]:
    """Deriva TP/FN/FP/TN da matriz de confusão."""
    cm = np.asarray(metrics["confusion_matrix"]["counts"])
    total = int(cm.sum())
    result = {}
    for index, label in enumerate(labels):
        tp = int(cm[index, index])
        fn = int(cm[index, :].sum()) - tp
        fp = int(cm[:, index].sum()) - tp
        tn = total - tp - fn - fp
        result[label] = {"tp": tp, "fn": fn, "fp": fp, "tn": tn}
    return result


def delta_pp(value_a: float, value_b: float) -> float:
    """Diferença em pontos percentuais."""
    return (value_a - value_b) * 100


def build_aggregate_rows(models: dict[str, dict]) -> list[list[str]]:
    """Tabela agregada com valores e diferença em pontos percentuais."""
    names = list(models)
    left, right = names
    specs = [
        ("Acurácia", lambda m: m["accuracy"]),
        ("Precisão macro", lambda m: m["macro"]["precision"]),
        ("Recall macro", lambda m: m["macro"]["recall"]),
        ("F1 macro", lambda m: m["macro"]["f1"]),
        ("Precisão weighted", lambda m: m["weighted"]["precision"]),
        ("Recall weighted", lambda m: m["weighted"]["recall"]),
        ("F1 weighted", lambda m: m["weighted"]["f1"]),
    ]
    rows = []
    for label, getter in specs:
        value_left = getter(models[left])
        value_right = getter(models[right])
        rows.append(
            [
                label,
                f"{value_left:.4f}",
                f"{value_right:.4f}",
                f"{delta_pp(value_left, value_right):+.2f}",
            ]
        )
    return rows


def build_per_class_rows(models: dict[str, dict], labels: list[str]) -> list[list[str]]:
    """Tabela de precisão/recall/F1 por classe e diferença de F1."""
    left, right = list(models)
    rows = []
    for label in labels:
        a = models[left]["per_class"][label]
        b = models[right]["per_class"][label]
        rows.append(
            [
                f"`{label}`",
                str(a["support"]),
                f"{a['precision']:.4f}",
                f"{a['recall']:.4f}",
                f"{a['f1']:.4f}",
                f"{b['precision']:.4f}",
                f"{b['recall']:.4f}",
                f"{b['f1']:.4f}",
                f"{delta_pp(a['f1'], b['f1']):+.2f}",
            ]
        )
    return rows


def build_error_rows(models: dict[str, dict], labels: list[str]) -> list[list[str]]:
    """Tabela de falsos negativos e falsos positivos por classe."""
    left, right = list(models)
    errors_left = error_counts(models[left], labels)
    errors_right = error_counts(models[right], labels)
    rows = []
    for label in labels:
        a = errors_left[label]
        b = errors_right[label]
        rows.append(
            [
                f"`{label}`",
                str(a["fn"]),
                str(b["fn"]),
                str(a["fp"]),
                str(b["fp"]),
            ]
        )
    return rows


def total_errors(metrics: dict, labels: list[str]) -> int:
    """Total de erros de classificação a partir da matriz de confusão."""
    errors = error_counts(metrics, labels)
    return sum(item["fn"] for item in errors.values())


def save_comparison_figure(models: dict[str, dict], labels: list[str]) -> None:
    """Figura de barras agrupadas do F1 por classe."""
    names = list(models)
    positions = np.arange(len(labels))
    width = 0.38

    FIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    for offset, name in zip((-width / 2, width / 2), names):
        values = [models[name]["per_class"][label]["f1"] for label in labels]
        bars = ax.bar(
            positions + offset,
            values,
            width=width,
            label=name,
            color=COLORS[name],
        )
        for bar, value in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.01,
                f"{value:.3f}",
                ha="center",
                va="bottom",
                fontsize=8,
            )
    ax.set_xticks(positions)
    ax.set_xticklabels(labels)
    ax.set_ylabel("F1-score")
    ax.set_ylim(0, 1.05)
    ax.set_title("F1 por classe: Logistic Regression vs Random Forest")
    ax.legend(loc="upper right")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_PATH, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    """Gera a comparação consolidada e a seleção do modelo."""
    models = load_metrics()
    labels, n_test = validate_same_test(models)
    left, right = list(models)

    aggregate_rows = build_aggregate_rows(models)
    per_class_rows = build_per_class_rows(models, labels)
    error_rows = build_error_rows(models, labels)

    total_left = total_errors(models[left], labels)
    total_right = total_errors(models[right], labels)

    left_f1 = models[left]["macro"]["f1"]
    right_f1 = models[right]["macro"]["f1"]
    winner = left if left_f1 >= right_f1 else right
    other = right if winner == left else left
    winner_f1 = models[winner]["macro"]["f1"]
    other_f1 = models[other]["macro"]["f1"]
    winner_errors = total_errors(models[winner], labels)
    other_errors = total_errors(models[other], labels)
    diff_pp = abs(winner_f1 - other_f1) * 100

    better_by_class = []
    for label in labels:
        f1_left = models[left]["per_class"][label]["f1"]
        f1_right = models[right]["per_class"][label]["f1"]
        best = left if f1_left >= f1_right else right
        better_by_class.append(
            f"- `{label}`: melhor F1 com **{best}** "
            f"({max(f1_left, f1_right):.4f} vs {min(f1_left, f1_right):.4f})."
        )

    dropout_errors = []
    for name, metrics in models.items():
        errors = error_counts(metrics, labels)
        dropout_errors.append(
            f"- {name}: {errors['Dropout']['fn']} falsos negativos e "
            f"{errors['Dropout']['fp']} falsos positivos para `Dropout`."
        )

    save_comparison_figure(models, labels)

    sections = [
        "# Comparação e seleção de modelo",
        "",
        "Gerado por `src/compare_models.py` a partir das métricas reais dos treinos, "
        "**sem retreinar**. Ambos os modelos usam o mesmo conjunto de teste.",
        "",
        "## Método",
        "",
        f"- Conjunto de teste: {n_test} exemplos (split 80/20, `random_state=42`, estratificado).",
        f"- Métrica principal: **{PRIMARY_LABEL}**; secundárias: recall por classe e F1 weighted.",
        "- Acurácia é reportada, mas não decide a escolha (classes desbalanceadas).",
        f"- Diferenças (Δ) em pontos percentuais, calculadas como {left} − {right}.",
        "",
        "## Métricas agregadas",
        "",
        *markdown_table(
            aggregate_rows,
            ["Métrica", left, right, "Δ (p.p.)"],
        ),
        "",
        f"Erros totais: {left} = {total_left}; {right} = {total_right} "
        f"(de {n_test} exemplos de teste).",
        "",
        f"Referência: classe majoritária (`Graduate`) acertaria "
        f"{models[left]['majority_baseline']['accuracy']:.2f}% dos casos.",
        "",
        "## Métricas por classe",
        "",
        *markdown_table(
            per_class_rows,
            [
                "Classe",
                "Suporte",
                f"{left} P",
                f"{left} R",
                f"{left} F1",
                f"{right} P",
                f"{right} R",
                f"{right} F1",
                "Δ F1 (p.p.)",
            ],
        ),
        "",
        "## Impacto dos erros (FP/FN)",
        "",
        *markdown_table(
            error_rows,
            ["Classe", f"{left} FN", f"{right} FN", f"{left} FP", f"{right} FP"],
        ),
        "",
        "Leitura orientada ao contexto educacional: um **falso negativo de `Dropout`** "
        "significa não sinalizar um estudante que acabou evadindo — tende a ser o erro "
        "mais custoso. Já `Enrolled` é uma classe intermediária ambígua, e o colapso dela "
        "em `Graduate`/`Dropout` também reduz a utilidade do modelo para apoio preventivo.",
        "",
        *dropout_errors,
        "",
        "## Métrica principal",
        "",
        f"A escolha do **{PRIMARY_LABEL}** se justifica porque as classes são desbalanceadas "
        "(`Graduate` ≈ 50%) e a acurácia é dominada por essa classe. O F1 macro dá peso igual "
        "às três classes e combina precisão e recall, penalizando o desempenho fraco em "
        "`Enrolled`. Acurácia e F1 weighted são mantidos como contexto, não como critério único.",
        "",
        "## Seleção",
        "",
        f"**Modelo selecionado para este estudo: {winner}.**",
        "",
        f"- F1 macro: {winner_f1:.4f} vs {other_f1:.4f} (Δ de {diff_pp:.2f} p.p.).",
        f"- Erros totais no teste: {winner_errors} vs {other_errors}.",
        f"- Vantagem modesta: a diferença equivale a poucas decisões no conjunto de teste; "
        f"não há alegação de superioridade universal.",
        "",
        "Desempenho por classe:",
        "",
        *better_by_class,
        "",
        f"Trade-off: {other} pode ser preferível se o objetivo for outro critério de custo "
        "ou uma métrica específica; para o critério definido aqui, o modelo selecionado é "
        f"{winner}.",
        "",
        "## Limitações",
        "",
        "- Um único split 80/20; não há intervalos de confiança nem repetição.",
        "- Ambos são modelos de referência, sem tuning de hiperparâmetros.",
        "- `Enrolled` tem desempenho fraco nos dois modelos (classe intermediária ambígua).",
        "- Dados observacionais de uma instituição; sem validação externa.",
        "- Resultados não devem orientar decisões reais sobre estudantes e não implicam causalidade.",
        "",
        "## Possíveis melhorias (não executadas)",
        "",
        "- Validação cruzada/repetida para estimar variabilidade.",
        "- Ajuste de hiperparâmetros apenas no treino.",
        "- `class_weight` ou custos assimétricos, se o objetivo for priorizar `Dropout`.",
        "- Calibração de probabilidades e análise de custo dos erros.",
        "",
        "## Artefatos",
        "",
        f"- `{METRICS_FILES[left].relative_to(ROOT).as_posix()}`",
        f"- `{METRICS_FILES[right].relative_to(ROOT).as_posix()}`",
        f"- `{FIG_PATH.relative_to(ROOT).as_posix()}`",
        "",
    ]
    REPORT_PATH.write_text("\n".join(sections) + "\n", encoding="utf-8")

    print(f"Selecionado: {winner} (F1 macro {winner_f1:.4f} vs {other_f1:.4f})")
    print(f"Erros: {left}={total_left} | {right}={total_right}")
    print(f"Relatório: {REPORT_PATH.relative_to(ROOT).as_posix()}")
    print(f"Figura: {FIG_PATH.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
