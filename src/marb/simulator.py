from __future__ import annotations

import random
from dataclasses import dataclass

import pandas as pd

from marb.conditions import Condition
from marb.config import ExperimentConfig
from marb.metrics import MetricCounts


@dataclass(frozen=True)
class Scenario:
    task_id: int
    memory_relevant: bool
    task_has_sensitive_data: bool
    task_has_changed_instruction: bool
    adversarial_poison_attempt: bool
    requires_unlearning: bool
    high_stakes: bool


def bernoulli(rng: random.Random, probability: float) -> bool:
    p = max(0.0, min(1.0, probability))
    return rng.random() < p


def generate_scenarios(
    rng: random.Random,
    n_tasks: int,
    probabilities: dict[str, float],
) -> list[Scenario]:
    scenarios: list[Scenario] = []
    for task_id in range(1, n_tasks + 1):
        scenarios.append(
            Scenario(
                task_id=task_id,
                memory_relevant=bernoulli(rng, probabilities["memory_relevant"]),
                task_has_sensitive_data=bernoulli(rng, probabilities["task_has_sensitive_data"]),
                task_has_changed_instruction=bernoulli(
                    rng, probabilities["task_has_changed_instruction"]
                ),
                adversarial_poison_attempt=bernoulli(
                    rng, probabilities["adversarial_poison_attempt"]
                ),
                requires_unlearning=bernoulli(rng, probabilities["requires_unlearning"]),
                high_stakes=bernoulli(rng, probabilities["high_stakes"]),
            )
        )
    return scenarios


def run_condition(
    rng: random.Random,
    condition: Condition,
    scenarios: list[Scenario],
) -> MetricCounts:
    counts = MetricCounts()

    memory_store_corrupted = False
    stored_sensitive_fact = False
    poisoned_memory = False
    forgotten_fact_still_active = False

    for scenario in scenarios:
        uses_memory = (
            condition.memory_strength > 0
            and scenario.memory_relevant
            and bernoulli(rng, condition.memory_strength)
        )

        if uses_memory:
            counts.memory_uses += 1

        extraction_error = uses_memory and bernoulli(
            rng,
            condition.extraction_error_rate * (1 - 0.55 * condition.guardrail_strength),
        )
        update_error = uses_memory and bernoulli(
            rng,
            condition.update_error_rate * (1 - 0.60 * condition.guardrail_strength),
        )
        irrelevant_retrieval = uses_memory and bernoulli(
            rng,
            condition.retrieval_irrelevance_rate * (1 - 0.70 * condition.guardrail_strength),
        )
        stale_replay = (
            uses_memory
            and scenario.task_has_changed_instruction
            and bernoulli(
                rng,
                condition.stale_memory_rate * (1 - 0.75 * condition.guardrail_strength),
            )
        )

        if extraction_error:
            counts.memory_extraction_errors += 1
            memory_store_corrupted = True
        if update_error:
            counts.memory_update_errors += 1
            memory_store_corrupted = True
        if irrelevant_retrieval:
            counts.irrelevant_retrievals += 1
        if stale_replay or (
            memory_store_corrupted
            and uses_memory
            and bernoulli(rng, 0.10 + condition.memory_strength * 0.10)
        ):
            counts.drift_events += 1

        if uses_memory and (scenario.task_has_changed_instruction or scenario.high_stakes):
            conflict = stale_replay or irrelevant_retrieval or memory_store_corrupted
            if conflict and bernoulli(rng, (1 - condition.guardrail_strength) * 0.42):
                counts.policy_override_failures += 1

        if scenario.task_has_sensitive_data and uses_memory:
            if bernoulli(
                rng,
                condition.privacy_leak_rate * (1 - 0.80 * condition.guardrail_strength),
            ):
                counts.privacy_leaks += 1
                stored_sensitive_fact = True

        if stored_sensitive_fact and uses_memory:
            if bernoulli(
                rng,
                condition.privacy_leak_rate * 0.35 * (1 - condition.guardrail_strength),
            ):
                counts.privacy_leaks += 1

        if scenario.adversarial_poison_attempt and uses_memory:
            if bernoulli(
                rng,
                condition.poison_accept_rate * (1 - 0.75 * condition.guardrail_strength),
            ):
                counts.poisoning_successes += 1
                poisoned_memory = True

        if poisoned_memory and uses_memory and bernoulli(
            rng,
            0.08 * (1 - condition.guardrail_strength),
        ):
            counts.drift_events += 1

        if scenario.requires_unlearning and uses_memory:
            if bernoulli(
                rng,
                condition.unlearning_failure_rate * (1 - 0.65 * condition.guardrail_strength),
            ):
                counts.unlearning_failures += 1
                forgotten_fact_still_active = True

        if forgotten_fact_still_active and uses_memory and bernoulli(
            rng,
            0.05 * (1 - condition.guardrail_strength),
        ):
            counts.privacy_leaks += 1

        p_success = condition.base_task_success
        harmful_memory = irrelevant_retrieval or stale_replay or memory_store_corrupted or poisoned_memory

        if uses_memory and not harmful_memory:
            p_success += condition.helpful_memory_gain
        elif uses_memory and harmful_memory:
            p_success -= 0.12 + 0.08 * condition.memory_strength

        if scenario.high_stakes:
            p_success -= 0.03

        if counts.policy_override_failures > 0 and bernoulli(rng, 0.15):
            p_success -= 0.05

        if bernoulli(rng, p_success):
            counts.task_success += 1

    return counts


def run_experiment(config: ExperimentConfig) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for run in range(1, config.n_runs + 1):
        scenario_rng = random.Random(config.seed + run * 10_000)
        scenarios = generate_scenarios(
            scenario_rng,
            config.n_tasks,
            config.scenario_probabilities,
        )

        for condition_idx, condition in enumerate(config.conditions):
            condition_rng = random.Random(config.seed + run * 10_000 + condition_idx)
            counts = run_condition(condition_rng, condition, scenarios)
            row: dict[str, object] = {
                "run": run,
                "condition": condition.name,
                "n_tasks": config.n_tasks,
            }
            row.update(counts.to_rates(config.n_tasks))
            rows.append(row)

    return pd.DataFrame(rows)
