PYTHON  ?= python3
VENV    := .venv
# Use the project virtual environment once `make install` created it.
PY       = $(shell [ -x $(VENV)/bin/python ] && echo $(VENV)/bin/python || echo $(PYTHON))
MAP     ?= maps/example.map
ARGS    ?= --visual
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
             --disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug test benchmark lint lint-strict clean fclean

install:
	@if $(PYTHON) -m venv $(VENV) >/dev/null 2>&1; then \
		echo "Installing into $(VENV)"; \
		$(VENV)/bin/python -m pip install --quiet --upgrade pip; \
		$(VENV)/bin/python -m pip install -r requirements.txt; \
	else \
		rm -rf $(VENV); \
		echo "python3 -m venv unavailable: installing for the current user"; \
		$(PYTHON) -m pip install --user -r requirements.txt \
		|| $(PYTHON) -m pip install --user --break-system-packages -r requirements.txt; \
	fi

run:
	$(PY) main.py $(MAP) $(ARGS)

debug:
	$(PY) -m pdb main.py $(MAP) $(ARGS)

test:
	$(PY) -m unittest discover -s tests -v

benchmark:
	@for map in maps/benchmarks/*/*.txt; do \
		printf "%-50s %4s turns\n" "$$map" "$$($(PY) main.py $$map | wc -l)"; \
	done

lint:
	$(PY) -m flake8 .
	$(PY) -m mypy . $(MYPY_FLAGS)

lint-strict:
	$(PY) -m flake8 .
	$(PY) -m mypy . --strict

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

fclean: clean
	rm -rf $(VENV)
