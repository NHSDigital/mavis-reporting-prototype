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

.PHONY: test
test:
	@poetry install
	@echo "Running all tests .."
	@poetry run pytest tests --verbose 

.PHONY: test-coverage
test-coverage:
	@poetry install
	@echo "Checking coverage on all tests .."
	@poetry run coverage run -m  pytest tests 
	@poetry run coverage report --fail-under=${FAIL_IF_UNDER}
	@poetry run coverage html
	@poetry run coverage xml coverage.xml
	@poetry run coverage-badge -o coverage.svg
	