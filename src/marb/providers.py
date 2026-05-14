from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AgentTask:
    task_id: str
    prompt: str
    expected_behavior: str | None = None
    sensitive: bool = False
    changed_instruction: bool = False
    adversarial: bool = False
    requires_unlearning: bool = False


@dataclass(frozen=True)
class AgentResult:
    task_id: str
    response: str
    used_memory: bool
    retrieved_memory_ids: list[str]
    policy_override_triggered: bool


class AgentProvider(Protocol):
    def run_task(self, task: AgentTask) -> AgentResult:
        """Run one benchmark task and return structured execution metadata."""


class StubProvider:
    """Deterministic provider for local development and tests."""

    def run_task(self, task: AgentTask) -> AgentResult:
        return AgentResult(
            task_id=task.task_id,
            response="stub-response",
            used_memory=False,
            retrieved_memory_ids=[],
            policy_override_triggered=False,
        )


class OpenAICompatibleProvider:
    """Skeleton for wiring a real LLM provider.

    This class is intentionally incomplete because production model use should define:

    - model name;
    - memory implementation;
    - tool policy;
    - logging and audit strategy;
    - privacy handling;
    - retry and rate-limit behavior.

    Never hard-code API keys. Use environment variables or a secret manager.
    """

    def __init__(self, model: str):
        self.model = model

    def run_task(self, task: AgentTask) -> AgentResult:
        raise NotImplementedError(
            "Implement provider-specific model calls and memory instrumentation here."
        )
