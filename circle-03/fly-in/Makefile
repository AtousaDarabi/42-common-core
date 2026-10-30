PYTHON = python3
MAP = ./maps/simple.map

install:
	pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

run:
	@$(PYTHON) main.py $(MAP)

debug:
	$(PYTHON) -m pdb main.py $(MAP)

test:
	$(PYTHON) -m unittest discover -s tests -v

lint:
	$(PYTHON) -m flake8 . --exclude=.venv
	$(PYTHON) -m mypy fly_in main.py tests --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 . --exclude=.venv
	$(PYTHON) -m mypy fly_in main.py tests --strict

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache
