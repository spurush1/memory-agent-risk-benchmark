# Memory Agent Risk Benchmark

A reproducible benchmark framework for evaluating memory architectures in LLM agents.

This project compares:

- `C0_No_Memory`
- `C1_Storage`
- `C2_Reflective`
- `C3_Experience`
- `C4_Guarded_Experience`

It measures task success, hallucination-like memory errors, drift, privacy leakage, policy override failure, poisoning success, and unlearning failure.

## Core thesis

> Production-grade agent memory should not be optimized only for richness or persistence. It should be governed by provenance, relevance arbitration, deterministic control, privacy constraints, and selective unlearning.

## Installation

```bash
git clone <your-repo-url>
cd memory-agent-risk-benchmark
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run synthetic benchmark

```bash
marb simulate --config configs/synthetic_default.yaml --out runs/synthetic_default
marb analyze --input runs/synthetic_default/results.csv --out runs/synthetic_default
```

## Run tests

```bash
pytest
```

## Optional real LLM integration

The project includes a provider interface in `src/marb/providers.py`.

Do not commit API keys. Set them only in your local environment or secret manager.

```bash
export OPENAI_API_KEY="..."
```

Then implement a provider that conforms to `AgentProvider`.

## Repository layout

```text
memory-agent-risk-benchmark/
  src/marb/
    cli.py
    config.py
    conditions.py
    simulator.py
    metrics.py
    providers.py
    analysis.py
  configs/
  datasets/
  tests/
  reports/
  notebooks/
```

## Journal workflow

1. Validate the experimental design with the synthetic benchmark.
2. Replace simulated agents with real LLM agent runs.
3. Use benchmark tasks for memory hallucination, poisoning, privacy leakage, and unlearning.
4. Report mean, standard deviation, confidence intervals, and ablations.
5. Publish code, configs, seeds, and task templates for reproducibility.

## License

MIT
