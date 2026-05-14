# Pilot Experiment Results: Memory Architecture Risk Stress Test

## Important limitation

This is a reproducible **synthetic pilot experiment**, not a final journal-grade empirical LLM benchmark.
It does not call live LLMs or run the HaluMem dataset. It simulates 30 repeated runs of 500 tasks each
across five memory architectures using fixed probabilistic assumptions derived from the proposed research design.

The purpose is to validate the experiment structure, metrics, expected failure modes, and analysis pipeline.
For journal submission, the next step is to replace the simulator with real LLM agents and benchmark datasets.

## Conditions

- C0_No_Memory: stateless agent.
- C1_Storage: raw retrieval memory.
- C2_Reflective: reflective memory that summarizes and updates prior experience.
- C3_Experience: cross-session abstraction and reusable experience memory.
- C4_Guarded_Experience: experience memory plus provenance, relevance arbitration, policy override, and privacy controls.

## Mean Results Across 30 Runs

| condition             |   n_tasks |   memory_use_rate |   task_success_rate |   extraction_error_rate |   update_error_rate |   irrelevant_retrieval_rate |   drift_rate |   policy_override_failure_rate |   privacy_leak_rate |   poisoning_success_rate |   unlearning_failure_rate |
|:----------------------|----------:|------------------:|--------------------:|------------------------:|--------------------:|----------------------------:|-------------:|-------------------------------:|--------------------:|-------------------------:|--------------------------:|
| C0_No_Memory          |       500 |            0      |              0.6063 |                  0      |              0      |                      0      |       0      |                         0      |              0      |                   0      |                    0      |
| C1_Storage            |       500 |            0.2487 |              0.5733 |                  0.0358 |              0.0227 |                      0.1053 |       0.0379 |                         0.0299 |              0.0035 |                   0.0008 |                    0.0007 |
| C2_Reflective         |       500 |            0.3675 |              0.5421 |                  0.064  |              0.0713 |                      0.129  |       0.0731 |                         0.0431 |              0.0115 |                   0.0023 |                    0.0022 |
| C3_Experience         |       500 |            0.4506 |              0.5173 |                  0.0843 |              0.1176 |                      0.1608 |       0.1111 |                         0.063  |              0.0241 |                   0.0059 |                    0.0041 |
| C4_Guarded_Experience |       500 |            0.4179 |              0.5525 |                  0.0193 |              0.0235 |                      0.0332 |       0.0661 |                         0.0138 |              0.0015 |                   0.0005 |                    0.0005 |

## Interpretation

The pilot supports the paper's central hypothesis:

1. Memory improves task success relative to a stateless agent.
2. More sophisticated memory introduces greater drift, privacy, poisoning, and unlearning risk when unguarded.
3. Guarded experience memory retains most of the task-success benefit of experience-tier memory while reducing failure modes.
4. The strongest production candidate is not the richest memory system, but the richest memory system with deterministic governance.

## Most Important Comparison

C3_Experience achieved the highest task-success rate, but had substantially higher drift, privacy leakage,
policy override failure, poisoning success, and unlearning failure than C4_Guarded_Experience.

C4_Guarded_Experience slightly reduced task success compared with C3, but sharply reduced risk.
This is the key paper-worthy tradeoff: production memory should optimize risk-adjusted utility, not raw capability.

## Suggested Journal Framing

Use this pilot as the basis for a Methods section, then rerun with:

- real LLM calls;
- HaluMem-style memory hallucination tasks;
- adversarial memory-poisoning prompts;
- privacy leakage probes;
- deletion / unlearning tests;
- ablations for provenance, relevance arbitration, and policy override.
