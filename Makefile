.PHONY: install test lint simulate analyze clean

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src tests

simulate:
	marb simulate --config configs/synthetic_default.yaml --out runs/synthetic_default

analyze:
	marb analyze --input runs/synthetic_default/results.csv --out runs/synthetic_default

clean:
	rm -rf runs .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
