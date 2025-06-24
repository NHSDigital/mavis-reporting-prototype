include scripts/init.mk

# ==============================================================================

.PHONY: install
install:
	npm install
	poetry config virtualenvs.in-project true
	poetry install

.PHONY: lint
lint:
	poetry run ruff check .

.PHONY: dev
dev:
	@npm install
	@poetry install
	@echo "Starting development servers ..."
	@echo "Press Ctrl+C to stop all processes"
	@poetry run honcho start -f Procfile.dev
