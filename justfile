format:
    uv run nox -s format

lint:
    uv run nox -s lint

test:
    uv run nox -s test

check:
    just format
    just lint
    just check