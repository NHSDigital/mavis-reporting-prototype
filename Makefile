.PHONY: clean
clean:
	@rm -f sentinel
	@rm -rf node_modules
	@rm -rf .venv
	@rm -rf __pycache__

sentinel: package.json package-lock.json pyproject.toml poetry.lock
	@echo "== Installing dependencies =="
	@npm install || (echo "Failed to install npm dependencies"; exit 1)
	@poetry config virtualenvs.in-project true
	@poetry install || (echo "Failed to install Python dependencies"; exit 1)
	@touch sentinel

.PHONY: install
install: sentinel
	
.PHONY: lint
lint: install
	poetry run ruff check .

.PHONY: dev
dev: install
	@echo "Starting development servers ..."
	@echo "Press Ctrl+C to stop all processes"
	@poetry run honcho start -f Procfile.dev

.PHONY: test
test: install
	@echo "Running all tests .."
	@poetry run pytest tests --verbose 

.PHONY: test-coverage
test-coverage: install
	@echo "Checking coverage on all tests .."
	@poetry run coverage run -m  pytest tests --verbose 
	@poetry run coverage report --fail-under=${FAIL_IF_UNDER}
	@poetry run coverage html
	@poetry run coverage xml coverage.xml
	@poetry run coverage-badge -o coverage.svg
	
