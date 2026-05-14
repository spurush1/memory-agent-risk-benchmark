from pathlib import Path

from marb.config import load_config


def test_load_config() -> None:
    config = load_config(Path("configs/synthetic_default.yaml"))
    assert config.n_runs == 30
    assert config.n_tasks == 500
    assert len(config.conditions) == 5
    assert config.conditions[0].name == "C0_No_Memory"
