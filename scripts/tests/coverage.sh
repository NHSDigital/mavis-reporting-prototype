#!/bin/bash

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"



poetry run coverage run -m pytest tests --verbose

poetry run coverage report
poetry run coverage html
