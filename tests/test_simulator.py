from pathlib import Path

from marb.config import load_config
from marb.simulator import run_experiment


def test_run_experiment_shape() -> None:
    config = load_config(Path("configs/synthetic_default.yaml"))
    df = run_experiment(config)
    assert len(df) == config.n_runs * len(config.conditions)
    assert "task_success_rate" in df.columns
    assert "privacy_leak_rate" in df.columns


def test_no_memory_has_no_memory_use() -> None:
    config = load_config(Path("configs/synthetic_default.yaml"))
    df = run_experiment(config)
    no_memory = df[df["condition"] == "C0_No_Memory"]
    assert float(no_memory["memory_use_rate"].max()) == 0.0
