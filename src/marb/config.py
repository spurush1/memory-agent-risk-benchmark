from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from marb.conditions import Condition


@dataclass(frozen=True)
class ExperimentConfig:
    seed: int
    n_runs: int
    n_tasks: int
    scenario_probabilities: dict[str, float]
    conditions: list[Condition]


def load_config(path: str | Path) -> ExperimentConfig:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        raw: dict[str, Any] = yaml.safe_load(f)

    conditions = [Condition(**item) for item in raw["conditions"]]

    return ExperimentConfig(
        seed=int(raw["seed"]),
        n_runs=int(raw["n_runs"]),
        n_tasks=int(raw["n_tasks"]),
        scenario_probabilities=dict(raw["scenario_probabilities"]),
        conditions=conditions,
    )
