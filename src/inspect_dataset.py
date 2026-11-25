"""Inspeção inicial do dataset escolhido do EduPredict (UCI ID 697).

Uso:
    python src/inspect_dataset.py

Gera ``reports/dataset_overview.md`` com dimensão, tipos, valores únicos,
valores ausentes, duplicatas, estatísticas numéricas e distribuição do alvo.
Não executa EDA completa, pré-processamento nem treinamento.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
REPORT_PATH = ROOT / "reports" / "dataset_overview.md"

DATASETS = [
    {
        "name": "ID 697 — Predict Students' Dropout and Academic Success",
        "path": RAW_DIR / "dropout_academic_success" / "data.csv",
        "sep": ";",
        "target": "Target",
    },
]


def load_dataset(path: Path, sep: str) -> pd.DataFrame:
    """Carrega um CSV preservando o texto e normaliza nomes de colunas."""
    frame = pd.read_csv(path, sep=sep, encoding="utf-8-sig")
    frame.columns = [str(column).strip() for column in frame.columns]
    return frame


def render_markdown(frame: pd.DataFrame, name: str, target: str, path: Path) -> str:
    """Monta a seção em Markdown com o diagnóstico de um dataset."""
    lines: list[str] = []
    lines.append(f"## {name}")
    lines.append("")
    lines.append(f"- Arquivo: `{path.relative_to(ROOT).as_posix()}`")
    lines.append(f"- Dimensão: {frame.shape[0]} linhas × {frame.shape[1]} colunas")
    lines.append(f"- Alvo inspecionado: `{target}`")
    lines.append(f"- Valores ausentes (total): {int(frame.isna().sum().sum())}")
    lines.append(f"- Linhas duplicadas: {int(frame.duplicated().sum())}")
    lines.append("")

    lines.append("### Colunas")
    lines.append("")
    lines.append("| # | Coluna | Tipo | Únicos | Ausentes |")
    lines.append("|---|--------|------|--------|----------|")
    for position, column in enumerate(frame.columns, start=1):
        lines.append(
            f"| {position} | `{column}` | {frame[column].dtype} | "
            f"{frame[column].nunique(dropna=True)} | {int(frame[column].isna().sum())} |"
        )
    lines.append("")

    if target in frame.columns:
        counts = frame[target].value_counts(dropna=False).sort_index()
        shares = frame[target].value_counts(normalize=True, dropna=False).sort_index() * 100
        lines.append("### Distribuição do alvo")
        lines.append("")
        lines.append("| Valor | Contagem | % |")
        lines.append("|-------|----------|---|")
        for value in counts.index:
            lines.append(f"| `{value}` | {int(counts[value])} | {shares[value]:.2f} |")
        lines.append("")

    numeric = frame.select_dtypes(include="number")
    if not numeric.empty:
        lines.append("### Estatísticas das colunas numéricas")
        lines.append("")
        summary = numeric.describe().transpose()
        lines.append("| Coluna | Mín | 25% | Mediana | 75% | Máx | Média | Desvio |")
        lines.append("|--------|-----|-----|---------|-----|-----|-------|--------|")
        for column, row in summary.iterrows():
            lines.append(
                f"| `{column}` | {row['min']:.2f} | {row['25%']:.2f} | {row['50%']:.2f} | "
                f"{row['75%']:.2f} | {row['max']:.2f} | {row['mean']:.2f} | {row['std']:.2f} |"
            )
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    """Executa a inspeção de todos os datasets configurados."""
    sections = [
        "# Visão geral do dataset escolhido",
        "",
        "Gerado por `src/inspect_dataset.py`. Dados reais, sem transformação de modelagem.",
        "",
    ]
    for dataset in DATASETS:
        path = Path(dataset["path"])
        if not path.exists():
            sections.append(f"## {dataset['name']}\n\nArquivo não encontrado: `{path}`\n")
            continue
        frame = load_dataset(path, dataset["sep"])
        sections.append(
            render_markdown(frame, dataset["name"], dataset["target"], path)
        )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(sections), encoding="utf-8")
    print(f"Relatório gravado em {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
