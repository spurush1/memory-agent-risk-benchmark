from pathlib import Path

from marb.analysis import summarize
from marb.config import load_config
from marb.simulator import run_experiment


def test_summarize() -> None:
    config = load_config(Path("configs/synthetic_default.yaml"))
    df = run_experiment(config)
    summary = summarize(df)
    assert "C4_Guarded_Experience" in summary.index
    assert "task_success_rate" in summary.columns
