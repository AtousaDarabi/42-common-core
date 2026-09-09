PYTHON ?= python3
MAP ?= tests/data/simple.map

.PHONY: run test lint typecheck check clean

run:
	$(PYTHON) -m fly_in.main $(MAP)

test:
	$(PYTHON) -m unittest discover -s tests

lint:
	$(PYTHON) -m flake8 fly_in tests

typecheck:
	$(PYTHON) -m mypy fly_in

check: test lint typecheck


