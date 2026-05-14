from __future__ import annotations

import argparse
from pathlib import Path

from marb.analysis import plot_metrics, write_markdown_report, write_summary
from marb.config import load_config
from marb.simulator import run_experiment


def simulate_command(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    results = run_experiment(config)
    results_path = out / "results.csv"
    results.to_csv(results_path, index=False)

    print(f"Wrote {results_path}")


def analyze_command(args: argparse.Namespace) -> None:
    out = Path(args.out)
    summary = write_summary(args.input, out)
    plot_paths = plot_metrics(summary, out)
    report_path = write_markdown_report(summary, out)

    print(f"Wrote {out / 'summary.csv'}")
    print(f"Wrote {report_path}")
    for path in plot_paths:
        print(f"Wrote {path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="marb",
        description="Memory Agent Risk Benchmark CLI",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    simulate = subparsers.add_parser("simulate", help="Run the synthetic benchmark")
    simulate.add_argument("--config", required=True, help="Path to YAML config")
    simulate.add_argument("--out", required=True, help="Output directory")
    simulate.set_defaults(func=simulate_command)

    analyze = subparsers.add_parser("analyze", help="Analyze benchmark results")
    analyze.add_argument("--input", required=True, help="Path to results CSV")
    analyze.add_argument("--out", required=True, help="Output directory")
    analyze.set_defaults(func=analyze_command)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
