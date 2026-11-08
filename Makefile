.PHONY: install run lint build check-dist package-install

install:
	uv sync

run:
	uv run database

lint:
	uv run ruff check .

build:
	uv build

check-dist:
	uvx twine check dist/*

package-install:
	uv tool install --force dist/*.whl
