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
	@echo "Starting Sass watcher and Flask development server..."
	@echo "Press Ctrl+C to stop both processes"
	@trap 'kill %1 %2 2>/dev/null; exit' INT TERM; \
	npm run build:scss:dev & \
	poetry run flask run --debug & \
	wait
