# Fly-in

Fly-in is a Python 3.10+ simulator for moving drones through a constrained
network of hubs and bidirectional connections.

## Development

Create a virtual environment and install development tools:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Run the parser against the sample map:

```sh
make run
```

Run the Python linter flake8 against the project code in fly_in and the test files in tests.

```sh
make lint
```

Run mypy, which is a static type checker for Python. It analyzes the code in the fly_in package and reports type errors.

```sh
make typecheck
```

Run tests and quality checks:

```sh
make check
```