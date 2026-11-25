"""Análise exploratória descritiva do dataset EduPredict (UCI ID 697).

Uso:
    python src/eda.py

Gera as figuras em ``reports/figures/`` e as tabelas em
``reports/eda_stats.md``. Não transforma dados nem treina modelos.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "raw" / "dropout_academic_success" / "data.csv"
FIG_DIR = ROOT / "reports" / "figures"
STATS_PATH = ROOT / "reports" / "eda_stats.md"

TARGET = "Target"
CLASSES = ["Dropout", "Enrolled", "Graduate"]
CLASS_COLORS = {"Dropout": "#d62728", "Enrolled": "#ff7f0e", "Graduate": "#2ca02c"}
MACRO_FEATURES = ["Unemployment rate", "Inflation rate", "GDP"]

KEY_NUMERIC = [
    "Age at enrollment",
    "Admission grade",
    "Previous qualification (grade)",
    "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)",
    "Curricular units 2nd sem (enrolled)",
    "Curricular units 2nd sem (approved)",
    "Curricular units 2nd sem (grade)",
]

CORR_FEATURES = [
    "Age at enrollment",
    "Admission grade",
    "Previous qualification (grade)",
    "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (evaluations)",
    "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)",
    "Curricular units 2nd sem (enrolled)",
    "Curricular units 2nd sem (evaluations)",
    "Curricular units 2nd sem (approved)",
    "Curricular units 2nd sem (grade)",
]

BINARY_FACTORS = [
    "Scholarship holder",
    "Debtor",
    "Tuition fees up to date",
    "Gender",
    "Daytime/evening attendance",
    "Displaced",
]

PINNED_BINARY = [
    "Daytime/evening attendance",
    "Displaced",
    "Educational special needs",
    "Debtor",
    "Tuition fees up to date",
    "Gender",
    "Scholarship holder",
    "International",
]


def load_dataset() -> pd.DataFrame:
    """Carrega a base bruta normalizando apenas os nomes das colunas."""
    frame = pd.read_csv(DATA_PATH, sep=";", encoding="utf-8-sig")
    frame.columns = [str(column).strip() for column in frame.columns]
    return frame


def class_share(frame: pd.DataFrame) -> pd.Series:
    """Retorna a distribuição percentual das classes na ordem fixa."""
    return frame[TARGET].value_counts(normalize=True).reindex(CLASSES) * 100


def describe_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Resumo estatístico das variáveis numéricas-chave."""
    summary = frame[KEY_NUMERIC].describe().transpose()
    return summary[["min", "25%", "50%", "75%", "max", "mean", "std"]]


def binary_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Distribuição das classes para cada valor dos fatores binários."""
    rows = []
    for column in PINNED_BINARY:
        for value in sorted(frame[column].dropna().unique()):
            subset = frame[frame[column] == value]
            counts = subset[TARGET].value_counts().reindex(CLASSES, fill_value=0)
            shares = counts / len(subset) * 100 if len(subset) else counts * np.nan
            rows.append(
                {
                    "Fator": column,
                    "Valor": int(value),
                    "n": int(len(subset)),
                    "% Dropout": shares["Dropout"],
                    "% Enrolled": shares["Enrolled"],
                    "% Graduate": shares["Graduate"],
                }
            )
    return pd.DataFrame(rows)


def course_table(frame: pd.DataFrame, column: str, top: int = 8) -> pd.DataFrame:
    """Taxas por categoria dos atributos codificados mais frequentes."""
    counts = frame[column].value_counts().head(top)
    rows = []
    for code, size in counts.items():
        subset = frame[frame[column] == code]
        shares = subset[TARGET].value_counts(normalize=True).reindex(CLASSES) * 100
        rows.append(
            {
                column: int(code),
                "n": int(size),
                "% Dropout": shares["Dropout"],
                "% Enrolled": shares["Enrolled"],
                "% Graduate": shares["Graduate"],
            }
        )
    return pd.DataFrame(rows)


def top_correlations(frame: pd.DataFrame) -> pd.DataFrame:
    """Pares de variáveis com maior correlação absoluta de Pearson."""
    matrix = frame[CORR_FEATURES].corr()
    pairs = (
        matrix.where(np.triu(np.ones(matrix.shape), k=1).astype(bool))
        .stack()
        .reset_index()
    )
    pairs.columns = ["Variavel 1", "Variavel 2", "Correlacao"]
    pairs["Abs"] = pairs["Correlacao"].abs()
    return pairs.sort_values("Abs", ascending=False).drop(columns="Abs").head(10)


def dataframe_to_markdown(frame: pd.DataFrame, decimals: int = 2) -> str:
    """Converte um DataFrame em tabela Markdown sem depender de tabulate."""
    columns = list(frame.columns)
    lines = ["| " + " | ".join(columns) + " |"]
    lines.append("|" + "|".join(["---"] * len(columns)) + "|")
    for _, row in frame.iterrows():
        cells = []
        for column in columns:
            value = row[column]
            if isinstance(value, (float, np.floating)):
                cells.append(f"{value:.{decimals}f}")
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def save_target_distribution(frame: pd.DataFrame) -> Path:
    """Figura 1: balanceamento das classes do alvo."""
    counts = frame[TARGET].value_counts().reindex(CLASSES)
    shares = counts / counts.sum() * 100
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(CLASSES, counts.values, color=[CLASS_COLORS[c] for c in CLASSES])
    for bar, count, share in zip(bars, counts.values, shares.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{count} ({share:.1f}%)",
            ha="center",
            va="bottom",
        )
    ax.set_title("Distribuição das classes do alvo")
    ax.set_xlabel("Classe")
    ax.set_ylabel("Número de estudantes")
    ax.set_ylim(0, counts.max() * 1.15)
    fig.tight_layout()
    path = FIG_DIR / "eda_01_target_distribution.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def save_boxplot(frame: pd.DataFrame, column: str, title: str, filename: str, ylabel: str) -> Path:
    """Figura de caixa de uma variável numérica por classe do alvo."""
    data = [frame.loc[frame[TARGET] == c, column].dropna().values for c in CLASSES]
    fig, ax = plt.subplots(figsize=(7, 5))
    box = ax.boxplot(
        data,
        tick_labels=CLASSES,
        patch_artist=True,
        widths=0.55,
        medianprops={"color": "black", "linewidth": 1.5},
    )
    for patch, name in zip(box["boxes"], CLASSES):
        patch.set_facecolor(CLASS_COLORS[name])
        patch.set_alpha(0.65)
    ax.set_title(title)
    ax.set_xlabel("Classe")
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    path = FIG_DIR / filename
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def save_correlation_heatmap(frame: pd.DataFrame) -> tuple[Path, pd.DataFrame]:
    """Figura 4: correlação de Pearson entre as numéricas-chave."""
    matrix = frame[CORR_FEATURES].corr()
    fig, ax = plt.subplots(figsize=(9, 7.5))
    image = ax.imshow(matrix.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(CORR_FEATURES)))
    ax.set_yticks(range(len(CORR_FEATURES)))
    labels = [c.replace("Curricular units ", "").replace(" sem ", " sem.") for c in CORR_FEATURES]
    ax.set_xticklabels(labels, rotation=60, ha="right", fontsize=7)
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_title("Correlação de Pearson entre variáveis numéricas")
    for i in range(len(CORR_FEATURES)):
        for j in range(len(CORR_FEATURES)):
            value = matrix.values[i, j]
            ax.text(j, i, f"{value:.1f}", ha="center", va="center", fontsize=6)
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    path = FIG_DIR / "eda_04_correlation_heatmap.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path, matrix


def save_binary_rates(frame: pd.DataFrame) -> Path:
    """Figura 5: taxa de Graduate e de Dropout por fator binário."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    positions = np.arange(len(BINARY_FACTORS))
    width = 0.38
    for ax, class_name in zip(axes, ["Graduate", "Dropout"]):
        for offset, value in zip((-width / 2, width / 2), (0, 1)):
            rates = []
            for factor in BINARY_FACTORS:
                subset = frame[frame[factor] == value]
                share = (subset[TARGET] == class_name).mean() * 100 if len(subset) else np.nan
                rates.append(share)
            ax.barh(
                positions + offset,
                rates,
                height=width,
                label=f"valor = {value}",
                color="#4c72b0" if value == 0 else "#dd8452",
            )
            for y, rate in zip(positions + offset, rates):
                if not np.isnan(rate):
                    ax.text(rate + 0.7, y, f"{rate:.0f}%", va="center", fontsize=7)
        ax.set_yticks(positions)
        ax.set_yticklabels(BINARY_FACTORS)
        ax.set_xlabel(f"% de {class_name}")
        ax.set_title(f"{class_name} por fator binário")
        ax.set_xlim(0, 100)
        ax.grid(axis="x", alpha=0.3)
    axes[0].legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    path = FIG_DIR / "eda_05_taxas_binarias_por_target.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def consistency_checks(frame: pd.DataFrame) -> list[str]:
    """Verificações simples de domínio e coerência, apenas para diagnóstico."""
    lines = []
    for label, semester in (("1º", "1st"), ("2º", "2nd")):
        approved = f"Curricular units {semester} sem (approved)"
        enrolled = f"Curricular units {semester} sem (enrolled)"
        violations = int((frame[approved] > frame[enrolled]).sum())
        lines.append(
            f"- {label} semestre: `approved > enrolled` em {violations} de {len(frame)} linhas."
        )
    for column in (
        "Admission grade",
        "Previous qualification (grade)",
        "Curricular units 1st sem (grade)",
        "Curricular units 2nd sem (grade)",
    ):
        lines.append(
            f"- `{column}`: mínimo {frame[column].min():.2f}, máximo {frame[column].max():.2f}."
        )
    lines.append(
        f"- `Age at enrollment`: mínimo {int(frame['Age at enrollment'].min())}, "
        f"máximo {int(frame['Age at enrollment'].max())}, "
        f"acima de 40 anos: {int((frame['Age at enrollment'] > 40).sum())} linhas."
    )
    for column in PINNED_BINARY:
        values = sorted(int(v) for v in frame[column].dropna().unique())
        lines.append(f"- `{column}`: valores observados {values}.")
    return lines


def main() -> None:
    """Executa a EDA, salva figuras e tabelas, e imprime um resumo."""
    frame = load_dataset()
    features = [c for c in frame.columns if c != TARGET and c not in MACRO_FEATURES]

    FIG_DIR.mkdir(parents=True, exist_ok=True)

    target_counts = frame[TARGET].value_counts().reindex(CLASSES)
    target_shares = target_counts / target_counts.sum() * 100
    binary = binary_table(frame)
    description = describe_table(frame)
    means = frame.groupby(TARGET)[KEY_NUMERIC].mean().reindex(CLASSES)
    medians = frame.groupby(TARGET)[KEY_NUMERIC].median().reindex(CLASSES)
    courses = course_table(frame, "Course")
    applications = course_table(frame, "Application mode")
    corr_pairs = top_correlations(frame)

    figures = [
        save_target_distribution(frame),
        save_boxplot(
            frame,
            "Curricular units 2nd sem (approved)",
            "Unidades aprovadas no 2º semestre por classe",
            "eda_02_approved_2nd_sem_por_target.png",
            "Unidades curriculares aprovadas",
        ),
        save_boxplot(
            frame,
            "Curricular units 2nd sem (grade)",
            "Nota média do 2º semestre por classe",
            "eda_03_grade_2nd_sem_por_target.png",
            "Nota média (0-20)",
        ),
    ]
    heatmap_path, _ = save_correlation_heatmap(frame)
    figures.append(heatmap_path)
    figures.append(save_binary_rates(frame))

    diagnostics = consistency_checks(frame)

    sections = [
        "# Estatísticas da EDA",
        "",
        "Gerado por `src/eda.py`. Apenas análise descritiva, sem transformação de dados.",
        "",
        "## Estrutura e qualidade",
        "",
        f"- Dimensão: {frame.shape[0]} linhas × {frame.shape[1]} colunas.",
        f"- Atributos usados na EDA: {len(features)} (3 indicadores macro excluídos).",
        f"- Valores ausentes: {int(frame.isna().sum().sum())}.",
        f"- Linhas duplicadas: {int(frame.duplicated().sum())}.",
        "",
        *diagnostics,
        "",
        "## Distribuição do alvo",
        "",
        dataframe_to_markdown(
            pd.DataFrame(
                {"Classe": CLASSES, "n": target_counts.values, "%": target_shares.values}
            )
        ),
        "",
        "## Estatísticas numéricas",
        "",
        dataframe_to_markdown(description.reset_index().rename(columns={"index": "Variavel"})),
        "",
        "## Médias por classe",
        "",
        dataframe_to_markdown(means.reset_index().rename(columns={"index": "Classe"})),
        "",
        "## Medianas por classe",
        "",
        dataframe_to_markdown(medians.reset_index().rename(columns={"index": "Classe"})),
        "",
        "## Fatores binários",
        "",
        dataframe_to_markdown(binary),
        "",
        "## Cursos mais frequentes",
        "",
        dataframe_to_markdown(courses),
        "",
        "## Modos de candidatura mais frequentes",
        "",
        dataframe_to_markdown(applications),
        "",
        "## Maiores correlações (Pearson)",
        "",
        dataframe_to_markdown(corr_pairs),
        "",
        "## Figuras",
        "",
        *[f"- `{path.relative_to(ROOT).as_posix()}`" for path in figures],
    ]
    STATS_PATH.write_text("\n".join(sections) + "\n", encoding="utf-8")

    print("Dimensao:", frame.shape)
    print("Alvo:", target_counts.to_dict())
    print("Figuras:", [p.name for p in figures])
    print("Tabelas:", STATS_PATH.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
