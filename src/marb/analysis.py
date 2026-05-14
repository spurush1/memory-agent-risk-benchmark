from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DEFAULT_METRICS = [
    ("task_success_rate", "Task Success Rate"),
    ("drift_rate", "Cognitive Drift Rate"),
    ("privacy_leak_rate", "Privacy Leak Rate"),
    ("policy_override_failure_rate", "Policy Override Failure Rate"),
    ("unlearning_failure_rate", "Unlearning Failure Rate"),
]


def summarize(results: pd.DataFrame) -> pd.DataFrame:
    return (
        results.groupby("condition")
        .mean(numeric_only=True)
        .drop(columns=["run"], errors="ignore")
        .round(4)
    )


def write_summary(results_csv: str | Path, out_dir: str | Path) -> pd.DataFrame:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    results = pd.read_csv(results_csv)
    summary = summarize(results)
    summary.to_csv(out / "summary.csv")

    return summary


def plot_metrics(summary: pd.DataFrame, out_dir: str | Path) -> list[Path]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    paths: list[Path] = []

    for metric, title in DEFAULT_METRICS:
        if metric not in summary.columns:
            continue
        means = summary[metric].sort_index()
        plt.figure(figsize=(9, 5))
        plt.bar(means.index, means.values)
        plt.xticks(rotation=30, ha="right")
        plt.ylabel(metric)
        plt.title(title)
        plt.tight_layout()
        path = out / f"{metric}.png"
        plt.savefig(path, dpi=160)
        plt.close()
        paths.append(path)

    return paths


def write_markdown_report(summary: pd.DataFrame, out_dir: str | Path) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "report.md"

    report = "# Memory Agent Risk Benchmark Report\n\n"
    report += "## Mean results\n\n"
    report += summary.to_markdown()
    report += "\n\n## Interpretation\n\n"
    report += (
        "The benchmark compares memory architectures under capability and risk metrics.\n\n"
        "A production-ready interpretation should emphasize risk-adjusted utility:\n\n"
        "- raw task success;\n"
        "- cognitive drift;\n"
        "- privacy leakage;\n"
        "- policy override failure;\n"
        "- poisoning success;\n"
        "- unlearning failure.\n\n"
        "The expected thesis is that guarded experience memory preserves much of the "
        "capability gain of experience-tier memory while reducing production risk.\n"
    )

    path.write_text(report, encoding="utf-8")
    return path
