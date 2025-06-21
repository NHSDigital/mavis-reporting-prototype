include scripts/init.mk

# ==============================================================================

.PHONY: install
install:
	poetry config virtualenvs.in-project true
	poetry install

.PHONY: lint
lint:
	poetry run ruff check .

.PHONY: run
run:
	poetry run flask run
