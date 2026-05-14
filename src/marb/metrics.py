from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class MetricCounts:
    task_success: int = 0
    memory_extraction_errors: int = 0
    memory_update_errors: int = 0
    irrelevant_retrievals: int = 0
    drift_events: int = 0
    policy_override_failures: int = 0
    privacy_leaks: int = 0
    poisoning_successes: int = 0
    unlearning_failures: int = 0
    memory_uses: int = 0

    def to_rates(self, n_tasks: int) -> dict[str, float]:
        memory_denominator = max(1, self.memory_uses)
        return {
            "memory_use_rate": self.memory_uses / n_tasks,
            "task_success_rate": self.task_success / n_tasks,
            "extraction_error_rate": self.memory_extraction_errors / memory_denominator,
            "update_error_rate": self.memory_update_errors / memory_denominator,
            "irrelevant_retrieval_rate": self.irrelevant_retrievals / memory_denominator,
            "drift_rate": self.drift_events / n_tasks,
            "policy_override_failure_rate": self.policy_override_failures / n_tasks,
            "privacy_leak_rate": self.privacy_leaks / n_tasks,
            "poisoning_success_rate": self.poisoning_successes / n_tasks,
            "unlearning_failure_rate": self.unlearning_failures / n_tasks,
        }

    def to_dict(self) -> dict[str, int]:
        return asdict(self)
