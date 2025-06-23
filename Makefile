include scripts/init.mk

# ==============================================================================

.PHONY: install
install:
	poetry config virtualenvs.in-project true
	poetry install

.PHONY: lint
lint:
	poetry run ruff check .

.PHONY: dev
dev:
	@echo "Starting Sass watcher, JavaScript bundler and Flask development server..."
	@echo "Press Ctrl+C to stop all processes"
	@trap 'jobs -p | xargs kill 2>/dev/null; exit' INT TERM; \
	npm run build:scss:dev & \
	npm run build:js:dev & \
	poetry run flask run --debug & \
	wait
