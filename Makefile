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
	
	@echo "== Copying NHSUK favicons =="
	@make copy-nhsuk-favicons
	
	@touch sentinel

.PHONY: install
install: sentinel
	
.PHONY: lint
lint: install
	poetry run ruff check .

.PHONY: dev
dev: install
	@echo "== Starting development servers =="
	@echo "Press Ctrl+C to stop all processes"
	@poetry run honcho start -f Procfile.dev

.PHONY: test
test:
	@true

.PHONY: test-coverage
test-coverage:
	@true

.PHONY: copy-nhsuk-favicons
copy-nhsuk-favicons:
	mkdir -p mavis_reporting/static/favicons
	cp -r node_modules/nhsuk-frontend/packages/assets/favicons/* mavis_reporting/static/favicons/
