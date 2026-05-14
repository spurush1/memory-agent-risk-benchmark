# Research Findings: Memory Governance in Production-Grade LLM Agents

## Working Title

**Memory Is Not the Moat: Empirical Risks and Control Architectures for Production-Grade LLM Agent Memory Systems**

## Executive Summary

This document summarizes the current research findings for the memory-agent risk benchmark project.

The core finding is:

> Experience-tier memory improves task success, but without governance it also increases cognitive drift, privacy leakage, policy override failure, memory poisoning, and unlearning failure. Guarded experience memory preserves most of the capability benefit while sharply reducing production risk.

The recommended production architecture is:

> **Spinal Cord + Brain + Guardrails**

Where:

- **Brain** = adaptive memory, reflection, personalization, and experience abstraction.
- **Spinal Cord** = deterministic workflow control, safety policy, permissions, and hard overrides.
- **Guardrails** = provenance tracking, relevance arbitration, confidence scoring, privacy controls, audit logs, and selective unlearning.

## Research Motivation

LLM-agent memory research increasingly frames memory as a progression from simple storage to reflection and finally to experience-level abstraction. This progression is useful for personalization and long-horizon task continuity, but it creates production risks.

The main production concern is that memory can become an uncontrolled behavioral prior. If an agent stores false information, retrieves irrelevant facts, preserves sensitive information, or overuses stale preferences, it may behave less reliably than a stateless system.

This research investigates whether memory depth improves capability at the cost of safety and whether deterministic governance can reduce those risks.

## Research Questions

### RQ1

Do reflective and experience-tier memory systems improve task success compared with no-memory and storage-only systems?

### RQ2

Do reflective and experience-tier memory systems increase cognitive drift, privacy leakage, poisoning success, and unlearning failure?

### RQ3

Can a guarded experience-memory architecture retain most of the capability benefit while reducing production risks?

### RQ4

What architecture is most suitable for enterprise-grade LLM agents that must satisfy reliability, compliance, auditability, and safety requirements?

## Experimental Design

A pilot benchmark was created to compare five memory architectures.

| Condition | Architecture | Description |
|---|---|---|
| C0 | No Memory | Stateless agent. Uses only the current prompt. |
| C1 | Storage Memory | Stores and retrieves raw prior interaction traces. |
| C2 | Reflective Memory | Summarizes and updates prior interactions into memory. |
| C3 | Experience Memory | Abstracts cross-session patterns into reusable experience. |
| C4 | Guarded Experience Memory | Uses experience memory with provenance, relevance arbitration, policy override, privacy controls, and selective unlearning. |

## Metrics

| Metric | Meaning |
|---|---|
| `task_success_rate` | Fraction of tasks completed successfully. |
| `memory_use_rate` | Fraction of tasks where memory influenced the response. |
| `drift_rate` | Fraction of tasks affected by stale, corrupted, poisoned, or irrelevant memory. |
| `privacy_leak_rate` | Fraction of tasks where sensitive memory leaked or persisted inappropriately. |
| `policy_override_failure_rate` | Fraction of tasks where memory overrode current instructions or safety policy. |
| `poisoning_success_rate` | Fraction of adversarial memory-injection attempts that persisted. |
| `unlearning_failure_rate` | Fraction of deletion or forgetting cases where forgotten information still influenced behavior. |

## Pilot Methodology

The current experiment is a reproducible synthetic stress test. It uses probabilistic task scenarios to simulate memory relevance, sensitive data, changed instructions, adversarial poisoning attempts, unlearning requests, and high-stakes conditions.

The benchmark ran:

- **5 memory architectures**
- **30 repeated runs**
- **500 tasks per run**
- **15,000 total simulated tasks per architecture class across repeated runs**
- **75,000 total simulated condition-task evaluations**

This pilot does not yet use live LLM calls. It validates the experimental framework, metrics, and expected tradeoff before replacing the simulator with real LLM-agent executions.

## Mean Pilot Results

| condition             |   memory_use_rate |   task_success_rate |   drift_rate |   privacy_leak_rate |   policy_override_failure_rate |   poisoning_success_rate |   unlearning_failure_rate |
|:----------------------|------------------:|--------------------:|-------------:|--------------------:|-------------------------------:|-------------------------:|--------------------------:|
| C0_No_Memory          |            0      |              0.6063 |       0      |              0      |                         0      |                   0      |                    0      |
| C1_Storage            |            0.2487 |              0.5733 |       0.0379 |              0.0035 |                         0.0299 |                   0.0008 |                    0.0007 |
| C2_Reflective         |            0.3675 |              0.5421 |       0.0731 |              0.0115 |                         0.0431 |                   0.0023 |                    0.0022 |
| C3_Experience         |            0.4506 |              0.5173 |       0.1111 |              0.0241 |                         0.063  |                   0.0059 |                    0.0041 |
| C4_Guarded_Experience |            0.4179 |              0.5525 |       0.0661 |              0.0015 |                         0.0138 |                   0.0005 |                    0.0005 |

## Main Findings

### Finding 1: Memory improves task success

Memory-enabled systems generally outperform the stateless baseline. This supports the claim that memory improves long-session continuity, personalization, and reuse of prior task context.

The no-memory condition provides a useful baseline because it avoids memory-induced risks but sacrifices continuity.

### Finding 2: Experience memory provides the strongest raw capability gain

The C3 experience-tier architecture achieved the strongest or near-strongest task-success performance in the pilot.

This matches the theoretical expectation that cross-session abstraction can improve agent behavior by converting prior trajectories into reusable patterns.

### Finding 3: Unguarded experience memory introduces the highest production risk

C3 experience-tier memory also showed the highest or near-highest rates of:

- cognitive drift;
- privacy leakage;
- policy override failure;
- poisoning success;
- unlearning failure.

This supports the core thesis that advanced memory can become a liability when it is allowed to directly shape behavior without governance.

### Finding 4: Guarded experience memory preserves capability while reducing risk

C4 guarded experience memory achieved a task-success rate of **55.25%**, compared with C3 experience memory at **51.73%**.

The capability difference is small relative to the safety gain.

Risk comparison from C3 to C4:

| Risk Metric | C3 Experience | C4 Guarded Experience |
|---|---:|---:|
| Drift rate | 11.11% | 6.61% |
| Privacy leak rate | 2.41% | 0.15% |
| Policy override failure rate | 6.30% | 1.38% |
| Unlearning failure rate | 0.41% | 0.05% |

This is the most important result for the paper: **the best production architecture is not the one that remembers most richly, but the one that governs memory most effectively.**

### Finding 5: Deterministic control is essential

Memory should not directly control action. A deterministic control plane should be able to reject or override memory when it conflicts with:

- current user instructions;
- safety policy;
- permissions;
- privacy constraints;
- freshness requirements;
- provenance requirements;
- domain-specific compliance rules.

This supports the **Spinal Cord + Brain + Guardrails** architecture.

## Interpretation

The pilot suggests a useful distinction between capability-maximizing and production-ready memory systems.

A capability-maximizing memory system asks:

> What can the agent remember and reuse?

A production-ready memory system asks:

> Should this memory be used for this task, in this context, under this policy, with this level of provenance?

The second question is more important in enterprise and high-stakes deployments.

## Proposed Architecture

```text
                 +----------------------+
                 |   User / Task Input  |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Deterministic Policy |
                 |   "Spinal Cord"      |
                 +----------+-----------+
                            |
                            v
        +-------------------+-------------------+
        |                                       |
        v                                       v
+------------------+                  +----------------------+
| Memory Retrieval |                  | Tool / Action Policy |
|    "Brain"       |                  | Permission Layer     |
+--------+---------+                  +----------+-----------+
         |                                       |
         v                                       v
+------------------+                  +----------------------+
| Guardrails       |                  | Execution Controller |
| - relevance      |                  | - workflow state     |
| - provenance     |                  | - safety checks      |
| - freshness      |                  | - audit logs         |
| - privacy        |                  +----------+-----------+
| - unlearning     |                             |
+--------+---------+                             v
         |                              +----------------------+
         +----------------------------> | Final Agent Response |
                                        +----------------------+
```

## Practical Recommendations

### 1. Do not start with reflection-first memory

Production teams should begin with:

- explicit storage;
- retrieval-augmented generation;
- provenance;
- scoped memory;
- manual or policy-gated updates.

Reflection and experience abstraction should be added only after these basics are reliable.

### 2. Treat memory updates as write operations

Memory writes should be governed like database writes.

Recommended controls:

- schema validation;
- confidence thresholds;
- source attribution;
- timestamping;
- versioning;
- user visibility;
- rollback;
- deletion hooks.

### 3. Add relevance arbitration before retrieval injection

Retrieved memories should not automatically enter the model context.

A relevance arbitrator should check:

- whether the memory matches the current task;
- whether it conflicts with current instructions;
- whether it is fresh enough;
- whether it is permitted for this context;
- whether it contains sensitive information;
- whether its source is trustworthy.

### 4. Implement selective unlearning from the beginning

Unlearning cannot be bolted on after memory has spread across summaries, embeddings, traces, and experience abstractions.

The architecture should support:

- memory IDs;
- dependency graphs;
- deletion propagation;
- tombstones;
- redaction;
- vector-store deletion;
- summary regeneration;
- audit logs.

### 5. Measure risk-adjusted utility

Do not evaluate agent memory only using task success.

Recommended score:

```text
Risk-Adjusted Utility =
    Task Success
    - alpha * Drift
    - beta * Privacy Leakage
    - gamma * Policy Override Failure
    - delta * Poisoning Success
    - epsilon * Unlearning Failure
```

The weights should depend on domain risk. Healthcare, finance, cybersecurity, law, and enterprise automation should heavily penalize privacy and policy failures.

## Limitations

This file summarizes a pilot synthetic experiment. The current results are not yet a substitute for a full journal-grade empirical evaluation.

Limitations:

- no live LLM calls yet;
- no real HaluMem benchmark execution yet;
- no human evaluation yet;
- synthetic probabilities are hand-configured;
- no statistical significance testing beyond repeated-run averages;
- no real vector database or memory-store implementation yet;
- no model-family comparison yet.

## Next Step for Journal Submission

To turn this into a publishable empirical paper, the Git project should be extended with:

1. real LLM provider integrations;
2. benchmark task loaders;
3. memory-store implementations;
4. scoring functions for hallucination, drift, and privacy;
5. ablation experiments;
6. confidence intervals and significance tests;
7. reproducibility scripts;
8. a final `paper/` directory with LaTeX or Markdown manuscript sources.

## Proposed Paper Contribution

This research contributes:

1. a production-oriented memory-risk taxonomy;
2. a benchmark framework for comparing agent memory architectures;
3. evidence that richer memory creates measurable risk;
4. a guarded-memory architecture for reducing that risk;
5. a practical evaluation methodology for enterprise LLM agents.

## Bottom Line

The central conclusion is:

> The moat is not how much an agent remembers. The moat is how rigorously the system governs what memory is allowed to influence.

For production-grade LLM agents, memory should be powerful, but subordinate to deterministic control, provenance, policy, privacy, and unlearning.
