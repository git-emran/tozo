format:
	black src tests
	isort src tests
	djhtml src/backend/templates -t 2 --in-place

lint:
	black --check src tests
	isort --check-only src tests
	flake8 src tests
	mypy src
	bandit -r src

test:
	pytest tests
