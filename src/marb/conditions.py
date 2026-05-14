from dataclasses import dataclass


@dataclass(frozen=True)
class Condition:
    name: str
    memory_strength: float
    base_task_success: float
    helpful_memory_gain: float
    extraction_error_rate: float
    update_error_rate: float
    retrieval_irrelevance_rate: float
    stale_memory_rate: float
    privacy_leak_rate: float
    poison_accept_rate: float
    unlearning_failure_rate: float
    guardrail_strength: float
